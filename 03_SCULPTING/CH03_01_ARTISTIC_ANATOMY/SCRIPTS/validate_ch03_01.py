"""
validate_ch03_01.py — Correcteur « Les masses du corps et le canon » (CH03.01).
Usage : … --python validate_ch03_01.py --python-exit-code 1 -- --exercise adult|child|gesture [--render]
Mesure les boîtes englobantes (monde) des 16 masses MASS_* :
  adult   : taille 1,6–1,9 m, pieds au sol, canon 6,8–8,2 têtes, repères (menton, entrejambe, genoux,
            coudes, bout des doigts) à ± 4–5 % de la taille, carrure 1,6–2,5 têtes, symétrie G/D,
            membres continus (pas de trou entre segments).
  child   : taille 0,9–1,3 m, canon 4,3–5,7 têtes, symétrie, continuité.
  gesture : bassin et cage thoracique inclinés en sens opposés (≥ 3° chacun, vue de face), épaule du
            côté d'appui plus basse, tête au-dessus du pied d'appui, deux pieds au sol ou sur la pointe.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

PARTS = ["Head", "Ribcage", "Pelvis"] + [f"{p}_{s}" for p in ("UpperArm", "Forearm", "Hand", "Thigh", "Shin", "Foot") for s in "LR"]
CHAINS = [("UpperArm", "Forearm"), ("Forearm", "Hand"), ("Thigh", "Shin"), ("Shin", "Foot")]


def masses():
    dg = bpy.context.evaluated_depsgraph_get()
    out = {}
    for o in bpy.context.scene.objects:
        if o.type != "MESH" or not o.name.upper().startswith("MASS_"):
            continue
        key = next((p for p in PARTS if o.name.upper() == ("MASS_" + p).upper() or o.name.upper().startswith(("MASS_" + p + ".").upper())), None)
        if key is None:
            continue
        ev = o.evaluated_get(dg)
        pts = [ev.matrix_world @ v.co for v in ev.data.vertices]
        if pts:
            out[key] = {"ob": o, "pts": pts,
                        "min": Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))),
                        "max": Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))}
    return out


def gap(a, b):
    """Écart entre les boîtes englobantes de deux masses (0 si elles se recouvrent)."""
    d = [max(0.0, a["min"][i] - b["max"][i], b["min"][i] - a["max"][i]) for i in range(3)]
    return math.sqrt(sum(x * x for x in d))


def tilt(ob):
    """Inclinaison de l'axe X local dans le plan de face (degrés, + = côté +X plus haut)."""
    x = ob.matrix_world.to_3x3() @ Vector((1, 0, 0))
    return math.degrees(math.atan2(x.z, abs(x.x) if abs(x.x) > 1e-6 else 1e-6)) * (1 if x.x >= 0 else -1)


def common(r, m, child):
    zs_max = max(v["max"].z for v in m.values())
    zs_min = min(v["min"].z for v in m.values())
    H = zs_max
    lo, hi = (0.9, 1.3) if child else (1.6, 1.9)
    r.check(lo <= H <= hi, f"Taille {H:.2f} m ({lo}–{hi} m)", "Le sommet du crâne fixe la taille.", 2)
    r.check(abs(zs_min) <= 0.02, f"Pieds au sol (point le plus bas z = {zs_min:.3f})", "z = 0 sous les pieds.", 1)
    head = m["Head"]["max"].z - m["Head"]["min"].z
    canon = H / head
    clo, chi = (4.3, 5.7) if child else (6.8, 8.2)
    r.check(clo <= canon <= chi, f"Canon : {canon:.2f} têtes ({clo}–{chi})", "Hauteur de la tête = taille / canon.", 3)
    sym = []
    for p in ("UpperArm", "Forearm", "Hand", "Thigh", "Shin", "Foot"):
        a, b = m.get(p + "_L"), m.get(p + "_R")
        if a and b:
            d = max(abs(a["min"].x + b["max"].x), abs(a["max"].x + b["min"].x), abs(a["min"].z - b["min"].z), abs(a["max"].z - b["max"].z))
            if d > 0.02:
                sym.append(f"{p} ({d * 100:.1f} cm)")
    holes = []
    for s in "LR":
        for a, b in CHAINS:
            if f"{a}_{s}" in m and f"{b}_{s}" in m and gap(m[f"{a}_{s}"], m[f"{b}_{s}"]) > 0.04:
                holes.append(f"{a}→{b}_{s}")
    return H, head, sym, holes


