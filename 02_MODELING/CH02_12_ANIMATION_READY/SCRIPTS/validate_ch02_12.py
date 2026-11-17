"""
validate_ch02_12.py — Correcteur « Le coude qui plie bien » (CH02.12).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_12.py -- --exercise arm [--render]
Le correcteur plie lui-même le bras à 90° au coude (déformation linéaire pondérée, comme une
armature avec des poids lissés sur ±3 cm) et mesure le volume conservé : la topologie seule est jugée.
Mesures de référence : 4 segments réguliers → 0,875 ; 4 boucles serrées au coude → 0,975.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Matrix  # noqa: E402

ELBOW = 0.30


def bent_volume_ratio(me, ang=90.0, width=0.06):
    bm = bmesh.new()
    bm.from_mesh(me)
    v0 = bm.calc_volume()
    rot = Matrix.Translation((0, 0, ELBOW)) @ Matrix.Rotation(math.radians(ang), 4, "X") @ Matrix.Translation((0, 0, -ELBOW))
    for v in bm.verts:
        t = min(1.0, max(0.0, (v.co.z - (ELBOW - width / 2)) / width))
        w = t * t * (3 - 2 * t)
        v.co = v.co * (1 - w) + (rot @ v.co) * w
    r = bm.calc_volume() / v0 if v0 else 0
    bm.free()
    return r


def main():
    r = L.Report("CH02.12 — Le coude qui plie bien")
    ob = L.obj("GEO_Arm")
    if not r.check(ob is not None and ob.type == "MESH", "GEO_Arm présent", "Ne renommez pas le bras.", 1):
        return r.finish()
    me = ob.data
    r.check(all(abs(s - 1) < 1e-4 for s in ob.scale), "Échelle d'objet à 1", "Ctrl+A > Scale.", 1)
    zs = [v.co.z for v in me.vertices]
    h = max(zs) - min(zs)
    r.check(0.55 <= h <= 0.65, f"Dimensions réelles : bras de {h * 100:.0f} cm (55–65)", "Ne mettez pas le bras à l'échelle.", 1)
    levels = sorted({round(z, 3) for z in zs})
    near = [z for z in levels if 0.22 <= z <= 0.38]
    r.check(len(near) >= 4, f"{len(near)} boucle(s) dans la zone du coude (z 0,22–0,38 ; ≥ 4 avec celle du coude)",
            "Ctrl+R autour du coude : au moins 3 boucles en plus.", 3)
    side = [p for p in me.polygons if abs(p.normal.z) < 0.5]
    q = sum(1 for p in side if len(p.vertices) == 4) / max(1, len(side))
    r.check(q >= 0.95, f"Flancs en quads ({100 * q:.0f} %)", "Loop Cut garde des quads ; évitez Knife/Fill.", 1)
    vr = bent_volume_ratio(me)
    r.check(vr >= 0.95, f"Volume conservé au pli de 90° : {100 * vr:.1f} % (≥ 95 % ; départ 87,5 %)",
            "Boucles plus nombreuses et plus serrées autour du coude.", 4)
    r.check(any(m.type == "ARMATURE" and m.object is not None for m in ob.modifiers), "Modificateur Armature conservé",
            "Ne supprimez pas le modificateur Armature.", 1, mandatory=False)
    groups = {g.name for g in ob.vertex_groups}
    r.check({"UpperArm", "Forearm"} <= groups, "Groupes de sommets UpperArm et Forearm conservés", "Ne supprimez pas les groupes.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
