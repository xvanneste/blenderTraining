"""
validate_ch03_08.py — Correcteur « Le poncho » (CH03.08, simulation de tissu).
Usage : … --python-exit-code 1 --python validate_ch03_08.py -- --exercise poncho [--render] [--debug]
CLOTH_Poncho (maillage) : modificateur Cloth APPLIQUÉ (le tissu est un maillage figé) ; pas de pénétration du corps
(SCULPT_Bust) ; tissu non étiré (arête moyenne ≤ 1,3 × l'arête au repos, la plus longue ≤ 2,5 ×) ; il couvre les épaules ;
il ne traverse pas le sol ; il présente des PLIS (rugosité locale suffisante) ; il n'est pas plus petit que les épaules.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402

PEN_MAX = 0.005        # fraction maximale de sommets dans le corps (calibré : solution 0 ; pénétrant 0,80)
COVER_MIN = 0.80       # couverture minimale des épaules (calibré : solution 0,94 ; trop petit 0,60 ; étiré 0)
WRINKLE_MIN = 3.0      # rugosité minimale (mm, 90e centile) (calibré : solution 10,6 ; lissé 0,93)


def peaks_circular(vals, min_prom):
    """Pics d'une série circulaire (maxima locaux dont la proéminence ≥ min_prom)."""
    n = len(vals)
    cnt = 0
    for i in range(n):
        v = vals[i]
        if v < vals[(i - 1) % n] or v < vals[(i + 1) % n]:
            continue
        # proéminence : on descend de chaque côté jusqu'à trouver plus haut ; on garde le plus haut des deux creux
        lm, j = v, 1
        while j < n and vals[(i - j) % n] <= v:
            lm = min(lm, vals[(i - j) % n])
            j += 1
        rm, k = v, 1
        while k < n and vals[(i + k) % n] <= v:
            rm = min(rm, vals[(i + k) % n])
            k += 1
        if j >= n and k >= n:        # sommet global : proéminence = v - min
            prom = v - min(vals)
        else:
            cands = []
            if j < n:
                cands.append(lm)
            if k < n:
                cands.append(rm)
            prom = v - max(cands)
        if prom >= min_prom:
            cnt += 1
    return cnt


