"""
build_ch03_04_files.py — « Le buste stylisé » (CH03.04, sculpture stylisée).

  STARTER_FILES/ch03_04_bust_starter.blend
      Studio, caméras de face et de profil, planche de design (3 silhouettes de référence en Grease
      Pencil : la « grosse tête », le « costaud », le « long ») ; aucun buste.
  COMPLETED_EXAMPLES/ch03_04_bust_solution.blend (+ _reference.png : face, 3/4, profil)
      Buste « grosse tête » : blocage en ellipsoïdes qui se chevauchent (poitrine, cou, tête, crâne, nez,
      arcades, menton, oreilles, mèche) → Join → Voxel Remesh (5 mm) → orbites creusées par Boolean
      Difference → Voxel Remesh → socle plat (Bisect + Fill) → SCULPT_Bust, un seul volume fermé.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_04_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH03.04 — LE BUSTE STYLISÉ (vues : Num 1 face, Num 3 profil)
1. Design : choisissez UNE idée forte (planche DESIGN : grosse tête, costaud, long) et un contraste
   de tailles net entre tête et épaules (au moins 25 % d'écart).
2. Blocage : Add > Metaball (Ball, Capsule, Ellipsoid…) : tête, cou, épaules, nez, arcades, menton,
   oreilles ; cochez Negative sur deux éléments pour creuser les orbites.
3. Object > Convert > Mesh ; renommez SCULPT_Body→ SCULPT_Bust ; Voxel Remesh (≈ 5 mm).
4. Socle plat : Edit Mode, tout sélectionner, Mesh > Bisect au ras du bas (Clear Inner + Fill),
   ou un Boolean Difference avec un grand cube.
5. Sculpt Mode : simplifiez, nettoyez, accentuez les plans ; gardez Mirror X.
Vérification : SCRIPTS/validate_ch03_04.py -- --exercise bust
"""
PARTS = [  # nom, centre, demi-dimensions (ellipsoïdes qui se chevauchent)
    ("Chest", (0, 0.0, 0.08), (0.21, 0.11, 0.1)),
    ("Neck", (0, 0.0, 0.19), (0.055, 0.055, 0.07)),
    ("Head", (0, 0.0, 0.34), (0.125, 0.135, 0.15)),
    ("Skull", (0, 0.03, 0.40), (0.11, 0.115, 0.1)),
    ("Nose", (0, -0.135, 0.315), (0.024, 0.04, 0.032)),
    ("Brow", (0, -0.112, 0.375), (0.085, 0.025, 0.02)),
    ("Chin", (0, -0.095, 0.24), (0.05, 0.045, 0.04)),
    ("Ear_L", (0.125, 0.0, 0.33), (0.018, 0.035, 0.045)),
    ("Ear_R", (-0.125, 0.0, 0.33), (0.018, 0.035, 0.045)),
    ("Hair", (0, 0.03, 0.495), (0.07, 0.09, 0.045)),
]
SOCKETS = [(0.048, -0.132, 0.345), (-0.048, -0.132, 0.345)]


def studio_views():
    L.studio(subject_height=0.6)
    c = L.collection("CAMERAS")
    front = L.camera("CAM_Front", c, (0, -1.25, 0.3), 50, make_active=True)
    S.look_at(front, (0, 0, 0.28))
    side = L.camera("CAM_Side", c, (1.25, 0, 0.3), 50, make_active=False)
    S.look_at(side, (0, 0, 0.28))
    tq = L.camera("CAM_34", c, (0.8, -1.0, 0.42), 50, make_active=False)
    S.look_at(tq, (0, 0, 0.28))
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.camera = front
    return sc


def design_board():
    ob, _cam, drw = None, None, None
    ob = G.new_object("GP_Design", L.collection("DESIGN"))
    ob.location = (-1.2, 0.5, 0)       # bcma_gp écrit déjà en (x, 0, z) : pas de rotation (sinon les silhouettes sont couchées au sol)
    ink = G.material(ob, "MAT_GP_Ink", (0.05, 0.05, 0.08))
    d = G.layer(ob, "DESIGN")
    ob.data.layers["DESIGN"].use_lights = False
    for i, (hw, hh, sw, nh) in enumerate(((0.16, 0.2, 0.2, 0.05), (0.09, 0.1, 0.32, 0.03), (0.08, 0.24, 0.12, 0.12))):
        x0 = -0.35 + i * 0.35
        G.ellipse(d, (x0, 0.3 + nh + hh / 2), hw / 2, hh / 2, 0.004, ink)
        G.polyline(d, [(x0 - 0.03, 0.3 + nh), (x0 - 0.03, 0.3), (x0 - sw / 2, 0.27), (x0 - sw / 2, 0.15),
                       (x0 + sw / 2, 0.15), (x0 + sw / 2, 0.27), (x0 + 0.03, 0.3), (x0 + 0.03, 0.3 + nh)], 0.004, ink)
    return ob


def bust():
    col = L.collection("SCULPT")
    clay = L.material("MAT_Clay", (0.75, 0.6, 0.5), 0.55)
    parts = [L.sphere("BLOCK_" + n, col, clay, radius=1, location=c, scale=r) for n, c, r in PARTS]
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_Bust", "ME_SCULPT_Bust"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ob.data.remesh_voxel_size = 0.005
    bpy.ops.object.voxel_remesh()
    # orbites : Boolean Difference avec deux sphères (outil non destructif, puis appliqué)
    for i, c in enumerate(SOCKETS):
        cutter = L.sphere(f"CUT_Socket_{i}", col, None, radius=0.03, location=c)
        m = ob.modifiers.new(f"Socket_{i}", "BOOLEAN")
        m.operation, m.object, m.solver = "DIFFERENCE", cutter, "EXACT"
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.data.objects.remove(cutter, do_unlink=True)
    bpy.ops.object.voxel_remesh()                      # remesh final : volume régulier, arêtes adoucies
    # socle plat : coupe au plan z = 0,005 et remplissage
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.005), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    ob.location.z = -0.005
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.data.use_mirror_x = True
    print(f"[BCMA] SCULPT_Bust : {len(ob.data.vertices)} sommets, {len(ob.data.polygons)} faces")
    return ob


def build(sol):
    L.reset("SC_Bust")
    sc = studio_views()
    design_board()
    if sol:
        bust()
    L.instructions(NOTE)
    return sc


def views(sc, out):
    tiles = []
    sc.render.resolution_x, sc.render.resolution_y = 720, 900
    for cam in ("CAM_Front", "CAM_34", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("bust", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_04_bust_starter.blend"))
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] solution avec plans sculptés à la brosse (Blender 5.2 via MCP) conservée : non régénérée")
        return
    sc = build(True)          # repli : blocage seul, sans sculpt des plans
    L.save(os.path.join(out, "ch03_04_bust_solution.blend"))
    for o in bpy.data.objects:
        if o.name == "GP_Design":
            o.hide_render = True
    views(sc, os.path.join(out, "ch03_04_bust_reference.png"))


if __name__ == "__main__":
    L.run(main)
