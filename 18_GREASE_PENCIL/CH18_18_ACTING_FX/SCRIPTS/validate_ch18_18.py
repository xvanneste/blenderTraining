"""
validate_ch18_18.py — Correcteur « Le plan animé de 5 s » (CH18.18).
Usage : … --python-exit-code 1 --python validate_ch18_18.py -- --exercise shot [--render]
Vérifie : durée 4,5–6 s à 24 i/s ; USER_Char (≥ 12 dessins, ≥ 3 tenues ≥ 6 images, parties rapides,
réaction 1–6 images après le début de l'effet, déformation écrasé/étiré) ; USER_FX (≥ 6 dessins,
éclair rapide, évolution de taille, clé vide finale) ; caméra : tremblement (≥ 5 clés en ≤ 14 images,
alternance) synchronisé à ±2 images sur l'effet, retour à la position de départ.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def frames_of(lay):
    out = []
    for fr in sorted(lay.frames, key=lambda f: f.frame_number):
        pts = [p.position for s in fr.drawing.strokes for p in s.points]
        if pts:
            xs, zs = [p.x for p in pts], [p.z for p in pts]
            out.append({"f": fr.frame_number, "n": len(fr.drawing.strokes), "w": max(xs) - min(xs), "h": max(zs) - min(zs)})
        else:
            out.append({"f": fr.frame_number, "n": 0, "w": 0, "h": 0})
    return out


def loc_curves(ob):
    """Courbes de location de l'objet : {indice: [(image, valeur)]} (actions par couches)."""
    out = {}
    ad = ob.animation_data if ob else None
    if not ad or not ad.action:
        return out
    for lay in getattr(ad.action, "layers", []):
        for st in lay.strips:
            for bag in getattr(st, "channelbags", []):
                for fc in bag.fcurves:
                    if fc.data_path == "location":
                        out[fc.array_index] = sorted((k.co.x, k.co.y) for k in fc.keyframe_points)
    return out


def main():
    sc = bpy.context.scene
    r = L.Report("CH18.18 — Plan animé de 5 s (acting, effet, caméra)")
    n = sc.frame_end - sc.frame_start + 1
    r.check(sc.render.fps == 24 and 108 <= n <= 144, f"Durée {n} images à {sc.render.fps} i/s (4,5–6 s)", "120 images = 5 s.", 1)
    ob = bpy.data.objects.get("GP_Practice")
    lays = {l.name: l for l in ob.data.layers} if ob and ob.type == "GREASEPENCIL" else {}
    if not r.check("USER_Char" in lays and "USER_FX" in lays, "Calques USER_Char et USER_FX présents", "Repartez du starter.", 1):
        return r.finish()
    ch = [x for x in frames_of(lays["USER_Char"]) if x["n"] > 0]
    fx_all = frames_of(lays["USER_FX"])
    fx = [x for x in fx_all if x["n"] > 0]
    # personnage
    fr = [x["f"] for x in ch] + [sc.frame_end + 1]
    holds = sum(1 for a, b in zip(fr, fr[1:]) if b - a >= 6)
    quick = sum(1 for a, b in zip(fr, fr[1:]) if b - a <= 2)
    r.check(len(ch) >= 12, f"Personnage : {len(ch)} dessins (≥ 12)", "Animez le jeu d'acteur.", 2)
    r.check(holds >= 3 and quick >= 3, f"Tenues lisibles ({holds} ≥ 3 de 6 images ou plus) et parties rapides ({quick} ≥ 3)",
            "Alternez poses tenues (lecture) et dessins rapides (action).", 2)
    hs = [x["h"] / x["w"] for x in ch if x["w"] > 0]
    r.check(hs and max(hs) / min(hs) >= 1.15, f"Écrasement / étirement du personnage (rapport des proportions {max(hs) / min(hs) if hs else 0:.2f})",
            "Sursaut : un dessin écrasé puis un étiré.", 2)
    if not r.check(len(fx) >= 6, f"Effet : {len(fx)} dessins (≥ 6)", "Éclair + fumée sur USER_FX.", 2):
        return r.finish()
    pop = fx[0]["f"]
    react = [x["f"] - pop for x in ch if 1 <= x["f"] - pop <= 6]
    r.check(bool(react), f"Réaction du personnage {react[0] if react else '—'} image(s) après le début de l'effet (1–6)",
            "Le personnage réagit juste APRÈS l'éclatement (pas avant, pas trop tard).", 2)
    first_gaps = [b["f"] - a["f"] for a, b in zip(fx[:3], fx[1:3])]
    r.check(first_gaps and max(first_gaps) <= 2, f"Éclair rapide (premiers dessins de l'effet espacés de {first_gaps})", "Éclair en un ou en deux.", 1)
    sizes = [x["w"] * x["h"] for x in fx]
    r.check(max(sizes) >= 1.5 * min(sizes), f"L'effet évolue (taille ×{max(sizes) / max(min(sizes), 1e-6):.1f})", "Grossir, monter, se dissiper.", 1)
    last_fx = max(x["f"] for x in fx)
    empty_after = any(x["n"] == 0 and x["f"] > last_fx for x in fx_all)
    r.check(empty_after, "L'effet disparaît (clé vide après le dernier dessin d'effet)", "Insert Blank Keyframe après la fumée.", 2)
    # caméra
    cam = sc.camera
    cur = loc_curves(cam)
    keys = sorted({f for c in cur.values() for f, _v in c})
    burst = [f for f in keys if pop - 2 <= f <= pop + 14]
    alt = 0
    for c in cur.values():
        vals = [v for f, v in c if pop - 2 <= f <= pop + 14]
        d = [b - a for a, b in zip(vals, vals[1:]) if abs(b - a) > 1e-4]
        alt = max(alt, sum(1 for a, b in zip(d, d[1:]) if a * b < 0))
    r.check(len(burst) >= 5 and alt >= 3, f"Tremblement de caméra : {len(burst)} clés autour de l'effet, {alt} changements de sens",
            "Clés de Location alternées (gauche/droite, haut/bas) sur ~10 images à partir de l'effet.", 3)
    r.check(bool(burst) and abs(burst[0] - pop) <= 2 or (len(burst) > 1 and abs(burst[1] - pop) <= 2),
            f"Tremblement synchronisé sur l'effet (image {pop})", "Première secousse à ±2 images de l'éclatement.", 1)
    back = all(abs(c[0][1] - c[-1][1]) < 0.01 for c in cur.values()) if cur else False
    r.check(back, "Caméra revenue à sa position de départ", "Dernière clé = première clé.", 1)
    if L.flag("--render"):
        sc.frame_set(pop + 1)
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
