"""
mcp_face06.py — mesure en direct des détails de visage de CH03.06 dans Blender 5.2 (MCP), même logique que validate_ch03_06.py.
Usage (après mcp_sculpt) : exec(open(…/mcp_face06.py).read(), H) ; H["feat"]() -> dict. Nécessite REF_Base (copie cachée du buste de départ).
"""
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

EX, EZ, TIP, CHIN, MZ = 0.032, 0.385, 0.341, 0.2588, 0.3085
_bvh = {}


def feat():
    ob = bpy.data.objects["SCULPT_Bust"]
    me = ob.data
    ref = bpy.data.objects["REF_Base"]
    if "b" not in _bvh:
        _bvh["b"] = BVHTree.FromPolygons([ref.matrix_basis @ v.co for v in ref.data.vertices], [tuple(p.vertices) for p in ref.data.polygons])
    bvh = _bvh["b"]
    refresh()  # noqa: F821  (défini dans mcp_sculpt, même espace de noms)
    n = len(me.vertices)
    P = coords(ob).astype(float)  # noqa: F821
    N = np.empty(n * 3, np.float32)
    me.vertices.foreach_get("normal", N)
    N = N.reshape(n, 3).astype(float)
    zone = (np.abs(P[:, 0]) < 0.09) & (P[:, 2] > 0.25) & (P[:, 2] < 0.46)
    idx = np.nonzero(zone)[0]
    s = np.zeros(n)
    for i in idx:
        loc, nor, _i, _d = bvh.find_nearest(Vector(P[i]))
        s[i] = 1000 * (Vector(P[i]) - loc).dot(nor)
    front = (N[:, 1] < -0.1) & (P[:, 1] < -0.04)
    out = {}
    lids = []
    for sg in (1, -1):
        rr = np.hypot(P[:, 0] - sg * EX, P[:, 2] - EZ)
        ann = front & (rr > 0.012) & (rr < 0.020)
        lids.append(round(float(np.mean(s[ann] >= 0.8)), 3) if ann.any() else 0)
    out["lids"] = lids
    under = (N[:, 2] < -0.2) & (P[:, 1] < -0.05) & (P[:, 2] > TIP - 0.020) & (P[:, 2] < TIP + 0.003) & (np.abs(P[:, 0]) < 0.020)
    out["nostrils"] = [int(np.sum(under & (P[:, 0] * sg > 0.002) & (s <= -1.5))) for sg in (1, -1)]
    band = front & (P[:, 2] > CHIN + 0.02) & (P[:, 2] < TIP - 0.012) & (np.abs(P[:, 0]) < 0.05)
    hit_ = band & (s <= -2.8)
    cen = hit_ & (np.abs(P[:, 0]) < 0.008)
    out["mouth_center"] = int(cen.sum())
    lift = None
    if cen.sum() >= 3:
        zc = float(P[cen, 2].mean())
        ends = []
        for sg in (1, -1):
            x, zprev = 0.0, zc
            while x < 0.030:
                sel = hit_ & (np.abs(P[:, 0] * sg - (x + 0.004)) < 0.002) & (np.abs(P[:, 2] - zprev) < 0.006)
                if not sel.any():
                    break
                x += 0.004
                zprev = float(P[sel, 2].mean())
            ends.append((x, zprev))
        lift = round(((ends[0][1] + ends[1][1]) / 2 - zc) * 1000, 2)
        out["mouth_width_cm"] = round((ends[0][0] + ends[1][0]) * 100, 1)
    out["lift_mm"] = lift
    out["ears"] = [int(np.sum(((P[:, 0] * sg > 0.066) & (P[:, 2] > EZ - 0.05) & (P[:, 2] < EZ + 0.045)) & (s <= -1.2))) for sg in (1, -1)]
    out["max_abs_mm"] = round(float(np.abs(s[idx]).max()), 2)
    return out
