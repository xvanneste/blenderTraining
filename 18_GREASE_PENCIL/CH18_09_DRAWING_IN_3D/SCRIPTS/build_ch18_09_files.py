"""
build_ch18_09_files.py — Scène « dessin dans l'espace 3D et organisation » (CH18.09).

  ASSETS/ch18_09_concept.png : image de référence (copie de la référence de CH18.05, licence BCMA).
  STARTER_FILES/ch18_09_set_starter.blend
      Sol (GEO_Ground), caméra CAM_Layout, soleil, image de référence REF_Concept (empty image,
      image empaquetée) ; objet GP_Set vide avec 4 calques : BG, MID, FG, GROUND.
  COMPLETED_EXAMPLES/ch18_09_set_solution.blend (+ _reference.png, + _top.png vue de dessus)
      Décor dessiné sur 4 profondeurs : montagnes (Y≈14), maison et arbres (Y≈3), arbre et
      buissons de premier plan (Y≈-5), route et herbes dessinées À PLAT sur le sol (plan Top).
Usage : blender -b --factory-startup --python build_ch18_09_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
ROOT = os.path.abspath(os.path.join(CH, "..", ".."))
NOTE = """CH18.09 — DESSIN DANS L'ESPACE 3D (GP_Set, Draw Mode)
Caméra CAM_Layout (Num 0) à Y = -12 regarde vers +Y. Image de référence : REF_Concept.
Dessinez un décor en profondeur dans GP_Set, un calque par plan :
1. BG (au moins 4 traits) : montagnes/ciel, à Y ≈ +12..+16 (curseur 3D à Y = 14, Stroke
   Placement : 3D Cursor, Drawing Plane : Front (X-Z)).
2. MID (au moins 4 traits) : maison, arbres, personnage, à Y ≈ +2..+4.
3. FG (au moins 4 traits) : éléments de premier plan à Y ≈ -6..-4 (attention : près de la caméra).
4. GROUND (au moins 3 traits) : route, chemin, herbes dessinés À PLAT sur le sol :
   Drawing Plane : Top (X-Y), curseur 3D à Z = 0. Ils doivent s'étendre sur au moins 6 m en Y.
