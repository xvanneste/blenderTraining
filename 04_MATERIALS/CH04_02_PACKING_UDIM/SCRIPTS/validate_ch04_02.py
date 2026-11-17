"""
validate_ch04_02.py — Correcteur « Packing et UDIM » (CH04.02).
Usage : … --python-exit-code 1 --python validate_ch04_02.py -- --exercise udim [--render] [--debug]
PROP_Chest : tuile UDIM d'une UV = 1001 + ⌊u⌋ + 10·⌊v⌋.
  - au moins 2 tuiles utilisées ;
  - aucun îlot à cheval sur deux tuiles ;
  - une image UDIM (source TILED) est branchée dans le matériau et possède TOUTES les tuiles utilisées ;
  - dans chaque tuile : pas de chevauchement (≥ 98 %), occupation ≥ 40 %, étirement moyen ≤ 1,15, densité de texels uniforme (écart-type du log ≤ 0,20).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH04_01_UV_UNWRAP", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
import validate_ch04_01 as V1  # noqa: E402


def tile_number(u, v):
    return 1001 + int(math.floor(u - 1e-6)) + 10 * int(math.floor(v - 1e-6))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.02 — Packing et UDIM")
    ob = bpy.data.objects.get("PROP_Chest")
    if not r.check(ob is not None and ob.type == "MESH" and ob.data.uv_layers.active is not None, "PROP_Chest avec un calque UV", "Partez du fichier de départ.", 2):
        return r.finish()
    me = ob.data
    uv = me.uv_layers.active.data
    # îlots et tuiles
    isl = V1.count_islands  # noqa: F841
    from build_ch04_01_files import islands  # noqa: E402
    lab = islands(ob)
    straddle, tiles_of_isl = 0, {}
    for k in np.unique(lab):
        ts = set()
        for p in me.polygons:
            if lab[p.index] == k:
                for li in p.loop_indices:
                    ts.add(tile_number(*uv[li].uv))
        tiles_of_isl[int(k)] = ts
        if len(ts) > 1:
            straddle += 1
    used = sorted({t for ts in tiles_of_isl.values() for t in ts})
    r.check(len(used) >= 2, f"Tuiles UDIM utilisées : {used} (≥ 2)", "Déplacez le groupe du couvercle dans la tuile 1002 (G, X, 1).", 3)
    r.check(straddle == 0, f"{straddle} îlot(s) à cheval sur deux tuiles (0 exigé)", "Un îlot doit rester entier dans UNE tuile : déplacez-le d'un bloc.", 4)
    # image UDIM
    img, ok_img = None, False
    for m in ob.data.materials:
        if m and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image is not None and n.image.source == "TILED":
                    img = n.image
    have = sorted(t.number for t in img.tiles) if img else []
    ok_img = img is not None and all(t in have for t in used)
    r.check(img is not None, "Une image UDIM (source Tiled) est branchée dans le matériau", "Image Texture > Source : UDIM Tiles.", 3)
    r.check(ok_img, f"L'image possède toutes les tuiles utilisées (image : {have} ; UV : {used})", "Ajoutez les tuiles manquantes (Image > UDIM Tiles > Add Tile).", 3)
    # mesures par tuile
    P, U = V1.tri_data(ob)
    tri_tile = np.array([tile_number(*u[0]) for u in U])
    detail = []
    for t in used:
        sel = tri_tile == t
        if sel.sum() == 0:
            continue
        off = np.array([(t - 1001) % 10, (t - 1001) // 10], float)
        Ut = U[sel] - off
        area3, areau, stretch, dens, ok = V1.metrics(P[sel], Ut)
        w = area3[ok] / area3[ok].sum()
        sm = float(np.sum(w * stretch[ok]))
        ld = np.log(dens[ok])
        sd = float(np.sqrt(np.sum(w * (ld - np.sum(w * ld)) ** 2)))
        ov, cov = V1.overlap_ratio(Ut)
        detail.append((t, sm, sd, ov, cov, float(np.exp(np.sum(w * ld)))))
        r.check(ov >= 0.98, f"Tuile {t} : pas de chevauchement ({100 * ov:.1f} %)", "Pack Islands dans cette tuile.", 3)
        r.check(cov >= 0.40, f"Tuile {t} : occupation {100 * cov:.0f} % (≥ 40)", "Packez chaque groupe : il doit remplir son carré.", 2)
        r.check(sm <= 1.15, f"Tuile {t} : étirement moyen {sm:.2f} (≤ 1,15)", "Refaites l'Unwrap.", 2)
        r.check(sd <= 0.20, f"Tuile {t} : densité uniforme (écart-type du log {sd:.2f} ≤ 0,20)", "Average Islands Scale AVANT de packer.", 2)
    if debug:
        print("[DEBUG] tuiles", used, "îlots à cheval", straddle, "image", have)
        for d in detail:
            print(f"[DEBUG] tuile {d[0]} : stretch {d[1]:.3f} dens_std {d[2]:.3f} overlap {d[3]:.4f} coverage {d[4]:.3f} longueur3D/UV {d[5]:.3f}")
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
