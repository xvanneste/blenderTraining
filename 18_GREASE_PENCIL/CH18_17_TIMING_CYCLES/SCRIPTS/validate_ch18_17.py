"""
validate_ch18_17.py — Correcteur « Timing, exposition, cycle de marche » (CH18.17).
Usage : … --python-exit-code 1 --python validate_ch18_17.py -- --exercise xsheet|walk [--render]
  xsheet : chaque dessin A…H (reconnu par sa signature) commence à l'image indiquée par le texte
           XSHEET ; ordre conservé ; fin de scène = FIN.
  walk   : cycle de 16 à 32 images (pair), dessins en un ou en deux, contacts au début et à la moitié
           (silhouette la plus large, symétriques), passages étroits, rebond (bas après le contact,
           haut après le passage), pieds au sol, marche sur place, onion « Show Start Frame ».
Testé avec : Blender 5.3.0.
Mesures sur la boîte englobante de chaque dessin (sommet = tête, largeur = écart jambes/bras).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def layer(name):
    ob = bpy.data.objects.get("GP_Practice")
    if not ob or ob.type != "GREASEPENCIL":
        return None, None
    return ob, next((l for l in ob.data.layers if l.name == name), None)


def signature(drawing):
    return [len(drawing.strokes), round(sum(p.position.x for s in drawing.strokes for p in s.points), 2)]


def xsheet(r, sc):
    _ob, lay = layer("USER_Turn")
    if not r.check(lay is not None, "Calque USER_Turn présent", "Repartez du starter.", 1):
        return
    sigs = json.loads(sc.get("bcma_xsheet_sigs", "{}"))
    t = bpy.data.texts.get("XSHEET")
    want, end = {}, None
    for line in (t.as_string().splitlines() if t else []):
        parts = line.split(";")
        if len(parts) >= 2 and parts[1].strip().isdigit():
            if parts[0].strip() == "FIN":
                end = int(parts[1])
            else:
                want[parts[0].strip()] = int(parts[1])
    got = {}
    for fr in lay.frames:
        sg = signature(fr.drawing)
        name = next((n for n, s in sigs.items() if s == sg), None)
        if name:
            got[name] = fr.frame_number
    r.check(len(got) == len(want) == 8, f"Les 8 dessins retrouvés ({len(got)}/8)", "Ne redessinez pas : déplacez les clés.", 2)
    ok = [n for n in want if got.get(n) == want[n]]
    bad = [f"{n} : {got.get(n)} au lieu de {want[n]}" for n in want if got.get(n) != want[n]]
    r.check(not bad, f"Exposition conforme à la feuille ({len(ok)}/{len(want)})", " ; ".join(bad[:4]), 4)
    order = [n for n, _f in sorted(got.items(), key=lambda kv: kv[1])]
    r.check(order == sorted(want), "Ordre des dessins conservé (A → H)", f"Ordre trouvé : {''.join(order)}", 2)
    r.check(sc.frame_end == end, f"Fin de scène {sc.frame_end} (attendu {end})", "Frame Range > End.", 1)


def measure(lay):
    rows = []
    for fr in sorted(lay.frames, key=lambda f: f.frame_number):
        xs = [p.position.x for s in fr.drawing.strokes for p in s.points]
        zs = [p.position.z for s in fr.drawing.strokes for p in s.points]
        if len(xs) >= 10:
            rows.append({"f": fr.frame_number, "w": max(xs) - min(xs), "top": max(zs), "bottom": min(zs),
                         "cx": sum(xs) / len(xs)})
    return rows


def nearest(rows, f):
    return min(rows, key=lambda x: abs(x["f"] - f))


def walk(r, sc):
    ob, lay = layer("USER_Walk")
    if not r.check(lay is not None, "Calque USER_Walk présent", "Repartez du starter.", 1):
        return
    n = sc.frame_end - sc.frame_start + 1
    r.check(16 <= n <= 32 and n % 2 == 0, f"Durée du cycle : {n} images (16 à 32, pair)", "Frame Range : 1 à 24 conseillé.", 1)
    rows = [x for x in measure(lay) if sc.frame_start <= x["f"] <= sc.frame_end]
    frames = [x["f"] for x in rows]
    gaps = [b - a for a, b in zip(frames, frames[1:])]
    if not r.check(len(rows) >= n // 2 and frames and frames[0] == sc.frame_start and max(gaps or [9]) <= 2,
                   f"{len(rows)} dessins dans le cycle, en un ou en deux (écart max {max(gaps or [0])})",
                   "Un dessin toutes les 1 à 2 images, le premier à l'image 1.", 3):
        return
    s0 = sc.frame_start
    c1, c2 = rows[0], nearest(rows, s0 + n // 2)
    p1, p2 = nearest(rows, s0 + n // 4), nearest(rows, s0 + 3 * n // 4)
    H = c1["top"] - c1["bottom"]
    narrow = max(p1["w"], p2["w"])
    r.check(min(c1["w"], c2["w"]) >= 1.25 * narrow,
            f"Contacts écartés ({c1['w']:.2f} / {c2['w']:.2f} m) vs passages serrés ({narrow:.2f} m)",
            "Contact : jambes au plus large ; passage : jambes croisées sous le corps.", 3)
    r.check(abs(c1["w"] - c2["w"]) <= 0.15 * c1["w"] and abs(c1["top"] - c2["top"]) <= 0.03 * H,
            "Second contact symétrique du premier (même pose, jambes inversées)", "Dessin de la moitié du cycle = dessin 1 inversé.", 2)
    tops = [x["top"] for x in rows]
    r.check(max(tops) - min(tops) >= 0.02 * H, f"Rebond du corps : {max(tops) - min(tops):.3f} m ({100 * (max(tops) - min(tops)) / H:.1f} % de la taille)",
            "La tête monte et descend (≥ 2 % de la taille).", 2)
    ok_half = 0
    for a in (s0, s0 + n // 2):
        q = n // 4
        first = [x for x in rows if a < x["f"] <= a + q]
        second = [x for x in rows if a + q < x["f"] < a + 2 * q]
        if first and second:
            lo = min(first + second, key=lambda x: x["top"])
            hi = max(first + second, key=lambda x: x["top"])
            if lo in first and hi in second:
                ok_half += 1
    r.check(ok_half == 2, f"Bas après le contact, haut après le passage ({ok_half}/2 pas)",
            "Position basse entre contact et passage ; haute entre passage et contact suivant.", 3)
    bots = [x["bottom"] for x in rows]
    r.check(max(bots) - min(bots) <= 0.12, f"Un pied toujours au sol (variation du point le plus bas {max(bots) - min(bots):.2f} m)",
            "Le pied d'appui reste sur la ligne de sol.", 2)
    cxs = [x["cx"] for x in rows]
    r.check(max(cxs) - min(cxs) <= 0.25 * H, f"Marche sur place (dérive {max(cxs) - min(cxs):.2f} m)",
            "Le corps reste sur l'axe ; c'est le pied d'appui qui glisse vers l'arrière.", 1)
    r.check(ob.data.use_onion_loop, "Onion skinning : Show Start Frame activé", "Object Data > Onion Skinning > Display.", 1)
    if L.flag("--render"):
        sc.frame_set(1)
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)


def main():
    ex = L.opt("--exercise", "walk")
    sc = bpy.context.scene
    r = L.Report(f"CH18.17 — Timing et cycles ({ex})")
    {"xsheet": xsheet, "walk": walk}[ex](r, sc)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
