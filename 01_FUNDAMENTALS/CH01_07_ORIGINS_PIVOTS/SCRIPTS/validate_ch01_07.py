"""
validate_ch01_07.py — Correcteur « la porte et la roue » (CH01.07).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch01_07.py --python-exit-code 1 -- --exercise door
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
from mathutils import Vector  # noqa: E402

WHEEL = Vector((2, 0))


def main():
    r = L.Report("CH01.07 — La porte et la roue")
    door = L.obj("GEO_Door")
    if not r.check(door is not None, "GEO_Door présente", "", 1):
        return r.finish()
    o = door.matrix_world.translation
    r.check((o - Vector((-0.45, 0, 0))).length < 0.025, f"Origine sur la charnière ({o.x:.2f}, {o.y:.2f}, {o.z:.2f})",
            "Shift+S > Cursor to Selected sur l'arête bas-gauche (2 sommets), puis Object > Set Origin > Origin to 3D Cursor.", 4)
    ang = math.degrees(door.matrix_world.to_euler().z)
    r.check(abs(abs(ang) - 90) < 1, f"Porte ouverte à 90° (rotation Z = {ang:.0f}°)", "R Z 90 Entrée.", 2)
    pts = [door.matrix_world @ v.co for v in door.data.vertices]
    near = min((Vector((p.x, p.y)) - Vector((-0.45, 0))).length for p in pts)
    far = max((Vector((p.x, p.y)) - Vector((-0.45, 0))).length for p in pts)
    r.check(near < 0.03 and 0.85 < far < 0.95, "La porte pivote sur sa charnière (elle reste attachée au cadre)",
            "Si la porte « flotte », l'origine n'était pas sur la charnière au moment de la rotation.", 3)
    r.check(min(p.z for p in pts) > -0.01 and max(p.z for p in pts) < 2.01, "Porte toujours au sol, hauteur intacte", "", 1)
    ok = True
    for i, start in enumerate((0, 120, 200)):
        b = L.obj(f"GEO_Bolt_{i + 1}")
        if b is None:
            ok = False
            continue
        p = Vector((b.location.x, b.location.y)) - WHEEL
        a = math.degrees(math.atan2(p.y, p.x)) % 360
        ok &= abs(p.length - 0.3) < 0.01 and min(abs(a - (start + 45) % 360), 360 - abs(a - (start + 45) % 360)) < 1
    r.check(ok, "Boulons tournés de 45° autour du centre de la roue",
            "Curseur au centre de la roue, Pivot Point = 3D Cursor, puis R Z 45.", 4)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
