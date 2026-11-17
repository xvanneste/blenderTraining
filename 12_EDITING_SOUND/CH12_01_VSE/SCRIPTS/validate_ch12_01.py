"""
validate_ch12_01.py — Correcteur « Video Sequencer » (CH12.01).
Usage : … --python-exit-code 1 --python validate_ch12_01.py -- --exercise vse [--debug]
Objets : quatre strips COLOR A_red, B_green, C_blue, D_yellow (fps 24, 64 × 36). Le correcteur lit les strips et RENDU le séquenceur (Workbench, Standard) :
  données : exactement ces quatre strips, aucun muet ; canal 1 pour tous ; ordre rouge, vert, bleu, jaune ; débuts 1, 25, 55, 73 ; durées 24, 30, 18, 24 (images) : montage bout à bout sans trou ni recouvrement ; plage de la scène 1–96 ;
  rendu : couleur dominante du pixel central à l'image 12 (rouge), 40 (vert), 63 (bleu) et 85 (jaune).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

GOOD = (("A_red", 1, 24), ("B_green", 25, 30), ("C_blue", 55, 18), ("D_yellow", 73, 24))
EXPECT = ((12, (1, 0, 0), "rouge"), (40, (0, 1, 0), "vert"), (63, (0, 0, 1), "bleu"), (85, (1, 1, 0), "jaune"))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.01 — Video Sequencer")
    sc = bpy.context.scene
    se = sc.sequence_editor
    names = sorted(s.name for s in se.strips_all) if se else []
    if not r.check(names == sorted(n for n, _, _ in GOOD), f"Les quatre strips sont présents : {names}", "Ne supprimez ni n'ajoutez de strip : A_red, B_green, C_blue, D_yellow.", 3):
        return r.finish()
    S = {s.name: s for s in se.strips_all}
    r.check(all(S[n].channel == 1 for n in S) and not any(S[n].mute for n in S), "Les quatre strips sont sur le canal 1 et non muets", "Strip > Channel : 1 pour tous (Sequencer : colonne de gauche).", 6)
    order = [s.name for s in sorted(S.values(), key=lambda s: s.frame_final_start)]
    r.check(order == ["A_red", "B_green", "C_blue", "D_yellow"], f"Ordre : {order} (rouge, vert, bleu, jaune)", "Remettez les strips dans l'ordre.", 6)
    dur = [S[n].frame_final_duration for n, _, _ in GOOD]
    r.check(dur == [24, 30, 18, 24], f"Durées : {dur} (24, 30, 18, 24)", "Poignées ou Strip > Time > Final Duration.", 8)
    starts = [S[n].frame_final_start for n, _, _ in GOOD]
    r.check(starts == [1, 25, 55, 73], f"Débuts : {starts} (1, 25, 55, 73 : bout à bout, sans trou)", "Déplacez les strips (G) : chacun commence à la fin du précédent.", 8)
    r.check(sc.frame_start == 1 and sc.frame_end == 96, f"Plage de la scène : {sc.frame_start}–{sc.frame_end} (1–96)", "Timeline : Frame End 96.", 4)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    sc.render.use_sequencer = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1201_val.png")
    bad = []
    for f, col, nm in EXPECT:
        sc.frame_set(f)
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], np.float32).reshape(36, 64, 4)[..., :3][::-1].copy()
        bpy.data.images.remove(im)
        c = px[18, 32]
        if np.abs(c - np.array(col)).max() > 0.2:
            bad.append(f"image {f} : attendu {nm}, rendu {tuple(round(float(v), 1) for v in c)}")
    r.check(not bad, "Rendu : rouge à l'image 12, vert à 40, bleu à 63, jaune à 85" if not bad else "Rendu faux : " + " ; ".join(bad), "Le séquenceur doit montrer la bonne couleur à chaque image test.", 10)
    if debug:
        print("[DEBUG]", {s.name: (s.frame_final_start, s.frame_final_duration, s.channel) for s in S.values()}, sc.frame_end)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
