"""
validate_ch03_09.py — Correcteur « La retopologie du visage » (CH03.09).
Usage : … --python-exit-code 1 --python validate_ch03_09.py -- --exercise retopo [--render] [--debug]
RETOPO_Face (maillage) sur SCULPT_Bust : ≥ 95 % de quads ; 300–2 500 faces (maillage léger) ; adhérence au sculpt (distance moyenne
des sommets à la surface ≤ 4 mm, 95ᵉ centile ≤ 8 mm) ; TROIS boucles intérieures ouvertes (yeux et bouche) placées au bon endroit ;
faces plus petites autour des yeux et de la bouche que sur le reste (≤ 80 %) ; topologie régulière (≥ 80 % des sommets intérieurs
de valence 4) ; couvre le devant du visage (≥ 85 %) ; normales vers l'extérieur (≥ 95 %).
Seuils calibrés sur la solution ET sur des fichiers faux (COUNTER_EXAMPLES). Testé avec : Blender 5.3.0.
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

EYE_X, EYE_Z, MOUTH_Z = 0.032, 0.385, 0.3085
MEAN_MAX, P95_MAX = 0.004, 0.008
DENSITY_MAX = 0.80
VALENCE_MIN = 0.80
COVER_MIN = 0.85
NORMALS_MIN = 0.95


def boundary_loops(bm):
    """Composantes connexes des arêtes de bord : [(sommets)]."""
    edges = [e for e in bm.edges if e.is_boundary]
    adj = {}
    for e in edges:
        a, b = e.verts[0].index, e.verts[1].index
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for s in adj:
        if s in seen:
            continue
        st, comp = [s], []
        seen.add(s)
        while st:
            x = st.pop()
            comp.append(x)
            for o in adj[x]:
                if o not in seen:
                    seen.add(o)
                    st.append(o)
        loops.append(comp)
    return loops


def main():
    debug = L.flag("--debug")
    r = L.Report("CH03.09 — La retopologie du visage")
    rt = bpy.data.objects.get("RETOPO_Face")
    bust = bpy.data.objects.get("SCULPT_Bust")
    if not r.check(rt is not None and rt.type == "MESH" and bust is not None, "Objets RETOPO_Face (maillage) et SCULPT_Bust", "Créez RETOPO_Face devant le visage.", 2):
        return r.finish()
    dg = bpy.context.evaluated_depsgraph_get()
    me = rt.evaluated_get(dg).to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(rt.matrix_world)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    nf = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    qr = quads / nf if nf else 0
    r.check(nf > 0 and qr >= 0.95, f"Tout en quads : {100 * qr:.0f} % de quads ({quads}/{nf})", "Pas de triangles ni de n-gones : Mesh > Faces > Tris to Quads, ou refaire proprement.", 3)
    r.check(300 <= nf <= 2500, f"{nf} faces (300–2 500 : un maillage léger)", "Trop dense : ce n'est plus une retopo ; trop peu : pas de boucles.", 2)
    # adhérence au sculpt
    mb = bust.evaluated_get(dg).to_mesh()
    BV = [bust.matrix_world @ v.co for v in mb.vertices]
    bvh = BVHTree.FromPolygons(BV, [tuple(p.vertices) for p in mb.polygons])
    P = np.array([v.co[:] for v in bm.verts])
    dist = []
    for p in P:
        loc, nor, _i, d = bvh.find_nearest(Vector(p))
        dist.append(d if loc is not None else 1.0)
    dist = np.array(dist)
    mean_d, p95 = float(dist.mean()), float(np.percentile(dist, 95))
    r.check(mean_d <= MEAN_MAX and p95 <= P95_MAX, f"Adhérence au sculpt : distance moyenne {mean_d * 1000:.1f} mm, 95ᵉ centile {p95 * 1000:.1f} mm (≤ {MEAN_MAX * 1000:.0f} / {P95_MAX * 1000:.0f})",
            "Shrinkwrap (Project, cible SCULPT_Bust, Offset ≈ 2 mm) puis Apply ; ou Snap > Face Project.", 3)
    # trous intérieurs (yeux, bouche)
    loops = boundary_loops(bm)
    info = []
    for comp in loops:
        pts = P[comp]
        info.append((len(comp), pts.mean(0), pts.max(0) - pts.min(0)))
    info.sort(key=lambda t: -(t[2][0] * t[2][2]))          # le plus grand en X×Z = bord extérieur
    inner = info[1:] if info else []
    need = [(EYE_X, EYE_Z), (-EYE_X, EYE_Z), (0.0, MOUTH_Z)]
    found = 0
    for (cx, cz) in need:
        for n, c, sz in inner:
            if math.hypot(c[0] - cx, c[2] - cz) <= 0.015:
                found += 1
                break
    r.check(found == 3, f"Trous aux bons endroits : {found}/3 (œil droit, œil gauche, bouche) parmi {len(inner)} trou(s) intérieur(s)",
            "Supprimez les faces au centre des boucles des yeux et de la bouche (ouvertures).", 4)
    # densité : faces plus petites près des yeux / de la bouche
    cen = np.array([f.calc_center_median()[:] for f in bm.faces]) if nf else np.zeros((0, 3))
    area = np.array([f.calc_area() for f in bm.faces]) if nf else np.zeros(0)
    near = np.zeros(nf, bool)
    for (cx, cz) in need:
        near |= (np.hypot(cen[:, 0] - cx, cen[:, 2] - cz) < 0.025) if nf else near
    ratio = float(area[near].mean() / area[~near].mean()) if near.any() and (~near).any() else 1.0
    r.check(ratio <= DENSITY_MAX, f"Densité resserrée autour des yeux et de la bouche : faces à {100 * ratio:.0f} % de la taille des autres (≤ {100 * DENSITY_MAX:.0f})",
            "Des boucles concentriques plus serrées autour des yeux et de la bouche (Inset Faces, Loop Cut).", 3)
    # régularité
    bnd = set()
    for e in bm.edges:
        if e.is_boundary:
            bnd.add(e.verts[0].index)
            bnd.add(e.verts[1].index)
    inter = [v for v in bm.verts if v.index not in bnd]
    val4 = sum(1 for v in inter if len(v.link_edges) == 4)
    vr = val4 / len(inter) if inter else 0
    r.check(vr >= VALENCE_MIN, f"Topologie régulière : {100 * vr:.0f} % des sommets intérieurs de valence 4 ({val4}/{len(inter)}) (≥ {100 * VALENCE_MIN:.0f})",
            "Peu de pôles (valence 3 ou 5) : ils tordent les boucles et les déformations.", 2)
    # couverture du devant du visage
    bvh_r = BVHTree.FromPolygons([Vector(p) for p in P], [tuple(v.index for v in f.verts) for f in bm.faces]) if nf else None
    samp = [(Vector(BV[i]), mb.vertices[i].normal) for i in range(0, len(BV), max(1, len(BV) // 4000))]
    tot = ok = 0
    for co, nor in samp:
        if abs(co.x) <= 0.06 and 0.27 <= co.z <= 0.46 and nor.y < -0.5:
            tot += 1
            if bvh_r is not None:
                loc, _n, _j, d = bvh_r.find_nearest(co)
                if loc is not None and d <= 0.012:
                    ok += 1
    cov = ok / tot if tot else 0
    r.check(cov >= COVER_MIN, f"Le devant du visage est couvert : {100 * cov:.0f} % (≥ {100 * COVER_MIN:.0f})", "Le maillage doit couvrir front, nez, joues, bouche, menton.", 2)
    # orientation des normales
    good = 0
    for f in bm.faces:
        loc, nor, _i, d = bvh.find_nearest(f.calc_center_median())
        if loc is not None and f.normal.dot(nor) > 0:
            good += 1
    nr = good / nf if nf else 0
    r.check(nr >= NORMALS_MIN, f"Normales vers l'extérieur : {100 * nr:.0f} % (≥ {100 * NORMALS_MIN:.0f})", "Mesh > Normals > Recalculate Outside.", 1)
    if debug:
        print(f"[DEBUG] faces={nf} quads={qr:.3f} mean={mean_d * 1000:.2f}mm p95={p95 * 1000:.2f}mm holes={[(n, tuple(round(v, 3) for v in c)) for n, c, s in inner]} density={ratio:.3f} valence4={vr:.3f} cover={cov:.3f} normals={nr:.3f}")
    bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
