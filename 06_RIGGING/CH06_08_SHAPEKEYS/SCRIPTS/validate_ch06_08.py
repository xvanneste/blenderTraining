"""
validate_ch06_08.py — Correcteur « Shape keys et drivers » (CH06.08).
Usage : … --python-exit-code 1 --python validate_ch06_08.py -- --exercise shapekeys [--debug]
Objets : CHR_Arm (tube lié, groupes upper/fore, modificateur Armature) et RIG_Arm (bones upper, fore).
  Configuration : shape keys « Basis » et « elbow_fix » (relatif à Basis, curseur 0–1) ; elbow_fix limité par le groupe de sommets « elbow » ;
                  un DRIVER sur la valeur de elbow_fix qui lit le bone fore ; fore en Rotation Mode XYZ Euler.
  Comportement (fore est tourné autour de Z puis remis) :
    repos : valeur ≤ 0,01 et maillage évalué = maillage sans le shape key (≤ 0,01 mm) ;
    45° : valeur 0,50 ± 0,05 ; 90° : valeur 1,00 ± 0,05 (le driver est linéaire et suit la pose) ;
    coude à 90° : rayon moyen de l'anneau du coude (x = 0,30) à 5,0 cm ± 3 mm de l'axe des bones (sans shape key : 4,1 cm) ;
    sommets loin du coude (x < 0,15 ou x > 0,45) : identiques avec et sans shape key (≤ 1 mm) ; au coude, le shape key déplace au moins un sommet d'au moins 5 mm.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def dist_centerline(p):
    best = 9.0
    for a, b in (((0, 0, 0), (0.3, 0, 0)), ((0.3, 0, 0), (0.3, 0.3, 0))):
        a, b = Vector(a), Vector(b)
        d = b - a
        t = max(0.0, min(1.0, (Vector(p) - a).dot(d) / d.length_squared))
        best = min(best, (Vector(p) - (a + d * t)).length)
    return best


def key_value(tube):
    bpy.context.view_layer.update()
    return float(tube.data.shape_keys.key_blocks["elbow_fix"].value)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.08 — Shape keys et drivers")
    tube, rig = bpy.data.objects.get("CHR_Arm"), bpy.data.objects.get("RIG_Arm")
    if not r.check(tube is not None and rig is not None, "CHR_Arm et RIG_Arm présents", "Partez du fichier de départ.", 2):
        return r.finish()
    r.check(any(m.type == "ARMATURE" and m.object == rig for m in tube.modifiers) and {"upper", "fore"} <= {g.name for g in tube.vertex_groups}, "Bras lié à RIG_Arm (modificateur Armature, groupes upper et fore)", "Ne défaites pas le skinning.", 2)
    sk = tube.data.shape_keys
    kb = sk.key_blocks if sk else None
    ok = kb is not None and "Basis" in kb and "elbow_fix" in kb
    if not r.check(ok, "Shape keys « Basis » et « elbow_fix » présents", "Object Data > Shape Keys > + (Basis puis elbow_fix).", 5):
        return r.finish()
    k = kb["elbow_fix"]
    r.check(k.relative_key.name == "Basis" and k.slider_min == 0.0 and k.slider_max == 1.0, "elbow_fix relatif à Basis, curseur 0–1", "Slider Min 0, Max 1.", 2)
    r.check(k.vertex_group == "elbow" and "elbow" in tube.vertex_groups, "elbow_fix limité par le groupe de sommets « elbow »", "Shape Keys > Vertex Group = elbow.", 4)
    drv = None
    if sk.animation_data:
        drv = next((f for f in sk.animation_data.drivers if "elbow_fix" in f.data_path and f.data_path.endswith(".value")), None)
    r.check(drv is not None, "Un driver pilote la valeur de elbow_fix", "Clic droit sur Value > Add Driver.", 5)
    bones = [t.bone_target for v in drv.driver.variables for t in v.targets] if drv is not None else []
    r.check("fore" in bones, f"Le driver lit le bone fore (lu : {bones})", "Variable Transform Channel : bone fore, Z Rotation.", 4)
    r.check(rig.pose.bones["fore"].rotation_mode == "XYZ", "fore en Rotation Mode XYZ Euler", "Bone > Transform > Rotation Mode.", 2)
    # comportement
    fore = rig.pose.bones["fore"]
    fore.rotation_euler = (0, 0, 0)
    rest = np.array([v.co[:] for v in tube.data.vertices])
    v0 = key_value(tube)
    with_key0 = coords(tube)
    k.mute = True
    no_key0 = coords(tube)
    k.mute = False
    r.check(v0 <= 0.01 and float(np.abs(with_key0 - no_key0).max()) <= 1e-5, f"Repos : valeur {v0:.3f} et maillage identique à celui sans shape key (écart {1000 * float(np.abs(with_key0 - no_key0).max()):.4f} mm)", "Le shape key ne doit rien changer au repos.", 4)
    vals = {}
    for ang in (45, 90):
        fore.rotation_euler = (0, 0, math.radians(ang))
        vals[ang] = key_value(tube)
    r.check(abs(vals[45] - 0.5) <= 0.05, f"Fore à 45° : valeur {vals[45]:.2f} (0,50 ± 0,05)", "Expression a / 1.5708 (90° = 1,5708 rad).", 3)
    r.check(abs(vals[90] - 1.0) <= 0.05, f"Fore à 90° : valeur {vals[90]:.2f} (1,00 ± 0,05)", "", 3)
    # à 90°
    fore.rotation_euler = (0, 0, math.radians(90))
    on = coords(tube)
    ring = [i for i in range(len(rest)) if abs(rest[i][0] - 0.30) < 1e-3]
    m_on = float(np.mean([dist_centerline(on[i]) for i in ring]))
    k.mute = True
    off = coords(tube)
    k.mute = False
    m_off = float(np.mean([dist_centerline(off[i]) for i in ring]))
    r.check(abs(m_on - 0.05) <= 0.003, f"Coude à 90° : rayon moyen {100 * m_on:.2f} cm (5,0 ± 0,3 ; sans shape key {100 * m_off:.2f} cm)", "Gonflez les sommets du coude dans le shape key (≈ +22 %).", 5)
    far = [i for i in range(len(rest)) if rest[i][0] < 0.15 or rest[i][0] > 0.45]
    far_d = float(np.abs(on[far] - off[far]).max())
    near_d = float(np.abs(on[ring] - off[ring]).max())
    r.check(far_d <= 0.001, f"Sommets loin du coude inchangés (écart max {1000 * far_d:.2f} mm ≤ 1)", "Limitez le shape key au groupe « elbow ».", 4)
    r.check(near_d >= 0.005, f"Au coude, le shape key déplace des sommets de {1000 * near_d:.1f} mm (≥ 5)", "Le shape key doit modifier le coude.", 3)
    fore.rotation_euler = (0, 0, 0)
    if debug:
        print("[DEBUG] v0", round(v0, 3), "vals", {a: round(b, 3) for a, b in vals.items()}, "ring on/off", round(m_on, 4), round(m_off, 4), "far", round(far_d, 5), "near", round(near_d, 4))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
