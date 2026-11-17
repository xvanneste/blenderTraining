"""Blender 5.3, depuis l’animatique de 15 s. Emballe la démonstration de livraison."""
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COURT = ROOT / "15_SHORT_FILMS/ASSETS_ATELIERS"
sys.path.insert(0, str(ROOT / "SCRIPTS"))
import bcma_lib as L

SRT = """1
00:00:05,000 --> 00:00:08,750
[Mina approche la main du bouton.]

2
00:00:09,000 --> 00:00:11,250
[Le signal retentit.]
"""
GUIDE = """# Sur le quai · livraison de démonstration · v001

Animatique 15 s, 640 × 360 à 24 i/s. Les dessins de layout sont des rendus d’origine du cours. Le mix et les sous-titres sont fournis pour répéter une livraison. Le master Matroska FFV1 conserve la sortie d’image de cette animatique sans perte de compression. Le WAV est séparé. La copie de revue utilise H.264/AAC.

Après extraction, ouvrez Projet/sur_le_quai_animatique.blend dans Blender 5.3. Ses trois images et son son se trouvent dans le même dossier. Lire le master et la revue. Comparer les départs d’images 1, 121 et 217. Le premier SRT décrit le geste et le second correspond au départ du clic à 9 s. Consulter MANIFEST.json si une pièce ne correspond pas à la livraison.

Crédits et provenance. Visuels, son synthétisé et textes créés pour Blender Cinema Master Academy. Ressources originales fournies pour la pratique du cursus.
"""


def main():
    bpy.ops.wm.open_mainfile(filepath=str(COURT / "sur_le_quai_animatique.blend"))
    scene = bpy.context.scene
    assert (scene.frame_end, scene.render.fps) == (360, 24)
    with tempfile.TemporaryDirectory(prefix="bcma_delivery_") as directory:
        folder = Path(directory)
        scene.render.ffmpeg.format = "MKV"
        scene.render.ffmpeg.codec = "FFV1"
        scene.render.ffmpeg.audio_codec = "NONE"
        scene.render.filepath = str(folder / "master_")
        bpy.ops.render.render(animation=True)
        [master] = list(folder.glob("master_*.mkv"))
        mix = folder / "mix.wav"
        bpy.ops.sound.mixdown(filepath=str(mix), check_existing=False,
                             container="WAV", codec="PCM", format="S16", split_channels=False)

        src_names = ("sur_le_quai_animatique.blend", "S010.png", "S020.png", "S030.png", "signal.wav")
        files = {f"Projet/{name}": (COURT / name).read_bytes() for name in src_names}
        files.update({
            "Master/sur_le_quai.mkv": master.read_bytes(),
            "Master/mix.wav": mix.read_bytes(),
            "Revue/sur_le_quai.mp4": (COURT / "sur_le_quai_animatique_0001-0360.mp4").read_bytes(),
            "Revue/fr.srt": SRT.encode("utf-8"),
            "LIRE.md": GUIDE.encode("utf-8"),
        })
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}
        manifest = {"version": "v001", "duree_ms": 15000, "fps": 24,
                    "sous_titres": "Revue/fr.srt", "fichiers": hashes}
        with zipfile.ZipFile(HERE / "livraison_demo.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
            archive.writestr("MANIFEST.json", json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    L.run(main)
