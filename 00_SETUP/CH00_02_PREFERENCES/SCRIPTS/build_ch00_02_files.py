"""
build_ch00_02_files.py — Génère le terrain d'entraînement à la navigation (CH00.02).

  STARTER_FILES/ch00_02_navigation_playground.blend
     Une « ville » de 400 blocs sur 200 m × 200 m, une aiguille minuscule (GEO_Needle)
     cachée entre les bâtiments, un objet très éloigné (GEO_FarBeacon, à 1 km), et un
     panneau de consignes. Sert à ressentir l'effet de Orbit Around Selection,
     Zoom to Mouse Position et Auto Depth.
  COMPLETED_EXAMPLES/ch00_02_navigation_solution.blend
     Même scène ; la caméra CAM_Needle cadre l'aiguille (résultat de l'exercice 3).

Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch00_02_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402

CH = L.chapter_dir(__file__)

INSTRUCTIONS = """CH00.02 — TERRAIN DE NAVIGATION
1. Sans changer les préférences : trouvez GEO_Needle (aiguille rouge) et zoomez dessus.
   Chronométrez-vous.
2. Activez Orbit Around Selection, Zoom to Mouse Position et Auto Depth
   (Edit > Preferences > Navigation). Recommencez. Comparez les temps.
3. Sélectionnez GEO_Needle dans l'Outliner puis View > Frame Selected (touche . du pavé
   numérique) : la méthode la plus rapide de toutes.
4. Trouvez GEO_FarBeacon (à 1 km). Pourquoi disparaît-il parfois ? (Clip End de la vue :
   N > View > Clip End)
5. Exercice 3 : placez la caméra CAM_Needle pour cadrer l'aiguille en gros plan
   (View > Align Active Camera to View, Ctrl+Alt+Num 0) et enregistrez en v001.
"""


def build(solution=False):
    L.reset("SC_Navigation")
    random.seed(42)
    city = L.collection("CITY")
    props = L.collection("PROPS")
    cams = L.collection("CAMERAS")
    m_bld = L.material("MAT_Building", (0.55, 0.57, 0.6), 0.7)
    m_ground = L.material("MAT_Ground", (0.12, 0.13, 0.12), 0.9)
    m_needle = L.material("MAT_Needle_Red", (0.9, 0.05, 0.03), 0.3, emission=(0.9, 0.05, 0.03), emission_strength=2)
    m_beacon = L.material("MAT_Beacon", (0.1, 0.6, 1.0), emission=(0.1, 0.6, 1.0), emission_strength=10)
    L.plane("GEO_Ground", city, m_ground, size=240)
    # Une seule donnée de maillage partagée par 400 blocs (duplication liée) : fichier léger.
    base = L.cube("GEO_Block_000", city, m_bld, size=1)
    me = base.data
    n = 0
    for ix in range(20):
        for iy in range(20):
            if ix == 10 and iy == 10:
                continue  # place libre au centre-ville
            h = random.uniform(3, 40)
            o = base if n == 0 else bpy_obj_copy(base, f"GEO_Block_{n:03d}", city)
            o.location = (-95 + ix * 10, -95 + iy * 10, h / 2)
            o.scale = (random.uniform(4, 7), random.uniform(4, 7), h)
            n += 1
    needle = L.cylinder("GEO_Needle", props, m_needle, radius=0.01, depth=0.25, vertices=12,
                        location=(20.0, -30.0, 0.125))  # dans une rue (entre deux rangées de blocs)
    L.sphere("GEO_FarBeacon", props, m_beacon, radius=3, location=(1000, 0, 20))
    tgt = L.empty("EMP_NeedleTarget", cams, needle.location, size=0.05)
    cam = L.camera("CAM_Needle", cams, (0, -60, 30), 50, make_active=True)
    if solution:
        cam.location = (20.0 + 0.45, -30.0 - 0.45, 0.32)
        cam.data.lens = 85
        L.track(cam, tgt)
    L.light("LGT_Sun", L.collection("LIGHTS"), "SUN", (0, 0, 50), 3, rotation=(40, 10, 30))
    L.world((0.35, 0.45, 0.6), 1.0, "WO_Sky")
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(INSTRUCTIONS)
    return me


def bpy_obj_copy(src, name, col):
    import bpy
    o = bpy.data.objects.new(name, src.data)  # même mesh : duplication liée (Alt+D)
    col.objects.link(o)
    return o


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch00_02_navigation_playground.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch00_02_navigation_solution.blend"))


if __name__ == "__main__":
    L.run(main)
