"""
validate_ch04_06.py — Correcteur « Texture Painting » (CH04.06).
Usage : … --python-exit-code 1 --python validate_ch04_06.py -- --exercise painting [--render] [--debug]
PROP_Can, matériau MAT_Can, image T_Can (analyse des PIXELS) :
  - l'image T_Can alimente Base Color (Image Texture -> Base Color) ;
  - l'image est empaquetée dans le .blend (sinon la peinture est perdue) ;
  - fond = couleur dominante de l'image ; « peint » = pixel dont l'écart au fond dépasse 0,08 (par canal) ;
  - la peinture couvre 3 % à 50 % de la surface dépliée (pixels des îlots UV) ;
  - au moins deux couleurs peintes (deux familles de couleur ≥ 5 % chacune des pixels peints) ;
  - au plus 1 % des pixels peints tombent hors des îlots UV (peinture perdue).
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def uv_mask(ob, size):
    me = ob.data
    uv = me.uv_layers.active.data
    me.calc_loop_triangles()
    M = np.zeros((size, size), bool)
    for t in me.loop_triangles:
        P = np.array([uv[l].uv[:] for l in t.loops]) * size
        x0, y0 = np.floor(P.min(0)).astype(int)
        x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, size - 1), min(y1, size - 1)
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (P[1, 1] - P[2, 1]) * (P[0, 0] - P[2, 0]) + (P[2, 0] - P[1, 0]) * (P[0, 1] - P[2, 1])
        if abs(d) < 1e-12:
            continue
        a = ((P[1, 1] - P[2, 1]) * (gx - P[2, 0]) + (P[2, 0] - P[1, 0]) * (gy - P[2, 1])) / d
        b = ((P[2, 1] - P[0, 1]) * (gx - P[2, 0]) + (P[0, 0] - P[2, 0]) * (gy - P[2, 1])) / d
        c = 1 - a - b
        M[y0:y1 + 1, x0:x1 + 1] |= (a >= -0.02) & (b >= -0.02) & (c >= -0.02)
    return M


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.06 — Texture Painting")
    ob = bpy.data.objects.get("PROP_Can")
    img = bpy.data.images.get("T_Can")
    mat = ob.active_material if ob and ob.data.materials else None
    if not r.check(ob is not None and img is not None and mat is not None and ob.data.uv_layers.active is not None, "PROP_Can, MAT_Can et l'image T_Can présents", "Partez du fichier de départ.", 2):
        return r.finish()
    nt = mat.node_tree
    b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    linked = b is not None and any(l.from_node.type == "TEX_IMAGE" and l.from_node.image == img and l.to_node == b and l.to_socket.name == "Base Color" for l in nt.links)
    r.check(linked, "T_Can branchée sur Base Color (Image Texture)", "Image Texture [Color] -> Base Color.", 3)
    r.check(img.packed_file is not None, "Image empaquetée dans le .blend", "Image > Pack, puis enregistrer : sinon la peinture est perdue à la fermeture.", 3)
    W, H = img.size
    px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
    q = np.round(px * 20).astype(np.int32)
    keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    base = keys[counts.argmax()] / 20.0
    painted = (np.abs(px - base).max(axis=2) > 0.08)
    mask = uv_mask(ob, W)
    inside = painted & mask
    cov = inside.sum() / max(mask.sum(), 1)
    r.check(0.03 <= cov <= 0.50, f"Peinture : {100 * cov:.1f} % de la surface dépliée (3–50 %)", "Trop peu : rien peint ; trop : le fond a été repeint.", 3)
    pp = px[painted]
    fam = set()
    share = {}
    if len(pp):
        hsv = np.array([_hue(c) for c in pp[:: max(1, len(pp) // 4000)]])
        for h in range(6):
            share[h] = float(np.mean(hsv == h))
        fam = {h for h, s in share.items() if s >= 0.05}
    r.check(len(fam) >= 2, f"Couleurs peintes : {len(fam)} famille(s) (≥ 2)", "Peignez au moins deux couleurs.", 2)
    out_frac = (painted & ~mask).sum() / max(painted.sum(), 1)
    r.check(out_frac <= 0.01, f"Peinture hors des îlots UV : {100 * out_frac:.1f} % (≤ 1 %)", "Peignez sur l'objet, pas dans le vide de l'image.", 2)
    if debug:
        print("[DEBUG] base", np.round(base, 2), "cov", round(float(cov), 3), "familles", sorted(fam), share, "hors UV", round(float(out_frac), 4), "peint total", int(painted.sum()))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


def _hue(c):
    """Famille de couleur : 0 rouge, 1 jaune/orange, 2 vert, 3 bleu/violet, 4 gris sombre, 5 gris clair."""
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[float(x) for x in c])
    if sat < 0.25:
        return 5 if v > 0.5 else 4
    if h < 0.08 or h >= 0.92:
        return 0
    if h < 0.2:
        return 1
    if h < 0.45:
        return 2
    return 3


if __name__ == "__main__":
    L.run(main)
