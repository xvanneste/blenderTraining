"""
validate_ch04_07.py — Correcteur « Baking » (CH04.07).
Usage : … --python-exit-code 1 --python validate_ch04_07.py -- --exercise baking [--render] [--debug]
HIGH_Rock (haute définition) / LOW_Rock (basse définition + UV) / image T_Rock_N (analyse des PIXELS) :
  - géométrie intacte : HIGH ≥ 10 000 faces, LOW ≤ 1 000 faces, LOW avec UV ; HIGH caché au rendu ;
  - T_Rock_N : espace colorimétrique Non-Color, empaquetée ;
  - chaîne Image Texture (T_Rock_N) -> Normal Map (espace Tangent) -> Normal du Principled BSDF ;
  - bake présent : dans les îlots UV, ≥ 85 % des pixels s'écartent du plat (0,5 ; 0,5 ; 1) d'au moins 0,02 ;
  - normales valides : longueur moyenne du vecteur décodé (2c − 1) entre 0,9 et 1,1, composante z moyenne ≥ 0,6.
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
        M[y0:y1 + 1, x0:x1 + 1] |= (a >= -0.02) & (b >= -0.02) & (1 - a - b >= -0.02)
    return M


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.07 — Baking")
    hi, lo, img = bpy.data.objects.get("HIGH_Rock"), bpy.data.objects.get("LOW_Rock"), bpy.data.images.get("T_Rock_N")
    if not r.check(hi is not None and lo is not None and img is not None and lo.data.uv_layers.active is not None, "HIGH_Rock, LOW_Rock (avec UV) et l'image T_Rock_N présents", "Partez du fichier de départ.", 2):
        return r.finish()
    r.check(len(hi.data.polygons) >= 10000 and len(lo.data.polygons) <= 1000, f"Géométrie : HIGH {len(hi.data.polygons)} faces, LOW {len(lo.data.polygons)} faces", "Ne modifiez pas les maillages.", 2)
    r.check(hi.hide_render, "HIGH_Rock caché au rendu", "Cacher le haute définition (icône caméra de l'Outliner).", 1)
    r.check(img.colorspace_settings.name == "Non-Color", f"T_Rock_N en espace colorimétrique {img.colorspace_settings.name} (Non-Color exigé)", "Une normal map est une donnée, pas une couleur : Non-Color.", 3)
    r.check(img.packed_file is not None, "T_Rock_N empaquetée dans le .blend", "Image > Pack, puis enregistrer.", 2)
    mat = lo.active_material
    nt = mat.node_tree if mat else None
    chain = False
    if nt:
        b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        for l in nt.links:
            if b is not None and l.to_node == b and l.to_socket.name == "Normal" and l.from_node.type == "NORMAL_MAP" and l.from_node.space == "TANGENT":
                col = l.from_node.inputs["Color"]
                chain = any(k.from_node.type == "TEX_IMAGE" and k.from_node.image == img for k in col.links)
    r.check(chain, "Image Texture T_Rock_N -> Normal Map (Tangent) -> Normal du Principled", "Un nœud Normal Map est obligatoire entre l'image et Normal.", 3)
    W, H = img.size
    px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
    mask = uv_mask(lo, W)
    sel = px[mask]
    dev = np.abs(sel - np.array([0.5, 0.5, 1.0])).max(axis=1)
    cov = float((dev > 0.02).mean()) if len(sel) else 0.0
    r.check(cov >= 0.85, f"Bake présent : {100 * cov:.0f} % des pixels des îlots UV portent du relief (≥ 85 %)", "Bakez tous les îlots ; Margin ≥ 8 px.", 4)
    n = sel * 2 - 1
    ln = np.linalg.norm(n, axis=1)
    mean_len, mean_z = float(ln.mean()), float(n[:, 2].mean())
    r.check(0.9 <= mean_len <= 1.1 and mean_z >= 0.6, f"Normales valides : longueur moyenne {mean_len:.2f}, z moyen {mean_z:.2f}", "Image bakée en Normal, espace Tangent.", 2)
    if debug:
        print("[DEBUG] couverture relief", round(cov, 3), "longueur", round(mean_len, 3), "z", round(mean_z, 3), "pixels UV", int(mask.sum()), "colorspace", img.colorspace_settings.name)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
