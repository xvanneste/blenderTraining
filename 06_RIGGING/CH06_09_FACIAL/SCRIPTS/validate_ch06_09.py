"""
validate_ch06_09.py — Correcteur « Rig facial » (CH06.09).
Usage : … --python-exit-code 1 --python validate_ch06_09.py -- --exercise facial [--debug]
Objets : GEO_Face (tête, groupes head/jaw, modificateur Armature) et RIG_Face (head, jaw, ctl_smile, ctl_blink).
  Configuration : shape keys Basis, smile, blink (relatifs à Basis, curseur 0–1), chacun limité par un groupe de sommets (smile_zone, blink_zone) ;
                  deux drivers (valeur ← Location X de la glissière) ; Limit Location sur chaque glissière ; jaw avec des poids (≥ 50 sommets pesés).
  Comportement (les commandes sont DÉPLACÉES puis remises ; mesures sur les sommets évalués) :
    Mâchoire (rotation X de −15°) : le menton (sommet le plus bas et le plus en avant) descend d'au moins 2 cm ; le haut du crâne (z > 0,06 m) reste (≤ 1 mm) ;
        poids lisses : aucune arête ne s'étire de plus de 1,8 fois sa longueur de repos (une coupure binaire donne 2,9) ;
    Sourire : glissière à 0,025 m → valeur 0,50 ± 0,05 ; à 0,05 m → 1,00 ± 0,05 ; les coins de la bouche montent de 10 à 14 mm ; les paupières restent (≤ 1 mm) ;
    Clignement : glissière à 0,05 m → valeur 1,00 ± 0,05 ; les paupières descendent de 10 à 14 mm ; la bouche reste (≤ 1 mm) ;
    Limite : glissière demandée à 0,20 m → valeur ≤ 1,05 et position effective ≤ 0,05 m.
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

CORNER = ((0.045, -0.1056, -0.04), (-0.045, -0.1056, -0.04))
EYE = ((0.04, -0.1086, 0.03), (-0.04, -0.1086, 0.03))


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def near(rest, centers, r):
    return np.array([min(np.linalg.norm(p - np.array(c)) for c in centers) < r for p in rest])


def kv(face, name):
    bpy.context.view_layer.update()
    return float(face.data.shape_keys.key_blocks[name].value)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.09 — Rig facial (mâchoire, sourire, clignement)")
    face, rig = bpy.data.objects.get("GEO_Face"), bpy.data.objects.get("RIG_Face")
    if not r.check(face is not None and rig is not None, "GEO_Face et RIG_Face présents", "Partez du fichier de départ.", 2):
        return r.finish()
    n = len(face.data.vertices)
    jaw_w = sum(1 for v in face.data.vertices for g in v.groups if face.vertex_groups[g.group].name == "jaw" and g.weight > 0.01)
    r.check(any(m.type == "ARMATURE" and m.object == rig for m in face.modifiers) and jaw_w >= 50, f"Tête liée à RIG_Face ; {jaw_w} sommets pesés sur jaw (≥ 50)", "Groupes head et jaw avec des poids lisses.", 4)
    sk = face.data.shape_keys
    kb = sk.key_blocks if sk else None
    ok = kb is not None and all(k in kb for k in ("Basis", "smile", "blink"))
    r.check(ok, "Shape keys Basis, smile et blink présents", "Object Data > Shape Keys.", 5)
    if ok:
        r.check(all(kb[k].relative_key.name == "Basis" and kb[k].slider_min == 0.0 and kb[k].slider_max == 1.0 for k in ("smile", "blink")), "smile et blink relatifs à Basis, curseur 0–1", "", 2)
        r.check(kb["smile"].vertex_group == "smile_zone" and kb["blink"].vertex_group == "blink_zone", "Chaque shape key est limité à sa zone (smile_zone, blink_zone)", "Shape Keys > Vertex Group.", 4)
    drv = {}
    if sk and sk.animation_data:
        for f in sk.animation_data.drivers:
            for k in ("smile", "blink"):
                if f'"{k}"' in f.data_path and f.data_path.endswith(".value"):
                    drv[k] = [t.bone_target for v in f.driver.variables for t in v.targets]
    r.check(drv.get("smile") == ["ctl_smile"] and drv.get("blink") == ["ctl_blink"], f"Drivers : smile ← ctl_smile, blink ← ctl_blink (lu : {drv})", "Variable Transform Channel : Location X, Local Space.", 5)
    pb = rig.pose.bones
    lims = {c: [x for x in pb[c].constraints if x.type == "LIMIT_LOCATION"] for c in ("ctl_smile", "ctl_blink")}
    r.check(all(lims[c] and lims[c][0].use_max_x and abs(lims[c][0].max_x - 0.05) <= 1e-4 for c in lims), "Limit Location sur chaque glissière (X max 0,05 m)", "Bone Constraints > Limit Location.", 3)
    if not ok:
        return r.finish()
    rest = np.array([v.co[:] for v in face.data.vertices])
    base = coords(face)
    mouth = near(rest, CORNER, 0.035)
    eyes = near(rest, EYE, 0.035)
    # mâchoire
    pb["jaw"].rotation_euler = (math.radians(-15), 0, 0)
    co = coords(face)
    pb["jaw"].rotation_euler = (0, 0, 0)
    chin = int(np.argmin(rest[:, 2] + rest[:, 1] + 0.001 * np.abs(rest[:, 0])))
    drop = float(base[chin][2] - co[chin][2])
    top = rest[:, 2] > 0.06
    top_d = float(np.abs(co[top] - base[top]).max())
    st = 0.0
    for e in face.data.edges:
        a, b = e.vertices
        st = max(st, float(np.linalg.norm(co[a] - co[b]) / np.linalg.norm(rest[a] - rest[b])))
    r.check(drop >= 0.02 and top_d <= 0.001, f"Mâchoire −15° : le menton descend de {100 * drop:.1f} cm (≥ 2) ; haut du crâne {1000 * top_d:.2f} mm (≤ 1)", "Poids de jaw sur le bas de la tête, 0 sur le haut.", 5)
    r.check(st <= 1.8, f"Poids de la mâchoire lisses : étirement d'arête max {st:.2f} fois (≤ 1,8)", "Dégradé de poids entre head et jaw, pas de coupure nette.", 4)

    def move(name, x):
        pb[name].location = Vector((x, 0, 0))
        co = coords(face)
        v = kv(face, "smile" if name == "ctl_smile" else "blink")
        ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
        eff = abs(float(ev.pose.bones[name].head.x)) - abs(float(rig.data.bones[name].head_local.x))     # déplacement EFFECTIF de la glissière (après contraintes)
        eff = eff if name == "ctl_smile" else -eff if rig.data.bones[name].head_local.x < 0 else eff
        effs[(name, x)] = eff
        return co, v

    out = {}
    effs = {}
    for name in ("ctl_smile", "ctl_blink"):
        for x in (0.025, 0.05, 0.20):
            co, v = move(name, x)
            out[(name, x)] = (co, v)
        pb[name].location = (0, 0, 0)
    co, v_half = out[("ctl_smile", 0.025)]
    co1, v_full = out[("ctl_smile", 0.05)]
    r.check(abs(v_half - 0.5) <= 0.05 and abs(v_full - 1.0) <= 0.05, f"Sourire : valeur {v_half:.2f} à 0,025 m et {v_full:.2f} à 0,05 m (0,50 et 1,00 ± 0,05)", "Expression x / 0.05.", 4)
    up = float((co1[mouth][:, 2] - base[mouth][:, 2]).max())
    eyes_d = float(np.abs(co1[eyes] - base[eyes]).max())
    r.check(0.010 <= up <= 0.014, f"Sourire à fond : les coins montent de {1000 * up:.1f} mm (10–14)", "Le shape key smile doit lever les coins de la bouche.", 4)
    r.check(eyes_d <= 0.001, f"Sourire : les paupières ne bougent pas ({1000 * eyes_d:.2f} mm ≤ 1)", "smile ne doit contenir que la zone de la bouche.", 4)
    cob, vb = out[("ctl_blink", 0.05)]
    dn = float((base[eyes][:, 2] - cob[eyes][:, 2]).max())
    mouth_d = float(np.abs(cob[mouth] - base[mouth]).max())
    r.check(abs(vb - 1.0) <= 0.05 and 0.010 <= dn <= 0.014, f"Clignement à fond : valeur {vb:.2f}, paupières −{1000 * dn:.1f} mm (10–14)", "Le shape key blink doit abaisser les paupières.", 4)
    r.check(mouth_d <= 0.001, f"Clignement : la bouche ne bouge pas ({1000 * mouth_d:.2f} mm ≤ 1)", "blink ne doit contenir que la zone des yeux.", 3)
    far = out[("ctl_smile", 0.20)]
    farb = out[("ctl_blink", 0.20)]
    e1, e2 = effs[("ctl_smile", 0.20)], effs[("ctl_blink", 0.20)]
    r.check(far[1] <= 1.05 and farb[1] <= 1.05 and max(abs(e1), abs(e2)) <= 0.0501, f"Glissière demandée à 0,20 m : valeurs {far[1]:.2f} et {farb[1]:.2f} (≤ 1,05) ; déplacement effectif {1000 * abs(e1):.0f} et {1000 * abs(e2):.0f} mm (≤ 50)", "Limit Location : X de 0 à 0,05 m.", 4)
    if debug:
        print("[DEBUG] drop", round(drop, 3), "top", round(top_d, 5), "stretch", round(st, 2), "half/full", round(v_half, 2), round(v_full, 2), "up", round(up, 4), "eyes_d", round(eyes_d, 5), "blink", round(vb, 2), round(dn, 4), "mouth_d", round(mouth_d, 5), "far", round(far[1], 2), round(farb[1], 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
