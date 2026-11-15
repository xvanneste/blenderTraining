"""
build_ch18_06_files.py — Scène « Grease Pencil : interface et objets » (CH18.06).

  STARTER_FILES/ch18_06_gp_scene_starter.blend
      Petit décor 3D (sol, maison, arbre), caméra CAM_Shot, soleil. AUCUN objet Grease Pencil.
  COMPLETED_EXAMPLES/ch18_06_gp_scene_solution.blend (+ _reference.png)
      Collection DRAWINGS avec GP_Character (calques LINE, COLOR dans le groupe CHAR ; SKETCH
      verrouillé) devant la maison, et GP_Background (collines) derrière la maison.
Usage : blender -b --factory-startup --python build_ch18_06_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH18.06 — GREASE PENCIL : INTERFACE ET OBJETS
Décor 3D fourni (maison GEO_House à 4 m derrière l'origine). Caméra : CAM_Shot (Num 0).
1. Créez une collection DRAWINGS (dans la Scene Collection).
2. Add > Grease Pencil > Blank : renommez l'objet GP_Character (F2). Placez-le DEVANT la maison
   (entre la caméra et la maison), dans DRAWINGS.
3. Dans ses calques (Properties > Object Data > Layers) : LINE, COLOR, SKETCH.
   Créez un groupe de calques CHAR (icône dossier) et glissez-y LINE et COLOR.
   Verrouillez SKETCH (cadenas).
4. Draw Mode (Ctrl+Tab) : dessinez un personnage sur LINE (au moins 6 traits).
5. Ajoutez un second objet GP_Background (Blank), placé DERRIÈRE la maison, dans DRAWINGS :
   dessinez des collines ou des nuages (au moins 6 traits). Tout doit être visible dans CAM_Shot.
6. Properties > View Layer > Passes > Data : cochez Z. Sans cette passe, le RENDU final (F12)
   dessine le Grease Pencil par-dessus la maison au lieu de le cacher derrière (constaté en
   5.2 et 5.3 ; le viewport, lui, est correct).
Vérification : SCRIPTS/validate_ch18_06.py -- --exercise organize
"""


def scene():
    L.reset("SC_GP_Scene")
    col = L.collection("SET")
    grass = L.material("MAT_Grass", (0.25, 0.42, 0.18), 0.9)
    wall = L.material("MAT_Wall", (0.75, 0.68, 0.55), 0.7)
    roof = L.material("MAT_Roof", (0.45, 0.12, 0.08), 0.6)
    bark = L.material("MAT_Bark", (0.25, 0.15, 0.08), 0.9)
    leaf = L.material("MAT_Leaf", (0.12, 0.35, 0.12), 0.8)
    L.plane("GEO_Ground", col, grass, size=60)
    L.cube("GEO_House", col, wall, size=2.0, location=(1.2, 4.0, 1.0))
    r = L.mesh(bpy.ops.mesh.primitive_cone_add, "GEO_Roof", col, roof, vertices=4, radius1=1.75, depth=1.0,
               location=(1.2, 4.0, 2.5), rotation=(0, 0, math.radians(45)))
    L.cylinder("GEO_Trunk", col, bark, radius=0.12, depth=1.4, location=(-2.2, 5.0, 0.7))
    L.sphere("GEO_Leaves", col, leaf, radius=0.8, location=(-2.2, 5.0, 1.9))
    cc = L.collection("CAMERAS")
    cl = L.collection("LIGHTS")
    cam = L.camera("CAM_Shot", cc, (0, -9.0, 1.6), 35)
    cam.rotation_euler = (math.radians(88), 0, 0)
    L.light("LGT_Sun", cl, "SUN", (3, -3, 8), 3.5, rotation=(50, 10, 30))
    L.world((0.55, 0.7, 0.9), 1.0, "WO_Sky")
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    return sc


def solution():
    dcol = L.collection("DRAWINGS")
    # Personnage : plan de dessin vertical face caméra, à y = 1.5 (devant la maison, y = 4)
    ch = G.new_object("GP_Character", dcol, (-0.6, 1.5, 0.0))
    ink = G.material(ch, "MAT_GP_Ink", (0.02, 0.02, 0.02))
    red = G.material(ch, "MAT_GP_Red", (0.75, 0.1, 0.08))
    gp = ch.data
    grp = gp.layer_groups.new("CHAR")
    for n in ("COLOR", "LINE"):
        gp.layers.new(n, layer_group=grp)
    sk = gp.layers.new("SKETCH")
    d = G.layer(ch, "SKETCH")
    G.ellipse(d, (0, 1.0), 0.35, 0.9, 0.004, ink, 24)
    sk.lock = True
    sk.opacity = 0.3
    d = G.layer(ch, "LINE")
    G.mannequin(d, 0.0, 0.0, 1.7, "walk", 0.012, ink)
    d = G.layer(ch, "COLOR")
    G.hatch_ellipse(d, (0.0, 1.17), 0.2, 0.3, 0.035, 0.5, 0.01, red)   # pull rouge (hachures)
    # Fond : collines et nuages derrière la maison (y = 9)
    bg = G.new_object("GP_Background", dcol, (0.0, 9.0, 0.0))
    G.material(bg, "MAT_GP_Ink", (0.02, 0.02, 0.02))
    blue = G.material(bg, "MAT_GP_Hills", (0.15, 0.3, 0.55))
    d = G.layer(bg, "HILLS")
    for k, (amp, base) in enumerate(((0.8, 1.2), (0.5, 0.6))):
        G.polyline(d, [(-12 + i * 0.6, base + amp * math.sin(i * 0.45 + k)) for i in range(41)], 0.03, blue)
    for cx, cz in ((-5.0, 5.0), (3.5, 5.6), (8.0, 4.6)):
        for j in range(3):
            G.circle(d, (cx + j * 0.7, cz + 0.2 * (j % 2)), 0.5, 0.015, 0, 24)
    G.polyline(d, [(-12, 0.0), (12, 0.0)], 0.02, blue)
    # Sans passe Z, le rendu final ne masque pas le GP derrière les maillages (constaté 5.2/5.3).
    bpy.context.view_layer.use_pass_z = True


def main():
    scene()
    L.instructions(NOTE)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_06_gp_scene_starter.blend"))
    sc = scene()
    solution()
    L.instructions(NOTE)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_06_gp_scene_solution.blend"))
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_06_gp_scene_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
