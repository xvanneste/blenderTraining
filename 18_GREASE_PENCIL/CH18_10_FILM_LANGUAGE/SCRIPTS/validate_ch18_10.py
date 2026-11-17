"""
validate_ch18_10.py — Correcteur CH18.10 (valeurs de plans).
Usage :
  … ch18_10_shots_<prenom>.blend --python-exit-code 1 --python validate_ch18_10.py -- --exercise shots
  … ch18_10_board_<prenom>.blend --python-exit-code 1 --python validate_ch18_10.py -- --exercise board
« shots » : chaque caméra est classée par bcma_shots.classify (hauteur du corps au bord bas de l'image).
« board » : quantité de dessin par le correcteur générique (gp_spec.json).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp_check as C  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

EXPECT = [("CAM_01_PE", "PE"), ("CAM_02_PM", "PM"), ("CAM_03_PA", "PA"), ("CAM_04_PRT", "PRT"),
          ("CAM_05_PRP", "PRP"), ("CAM_06_GP", "GP"), ("CAM_07_TGP", "TGP")]


def in_frame(sc, cam, p, margin=0.0):
    v = world_to_camera_view(sc, cam, Vector(p))
    return v.z > 0 and margin <= v.x <= 1 - margin and margin <= v.y <= 1 - margin


def forward(cam):
    return (cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))).normalized()


def shots():
    r = L.Report("CH18.10 — Les valeurs de plans (caméras)")
    sc = bpy.context.scene
    a, b = L.obj("CHR_A"), L.obj("CHR_B")
    if not r.check(a is not None and b is not None, "CHR_A et CHR_B présents", "Ne déplacez pas les personnages.", 1):
        return r.finish()
    base = tuple(a.location)
    for name, code in EXPECT:
        cam = L.obj(name)
        if not r.check(cam is not None and cam.type == "CAMERA", f"{name} présente", "Add > Camera, F2.", 1):
            continue
        got, info = S.classify(sc, cam, base)
        centered = 0.15 <= info["x_yeux"] <= 0.85
        cut = info.get("coupe")
        detail = f"coupe à {cut:.2f} m" if cut is not None else f"personnage entier ({100 * info.get('fraction', 0):.0f} % de la hauteur)"
        r.check(got == code and centered, f"{name} : {S.SHOTS[code][0]} — mesuré {got or '?'} ({detail})",
                f"Attendu : {S.SHOTS[code][1]} ; A au centre horizontalement.", 2)
    cup = L.obj("PROP_Cup")
    cam = L.obj("CAM_08_INS")
    if r.check(cam is not None and cup is not None, "CAM_08_INS présente", "", 1):
        corners = [cup.matrix_world @ Vector(c) for c in cup.bound_box]
        vs = [world_to_camera_view(sc, cam, p) for p in corners]
        hy = max(v.y for v in vs) - min(v.y for v in vs)
        hx = max(v.x for v in vs) - min(v.x for v in vs)
        c = world_to_camera_view(sc, cam, cup.matrix_world.translation)
        ok = c.z > 0 and 0.2 <= c.x <= 0.8 and 0.2 <= c.y <= 0.8 and max(hx, hy) >= 0.3
        r.check(ok, f"CAM_08_INS : la tasse occupe {100 * max(hx, hy):.0f} % du cadre (≥ 30 %, centrée)",
                "Rapprochez la caméra de PROP_Cup, objet au centre.", 2)
    eyes_a = (base[0], base[1], 1.62)
    cam = L.obj("CAM_09_PLONGEE")
    if r.check(cam is not None, "CAM_09_PLONGEE présente", "", 1):
        r.check(cam.matrix_world.translation.z > 2.1 and forward(cam).z < -0.2 and in_frame(sc, cam, eyes_a),
                "Plongée : caméra au-dessus des yeux, regard vers le bas, A cadré", "Montez la caméra, inclinez-la vers le bas.", 2)
    cam = L.obj("CAM_10_CONTREPLONGEE")
    if r.check(cam is not None, "CAM_10_CONTREPLONGEE présente", "", 1):
        r.check(cam.matrix_world.translation.z < 1.0 and forward(cam).z > 0.15 and in_frame(sc, cam, eyes_a),
                "Contre-plongée : caméra basse, regard vers le haut, A cadré", "Descendez la caméra (< 1 m), inclinez-la vers le haut.", 2)
    c1, c2 = L.obj("CAM_11_CHAMP"), L.obj("CAM_12_CONTRECHAMP")
    if r.check(c1 is not None and c2 is not None, "CAM_11_CHAMP et CAM_12_CONTRECHAMP présentes", "", 1):
        eyes_b = (b.location.x, b.location.y, 1.62)
        r.check(in_frame(sc, c1, eyes_b) and in_frame(sc, c2, eyes_a), "Champ cadre B, contrechamp cadre A",
                "CAM_11 regarde B, CAM_12 regarde A.", 2)
        ax = b.location - a.location
        side = lambda p: ax.x * (p.y - a.location.y) - ax.y * (p.x - a.location.x)
        s1, s2 = side(c1.matrix_world.translation), side(c2.matrix_world.translation)
        r.check(s1 * s2 > 0 and min(abs(s1), abs(s2)) > 0.2, "Règle des 180° : les deux caméras du même côté de l'axe A–B",
                "Placez les deux caméras du même côté de la ligne qui relie les personnages.", 3)
    return r.finish()


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ex = argv[argv.index("--exercise") + 1] if "--exercise" in argv else "shots"
    if ex == "board":
        return C.main(__file__)
    return shots()


if __name__ == "__main__":
    L.run(main)
