"""
validate_ch18_11.py — Correcteur CH18.11 (dialogue découpé).
Usage : … --python-exit-code 1 --python validate_ch18_11.py -- --exercise dialogue | board
« dialogue » : marqueurs liés aux caméras, règle des 180°, A à gauche / B à droite dans chaque plan,
variété (master + plans sur A seul + plans sur B seul + insert), durées ≥ 24 images.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp_check as C  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402


def eye_pos(sc, cam, ob):
    v = world_to_camera_view(sc, cam, Vector((ob.location.x, ob.location.y, 1.62)))
    return v if (v.z > 0 and 0 <= v.x <= 1 and 0 <= v.y <= 1) else None


def dialogue():
    r = L.Report("CH18.11 — Le dialogue découpé")
    sc = bpy.context.scene
    a, b, cup = L.obj("CHR_A"), L.obj("CHR_B"), L.obj("PROP_Cup")
    if not r.check(a and b and cup, "Personnages et tasse présents", "Ne supprimez rien du plateau.", 1):
        return r.finish()
    ms = sorted([m for m in sc.timeline_markers if m.name.upper().startswith("SH")], key=lambda m: m.frame)
    r.check(len(ms) >= 6, f"{len(ms)} marqueur(s) SH… (≥ 6)", "Timeline : M, puis F2 pour nommer SH010…", 2)
    bound = [m for m in ms if m.camera is not None]
    r.check(ms and len(bound) == len(ms), f"Marqueurs liés à une caméra ({len(bound)}/{len(ms)})",
            "Sélectionnez la caméra puis le marqueur : Marker > Bind Camera to Markers (Ctrl+B).", 2)
    gaps = [m2.frame - m1.frame for m1, m2 in zip(ms, ms[1:])]
    r.check(gaps and min(gaps) >= 24, f"Plans d'au moins 24 images (plus court : {min(gaps) if gaps else 0})",
            "Espacez les marqueurs d'au moins 1 s.", 1)
    r.check(ms and sc.frame_end >= ms[-1].frame + 24, "Le dernier plan dure au moins 24 images", "Scene > Frame End.", 1)
    ax = b.location - a.location
    side = lambda p: ax.x * (p.y - a.location.y) - ax.y * (p.x - a.location.x)
    sides = [side(m.camera.matrix_world.translation) for m in bound]
    r.check(sides and (all(s > 0.2 for s in sides) or all(s < -0.2 for s in sides)),
            "Règle des 180° : toutes les caméras du même côté de l'axe A–B", "Ramenez la caméra fautive de l'autre côté.", 3)
    kinds, bad = set(), []
    for m in bound:
        cam = m.camera
        pa, pb = eye_pos(sc, cam, a), eye_pos(sc, cam, b)
        c = world_to_camera_view(sc, cam, cup.matrix_world.translation)
        if pa and pb:
            kinds.add("master")
            if not pa.x < pb.x:
                bad.append(m.name)
        elif pa:
            kinds.add("A")
            if pa.x > 0.55:
                bad.append(m.name)
        elif pb:
            kinds.add("B")
            if pb.x < 0.45:
                bad.append(m.name)
        elif c.z > 0 and 0.2 <= c.x <= 0.8 and 0.2 <= c.y <= 0.8:
            kinds.add("insert")
    r.check(not bad, "Continuité : A toujours à gauche, B toujours à droite" + (f" (fautif : {', '.join(bad)})" if bad else ""),
            "Décalez la visée : A dans la moitié gauche, B dans la moitié droite.", 3)
    r.check({"master", "A", "B"} <= kinds, f"Variété : master + plans sur A + plans sur B ({', '.join(sorted(kinds))})",
            "Il faut au moins un plan large, un plan sur A seul et un plan sur B seul.", 2)
    r.check("insert" in kinds, "Un insert (tasse au centre du cadre)", "Une caméra très proche de PROP_Cup.", 1, mandatory=False)
    return r.finish()


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ex = argv[argv.index("--exercise") + 1] if "--exercise" in argv else "dialogue"
    return C.main(__file__) if ex == "board" else dialogue()


if __name__ == "__main__":
    L.run(main)