def main():
    debug = L.flag("--debug")
    r = L.Report("CH03.08 — Le poncho (tissu)")
    cl = bpy.data.objects.get("CLOTH_Poncho")
    body = bpy.data.objects.get("SCULPT_Bust")
    if not r.check(cl is not None and cl.type == "MESH" and body is not None, "Objets CLOTH_Poncho (maillage) et SCULPT_Bust", "Partez du fichier de départ.", 2):
        return r.finish()
    r.check(not any(m.type == "CLOTH" for m in cl.modifiers), "Le modificateur Cloth est APPLIQUÉ (le tissu est un maillage figé)",
            "À l'image où le tissu est au repos : Ctrl+A sur le modificateur Cloth (Apply).", 2)
    dg = bpy.context.evaluated_depsgraph_get()
    me_c = cl.evaluated_get(dg).to_mesh()
    P = np.array([cl.matrix_world @ v.co for v in me_c.vertices])
    me_b = body.evaluated_get(dg).to_mesh()
    BV = np.array([body.matrix_world @ v.co for v in me_b.vertices])
    BN = np.array([(body.matrix_world.to_3x3() @ v.normal).normalized()[:] for v in me_b.vertices])
    bvh_b = BVHTree.FromPolygons([Vector(v) for v in BV], [tuple(p.vertices) for p in me_b.polygons])
    bvh_c = BVHTree.FromPolygons([Vector(v) for v in P], [tuple(p.vertices) for p in me_c.polygons])
    r.check(len(P) > 500, f"{len(P)} sommets (≥ 500)", "Subdivisez le tissu (maille ≈ 1,6 cm).", 1)
    # pénétration : sommets du tissu situés DANS le corps
    inside = 0
    for p in P:
        loc, nor, _i, d = bvh_b.find_nearest(Vector(p))
        if loc is not None and d < 0.05 and (Vector(p) - loc).dot(nor) < -0.0005:
            inside += 1
    pen = inside / len(P)
    r.check(pen <= PEN_MAX, f"Pas de pénétration : {100 * pen:.2f} % des sommets dans le corps (≤ {100 * PEN_MAX:.2f} %)",
            "Le tissu traverse le corps : Collision sur le COLLIDER (visible dans la vue 3D, pas masqué), distance de collision ≥ 3 mm.", 3)
    # étirement
    rest = float(cl.get("rest_edge", 0.016))
    edges = np.array([(P[e.vertices[0]] - P[e.vertices[1]]) for e in me_c.edges])
    el = np.linalg.norm(edges, axis=1)
    r.check(el.mean() <= 1.3 * rest and el.max() <= 2.5 * rest,
            f"Tissu non étiré : arête moyenne {el.mean() * 1000:.1f} mm (repos {rest * 1000:.1f}), plus longue {el.max() * 1000:.1f} mm",
            "Rigidités (Tension, Compression) plus fortes ; pas de mise à l'échelle du tissu après simulation.", 2)
    # sol
    r.check(P[:, 2].min() >= -0.003, f"Le tissu ne traverse pas le sol (z min = {P[:, 2].min() * 1000:.1f} mm)", "Ajoutez Collision au sol.", 1)
    # couverture des épaules
    sel = [i for i in range(len(BV)) if BN[i][2] > 0.3 and 0.06 <= BV[i][2] <= 0.17 and math.hypot(BV[i][0], BV[i][1]) >= 0.09]
    cov = 0.0
    if sel:
        ok = 0
        for i in sel:
            loc, _n, _j, d = bvh_c.find_nearest(Vector(BV[i]))
            if loc is not None and d <= 0.012:
                ok += 1
        cov = ok / len(sel)
    r.check(cov >= COVER_MIN, f"Le tissu couvre les épaules : {100 * cov:.0f} % de la zone des épaules à moins de 1,2 cm (≥ {100 * COVER_MIN:.0f})",
            "Tissu trop petit, ou tombé à côté : agrandissez-le / placez-le au-dessus des épaules.", 3)
    # plis : rugosité locale = écart (mm) d'un sommet à la moyenne de ses voisins, sur les sommets intérieurs au-dessus du sol
    n = len(P)
    E = np.array([[e.vertices[0], e.vertices[1]] for e in me_c.edges])
    a_, b_ = E[:, 0], E[:, 1]
    deg = np.bincount(np.concatenate([a_, b_]), minlength=n).astype(float)
    deg[deg == 0] = 1
    acc = np.zeros_like(P)
    np.add.at(acc, a_, P[b_])
    np.add.at(acc, b_, P[a_])
    lap = 1000.0 * np.linalg.norm(acc / deg[:, None] - P, axis=1)
    bm_b = bmesh.new()
    bm_b.from_mesh(me_c)
    border = np.zeros(n, bool)
    for e in bm_b.edges:
        if e.is_boundary:
            border[e.verts[0].index] = border[e.verts[1].index] = True
    bm_b.free()
    interior = ~border
    wr = float(np.percentile(lap[interior], 90)) if interior.any() else 0.0
    if debug:
        print(f"[DEBUG] pen={pen:.5f} inside={inside} cov={cov:.3f} (n={len(sel)}) edges mean/max={el.mean() * 1000:.2f}/{el.max() * 1000:.2f} mm zmin={P[:, 2].min():.4f}")
        print(f"[DEBUG] rugosité (mm) médiane={np.median(lap[interior]):.3f} p90={wr:.3f} p99={np.percentile(lap[interior], 99):.3f}")
    r.check(wr >= WRINKLE_MIN, f"Plis : rugosité du tissu {wr:.2f} mm (90ᵉ centile ; ≥ {WRINKLE_MIN})",
            "Un tissu qui tombe forme des plis : flexion plus faible, plus de matière ; un tissu trop lisse est un plastique.", 3)
    me_c.clear_geometry() if False else None
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
