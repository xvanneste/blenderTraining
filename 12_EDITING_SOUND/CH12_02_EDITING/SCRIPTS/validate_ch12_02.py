"""
validate_ch12_02.py — Correcteur « Montage narratif » (CH12.02).
Usage : … --python-exit-code 1 --python validate_ch12_02.py -- --exercise editing [--debug]
Objets : six strips COLOR SH1_wide, SH2_medium, SH3_close, SH4_medium, SH5_close, SH6_wide (le nom se termine par l'échelle de plan). Le correcteur lit les strips et rend le séquenceur (Workbench, Standard) :
  structure : les six plans et UN strip Crossfade (type CROSS) ; les cinq premiers plans (triés par début) sont sur le canal 1 ; SH6_wide (la résolution) est sur un autre canal ;
  échelles : aucune échelle identique à deux plans consécutifs (SH6 après le cinquième) ;
  rythme : durées des cinq premiers plans (par début) non croissantes ; durée de SH6 ≥ 2 × durée du cinquième ;
  fondu : SH6 commence 8 à 16 images avant la fin du cinquième plan ; le Crossfade a pour entrées le cinquième plan (input_1) et SH6 (input_2) et dure 8 à 16 images ;
  plage : dernière image de la scène = dernière image du dernier plan ; total de 100 à 130 images ;
  rendu : au milieu du fondu, couleur égale au mélange à 50 % des couleurs du cinquième plan et de SH6 (écart ≤ 0,15).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ["SH1_wide", "SH2_medium", "SH3_close", "SH4_medium", "SH5_close", "SH6_wide"]


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.02 — Montage narratif")
    sc = bpy.context.scene
    se = sc.sequence_editor
    allst = list(se.strips_all) if se else []
    S = {s.name: s for s in allst if s.type == "COLOR"}
    cross = [s for s in allst if s.type == "CROSS"]
    if not r.check(sorted(S) == sorted(NAMES), f"Les six plans sont présents : {sorted(S)}", "Ne supprimez ni n'ajoutez de plan.", 3):
        return r.finish()
    others = sorted((S[n] for n in NAMES if n != "SH6_wide"), key=lambda s: s.frame_final_start)
    six = S["SH6_wide"]
    seq = others + [six]
    r.check(all(s.channel == 1 for s in others) and six.channel != 1, f"Canaux : plans 1–5 sur le canal 1, SH6 sur le canal {six.channel}", "SH6 sur le canal 2 pour le fondu.", 5)
    size = lambda s: s.name.rsplit("_", 1)[1]
    jumps = [f"{a.name}→{b.name}" for a, b in zip(seq, seq[1:]) if size(a) == size(b)]
    r.check(not jumps, "Aucune échelle identique à deux plans consécutifs" if not jumps else f"Faux raccords d'échelle (jump cut) : {', '.join(jumps)}", "Alternez wide, medium, close : changez l'ordre.", 8)
    d = [s.frame_final_duration for s in others]
    r.check(all(d[i] >= d[i + 1] for i in range(len(d) - 1)), f"Rythme qui accélère : durées {d} (non croissantes)", "Chaque plan dure au plus autant que le précédent.", 8)
    r.check(six.frame_final_duration >= 2 * d[-1], f"Résolution : SH6 dure {six.frame_final_duration} images (≥ 2 × {d[-1]})", "Le dernier plan respire : au moins deux fois le cinquième.", 8)
    ov = others[-1].frame_final_end - six.frame_final_start
    r.check(8 <= ov <= 16, f"Recouvrement SH5/SH6 : {ov} images (8–16)", "SH6 commence 12 images avant la fin du cinquième plan.", 6)
    ok = len(cross) == 1 and cross[0].input_1 == others[-1] and cross[0].input_2 == six and 8 <= cross[0].frame_final_duration <= 16
    r.check(ok, "Crossfade : entrées (cinquième plan, SH6), durée " + (f"{cross[0].frame_final_duration} images" if cross else "—"), "Sélectionnez le cinquième plan puis SH6 : Add > Transition > Crossfade.", 8)
    last = max(s.frame_final_end for s in S.values()) - 1
    total = last
    r.check(sc.frame_start == 1 and sc.frame_end == last and 100 <= total <= 130, f"Plage de la scène : 1–{sc.frame_end} (dernière image du montage {last} ; total 100–130)", "Frame End = dernière image du dernier plan.", 6)
    if ok:
        mid = (cross[0].frame_final_start + cross[0].frame_final_end) // 2
        sc.render.engine = "BLENDER_WORKBENCH"
        sc.view_settings.view_transform = "Standard"
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
        sc.render.use_sequencer = True
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        sc.frame_set(mid)
        p = os.path.join(tempfile.gettempdir(), "bcma_ch1202_val.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], np.float32).reshape(36, 64, 4)[..., :3][::-1].copy()
        bpy.data.images.remove(im)
        want = (np.array(others[-1].color) + np.array(six.color)) / 2.0
        got = px[18, 32]
        r.check(np.abs(got - want).max() <= 0.15, f"Rendu au milieu du fondu (image {mid}) : {tuple(round(float(v), 2) for v in got)} (attendu {tuple(round(float(v), 2) for v in want)})", "Le fondu doit mélanger les deux plans.", 8)
    else:
        r.check(False, "Rendu au milieu du fondu non contrôlé (Crossfade manquant ou faux)", "Voir le contrôle Crossfade.", 8)
    if debug:
        print("[DEBUG]", [(s.name, s.frame_final_start, s.frame_final_duration, s.channel) for s in seq], "cross", [(c.frame_final_start, c.frame_final_duration) for c in cross], sc.frame_end)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
