"""
bcma_render_benchmark.py — Benchmark comparatif CPU / GPU avec Cycles (CH00.01, L4).

Ouvre la mire de test du chapitre (ou le .blend passé avec --file), puis rend la
même image avec chaque périphérique disponible (CPU, puis GPU CUDA et/ou OptiX)
avec un nombre d'échantillons FIXE (échantillonnage adaptatif désactivé et
débruitage désactivé, pour que la comparaison soit honnête).

Usage :
  blender -b --factory-startup --python bcma_render_benchmark.py -- [options]
Options :
  --file  chemin.blend      (défaut : STARTER_FILES/ch00_01_testcard_starter.blend)
  --out   dossier           (défaut : <chapitre>/SCRIPTS/reports/benchmark)
  --samples N               (défaut : 64)
  --percent P               (défaut : 50  → 960×540)
  --devices CPU,CUDA,OPTIX  (défaut : tous ceux qui sont disponibles)
  --no-warmup               (ne pas faire de rendu de chauffe GPU avant la mesure)

Sorties : une image PNG par périphérique + benchmark_<date>.json + .md
Testé avec : Blender 5.3.0 (Windows 11, i9-10900 + RTX 3080).
"""
import datetime as _dt
import json
import os
import sys
import time

import bpy

CHAPTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    def opt(name, default):
        return argv[argv.index(name) + 1] if name in argv else default

    return {
        "file": os.path.abspath(opt("--file", os.path.join(CHAPTER_DIR, "STARTER_FILES", "ch00_01_testcard_starter.blend"))),
        # chemin absolu : après open_mainfile, un chemin relatif serait ambigu
        "out": os.path.abspath(opt("--out", os.path.join(CHAPTER_DIR, "SCRIPTS", "reports", "benchmark"))),
        "samples": int(opt("--samples", "64")),
        "percent": int(opt("--percent", "50")),
        "devices": opt("--devices", ""),
        "warmup": "--no-warmup" not in argv,
    }


def available_devices():
    cp = bpy.context.preferences.addons["cycles"].preferences
    found = ["CPU"]
    for api in ("CUDA", "OPTIX", "HIP", "ONEAPI"):
        try:
            cp.compute_device_type = api
            cp.refresh_devices()
            if any(d.type == api for d in cp.get_devices_for_type(api)):
                found.append(api)
        except Exception:
            pass
    return found


def select_device(scene, api):
    """Active un seul type de périphérique pour la mesure."""
    cp = bpy.context.preferences.addons["cycles"].preferences
    if api == "CPU":
        scene.cycles.device = "CPU"
        return ["CPU"]
    cp.compute_device_type = api
    cp.refresh_devices()
    used = []
    for d in cp.get_devices_for_type(api):
        d.use = d.type == api          # GPU seulement (pas de rendu hybride CPU+GPU)
        if d.use:
            used.append(d.name)
    scene.cycles.device = "GPU"
    return used


def main():
    args = parse_args()
    bpy.ops.wm.open_mainfile(filepath=args["file"])
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = args["samples"]
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.use_denoising = False
    scene.render.resolution_percentage = args["percent"]
    scene.render.image_settings.file_format = "PNG"
    os.makedirs(args["out"], exist_ok=True)

    devices = args["devices"].split(",") if args["devices"] else available_devices()
    results = []
    for api in devices:
        used = select_device(scene, api)
        if args["warmup"] and api != "CPU":
            # Rendu de chauffe minuscule : le premier rendu GPU charge/compile les
            # noyaux (kernels) Cycles, ce qui fausserait la mesure.
            pct, smp = scene.render.resolution_percentage, scene.cycles.samples
            scene.render.resolution_percentage, scene.cycles.samples = 5, 1
            bpy.ops.render.render(write_still=False)
            scene.render.resolution_percentage, scene.cycles.samples = pct, smp
        scene.render.filepath = os.path.join(args["out"], f"bench_{api.lower()}.png")
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        dt = time.perf_counter() - t0
        results.append({"api": api, "devices": used, "seconds": round(dt, 2),
                        "image": scene.render.filepath})
        print(f"[BCMA] {api:6s} {dt:7.2f} s  ({', '.join(used)})")

    base = next((r["seconds"] for r in results if r["api"] == "CPU"), None)
    for r in results:
        r["speedup_vs_cpu"] = round(base / r["seconds"], 2) if base and r["seconds"] else None

    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = {"blender": bpy.app.version_string, "file": args["file"], "samples": args["samples"],
            "resolution": [scene.render.resolution_x * args["percent"] // 100,
                           scene.render.resolution_y * args["percent"] // 100],
            "results": results, "date": stamp}
    with open(os.path.join(args["out"], f"benchmark_{stamp}.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    md = ["# Benchmark BCMA", "", f"Blender {meta['blender']} — {meta['samples']} échantillons — "
          f"{meta['resolution'][0]}×{meta['resolution'][1]}", "",
          "| API | Périphérique(s) | Temps (s) | Accélération vs CPU |", "|---|---|---|---|"]
    md += [f"| {r['api']} | {', '.join(r['devices'])} | {r['seconds']} | ×{r['speedup_vs_cpu']} |"
           for r in results]
    with open(os.path.join(args["out"], f"benchmark_{stamp}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("[BCMA] Benchmark terminé.")


if __name__ == "__main__":
    main()
