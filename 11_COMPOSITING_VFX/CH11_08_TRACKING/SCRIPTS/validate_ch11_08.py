"""
validate_ch11_08.py — Correcteur « Tracking et matchmoving » (CH11.08).
Usage : … --python-exit-code 1 --python validate_ch11_08.py -- --exercise tracking [--debug]
Données : clip « ch11_08 » (séquence de 40 images 320 × 180 dans « ch11_08_clip/ », chemin relatif) filmé par une caméra de 35 mm / capteur 36 mm qui avance en translation de x = −1 à +1 m devant 48 points 3D (parallaxe).
Le correcteur contrôle ce que le fichier ENREGISTRE puis le REPRODUIT :
  clip : retrouvé, 320 × 180, 40 images ; caméra du clip : capteur 36 mm et focale de 31,5 à 38,5 mm (35 ± 10 %) ;
  pistes : au moins 12 pistes d'au moins 30 marqueurs ;
  reconstruction enregistrée : valide, erreur de reprojection moyenne ≤ 1,0 pixel (solution : 0,75) ;
  reproduction : Solve Camera Motion relancé par le correcteur (éditeur de clip temporaire) avec les pistes de l'élève : reconstruction valide et erreur ≤ 1,0 pixel (si aucune fenêtre n'est disponible, ce contrôle est signalé comme non effectué et ne compte pas).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.08 — Tracking et matchmoving")
    clip = bpy.data.movieclips.get("ch11_08")
    if not r.check(clip is not None, "Clip « ch11_08 » présent", "Partez du fichier de départ.", 2):
        return r.finish()
    ok_clip = tuple(clip.size) == (320, 180) and clip.frame_duration == 40
    if not r.check(ok_clip, f"Clip retrouvé : {tuple(clip.size)}, {clip.frame_duration} images", "Le dossier ch11_08_clip/ doit rester à côté du fichier.", 4):
        return r.finish()
    trk = clip.tracking
    cam = trk.camera
    r.check(abs(cam.sensor_width - 36.0) < 0.01 and 31.5 <= cam.focal_length <= 38.5, f"Caméra du clip : capteur {cam.sensor_width:.1f} mm, focale {cam.focal_length:.1f} mm (31,5–38,5)", "Movie Clip Editor > Tracking > Camera : Focal Length 35 mm, Sensor Width 36 mm.", 6)
    lens = [len(t.markers) for t in trk.tracks]
    nlong = sum(1 for n in lens if n >= 30)
    r.check(nlong >= 12, f"Pistes : {len(lens)} ; {nlong} d'au moins 30 marqueurs (≥ 12)", "Detect Features à l'image 1, puis Track Markers (sélectionnez les pistes, suivi vers l'avant sur toute la séquence).", 8)
    rec = trk.reconstruction
    r.check(rec.is_valid and rec.average_error <= 1.0, f"Reconstruction enregistrée : {'valide' if rec.is_valid else 'invalide'}, erreur moyenne {rec.average_error:.2f} px (≤ 1,0)", "Solve Camera Motion (Movie Clip Editor > Solve).", 8)
    wm = bpy.context.window_manager
    if wm.windows:
        win = wm.windows[0]
        area = win.screen.areas[0]
        keep = area.type
        area.type = "CLIP_EDITOR"
        sp = area.spaces.active
        sp.clip = clip
        reg = [x for x in area.regions if x.type == "WINDOW"][0]
        try:
            with bpy.context.temp_override(window=win, area=area, region=reg, space_data=sp):
                bpy.context.scene.active_clip = clip
                try:
                    res = bpy.ops.clip.solve_camera()
                except RuntimeError as e:  # noqa: BLE001
                    res = {str(e)[:40]}
            ok = "FINISHED" in res and trk.reconstruction.is_valid and trk.reconstruction.average_error <= 1.0
            r.check(ok, f"Reproduction : Solve Camera Motion relancé : {'valide' if trk.reconstruction.is_valid else 'invalide'}, erreur {trk.reconstruction.average_error:.2f} px (≤ 1,0)", "La résolution doit pouvoir être refaite avec vos pistes.", 8)
        finally:
            area.type = keep
    else:
        print("  (reproduction non effectuée : aucune fenêtre disponible)")
    if debug:
        print("[DEBUG] lens", lens, "valid", rec.is_valid, "err", rec.average_error, "focal", cam.focal_length)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
