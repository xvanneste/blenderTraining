"""
validate_ch04_01.py — Correcteur « UV propres » (CH04.01).
Usage : … --python-exit-code 1 --python validate_ch04_01.py -- --exercise uv [--render] [--debug]
PROP_Chest, calque UV actif :
  - toutes les UV dans [0, 1] ;
  - distorsion : étirement moyen (rapport des valeurs singulières du jacobien 3D→UV, pondéré par l'aire) ≤ 1,15 et 95ᵉ centile ≤ 1,6 ;
  - densité de texels uniforme : écart-type du log de la densité (pondéré) ≤ 0,20 ;
  - aucun chevauchement : l'union rastérisée (1024²) vaut ≥ 98 % de la somme des aires ;
  - occupation de l'espace UV ≥ 50 % ;
  - 4 à 40 îlots ; au moins 6 arêtes marquées comme seams.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

STRETCH_MEAN, STRETCH_P95, DENS_STD, OVERLAP_MIN, COVER_MIN = 1.15, 1.6, 0.20, 0.98, 0.50
RES = 1024


def tri_data(ob):
    """Pour chaque triangle : positions 3D (échelle objet appliquée) et UV."""
    me = ob.data
    me.calc_loop_triangles()
    uv = me.uv_layers.active.data
    sc = np.array(ob.scale)
    V = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", V)
    V = V.reshape(-1, 3) * sc
    P, U = [], []
    for t in me.loop_triangles:
        P.append([V[v] for v in t.vertices])
        U.append([uv[l].uv[:] for l in t.loops])
    return np.array(P, float), np.array(U, float)


def metrics(P, U):
    e1, e2 = P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]
    u1, u2 = U[:, 1] - U[:, 0], U[:, 2] - U[:, 0]
    area3 = 0.5 * np.linalg.norm(np.cross(e1, e2), axis=1)
    areau = 0.5 * np.abs(u1[:, 0] * u2[:, 1] - u1[:, 1] * u2[:, 0])
    ok = (areau > 1e-12) & (area3 > 1e-12)
    stretch = np.ones(len(P))
    dens = np.zeros(len(P))
    for i in np.nonzero(ok)[0]:
        A = np.array([[u1[i, 0], u2[i, 0]], [u1[i, 1], u2[i, 1]]])
        B = np.stack([e1[i], e2[i]], axis=1)
        J = B @ np.linalg.inv(A)
        s = np.linalg.svd(J, compute_uv=False)
        stretch[i] = s[0] / max(s[1], 1e-12)
        dens[i] = np.sqrt(s[0] * s[1])                 # longueur 3D par unité UV (∝ 1 / densité de texels)
    return area3, areau, stretch, dens, ok


def overlap_ratio(U):
    cnt = np.zeros((RES, RES), np.int16)
    for t in U:
        pts = np.clip(t * (RES - 1), 0, RES - 1)
        x0, y0 = np.floor(pts.min(0)).astype(int)
        x1, y1 = np.ceil(pts.max(0)).astype(int)
        if x1 <= x0 or y1 <= y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        px, py = xs + 0.5, ys + 0.5
        a, b, c = pts
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-9:
            continue
        l1 = ((b[1] - c[1]) * (px - c[0]) + (c[0] - b[0]) * (py - c[1])) / d
        l2 = ((c[1] - a[1]) * (px - c[0]) + (a[0] - c[0]) * (py - c[1])) / d
        m = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        cnt[ys[m], xs[m]] += 1
    covered = int((cnt > 0).sum())
    total = int(cnt.sum())
    return (covered / total if total else 0.0), covered / (RES * RES)


def count_islands(ob):
    me = ob.data
    uv = me.uv_layers.active.data
    parent = list(range(len(me.polygons)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    corner = {}
    for p in me.polygons:
        for li in p.loop_indices:
            key = (me.loops[li].vertex_index, round(uv[li].uv[0], 4), round(uv[li].uv[1], 4))
            if key in corner:
                parent[find(corner[key])] = find(p.index)
            else:
                corner[key] = p.index
    return len({find(i) for i in range(len(me.polygons))})


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.01 — UV propres")
    ob = bpy.data.objects.get("PROP_Chest")
    if not r.check(ob is not None and ob.type == "MESH" and ob.data.uv_layers.active is not None, "PROP_Chest avec un calque UV", "Partez du fichier de départ.", 2):
        return r.finish()
    P, U = tri_data(ob)
    inb = bool(np.all(U >= -1e-4) and np.all(U <= 1 + 1e-4))
    r.check(inb, f"Toutes les UV dans [0, 1] (min {U.min():.2f}, max {U.max():.2f})", "UV > Pack Islands, ou mettez à l'échelle pour tout faire tenir dans le carré.", 3)
    area3, areau, stretch, dens, ok = metrics(P, U)
    w = area3[ok] / area3[ok].sum()
    sm = float(np.sum(w * stretch[ok]))
    order = np.argsort(stretch[ok])
    cw = np.cumsum(w[order])
    p95 = float(stretch[ok][order][np.searchsorted(cw, 0.95)])
    r.check(sm <= STRETCH_MEAN and p95 <= STRETCH_P95, f"Distorsion : étirement moyen {sm:.2f} (≤ {STRETCH_MEAN}), 95ᵉ centile {p95:.2f} (≤ {STRETCH_P95})",
            "Des seams sur les arêtes vives puis Unwrap (Angle Based / Conformal) ; vérifiez le damier.", 4)
    ld = np.log(dens[ok])
    mu = float(np.sum(w * ld))
    sd = float(np.sqrt(np.sum(w * (ld - mu) ** 2)))
    r.check(sd <= DENS_STD, f"Densité de texels uniforme : écart-type du log {sd:.2f} (≤ {DENS_STD})", "UV > Average Islands Scale : tous les îlots à la même échelle.", 3)
    ov, cov = overlap_ratio(U)
    r.check(ov >= OVERLAP_MIN, f"Pas de chevauchement : union / somme des aires = {100 * ov:.1f} % (≥ {100 * OVERLAP_MIN:.0f})", "Des îlots se recouvrent : Pack Islands.", 4)
    r.check(cov >= COVER_MIN, f"Espace UV utilisé : {100 * cov:.0f} % (≥ {100 * COVER_MIN:.0f})", "Packez et agrandissez : de l'espace perdu = textures plus floues.", 2)
    ni = count_islands(ob)
    r.check(4 <= ni <= 40, f"{ni} îlots (4–40)", "Trop peu : une seule peau étirée ; trop : couture partout.", 1)
    ns = sum(1 for e in ob.data.edges if e.use_seam)
    r.check(ns >= 6, f"{ns} arêtes marquées comme seams (≥ 6)", "Mark Seam sur les arêtes vives.", 2)
    if debug:
        print(f"[DEBUG] stretch mean={sm:.3f} p95={p95:.3f} dens_std={sd:.3f} overlap_ratio={ov:.4f} coverage={cov:.3f} islands={ni} seams={ns} U[{U.min():.2f},{U.max():.2f}]")
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
