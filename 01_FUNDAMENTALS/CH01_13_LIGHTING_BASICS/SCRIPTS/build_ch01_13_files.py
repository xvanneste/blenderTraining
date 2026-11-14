"""
build_ch01_13_files.py — Le buste dans le noir (CH01.13 : éclairage élémentaire).

  STARTER_FILES/ch01_13_bust_starter.blend
      Un buste (Suzanne sur socle) face à la caméra (regarde -Y), monde presque noir,
      AUCUNE lumière. Rendu actuel : noir.
  COMPLETED_EXAMPLES/ch01_13_bust_solution.blend
      Éclairage trois points : LGT_Key (Area 450 W, avant-gauche, en hauteur, 4500 K),
      LGT_Fill (Area 70 W, avant-droite, plus basse, 6500 K), LGT_Rim (Spot 900 W, derrière).
Usage : blender -b --factory-startup --python build_ch01_13_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.13 — LE BUSTE DANS LE NOIR (mode Rendered : Z > Rendered)
Éclairez le buste avec un ÉCLAIRAGE TROIS POINTS (Shift+A > Light) :
- KEY (principale) : la plus puissante, devant le sujet (côté caméra), décalée sur le côté,
  au-dessus de la tête. Nom : LGT_Key.
- FILL (remplissage) : du côté opposé, 2 à 8 fois moins puissante. Nom : LGT_Fill.
- RIM (contre-jour) : DERRIÈRE le sujet, en hauteur, pour détacher la silhouette. Nom : LGT_Rim.
Le monde doit rester sombre (Strength ≤ 0,3). L'image ne doit être ni noire ni brûlée.
Bonus : utilisez Temperature (K) : key chaude (~4000–5000 K), fill froide (~6500–8000 K).
"""
SUBJECT_Y = 0.0


def build(solution):
    L.reset("SC_Bust")
    col = L.collection("PROPS")
    setc = L.collection("SET")
    grey = L.material("MAT_Backdrop", (0.12, 0.12, 0.13), 0.7)
    L.plane("GEO_Floor", setc, grey, size=20)
    L.plane("GEO_Backdrop", setc, grey, size=20, location=(0, 7, 10), rotation=(1.5708, 0, 0))
    L.cylinder("GEO_Plinth", col, L.material("MAT_Marble", (0.75, 0.74, 0.72), 0.3), radius=0.35, depth=1.0,
               location=(0, SUBJECT_Y, 0.5))
    bust = L.mesh(bpy.ops.mesh.primitive_monkey_add, "GEO_Bust", col, L.material("MAT_Plaster", (0.8, 0.78, 0.74), 0.55),
                  size=0.9, location=(0, SUBJECT_Y, 1.4))
    sub = bust.modifiers.new("Subdivision", "SUBSURF")
    sub.levels, sub.render_levels = 1, 2
    for p in bust.data.polygons:
        p.use_smooth = True
    tgt = L.empty("EMP_Target", L.collection("CAMERAS"), (0, SUBJECT_Y, 1.35))
    L.camera("CAM_Main", L.collection("CAMERAS"), (0.6, -5.5, 1.6), 65, tgt)
    L.world((0.01, 0.01, 0.012), 0.2, "WO_Dark")
    if solution:
        lc = L.collection("LIGHTS")
        key = L.light("LGT_Key", lc, "AREA", (-2.2, -2.2, 2.8), 450, 0.8, target=tgt)
        fill = L.light("LGT_Fill", lc, "AREA", (2.5, -2.0, 1.6), 70, 2.0, target=tgt)
        rim = L.light("LGT_Rim", lc, "SPOT", (1.0, 2.5, 3.0), 900, target=tgt)
        for lt, k in ((key, 4500), (fill, 7000)):
            lt.data.use_temperature = True
            lt.data.temperature = k
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.eevee.taa_render_samples = 32
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_13_bust_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_13_bust_solution.blend"))


if __name__ == "__main__":
    L.run(main)
