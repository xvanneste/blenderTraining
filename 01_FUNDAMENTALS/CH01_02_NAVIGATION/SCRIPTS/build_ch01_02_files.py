"""
build_ch01_02_files.py — Fichiers de CH01.02 (navigation 3D).

  STARTER_FILES/ch01_02_museum_starter.blend
      Un petit musée : statue (GEO_Statue) sur socle, 6 « œuvres » dispersées dont une
      minuscule (GEO_Coin), un objet caché derrière un mur (GEO_Hidden), caméras vides
      CAM_Front, CAM_Right, CAM_Top mal placées.
  COMPLETED_EXAMPLES/ch01_02_museum_solution.blend
      Les trois caméras orthographiques cadrent la statue de face, de droite, de dessus.
Usage : blender -b --factory-startup --python build_ch01_02_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.02 — LE MUSÉE
Navigation : MMB orbite · Shift+MMB pan · molette zoom · Num 1/3/7 vues · Num 5 persp/ortho
Num . cadrer la sélection · Home tout cadrer · Num / vue locale · Shift+` navigation Walk/Fly
1. Trouvez GEO_Coin (une pièce de 2 cm) et cadrez-la.
2. Trouvez GEO_Hidden (derrière un mur) sans déplacer le mur : vue locale ou Alt+B.
3. Exercice 3 : réglez CAM_Front, CAM_Right et CAM_Top en caméras ORTHOGRAPHIQUES qui
   cadrent GEO_Statue de face (vue depuis -Y), de droite (depuis +X) et de dessus.
   Méthode : Num 1 → Ctrl+Num 0 sur la caméra → Ctrl+Alt+Num 0 … puis
   Object Data > Lens > Type = Orthographic et Orthographic Scale.
"""


def build(solution):
    L.reset("SC_Museum")
    st = L.studio(subject_height=2.0)
    art = L.collection("ART")
    walls = L.collection("WALLS")
    stone = L.material("MAT_Stone", (0.7, 0.68, 0.62), 0.7)
    bronze = L.material("MAT_Bronze", (0.55, 0.35, 0.15), 0.35, 1.0)
    L.cylinder("GEO_Plinth", art, stone, radius=0.5, depth=1.0, location=(0, 0, 0.5))
    statue = L.mesh(bpy.ops.mesh.primitive_monkey_add, "GEO_Statue", art, bronze, size=1.0, location=(0, 0, 1.45))
    statue.rotation_euler = (math.radians(10), 0, 0)
    for p in statue.data.polygons:
        p.use_smooth = True
    L.cylinder("GEO_Coin", art, L.material("MAT_Gold", (1, 0.75, 0.3), 0.2, 1.0), radius=0.01, depth=0.002,
               location=(4.2, -3.1, 0.001))
    L.cube("GEO_Wall", walls, stone, size=1, location=(-5, 2, 1.5), scale=(0.2, 4, 3))
    L.sphere("GEO_Hidden", art, L.material("MAT_Red", (0.9, 0.05, 0.05)), radius=0.3, location=(-5.6, 2, 0.3))
    for i, (x, y) in enumerate([(5, 4), (-4, -5), (6, -1), (-2, 6)]):
        L.cube(f"GEO_Artwork_{i + 1:02d}", art, stone, size=0.6, location=(x, y, 0.3))
    cams = L.collection("CAMERAS")
    for name, loc, rot in [("CAM_Front", (0, -10, 1.2), (90, 0, 0)), ("CAM_Right", (10, 0, 1.2), (90, 0, 90)),
                           ("CAM_Top", (0, 0, 12), (0, 0, 0))]:
        c = L.camera(name, cams, (3, -3, 3) if not solution else loc, 50, make_active=False)
        if solution:
            c.rotation_euler = [math.radians(a) for a in rot]
            c.data.type = "ORTHO"
            c.data.ortho_scale = 3.2
            if name == "CAM_Top":
                c.location = (0, 0, 12)
            else:
                c.location.z = 1.2
    bpy.context.scene.camera = bpy.data.objects["CAM_Front"] if solution else st["camera"]
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_02_museum_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_02_museum_solution.blend"))


if __name__ == "__main__":
    L.run(main)
