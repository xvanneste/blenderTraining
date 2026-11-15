"""
build_ch18_20_files.py — « Du board au layout 3D » (CH18.20, phase 18 module F).

  STARTER_FILES/ch18_20_layout_starter.blend
      Décor 3D (SET), 3 caméras CAM_SH0010/20/30 liées à 3 marqueurs (images 1, 73, 121 ; fin 168) ;
      pour chaque caméra, un objet GP « BOARD_SHxxxx » ENFANT de la caméra (à 0,5 m devant elle) qui
      contient le croquis du plan (silhouette du personnage, flèche) — le storyboard dessiné DANS la
      caméra. Personnage 3D CHR_A (mannequin 1,75 m) posé hors champ, non animé.
  COMPLETED_EXAMPLES/ch18_20_layout_solution.blend (+ _contact.png : rendu des 3 plans, boards visibles)
      Blocking : CHR_A animé (Location, interpolation Constant) aux images 1, 73, 121 pour coïncider avec
      la silhouette du board de chaque plan ; caméras inchangées ; boards exclus du rendu final.
Usage : blender -b --factory-startup --python build_ch18_20_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
D = 0.5                      # distance du board devant la caméra (devant tout sujet du plan)
# code, image, position caméra, point visé, focale, position du personnage, rotation Z (degrés)
SHOTS = [("SH0010", 1, (4.5, -6.5, 2.2), (0.0, 1.0, 0.9), 30, (-1.8, 2.2, 0.0), -60),
         ("SH0020", 73, (2.2, -2.8, 1.5), (0.3, 1.0, 1.1), 40, (0.3, 1.0, 0.0), -20),
         ("SH0030", 121, (1.1, -0.9, 1.6), (0.35, 1.0, 1.45), 50, (0.3, 1.0, 0.0), -20)]
END = 168
NOTE = """CH18.20 — DU BOARD AU LAYOUT 3D (vue caméra : Num 0 ; changer de plan : flèches haut/bas = marqueurs)
Le storyboard est dessiné DANS chaque caméra : objets GP BOARD_SH0010/20/30, enfants des caméras.
Votre travail : le BLOCKING 3D du personnage CHR_A d'après ces dessins.
1. Placez-vous sur le marqueur SH0010 (image 1), vue caméra : déplacez/tournez CHR_A pour que le
   mannequin se superpose à la silhouette dessinée (pieds sur les pieds, tête sur la tête).
   Insérez une clé : K > Location & Rotation (I insère Location, Rotation et Scale par défaut).
2. Même chose aux images 73 (SH0020) et 121 (SH0030).
3. Graph Editor ou Dope Sheet : clés de CHR_A en interpolation Constant (T) — le personnage « saute »
   à la coupe au lieu de glisser entre les plans.
4. NE MODIFIEZ PAS les caméras (elles viennent du board).
5. Excluez les boards du rendu final : Outliner > icône appareil photo (Disable in Renders).
   Astuce : dans la vue, masquez (H) les boards des autres plans pour ne voir que celui du plan courant.
