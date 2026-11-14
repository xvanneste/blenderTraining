"""
build_ch01_14_files.py — Le premier rendu final (CH01.14).

  STARTER_FILES/ch01_14_final_render_starter.blend
      Nature morte éclairée (tasse, théière stylisée, livres, pommes) + caméra : prête à être
      rendue, mais réglages de rendu par défaut (EEVEE, 50 %, sortie /tmp, vue Standard).
  COMPLETED_EXAMPLES/ch01_14_final_render_solution.blend
      Cycles GPU, 128 échantillons adaptatifs (seuil 0,02), débruitage, 1920×1080 100 %,
      PNG RGB 8 bits, AgX + Look « AgX - Medium High Contrast », sortie //renders/.
  COMPLETED_EXAMPLES/renders/ch01_14_final.png       rendu final Cycles (1920×1080)
  COMPLETED_EXAMPLES/renders/ch01_14_eevee.png       même plan en EEVEE (comparaison)
Usage : blender -b --factory-startup --python build_ch01_14_files.py --python-exit-code 1
        (le rendu utilise OptiX/CUDA si disponible, sinon le CPU)
Testé avec : Blender 5.3.0 (RTX 3080, OptiX).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.14 — LE PREMIER RENDU FINAL
Réglez puis rendez :
1. Render : Cycles, Device GPU Compute, Sampling > Render : Noise Threshold 0,02,
   Max Samples 128, Denoise coché.
2. Output : 1920 × 1080, 100 %, File Format PNG, Color RGB, Color Depth 8.
   Output path : //renders/ch01_14_final_
3. Render > Color Management : View Transform AgX, Look « AgX - Medium High Contrast ».
4. F12. Dans la fenêtre de rendu : Image > Save As (Shift+Alt+S) ->
   renders/ch01_14_final.png (dossier renders à côté de votre .blend).
5. Bonus : passez en EEVEE, F12, enregistrez renders/ch01_14_eevee.png, comparez.
"""


def build(solution):
    L.reset("SC_StillLife")
    st = L.studio(subject_height=0.6, key=350, fill=60, rim=400)
    st["camera"].location = (0.9, -3.2, 1.25)
    st["camera"].data.lens = 70
    st["target"].location = (0, 0, 0.35)
    col = L.collection("PROPS")
    table = L.material("MAT_Wood_Table", (0.35, 0.2, 0.1), 0.45)
    L.cube("GEO_Table", col, table, size=1, location=(0, 0.2, 0.1), scale=(2.2, 1.2, 0.2))
    china = L.material("MAT_China", (0.85, 0.85, 0.82), 0.15)
    cup = L.cylinder("GEO_Cup", col, china, radius=0.09, depth=0.12, location=(-0.35, -0.1, 0.26), vertices=48)
    for poly in cup.data.polygons:
        poly.use_smooth = abs(poly.normal.z) < 0.5  # côtés lissés, fond et dessus plats
    s = cup.modifiers.new("Solidify", "SOLIDIFY")
    s.thickness = 0.008
    pot = L.sphere("GEO_Teapot", col, L.material("MAT_Teal", (0.05, 0.35, 0.38), 0.2), radius=0.2,
                   location=(0.15, 0.25, 0.37), scale=(1.2, 1, 0.85))
    pot.modifiers.new("Subdivision", "SUBSURF").render_levels = 2
    L.cylinder("GEO_Spout", col, L.material("MAT_Teal", (0.05, 0.35, 0.38), 0.2), radius=0.03, depth=0.25,
               location=(0.45, 0.25, 0.42), rotation=(0, 1.0, 0))
    for i, (z, c) in enumerate([(0.225, (0.5, 0.1, 0.1)), (0.275, (0.1, 0.2, 0.45)), (0.32, (0.7, 0.6, 0.3))]):
        L.cube(f"GEO_Book_{i + 1}", col, L.material(f"MAT_Book_{i + 1}", c, 0.6), size=1,
               location=(0.65, -0.05, z), scale=(0.32, 0.22, 0.045), rotation=(0, 0, 0.15 * i))
    for i, (x, y) in enumerate([(-0.1, -0.35), (0.05, -0.42)]):
        L.sphere(f"GEO_Apple_{i + 1}", col, L.material("MAT_Apple", (0.55, 0.05, 0.03), 0.35), radius=0.06,
                 location=(x, y, 0.26))
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 50
    sc.render.filepath = "/tmp/"
    sc.view_settings.view_transform = "Standard"
    if solution:
        sc.render.engine = "CYCLES"
        sc.cycles.device = "GPU"
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.02
        sc.cycles.samples = 128
        sc.cycles.use_denoising = True
        sc.render.resolution_percentage = 100
        im = sc.render.image_settings
        im.file_format, im.color_mode, im.color_depth = "PNG", "RGB", "8"
        sc.render.filepath = "//renders/ch01_14_final_"
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"
    L.instructions(NOTE)
    return sc


def use_best_device(sc):
    cp = bpy.context.preferences.addons["cycles"].preferences
    for api in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            cp.compute_device_type = api
            cp.refresh_devices()
            devs = [d for d in cp.get_devices_for_type(api) if d.type == api]
            if devs:
                for d in cp.devices:
                    d.use = d.type == api
                return api
        except Exception:
            continue
    sc.cycles.device = "CPU"
    return "CPU"


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_14_final_render_starter.blend"))
    sc = build(True)
    path = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_14_final_render_solution.blend"))
    api = use_best_device(sc)
    out = os.path.join(os.path.dirname(path), "renders")
    os.makedirs(out, exist_ok=True)
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(os.path.join(out, "ch01_14_final.png"))
    print(f"[BCMA] rendu Cycles ({api}) enregistré")
    sc.render.engine = "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = 64
    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(os.path.join(out, "ch01_14_eevee.png"))
    print("[BCMA] rendu EEVEE enregistré")
    return 0


if __name__ == "__main__":
    L.run(main)