def main():
    ex = L.opt("--exercise", "adult")
    r = L.Report(f"CH03.01 — Masses et proportions ({ex})")
    m = masses()
    missing = [p for p in PARTS if p not in m]
    if not r.check(not missing, f"16 masses nommées présentes ({16 - len(missing)}/16)",
                   f"Manquantes : {', '.join('MASS_' + p for p in missing[:6])}", 2):
        return r.finish()
    H, head, sym, holes = common(r, m, ex == "child")
    r.check(not holes, "Membres continus (segments qui se touchent)", f"Trous : {holes}", 2)
    if ex in ("adult", "child"):
        r.check(not sym, "Symétrie gauche / droite (≤ 2 cm)", f"Écarts : {sym}", 2)
    if ex == "adult":
        marks = [("Menton", m["Head"]["min"].z, 0.87, 0.04),
                 ("Épaules", max(m["UpperArm_L"]["max"].z, m["UpperArm_R"]["max"].z), 0.82, 0.04), ("Entrejambe", m["Pelvis"]["min"].z, 0.50, 0.04),
                 ("Genoux", min(m["Thigh_L"]["min"].z, m["Thigh_R"]["min"].z), 0.28, 0.04),
                 ("Coudes", min(m["UpperArm_L"]["min"].z, m["UpperArm_R"]["min"].z), 0.62, 0.05),
                 ("Bout des doigts", min(m["Hand_L"]["min"].z, m["Hand_R"]["min"].z), 0.38, 0.05)]
        bad = [f"{n} {z / H:.2f} H (attendu {f:.2f})" for n, z, f, tol in marks if abs(z / H - f) > tol]
        r.check(not bad, "Repères du canon : menton, épaules, entrejambe, genoux, coudes, bout des doigts", " ; ".join(bad), 4)
        width = m["UpperArm_L"]["max"].x - m["UpperArm_R"]["min"].x
        r.check(1.6 <= width / head <= 2.5, f"Carrure {width:.2f} m = {width / head:.2f} têtes (1,6–2,5)", "Épaules ≈ 2 têtes chez l'adulte.", 2)
    if ex == "gesture":
        tp, tc = tilt(m["Pelvis"]["ob"]), tilt(m["Ribcage"]["ob"])
        r.check(abs(tp) >= 3 and abs(tc) >= 3 and tp * tc < 0,
                f"Bassin {tp:+.1f}° et cage {tc:+.1f}° inclinés en sens opposés (≥ 3° chacun)",
                "Contrapposto : tournez bassin et cage (R Y) en sens contraires, vue de face.", 3)
        feet = {s: (m[f"Foot_{s}"]["min"] + m[f"Foot_{s}"]["max"]) / 2 for s in "LR"}
        hx = (m["Head"]["min"].x + m["Head"]["max"].x) / 2
        sup = min(feet, key=lambda s: abs(feet[s].x - hx))
        r.check(abs(feet[sup].x - hx) <= 0.06, f"Tête au-dessus du pied d'appui ({sup}, écart {abs(feet[sup].x - hx) * 100:.1f} cm)",
                "La tête se place à l'aplomb du pied qui porte le poids.", 3)
        shoulder = {s: m[f"UpperArm_{s}"]["max"].z for s in "LR"}
        other = "L" if sup == "R" else "R"
        r.check(shoulder[sup] < shoulder[other] - 0.01, f"Épaule du côté d'appui plus basse ({shoulder[sup]:.3f} < {shoulder[other]:.3f})",
                "Côté d'appui : hanche haute, épaule basse.", 2)
        r.check(all(m[f"Foot_{s}"]["min"].z <= 0.03 for s in "LR"), "Les deux pieds touchent le sol (pointe pour la jambe libre)", "", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
