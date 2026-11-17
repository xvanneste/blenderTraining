"""
validate_ch03_07.py — Correcteur « Mains et pieds » (CH03.07).
Usage : … --python-exit-code 1 --python validate_ch03_07.py -- --exercise hand|foot [--render] [--debug]
Convention : bout des doigts / orteils vers +Y ; main à plat, pouce vers +X ; pied posé sur z = 0, gros orteil vers +X.
hand (SCULPT_Hand) : un volume fermé ; 20–27 cm, 12–22 cm de large (pouce écarté) ; CINQ doigts séparés (pics de la silhouette vue de
  dessus) ; le pouce est le plus court, à une extrémité ; le majeur est le plus long ; l'auriculaire le plus court des
  quatre ; index et annulaire entre 80 % et 100 % du majeur ; pouce ≈ 40–75 % de la longueur du majeur ; doigts qui
  s'effilent (base plus large que le bout).
foot (SCULPT_Foot) : un volume fermé ; 22–32 cm de long, 8–13 cm de large à l'avant-pied ; semelle plane (≥ 80 cm² sur z = 0) ;
  CINQ orteils séparés, le gros orteil le plus long et les autres décroissants ; voûte plantaire (≥ 1 cm sous le milieu du
  pied) ; talon plus étroit que l'avant-pied (50–85 %).
Seuils calibrés sur les solutions ET sur des fichiers faux (COUNTER_EXAMPLES). Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

BIN = 0.002


def components(bm):
    seen, n = set(), 0
    for v in bm.verts:
        if v.index in seen:
            continue
        n += 1
        st = [v]
        seen.add(v.index)
        while st:
            x = st.pop()
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    st.append(o)
    return n


def top_profile(P):
    """Silhouette vue de dessus : y maximal par tranche de x (BIN = 2 mm). Renvoie (x_centres, y_max)."""
    x0 = P[:, 0].min()
    idx = ((P[:, 0] - x0) / BIN).astype(int)
    n = idx.max() + 1
    prof = np.full(n, np.nan)
    for i in range(n):
        sel = P[idx == i, 1]
        if len(sel):
            prof[i] = sel.max()
    xs = x0 + (np.arange(n) + 0.5) * BIN
    floor = np.nanmin(prof)
    return xs, np.where(np.isnan(prof), floor, prof)


def peaks(xs, prof, min_prom, w=3):
    """Pics de la silhouette : maxima locaux (±w tranches) dont la proéminence est ≥ min_prom. [(x, y, prom)]."""
    out = []
    n = len(prof)
    i = 0
    while i < n:
        lo, hi = max(0, i - w), min(n, i + w + 1)
        if prof[i] >= prof[lo:hi].max() and (i == 0 or prof[i] > prof[i - 1] or prof[i] > prof[min(i + 1, n - 1)]):
            j = i
            while j + 1 < n and prof[j + 1] == prof[i]:
                j += 1
            left = i
            lmin = prof[i]
            while left > 0 and prof[left - 1] <= prof[i]:
                left -= 1
                lmin = min(lmin, prof[left])
            right = j
            rmin = prof[i]
            while right < n - 1 and prof[right + 1] <= prof[i]:
                right += 1
                rmin = min(rmin, prof[right])
            lside = left > 0
            rside = right < n - 1
            base = max(lmin if lside else -1e9, rmin if rside else -1e9)
            if not lside and not rside:
                base = lmin
            elif not lside:
                base = rmin if False else max(rmin, prof.min())
            prom = prof[i] - (base if base > -1e8 else prof.min())
            # proéminence « classique » : on prend le plus haut des deux creux (côté qui rejoint un point plus haut)
            lm = prof[left:i + 1].min() if left < i else prof[i]
            rm = prof[j:right + 1].min() if right > j else prof[i]
            bounded_l = left > 0 and prof[left - 1] > prof[i]
            bounded_r = right < n - 1 and prof[right + 1] > prof[i]
            cands = []
            if bounded_l:
                cands.append(lm)
            if bounded_r:
                cands.append(rm)
            prom = prof[i] - (max(cands) if cands else prof.min())
            if prom >= min_prom:
                out.append((float(xs[(i + j) // 2]), float(prof[i]), float(prom)))
            i = j + 1
        else:
            i += 1
    return out


def width_at(P, y, xc, half=0.014, tol=0.0025):
    sel = P[(np.abs(P[:, 1] - y) < tol) & (np.abs(P[:, 0] - xc) < half)]
    return float(sel[:, 0].max() - sel[:, 0].min()) if len(sel) > 3 else 0.0


def main():
    debug = L.flag("--debug")
    exercise = L.opt("--exercise", "hand")
    name = "SCULPT_Hand" if exercise == "hand" else "SCULPT_Foot"
    r = L.Report(f"CH03.07 — {'La main' if exercise == 'hand' else 'Le pied'}")
    ob = bpy.data.objects.get(name)
    if not r.check(ob is not None and ob.type == "MESH", f"Objet {name} (maillage)", "Partez du fichier de départ ; nommez l'objet ainsi.", 2):
        return r.finish()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(ob.matrix_world)
    bm.verts.ensure_lookup_table()
    nc = components(bm)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nc == 1 and nm == 0, f"Un seul volume fermé ({nc} morceau(x), {nm} arête(s) ouvertes)", "Voxel Remesh ; boucher la coupe du poignet / de la cheville.", 3)
    P = np.array([v.co[:] for v in bm.verts])
    ext = P.max(0) - P.min(0)
    xs, prof = top_profile(P)
    y0 = P[:, 1].min()
    if exercise == "hand":
        r.check(0.20 <= ext[1] <= 0.27, f"Longueur {ext[1] * 100:.1f} cm (20–27 : poignet → bout du majeur, doigts vers +Y)", "Échelle réelle ; main à plat, doigts vers +Y.", 2)
        r.check(0.12 <= ext[0] <= 0.22, f"Largeur {ext[0] * 100:.1f} cm (12–22 : de l'auriculaire au pouce écarté)", "Paume + pouce écarté.", 1)
        r.check(0.015 <= ext[2] <= 0.06, f"Épaisseur {ext[2] * 100:.1f} cm (1,5–6)", "Une main à plat, pas une boule.", 1)
        pk = peaks(xs, prof, 0.02)
        pk.sort(key=lambda t: t[0])
        ok5 = len(pk) == 5
        r.check(ok5, f"Cinq doigts séparés (silhouette de dessus : {len(pk)} pic(s))", "Quatre doigts + pouce, séparés par des creux d'au moins 2 cm (pas de moufle).", 4)
        if debug:
            print("[DEBUG] pics (x, y, prom) :", [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in pk])
        if ok5:
            thumb_i = min(range(5), key=lambda i: pk[i][1])
            r.check(thumb_i in (0, 4), "Le pouce (pic le plus bas) est à une extrémité", "Le pouce sort sur le côté de la paume.", 2)
            fingers = [pk[i] for i in range(5) if i != thumb_i]
            if thumb_i == 4:
                order = fingers[::-1]          # du côté du pouce vers l'auriculaire : index, majeur, annulaire, auriculaire
            else:
                order = fingers
            if thumb_i == 0:
                order = fingers[::-1][::-1]
                order = fingers                 # pouce à gauche : fingers déjà ordonnés de l'index à l'auriculaire
            h = [f[1] - y0 for f in order]
            mid = h[1]
            r.check(h[1] >= h[0] and h[1] >= h[2] and h[1] >= h[3], f"Le majeur est le plus long ({h[1] * 100:.1f} cm ; index {h[0] * 100:.1f}, annulaire {h[2] * 100:.1f}, auriculaire {h[3] * 100:.1f})", "Majeur > annulaire ≈ index > auriculaire.", 2)
            r.check(h[3] < min(h[0], h[2]) - 0.01, "L'auriculaire est le plus court des quatre doigts (d'au moins 1 cm)", "L'auriculaire dépasse à peine la dernière articulation de l'annulaire.", 2)
            r.check(0.80 <= h[0] / mid <= 1.0 and 0.80 <= h[2] / mid <= 1.0, f"Index {100 * h[0] / mid:.0f} % et annulaire {100 * h[2] / mid:.0f} % du majeur (80–100)", "Index et annulaire un peu plus courts que le majeur.", 1)
            tr = (pk[thumb_i][1] - y0) / mid
            r.check(0.40 <= tr <= 0.75, f"Pouce = {100 * tr:.0f} % de la longueur du majeur (40–75)", "Le pouce part du poignet et atteint à peu près la première articulation de l'index.", 2)
            xm = order[1][0]
            ytip = order[1][1]
            Lf = ytip - 0.105
            w_base = width_at(P, ytip - 0.80 * Lf, xm)
            w_tip = width_at(P, ytip - 0.20 * Lf, xm)
            r.check(w_tip > 0 and w_base / max(w_tip, 1e-6) >= 1.05, f"Le majeur s'effile (base {w_base * 1000:.1f} mm, près du bout {w_tip * 1000:.1f} mm ; ×{w_base / max(w_tip, 1e-6):.2f} ≥ 1,05)", "Un doigt est plus large à la base qu'au bout.", 1)
    else:
        r.check(0.22 <= ext[1] <= 0.32, f"Longueur {ext[1] * 100:.1f} cm (22–32 : talon → gros orteil)", "Échelle réelle (≈ 27 cm).", 2)
        r.check(0.10 <= ext[2] <= 0.20, f"Hauteur {ext[2] * 100:.1f} cm (10–20 : avec le bas de la jambe)", "Cheville et début de jambe.", 1)
        base_area = sum(f.calc_area() for f in bm.faces if f.normal.z < -0.95 and abs(f.calc_center_median().z - P[:, 2].min()) < 0.004)
        r.check(base_area >= 0.008, f"Semelle plane ({base_area * 1e4:.0f} cm² sur le sol, ≥ 80)", "Talon et balle posés sur z = 0 (Bisect + Fill).", 2)
        zmin = P[:, 2].min()
        arch = P[(P[:, 1] > 0.08) & (P[:, 1] < 0.13) & (np.abs(P[:, 0]) < 0.03)]
        clear = float(arch[:, 2].min() - zmin) if len(arch) else 0.0
        r.check(clear >= 0.010, f"Voûte plantaire : le milieu du pied est à {clear * 100:.1f} cm du sol (≥ 1)", "Une voûte : le milieu du pied ne touche pas le sol.", 3)
        fore = P[np.abs(P[:, 1] - 0.19) < 0.004]
        heel = P[np.abs(P[:, 1] - 0.035) < 0.004]
        wf = float(fore[:, 0].max() - fore[:, 0].min()) if len(fore) else 0.0
        wh = float(heel[:, 0].max() - heel[:, 0].min()) if len(heel) else 0.0
        r.check(0.08 <= wf <= 0.13, f"Avant-pied large de {wf * 100:.1f} cm (8–13)", "La balle du pied ≈ 10 cm.", 1)
        ratio_h = wh / wf if wf > 0 else 0.0
        r.check(0.50 <= ratio_h <= 0.85, f"Talon {100 * ratio_h:.0f} % de l'avant-pied (50–85)", "Le talon est plus étroit que l'avant du pied.", 2)
        pk = peaks(xs, prof, 0.006)
        pk.sort(key=lambda t: t[0])
        if debug:
            print("[DEBUG] pics (x, y, prom) :", [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in pk])
        ok5 = len(pk) == 5
        r.check(ok5, f"Cinq orteils séparés (silhouette de dessus : {len(pk)} pic(s))", "Cinq orteils, séparés par des sillons (pas un bloc).", 4)
        if ok5:
            ys = [p[1] for p in pk]
            big = int(np.argmax(ys))
            r.check(big in (0, 4), "Le plus long orteil est à une extrémité (gros orteil)", "Le gros orteil est sur le côté du pied.", 2)
            seq = ys[::-1] if big == 4 else ys
            dec = all(seq[i] >= seq[i + 1] - 0.002 for i in range(4))
            r.check(dec, "Les orteils décroissent du gros orteil au petit (à 2 mm près)", "Gros orteil > 2ᵉ > 3ᵉ > 4ᵉ > petit orteil.", 2)
    bm.free()
    ev.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
