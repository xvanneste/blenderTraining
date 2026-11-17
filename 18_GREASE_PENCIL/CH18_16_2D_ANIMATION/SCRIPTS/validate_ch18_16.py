"""
validate_ch18_16.py — Correcteur « La balle rebondissante 2D » (CH18.16).
Usage : … --python-exit-code 1 --python validate_ch18_16.py -- --exercise keys|bounce [--render]
Mesure, pour chaque image clé du calque USER_Ball : centre, largeur, hauteur de la balle (boîte
englobante des traits). En déduit contacts (bas de la balle au sol, minimum local), sommets
(maximum entre deux contacts), amortissement, progression horizontale, et pour « bounce » :
fréquence des dessins, ralenti aux sommets (espacement), étirement/écrasement, volume, types de clés.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

KEY_TYPES = {"KEYFRAME", "EXTREME"}


def measure(lay):
    rows = []
    for fr in sorted(lay.frames, key=lambda f: f.frame_number):
        xs, zs = [], []
        for s in fr.drawing.strokes:
            for p in s.points:
                xs.append(p.position.x)
                zs.append(p.position.z)
        if len(xs) < 8:
            continue
        rows.append({"f": fr.frame_number, "x": (min(xs) + max(xs)) / 2, "z": (min(zs) + max(zs)) / 2,
                     "bottom": min(zs), "w": max(xs) - min(xs), "h": max(zs) - min(zs), "type": fr.keyframe_type})
    return rows


def analyse(rows, ground, tol=0.1):
    contacts = []
    for i, r in enumerate(rows):
        if r["bottom"] > ground + tol:
            continue
        prev_z = rows[i - 1]["z"] if i > 0 else 1e9
        next_z = rows[i + 1]["z"] if i + 1 < len(rows) else 1e9
        if r["z"] <= prev_z and r["z"] <= next_z:
            contacts.append(i)
    apexes = []
    bounds = [0] + contacts
    for a, b in zip(bounds, bounds[1:]):
        seg = rows[a:b + 1]
        if len(seg) >= 2:
            j = max(range(len(seg)), key=lambda k: seg[k]["z"])
            if a + j not in contacts:
                apexes.append(a + j)
    return contacts, apexes


def main():
    ex = L.opt("--exercise", "bounce")
    sc = bpy.context.scene
    r = L.Report(f"CH18.16 — Balle rebondissante 2D ({ex})")
    ground, rad = float(sc.get("bcma_ground", -2.6)), float(sc.get("bcma_ball_r", 0.35))
    ob = bpy.data.objects.get("GP_Practice")
    lay = next((l for l in ob.data.layers if l.name == "USER_Ball"), None) if ob and ob.type == "GREASEPENCIL" else None
    if not r.check(lay is not None, "Calque USER_Ball présent", "Repartez du starter.", 1):
        return r.finish()
    rows = measure(lay)
    if not r.check(len(rows) >= 7, f"{len(rows)} dessin(s) de balle (≥ 7)", "Une image clé par pose.", 2):
        return r.finish()
    contacts, apexes = analyse(rows, ground)
    r.check(len(contacts) >= 3, f"{len(contacts)} contact(s) au sol (≥ 3)",
            "Au contact, le bas de la balle touche la ligne de sol (± 0,1 m).", 3)
    hs = [rows[i]["z"] - ground - rad for i in apexes]
    dec = len(hs) >= 3 and all(b < 0.9 * a for a, b in zip(hs, hs[1:]))
    r.check(dec, "Rebonds amortis : sommets de plus en plus bas (" + " → ".join(f"{h:.2f}" for h in hs) + " m)",
            "Chaque sommet ≈ 60 % du précédent.", 3)
    xs = [x["x"] for x in rows]
    mono = all(b >= a - 0.02 for a, b in zip(xs, xs[1:]))
    r.check(mono and xs[-1] - xs[0] >= 6, f"Progression vers la droite ({xs[-1] - xs[0]:.1f} m, régulière)",
            "La balle avance sans revenir en arrière (≥ 6 m).", 2)
    poses = set(contacts) | set(apexes)
    good_types = sum(1 for i in poses if rows[i]["type"] in KEY_TYPES)
    if ex == "keys":
        r.check(len(rows) <= 14, f"Poses clés seulement ({len(rows)} dessins ≤ 14)", "Les intervalles viennent à l'étape 2.", 1)
        r.check(good_types == len(poses), f"Contacts et sommets en type Keyframe/Extreme ({good_types}/{len(poses)})",
                "Dope Sheet : sélection, R > Keyframe ou Extreme.", 2)
        sq = sum(1 for i in contacts if rows[i]["w"] / rows[i]["h"] >= 1.15)
        r.check(sq >= 2, f"Écrasement visible à {sq} contact(s) (largeur/hauteur ≥ 1,15)", "Balle aplatie au sol.", 2)
    else:
        frames = [x["f"] for x in rows]
        last_c = rows[contacts[-1]]["f"] if contacts else frames[-1]
        gaps = [b - a for a, b in zip(frames, frames[1:]) if b <= last_c]
        mean_gap = sum(gaps) / len(gaps) if gaps else 99
        r.check(len(rows) >= 20 and mean_gap <= 2.5 and max(gaps or [99]) <= 4,
                f"Animation complète : {len(rows)} dessins, écart moyen {mean_gap:.2f} image(s), max {max(gaps or [0])}",
                "Un dessin toutes les 1 à 2 images (« en un » ou « en deux »).", 3)
        # ralenti aux sommets : vitesse verticale (m/image) dans le tiers haut vs le tiers bas de chaque arc
        top, low = [], []
        for a, b in zip(rows, rows[1:]):
            if b["f"] > last_c:
                break
            v = abs(b["z"] - a["z"]) / (b["f"] - a["f"])
            hmid = (a["z"] + b["z"]) / 2 - ground - rad
            hmax = max(hs) if hs else 1
            (top if hmid > 0.66 * min(hmax, max(a["z"], b["z"]) - ground - rad + 1e-6) else low).append(v)
        ratio = (sum(top) / len(top)) / (sum(low) / len(low)) if top and low else 1
        r.check(ratio < 0.6, f"Ralenti aux sommets : vitesse haut / bas = {ratio:.2f} (< 0,6)",
                "Rapprochez les intervalles près des sommets, écartez-les près du sol.", 3)
        sq = sum(1 for i in contacts if rows[i]["w"] / rows[i]["h"] >= 1.15)
        r.check(sq >= 2, f"Écrasement au contact ({sq} contact(s), largeur/hauteur ≥ 1,15)", "", 2)
        st = sum(1 for i in contacts for j in (i - 1, i + 1) if 0 <= j < len(rows) and rows[j]["h"] / rows[j]["w"] >= 1.1)
        r.check(st >= 2, f"Étirement juste avant/après le contact ({st} dessin(s), hauteur/largeur ≥ 1,1)",
                "Balle allongée dans le sens du mouvement près du sol.", 2)
        areas = [x["w"] * x["h"] / (2 * rad) ** 2 for x in rows]
        r.check(min(areas) >= 0.65 and max(areas) <= 1.35, f"Volume conservé (aire relative {min(areas):.2f}–{max(areas):.2f})",
                "Écraser = élargir autant qu'on aplatit.", 2)
        inb = [x for i, x in enumerate(rows) if i not in poses]
        marked = sum(1 for x in inb if x["type"] != "KEYFRAME")
        r.check(good_types >= len(poses) - 1 and inb and marked >= 0.5 * len(inb),
                f"Types de clés : poses {good_types}/{len(poses)} Keyframe/Extreme, intervalles {marked}/{len(inb)} marqués",
                "Dope Sheet : intervalles en Breakdown (R).", 2)
    if L.flag("--render"):
        sc.frame_set(rows[contacts[0]]["f"] if contacts else 1)
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
