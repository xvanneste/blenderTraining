"""
validate_ch07_13.py — Correcteur « Animation non linéaire » (CH07.13).
Usage : … --python-exit-code 1 --python validate_ch07_13.py -- --exercise nla [--debug]
Objet : GEO_Crate (actions « Slide » : X de 0 à 4 sur les images 1–25 ; « Spin » : rotation Z de 0° à 180° sur 1–25, interpolation linéaire).
  Configuration : aucune action ACTIVE (animation_data.action est vide : tout vient du NLA) ;
                  deux pistes NLA nommées « Move » puis « Spin » (de bas en haut) ;
                  « Move » : un strip de l'action Slide, début à l'image 1, répété 2 fois (repeat 2) : fin à l'image 49 ;
                  « Spin » : un strip de l'action Spin, de l'image 13 à l'image 37, fondu d'entrée (Blend In) de 6 images ; plage de la scène 1–49 à 24 i/s.
  Évalué : X(13) = 2,00 ; X(30) = 0,83 ; X(37) = 2,00 (± 0,05 : le strip répété repart de 0 à l'image 25) ; rotation Z : 0° à l'image 13 (± 1°), 90° à l'image 25 (± 2°), 180° à l'image 37 (± 2°) ;
           fondu : à l'image 16 la rotation vaut 11,25° (± 3°) (influence 0,5 pendant le fondu d'entrée).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.13 — Animation non linéaire (NLA)")
    ob = bpy.data.objects.get("GEO_Crate")
    if not r.check(ob is not None and ob.animation_data is not None, "GEO_Crate animée présente", "Partez du fichier de départ.", 2):
        return r.finish()
    ad = ob.animation_data
    sc = bpy.context.scene
    r.check(ad.action is None, f"Aucune action active (valeur : {ad.action.name if ad.action else None})", "Poussez l'action dans le NLA (Push Down) : une action active passe PAR-DESSUS les pistes.", 4)
    names = [t.name for t in ad.nla_tracks]
    r.check(names == ["Move", "Spin"], f"Pistes NLA : {names} (attendu : Move puis Spin)", "Deux pistes, nommées Move (en bas) et Spin (au-dessus).", 4)
    tr = {t.name: t for t in ad.nla_tracks}
    mv = list(tr["Move"].strips) if "Move" in tr else []
    ok = len(mv) == 1 and mv[0].action is not None and mv[0].action.name == "Slide" and abs(mv[0].frame_start - 1) <= 0.01 and abs(mv[0].frame_end - 49) <= 0.01 and mv[0].repeat == 2
    r.check(ok, f"Piste Move : {[(s.action.name if s.action else None, s.frame_start, s.frame_end, s.repeat) for s in mv]} (un strip Slide, images 1 à 49, repeat 2)", "Strip Slide à l'image 1, Repeat = 2.", 6)
    sp = list(tr["Spin"].strips) if "Spin" in tr else []
    ok2 = len(sp) == 1 and sp[0].action is not None and sp[0].action.name == "Spin" and abs(sp[0].frame_start - 13) <= 0.01 and abs(sp[0].frame_end - 37) <= 0.01 and abs(sp[0].blend_in - 6) <= 0.01
    r.check(ok2, f"Piste Spin : {[(s.action.name if s.action else None, s.frame_start, s.frame_end, s.blend_in) for s in sp]} (un strip Spin, images 13 à 37, Blend In 6)", "Strip Spin à l'image 13, Blend In = 6, échelle 1.", 6)
    r.check(sc.frame_start == 1 and sc.frame_end == 49 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–49 à 24)", "End = 49.", 2)

    def val(f):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        return ob.location.x, math.degrees(ob.rotation_euler.z)
    xs = {f: val(f)[0] for f in (13, 30, 37)}
    rs = {f: val(f)[1] for f in (13, 16, 25, 37)}
    sc.frame_set(1)
    r.check(abs(xs[13] - 2) <= 0.05 and abs(xs[30] - 0.833) <= 0.05 and abs(xs[37] - 2) <= 0.05, f"Position évaluée : X(13) = {xs[13]:.2f}, X(30) = {xs[30]:.2f}, X(37) = {xs[37]:.2f} (2,00 ; 0,83 ; 2,00)", "Le strip répété repart de 0 à l'image 25.", 6)
    r.check(abs(rs[13]) <= 1 and abs(rs[25] - 90) <= 2 and abs(rs[37] - 180) <= 2, f"Rotation évaluée : {rs[13]:.1f}° (image 13), {rs[25]:.1f}° (25), {rs[37]:.1f}° (37) = 0°, 90°, 180°", "Strip Spin de 13 à 37, échelle 1.", 5)
    r.check(abs(rs[16] - 11.25) <= 3, f"Fondu d'entrée : rotation à l'image 16 = {rs[16]:.1f}° (11,25 ± 3 avec Blend In 6)", "Blend In du strip Spin = 6 images.", 4)
    if debug:
        print("[DEBUG] tracks", names, "x", {k: round(v, 3) for k, v in xs.items()}, "rot", {k: round(v, 2) for k, v in rs.items()})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