5. Properties > View Layer > Passes > Data > Z (rendu correct, voir CH18.06).
6. Conseillé : décochez « Lights » des 4 calques (couleurs plates, non assombries par le soleil).
Orbitez pour vérifier la profondeur. Vérification : SCRIPTS/validate_ch18_09.py -- --exercise set
"""


def scene():
    L.reset("SC_Set")
    col = L.collection("SET")
    grass = L.material("MAT_Grass", (0.35, 0.5, 0.25), 0.9)
    L.plane("GEO_Ground", col, grass, size=80)
    cc, cl = L.collection("CAMERAS"), L.collection("LIGHTS")
    cam = L.camera("CAM_Layout", cc, (0, -12.0, 1.7), 28)
    cam.rotation_euler = (math.radians(86), 0, 0)
    L.light("LGT_Sun", cl, "SUN", (0, -5, 10), 3.0, rotation=(45, 0, 20))
    L.world((0.6, 0.75, 0.95), 1.0, "WO_Sky")
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    # Image de référence (empaquetée dans le .blend)
    src = os.path.join(ROOT, "18_GREASE_PENCIL", "CH18_05_COMPOSITION", "COMPLETED_EXAMPLES",
                       "ch18_05_composition_reference.png")
    dst = os.path.join(CH, "ASSETS", "ch18_09_concept.png")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    img = bpy.data.images.load(dst)
    img.pack()
    ref = bpy.data.objects.new("REF_Concept", None)
    ref.empty_display_type = "IMAGE"
    ref.data = img
    ref.empty_display_size = 6.0
    ref.location = (-9.0, 6.0, 3.0)
    ref.rotation_euler = (math.radians(90), 0, math.radians(20))
    L.collection("REFERENCES").objects.link(ref)
    d = L.collection("DRAWINGS")
    ob = G.new_object("GP_Set", d)
    G.material(ob, "MAT_GP_Ink", (0.02, 0.02, 0.02))
    for n in ("GROUND", "BG", "MID", "FG"):
        G.layer(ob, n)
    return sc, ob


def tree(d, x, y, h, rad, mat, fill_mat):
    G.polyline(d, [(x - 0.08 * h, y, 0), (x - 0.05 * h, y, 0.55 * h)], rad, mat)
    G.polyline(d, [(x + 0.08 * h, y, 0), (x + 0.05 * h, y, 0.55 * h)], rad, mat)
    G.polyline(d, [(x + 0.3 * h * math.cos(t), y, 0.78 * h + 0.28 * h * math.sin(t))
                   for t in [i * 2 * math.pi / 28 for i in range(28)]], rad, fill_mat, cyclic=True, fill=True)


def solution(ob):
    ink = 0
    mtn = G.material(ob, "MAT_GP_Mountain", (0.25, 0.3, 0.45), fill=(0.55, 0.62, 0.78))
    leaf = G.material(ob, "MAT_GP_Leaf", (0.05, 0.15, 0.05), fill=(0.2, 0.45, 0.2))
    wall = G.material(ob, "MAT_GP_Wall", (0.02, 0.02, 0.02), fill=(0.9, 0.8, 0.6))
    roof = G.material(ob, "MAT_GP_Roof", (0.02, 0.02, 0.02), fill=(0.7, 0.2, 0.12))
    road = G.material(ob, "MAT_GP_Road", (0.3, 0.25, 0.2), fill=(0.6, 0.55, 0.45))
    lay = lambda n: G.layer(ob, n)
    # BG : montagnes à Y = 14
    d = lay("BG")
    for k, (x0, w, h) in enumerate(((-14, 9, 5.5), (-6, 11, 7.0), (4, 10, 6.0), (11, 9, 4.5))):
        G.polyline(d, [(x0, 14 + k * 0.4, 0), (x0 + w / 2, 14 + k * 0.4, h), (x0 + w, 14 + k * 0.4, 0)], 0.04, mtn,
                   cyclic=True, fill=True)
    # MID : maison et arbres à Y ≈ 3
    d = lay("MID")
    G.polyline(d, [(1.5, 3, 0), (4.5, 3, 0), (4.5, 3, 2.0), (1.5, 3, 2.0)], 0.02, wall, cyclic=True, fill=True)
    G.polyline(d, [(1.2, 3, 2.0), (3.0, 3, 3.3), (4.8, 3, 2.0)], 0.02, roof, cyclic=True, fill=True)
    G.polyline(d, [(2.7, 2.98, 0), (3.3, 2.98, 0), (3.3, 2.98, 1.1), (2.7, 2.98, 1.1)], 0.015, ink, cyclic=True)
    tree(d, -2.5, 3.5, 3.2, 0.02, ink, leaf)
    tree(d, 6.5, 4.0, 2.6, 0.02, ink, leaf)
    G.mannequin(d, -0.3, 0.0, 1.7, "walk", 0.012, ink)
    # FG : grand arbre coupé par le cadre et buissons à Y = -5
    d = lay("FG")
    tree(d, -4.2, -5.0, 4.5, 0.03, ink, leaf)
    for bx in (3.0, 3.8, 4.6):
        G.polyline(d, [(bx + 0.5 * math.cos(t), -5.0, 0.35 + 0.35 * math.sin(t)) for t in [i * math.pi / 14 for i in range(15)]],
                   0.025, leaf, cyclic=True, fill=True)
    # GROUND : route et herbes à plat (Z = 0.02)
    d = lay("GROUND")
    G.polyline(d, [(-1.6, -9, 0.02), (1.4, -9, 0.02), (0.55, 13, 0.02), (-0.15, 13, 0.02)], 0.02, road,
               cyclic=True, fill=True)
    for y in range(-8, 12, 2):
        G.polyline(d, [(-0.1 + y * -0.01, y, 0.03), (-0.1 + y * -0.01, y + 0.9, 0.03)], 0.03, ink, opacity=0.6)
    for gx, gy in ((-3, -7), (2.5, -6), (-2, -2), (2.2, 0), (-1.8, 6)):
        for j in range(4):
            G.polyline(d, [(gx + j * 0.15, gy, 0.02), (gx + j * 0.15 + 0.05, gy + 0.35, 0.02)], 0.01, ink)


def main():
    sc, ob = scene()
    L.instructions(NOTE)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_09_set_starter.blend"))
    sc, ob = scene()
    # le personnage du calque MID est dessiné dans le plan Y = 0 : on le décale à Y = 2
    solution(ob)
    d = ob.data.layers["MID"].frames[0].drawing
    for s in d.strokes:
        for p in s.points:
            if p.position.y == 0.0:
                p.position.y = 2.0
    d.tag_positions_changed()
    bpy.context.view_layer.use_pass_z = True
    for l in ob.data.layers:          # couleurs « plates » : les calques ignorent le soleil
        l.use_lights = False
    L.instructions(NOTE)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_09_set_solution.blend"))
    out = os.path.dirname(p)
    sc.render.filepath = os.path.join(out, "ch18_09_set_reference.png")
    bpy.ops.render.render(write_still=True)
    # vue de dessus : montre les profondeurs
    top = L.camera("CAM_Top", L.collection("CAMERAS"), (0, 3, 60), 50, make_active=True)
    top.data.type = "ORTHO"
    top.data.ortho_scale = 46
    top.data.clip_end = 200
    sc.render.filepath = os.path.join(out, "ch18_09_set_top.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