Vérification : SCRIPTS/validate_ch18_20.py -- --exercise layout
"""


def to_plane(cam, p):
    """Projette un point du monde sur le plan du board (repère local de la caméra, z = −D)."""
    pc = cam.matrix_world.inverted() @ Vector(p)
    k = D / -pc.z
    return (pc.x * k, pc.y * k, -D)


def board(cam, code, char_loc, rotz):
    ob = G.new_object("BOARD_" + code, L.collection("BOARDS"))
    ob.parent = cam
    ink = G.material(ob, "MAT_GP_Board", (0.85, 0.15, 0.1))
    d = G.layer(ob, "Board")
    ob.data.layers["Board"].use_lights = False
    x, y, _z = char_loc
    a = math.radians(rotz)
    side = Vector((math.cos(a), math.sin(a), 0)) * 0.22

    def P(dx, dz, s=0.0):
        return to_plane(cam, (x + side.x * s + dx, y + side.y * s, dz))

    head = [to_plane(cam, (x + 0.12 * math.cos(t) * math.cos(a), y + 0.12 * math.cos(t) * math.sin(a), 1.63 + 0.13 * math.sin(t)))
            for t in [i * 2 * math.pi / 20 for i in range(21)]]
    G.polyline(d, head, 0.001, ink)
    G.polyline(d, [P(0, 1.48), P(0, 0.9)], 0.001, ink)                                   # buste
    G.polyline(d, [P(0, 0.9, -1), P(0, 0.02, -0.6)], 0.001, ink)                         # jambes
    G.polyline(d, [P(0, 0.9, 1), P(0, 0.02, 0.6)], 0.001, ink)
    G.polyline(d, [P(0, 1.42, -1.3), P(0, 0.85, -1.4)], 0.001, ink)                      # bras
    G.polyline(d, [P(0, 1.42, 1.3), P(0, 0.85, 1.4)], 0.001, ink)
    G.polyline(d, [P(-0.35, 0.0), P(0.35, 0.0)], 0.0008, ink)                             # ligne de sol sous les pieds
    return ob


def build(sol):
    sc = L.reset("SC_Layout")
    s = L.collection("SET")
    L.plane("GEO_Floor", s, L.material("MAT_Floor", (0.5, 0.47, 0.42), 0.8), size=14, location=(0, 1, 0))
    wall = L.material("MAT_Wall", (0.72, 0.7, 0.65), 0.9)
    L.cube("GEO_WallBack", s, wall, size=1, location=(0, 4.1, 2), scale=(14, 0.2, 4))
    L.cube("GEO_WallLeft", s, wall, size=1, location=(-4.1, 1, 2), scale=(0.2, 7, 4))
    L.cube("GEO_Table", s, L.material("MAT_Wood", (0.5, 0.33, 0.18), 0.6), size=1, location=(1.4, 1.6, 0.4), scale=(1.2, 0.7, 0.8))
    L.light("LGT_Sun", L.collection("LIGHTS"), "SUN", (2, -3, 6), 3.0, rotation=(50, 0, 30))
    L.world((0.55, 0.6, 0.68), 0.6, "WO_Room")
    sc = L.render_defaults("BLENDER_EEVEE", 25)
    sc.frame_start, sc.frame_end = 1, END
    bpy.context.view_layer.use_pass_z = True
    chr_ = S.mannequin_mesh("CHR_A", L.collection("CHARACTERS"), (-3.2, 3.0, 0.0), L.material("MAT_A", (0.75, 0.3, 0.2), 0.6))
    cams = L.collection("CAMERAS")
    stored = {}
    for code, f, loc, tgt, lens, cloc, rotz in SHOTS:
        cam = L.camera("CAM_" + code, cams, loc, lens, make_active=False)
        S.look_at(cam, tgt)
        bpy.context.view_layer.update()
        m = sc.timeline_markers.new(code, frame=f)
        m.camera = cam
        stored[code] = [list(r) for r in cam.matrix_world]
        b = board(cam, code, cloc, rotz)
        if sol:
            b.hide_render = True
    sc["bcma_cams"] = json.dumps(stored)
    sc.camera = bpy.data.objects["CAM_SH0010"]
    if sol:
        for code, f, loc, tgt, lens, cloc, rotz in SHOTS:
            chr_.location = cloc
            chr_.rotation_euler = (0, 0, math.radians(rotz))
            chr_.keyframe_insert("location", frame=f)
            chr_.keyframe_insert("rotation_euler", frame=f)
        for lay in chr_.animation_data.action.layers:
            for st in lay.strips:
                for bag in st.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:
                            k.interpolation = "CONSTANT"
    L.instructions(NOTE)
    return sc


def contact(sc, out):
    sc.render.resolution_percentage = 25
    W, H = sc.render.resolution_x // 4, sc.render.resolution_y // 4
    sheet = np.zeros((H, W * len(SHOTS), 4), dtype=np.float32)
    for i, (code, f, *_r) in enumerate(SHOTS):
        for b in bpy.data.objects:                   # seul le board du plan courant est rendu
            if b.name.startswith("BOARD_"):
                b.hide_render = b.name != "BOARD_" + code
        sc.frame_set(f)
        p = os.path.join(bpy.app.tempdir, f"lay_{code}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        sheet[:, i * W:(i + 1) * W] = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
    img = bpy.data.images.new("layout_contact", W * len(SHOTS), H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_20_layout_starter.blend"))
    sc = build(True)
    L.save(os.path.join(out, "ch18_20_layout_solution.blend"))
    contact(sc, os.path.join(out, "ch18_20_layout_contact.png"))


if __name__ == "__main__":
    L.run(main)
