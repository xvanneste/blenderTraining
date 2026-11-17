"""
build_ch01_12_files.py — Le portrait du gardien (CH01.12 : caméras).

  STARTER_FILES/ch01_12_portrait_starter.blend
      Un « gardien » stylisé (corps + tête, EMP_Head marque le regard à 1,65 m) devant un
      phare en arrière-plan ; CAM_Shot : caméra 24 mm placée au hasard, sans profondeur de champ.
  COMPLETED_EXAMPLES/ch01_12_portrait_solution.blend
      CAM_Shot : 50 mm, à hauteur d'œil, tête du gardien sur le tiers supérieur gauche,
      profondeur de champ activée (Focus on Object = EMP_Head, f/2.8), guides des tiers.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch01_12_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.12 — LE PORTRAIT DU GARDIEN (caméra CAM_Shot, vue caméra : Num 0)
1. Focale portrait : 50 à 85 mm (solution : 50 mm) (Object Data > Lens > Focal Length).
2. Caméra à hauteur d'œil : 1,4 à 1,9 m du sol, à 2–6 m du gardien.
3. Composition : la tête (EMP_Head) sur une ligne des TIERS : en haut (≈ 2/3 de la hauteur)
   et à gauche ou à droite (≈ 1/3 ou 2/3 de la largeur). Activez les guides :
   Object Data > Viewport Display > Composition Guides > Thirds.
4. Le phare doit rester visible dans le cadre (arrière-plan).
5. Profondeur de champ : Depth of Field coché, Focus on Object = EMP_Head, F-Stop ≤ 4.
Astuce : naviguez, Ctrl+Alt+Num 0, puis affinez avec Lock Camera to View (N > View) — et
pensez à le désactiver ensuite.
"""


def build(solution):
    L.reset("SC_Portrait")
    sc = bpy.context.scene
    col = L.collection("CHARACTERS")
    setc = L.collection("SET")
    skin = L.material("MAT_Skin", (0.8, 0.55, 0.42), 0.5)
    coat = L.material("MAT_Coat", (0.12, 0.2, 0.35), 0.7)
    L.plane("GEO_Ground", setc, L.material("MAT_Sand", (0.55, 0.5, 0.4), 0.9), size=80)
    L.cylinder("GEO_Body", col, coat, radius=0.28, depth=1.5, location=(0, 0, 0.75))  # cou : la tête repose sur le corps
    L.sphere("GEO_Head", col, skin, radius=0.16, location=(0, 0, 1.6))
    head = L.empty("EMP_Head", col, (0, -0.1, 1.65), "SPHERE", 0.05)
    white = L.material("MAT_White", (0.85, 0.85, 0.85), 0.6)
    red = L.material("MAT_Red", (0.6, 0.08, 0.06), 0.6)
    L.cylinder("GEO_Lighthouse", setc, white, radius=1.2, depth=10, location=(9, 30, 5))
    L.cylinder("GEO_Lighthouse_Band", setc, red, radius=1.22, depth=1.5, location=(9, 30, 7))
    L.light("LGT_Sun", L.collection("LIGHTS"), "SUN", (0, 0, 10), 4, rotation=(55, 0, 35))
    L.world((0.45, 0.55, 0.75), 1.0, "WO_Sky")
    cam = L.camera("CAM_Shot", L.collection("CAMERAS"), (6, -3, 0.4), 24)
    cam.rotation_euler = (math.radians(95), 0, math.radians(70))
    cam.data.show_composition_thirds = False
    if solution:
        cam.data.lens = 50
        cam.data.show_composition_thirds = True
        cam.location = (0.55, -4.2, 1.6)
        sc.camera = cam
        sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
        # Orientation calculée numériquement : tête en (1/3 ; 2/3) du cadre (règle des tiers)
        def proj(pitch, yaw):
            cam.rotation_euler = (pitch, 0, yaw)
            bpy.context.view_layer.update()
            p = world_to_camera_view(sc, cam, head.matrix_world.translation)
            return p.x - 1 / 3, p.y - 2 / 3

        pitch, yaw, h = math.radians(90), 0.0, 1e-3
        for _ in range(20):  # méthode de Newton à dérivées numériques
            ex, ey = proj(pitch, yaw)
            if abs(ex) < 1e-5 and abs(ey) < 1e-5:
                break
            a1, b1 = proj(pitch + h, yaw)
            a2, b2 = proj(pitch, yaw + h)
            j11, j12, j21, j22 = (a1 - ex) / h, (a2 - ex) / h, (b1 - ey) / h, (b2 - ey) / h
            det = j11 * j22 - j12 * j21
            pitch -= (j22 * ex - j12 * ey) / det
            yaw -= (-j21 * ex + j11 * ey) / det
        cam.rotation_euler = (pitch, 0, yaw)
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = head
        cam.data.dof.aperture_fstop = 2.8
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)
    if solution:
        bpy.context.view_layer.update()
        p = world_to_camera_view(sc, cam, head.matrix_world.translation)
        print(f"[BCMA] tête dans le cadre : x={p.x:.3f} y={p.y:.3f}")


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_12_portrait_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_12_portrait_solution.blend"))


if __name__ == "__main__":
    L.run(main)
