"""
validate_ch00_01.py — Correcteur automatique des exercices du chapitre CH00.01.

Vérifie un fichier .blend rendu par l'apprenant et affiche une note détaillée.

Usage :
  blender -b --factory-startup <votre_fichier.blend> --python validate_ch00_01.py -- --exercise EX
avec EX parmi :
  testcard      Configuration Cycles GPU
  testcard_cpu  Configuration Cycles CPU
  broken    Exercice 3 (difficile) : les 5 pannes de rendu sont-elles réparées ?

Option : --render   effectue en plus un mini-rendu (25 %, 8 échantillons) et vérifie
                    que l'image n'est pas noire.
Code de retour : 0 si toutes les vérifications obligatoires passent, 1 sinon
(placez --python-exit-code 1 avant --python pour signaler aussi une exception Python).

Testé avec : Blender 5.3.0.
"""
import argparse
import os
import re
import sys
import tempfile

import bpy


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Correcteur CH00.01")
    parser.add_argument("--exercise", choices=("testcard", "testcard_cpu", "broken"), default="testcard")
    parser.add_argument("--render", action="store_true")
    return parser.parse_args(argv)


class Report:
    def __init__(self):
        self.items = []

    def check(self, ok, label, hint, points=1, mandatory=True):
        self.items.append((bool(ok), label, hint, points, mandatory))

    def print(self):
        got = sum(i[3] for i in self.items if i[0])
        total = sum(i[3] for i in self.items)
        print("\n================ BCMA — CORRECTION CH00.01 ================")
        for ok, label, hint, pts, mand in self.items:
            tag = "✔" if ok else ("✘" if mand else "–")
            print(f" {tag} [{pts} pt] {label}")
            if not ok:
                print(f"      → piste : {hint}")
        print(f"------------------------------------------------------------\n Score : {got}/{total}")
        failed = [i for i in self.items if i[4] and not i[0]]
        print(" RÉSULTAT :", "VALIDÉ" if not failed else f"À CORRIGER ({len(failed)} point(s) obligatoire(s))")
        print("============================================================\n")
        return 0 if not failed else 1


def image_mean_luminance(path):
    img = bpy.data.images.load(path)
    px = list(img.pixels)
    n = len(px) // 4
    lum = sum(0.2126 * px[i * 4] + 0.7152 * px[i * 4 + 1] + 0.0722 * px[i * 4 + 2] for i in range(n)) / max(n, 1)
    bpy.data.images.remove(img)
    return lum


def quick_render(scene):
    scene.render.resolution_percentage = 25
    scene.cycles.samples = 8
    scene.cycles.use_denoising = False
    scene.cycles.device = "CPU"  # rendu de contrôle portable, indépendant du GPU
    with tempfile.TemporaryDirectory(prefix="bcma_ch00_01_") as directory:
        path = os.path.join(directory, "controle.png")
        scene.render.filepath = path
        scene.render.image_settings.media_type = "IMAGE"
        scene.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(write_still=True)
        return image_mean_luminance(path)


def validate_testcard(r, scene, device="GPU"):
    fname = os.path.basename(bpy.data.filepath)
    r.check(scene.render.engine == "CYCLES", "Moteur de rendu = Cycles",
            "Properties > Render > Render Engine > Cycles", 2)
    label = "GPU Compute" if device == "GPU" else "CPU"
    r.check(scene.cycles.device == device, f"Périphérique = {label}",
            f"Render Properties > Device > {label}", 2)
    r.check(32 <= scene.cycles.samples <= 512, f"Échantillons de rendu raisonnables ({scene.cycles.samples})",
            "Render > Sampling > Render > Max Samples entre 32 et 512 pour un test", 1)
    r.check(scene.cycles.use_denoising, "Débruitage activé au rendu",
            "Render > Sampling > Render > Denoise", 1)
    r.check(scene.render.resolution_percentage == 100, "Résolution à 100 %",
            "Output > Format > Resolution % = 100", 1)
    r.check(scene.render.filepath.startswith("//"), f"Chemin de sortie relatif ({scene.render.filepath})",
            "Output > Output : un chemin commençant par // (relatif au .blend)", 1)
    r.check(re.search(r"_v\d{3}\.blend$", fname) is not None or "solution" in fname,
            f"Nom de fichier versionné ({fname})",
            "Enregistrez sous ch00_01_testcard_<prenom>_v001.blend (puis Ctrl+Alt+S pour v002…)", 1,
            mandatory=False)


def validate_broken(r, scene):
    cam = scene.camera
    r.check(cam is not None and cam.data.clip_end >= 20, "Panne 1 réparée : Clip End de la caméra",
            "Sélectionnez la caméra > Object Data (icône caméra verte) > Clip End", 2)
    key = bpy.data.objects.get("LGT_Key")
    r.check(key is not None and not key.hide_render, "Panne 2 réparée : LGT_Key visible au rendu",
            "Outliner > filtre (entonnoir) > afficher l'icône appareil photo, puis réactivez-la", 2)
    bg = None
    if scene.world and scene.world.node_tree:
        bg = next((n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND"), None)
    r.check(bg is not None and bg.inputs["Strength"].default_value > 0.05,
            "Panne 3 réparée : intensité du World > 0",
            "Properties > World > Surface > Strength", 2)
    props = bpy.data.collections.get("PROPS")
    r.check(props is not None and not props.hide_render, "Panne 4 réparée : collection PROPS rendue",
            "Outliner > activez l'icône appareil photo de la collection PROPS", 2)
    r.check(scene.render.resolution_percentage == 100, "Panne 5 réparée : résolution à 100 %",
            "Properties > Output > Format > % sous Resolution", 2)


def main():
    options = args()
    exercise = options.exercise
    scene = bpy.context.scene
    r = Report()
    if not bpy.data.filepath:
        print("[BCMA] Aucun fichier ouvert : passez le .blend AVANT --python.")
        sys.exit(1)
    print(f"[BCMA] Fichier : {bpy.data.filepath}  —  exercice : {exercise}")
    if exercise == "broken":
        validate_broken(r, scene)
    else:
        validate_testcard(r, scene, device="CPU" if exercise == "testcard_cpu" else "GPU")
    if options.render:
        lum = quick_render(scene)
        r.check(lum > 0.02, f"Rendu de contrôle non noir (luminance moyenne {lum:.3f})",
                "L'image est (presque) noire : lumières, monde, caméra ou collections ?", 2)
    code = r.print()
    sys.exit(code)


if __name__ == "__main__":
    main()
