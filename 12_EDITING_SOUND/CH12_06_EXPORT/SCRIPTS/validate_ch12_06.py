"""
validate_ch12_06.py — Correcteur « Export et livraison » (CH12.06).
Usage : … --python-exit-code 1 --python validate_ch12_06.py -- --exercise export [--debug]
Objets : strips PICTURE (COLOR, 1–48) et TONE (son de 2 s). Le correcteur LANCE le rendu de l'animation avec les réglages de sortie de l'élève (dossier temporaire) et ANALYSE le fichier .mp4 produit avec SCRIPTS/mp4probe.py (boîtes ISO : ftyp, mvhd, trak/hdlr/stsd) :
  conteneur : un fichier .mp4 est produit (marque ftyp présente) ;
  codec vidéo : piste « vide » de codec avc1 (H.264) ; codec audio : piste « soun » de codec mp4a (AAC) ;
  résolution : 640 × 360 ; durée : 2,0 s ± 0,1 ; cadence de la scène : 24 i/s ; poids ≤ 400 Ko.
Les strips (PICTURE, TONE) ne doivent pas être modifiés.
Testé avec : Blender 5.3.0.
"""
import glob
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, HERE)
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import mp4probe  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.06 — Export et livraison")
    sc = bpy.context.scene
    se = sc.sequence_editor
    names = sorted(s.name for s in se.strips_all) if se else []
    if not r.check(names == ["PICTURE", "TONE"], f"Strips PICTURE et TONE présents : {names}", "Ne modifiez pas le montage.", 3):
        return r.finish()
    r.check(sc.render.fps == 24 and sc.render.fps_base == 1.0, f"Cadence : {sc.render.fps} i/s (24)", "Output Properties > Format : Frame Rate 24 fps.", 4)
    tmp = tempfile.mkdtemp(prefix="bcma_ch1206v_")
    keep = sc.render.filepath
    sc.render.filepath = os.path.join(tmp, "web_")
    try:
        bpy.ops.render.render(animation=True)
    finally:
        sc.render.filepath = keep
    mp4 = glob.glob(os.path.join(tmp, "web_*.mp4"))
    others = [os.path.basename(f) for f in os.listdir(tmp)]
    if not r.check(bool(mp4), "Un fichier .mp4 est produit" if mp4 else f"Aucun .mp4 produit (fichiers : {others[:3]}…)", "Output > média Vidéo, File Format FFmpeg Video, conteneur MPEG-4.", 10):
        shutil.rmtree(tmp, ignore_errors=True)
        return r.finish()
    res = mp4probe.analyse(mp4[0])
    size = os.path.getsize(mp4[0])
    shutil.rmtree(tmp, ignore_errors=True)
    vid = next((t for t in res["tracks"] if t["kind"] == "vide"), None)
    aud = next((t for t in res["tracks"] if t["kind"] == "soun"), None)
    r.check(vid is not None and vid["codec"] == "avc1", f"Codec vidéo : {vid['codec'] if vid else 'aucune piste'} (avc1 = H.264)", "Encoding > Video Codec : H.264.", 8)
    r.check(aud is not None and aud["codec"] == "mp4a", f"Codec audio : {aud['codec'] if aud else 'aucune piste audio'} (mp4a = AAC)", "Encoding > Audio Codec : AAC.", 8)
    r.check(vid is not None and (vid["width"], vid["height"]) == (640, 360), f"Résolution : {vid['width'] if vid else 0} × {vid['height'] if vid else 0} (640 × 360)", "Résolution 640 × 360 à 100 %.", 8)
    r.check(abs(res["duration"] - 2.0) <= 0.1, f"Durée : {res['duration']:.3f} s (2,0 ± 0,1)", "Plage 1–48 à 24 i/s.", 8)
    r.check(size <= 400 * 1024, f"Poids : {size / 1024:.0f} Ko (≤ 400 Ko)", "Qualité / débit trop élevés.", 4)
    if debug:
        print("[DEBUG]", res, size)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
