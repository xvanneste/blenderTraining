"""
validate_ch02_11.py — Correcteur « Déplier une caisse et une boîte de conserve » (CH02.11).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_11.py --python-exit-code 1 -- --exercise uv [--render]
Mesures sur les UV : bornes 0–1, occupation, chevauchement (rasterisation 128 × 128 des triangles UV),
étirement (dispersion du rapport surface UV / surface 3D, pondérée par la surface).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

N = 128


def tri_area2(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def uv_stats(me):
    uv = me.uv_layers.active.data
    me.calc_loop_triangles()
    inside = all(-1e-4 <= d.uv.x <= 1 + 1e-4 and -1e-4 <= d.uv.y <= 1 + 1e-4 for d in uv)
    owner = [[-1] * N for _ in range(N)]
    overlap = 0
    covered = 0
    uv_area = 0.0
    ratios = []
    for t in me.loop_triangles:
        a, b, c = (uv[i].uv for i in t.loops)
        ar = abs(tri_area2(a, b, c)) / 2
        uv_area += ar
        if t.area > 0:
            ratios.append((ar / t.area, t.area))
        xs = [p.x for p in (a, b, c)]; ys = [p.y for p in (a, b, c)]
        for i in range(max(0, int(min(xs) * N)), min(N, int(max(xs) * N) + 1)):
            for j in range(max(0, int(min(ys) * N)), min(N, int(max(ys) * N) + 1)):
                p = ((i + 0.5) / N, (j + 0.5) / N)
                d1, d2, d3 = tri_area2(a, b, p), tri_area2(b, c, p), tri_area2(c, a, p)
                if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
                    if owner[i][j] == -1:
                        owner[i][j] = t.polygon_index
                        covered += 1
                    elif owner[i][j] != t.polygon_index:
                        overlap += 1
    tot = sum(w for _, w in ratios)
    mean = sum(r * w for r, w in ratios) / tot
    var = sum(w * (r - mean) ** 2 for r, w in ratios) / tot
    cv = (var ** 0.5) / mean if mean else 9
    return inside, uv_area, overlap / max(1, covered), cv


def has_checker(ob):
    for m in ob.data.materials:
        if m and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image and n.image.source == "GENERATED" and n.image.generated_type in ("UV_GRID", "COLOR_GRID"):
                    return True
    return False


def main():
    r = L.Report("CH02.11 — Déplier une caisse et une boîte de conserve")
    for name in ("GEO_Crate", "GEO_Can"):
        ob = L.obj(name)
        if not r.check(ob is not None and ob.type == "MESH", f"{name} présent", "Ne renommez pas les objets.", 1):
            continue
        me = ob.data
        if not r.check(len(me.uv_layers) > 0, f"{name} : carte UV présente", "Edit Mode, A, U > Unwrap ou Smart UV Project.", 3):
            continue
        inside, area, ov, cv = uv_stats(me)
        r.check(inside, f"{name} : UV dans le carré 0–1", "UV Editor : UV > Pack Islands.", 1)
        r.check(0.3 <= area <= 1.0, f"{name} : occupation de l'espace UV {100 * area:.0f} % (30–100 %)",
                "Pack Islands pour remplir l'espace sans déborder.", 1)
        r.check(ov <= 0.02, f"{name} : chevauchement {100 * ov:.1f} % (≤ 2 %)", "Îles superposées : re-déplier, Pack Islands.", 2)
        r.check(cv <= 0.25, f"{name} : étirement faible (dispersion de densité {cv:.2f} ≤ 0,25)",
                "Coutures mal placées : damier déformé ; Average Islands Scale.", 2)
        r.check(has_checker(ob), f"{name} : matériau damier (UV Grid / Color Grid)", "Gardez MAT_Checker pour contrôler.", 1, mandatory=False)
    can = L.obj("GEO_Can")
    if can:
        ns = sum(1 for e in can.data.edges if e.use_seam)
        r.check(ns >= 33, f"GEO_Can : {ns} arête(s) de couture (≥ 33 : 1 verticale + 2 cercles de 16+)",
                "Edge > Mark Seam sur une arête verticale et les deux cercles des couvercles.", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
