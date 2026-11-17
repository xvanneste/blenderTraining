"""
validate_p3.py — Correcteur du projet P3 « Le personnage complet » (sculpt → retopologie → UV → bake → matériau).
Usage : blender -b --factory-startup <p3_character_<prenom>.blend> --python-exit-code 1 --python validate_p3.py [-- --debug]
Objets : HIGH_<Nom> (sculpt haute définition) et CHR_<Nom>_Body (retopologie, avec UV). Planche : renders/p3_turnaround.png à côté du .blend.
  Sculpt    : HIGH_<Nom> ≥ 20 000 faces, caché au rendu.
  Retopo    : CHR_<Nom>_Body 2 000–10 000 faces, ≥ 90 % de quads ; données ME_CHR_<Nom>_Body ; maillage fermé ; ≥ 5 fois moins de faces que HIGH ;
              adhérence au sculpt : distance moyenne des sommets à HIGH ≤ 1,5 cm, 95ᵉ centile ≤ 4 cm ; normales vers l'extérieur.
  Rig-ready : transformations appliquées (échelle 1, rotation 0) ; taille 1,55–1,95 m ; pieds au sol (±1 cm) ; origine en (0, 0, 0) ± 5 cm en XY ; Z haut.
  UV        : un calque UV ; étirement moyen ≤ 1,35 ; chevauchement ≥ 98 % ; occupation ≥ 35 % ; tout dans [0,1]².
  Bake      : image T_<Nom>_N Non-Color, empaquetée, branchée Image -> Normal Map (Tangent) -> Normal de MAT_CHR_<Nom> ; relief dans ≥ 5 % des pixels des îlots ;
              normales valides (longueur moyenne 0,9–1,1).
  Matériau  : Subsurface Weight ≥ 0,5, Radius R > V > B, Base Color chair (R > V > B).
  Rendu     : renders/p3_turnaround.png ≥ 1600 px, non noire.
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "04_MATERIALS", "CH04_01_UV_UNWRAP", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "04_MATERIALS", "CH04_07_BAKING", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
import validate_ch04_01 as V1  # noqa: E402
import validate_ch04_07 as V7  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def main():
    debug = L.flag("--debug")
    r = L.Report("Projet P3 — Le personnage complet")
    hi = next((o for o in bpy.data.objects if re.match(r"^HIGH_[A-Za-z0-9]+$", o.name) and o.type == "MESH"), None)
    lo = next((o for o in bpy.data.objects if re.match(r"^CHR_[A-Za-z0-9]+_Body$", o.name) and o.type == "MESH"), None)
    if not r.check(hi is not None and lo is not None, "Objets HIGH_<Nom> et CHR_<Nom>_Body présents", "Nommage : HIGH_Hero (sculpt) et CHR_Hero_Body (retopo).", 6):
        return r.finish()
    nom = lo.name.split("_")[1]
    r.check(hi.name == f"HIGH_{nom}", f"Mêmes <Nom> pour HIGH et CHR ({hi.name}, {lo.name})", "", 1)
    r.check(lo.data.name == f"ME_CHR_{nom}_Body", f"Données nommées ME_CHR_{nom}_Body (actuel : {lo.data.name})", "Renommez les données du maillage.", 1)
    nh, nl = len(hi.data.polygons), len(lo.data.polygons)
    r.check(nh >= 20000, f"Sculpt : {nh} faces (≥ 20 000)", "Le sculpt doit porter du détail.", 3)
    r.check(hi.hide_render, "HIGH caché au rendu", "Icône caméra de l'Outliner.", 1)
    quads = sum(1 for p in lo.data.polygons if len(p.vertices) == 4)
    r.check(2000 <= nl <= 10000, f"Retopo : {nl} faces (2 000–10 000)", "Un corps animable : quelques milliers de faces.", 3)
    r.check(nl > 0 and quads / nl >= 0.90, f"Retopo : {100 * quads / max(nl, 1):.0f} % de quads (≥ 90)", "Retopologie en quads (Quadriflow, Poly Build…).", 3)
    r.check(nh >= 5 * nl, f"HIGH ≥ 5 × LOW ({nh} / {nl})", "Le basse définition doit être bien plus léger.", 1)
    bm = bmesh.new()
    bm.from_mesh(lo.data)
    bound = sum(1 for e in bm.edges if len(e.link_faces) != 2)
    bm.free()
    r.check(bound == 0, f"Maillage fermé ({bound} arête(s) non manifold)", "Pas de trous ni d'arêtes ouvertes.", 2)
    # Adhérence au sculpt (coordonnées monde)
    dg = bpy.context.evaluated_depsgraph_get()
    hv = [hi.matrix_world @ v.co for v in hi.data.vertices]
    bvh = BVHTree.FromPolygons(hv, [tuple(p.vertices) for p in hi.data.polygons])
    d, outward = [], 0
    for v in lo.data.vertices:
        pw = lo.matrix_world @ v.co
        loc, nrm, idx, dist = bvh.find_nearest(pw)
        if loc is None:
            continue
        d.append(dist)
        if (pw - loc).dot(nrm) >= -1e-4 or dist < 0.003:
            outward += 1
    d = np.array(d)
    mean_d, p95 = float(d.mean()) if len(d) else 9.0, float(np.percentile(d, 95)) if len(d) else 9.0
    r.check(mean_d <= 0.015 and p95 <= 0.04, f"Adhérence au sculpt : moyenne {100 * mean_d:.2f} cm (≤ 1,5), 95ᵉ centile {100 * p95:.2f} cm (≤ 4)", "Le basse définition doit suivre le sculpt (Shrinkwrap, snapping).", 4)
    # Rig-ready
    sc_ok = all(abs(s - 1) < 1e-4 for s in lo.scale) and all(abs(a) < 1e-4 for a in lo.rotation_euler)
    r.check(sc_ok, f"Transformations appliquées (échelle {tuple(round(s, 3) for s in lo.scale)})", "Object > Apply > All Transforms.", 2)
    zs = [(lo.matrix_world @ v.co).z for v in lo.data.vertices]
    xs = [(lo.matrix_world @ v.co).x for v in lo.data.vertices]
    h = max(zs) - min(zs)
    r.check(1.55 <= h <= 1.95, f"Taille {h:.2f} m (1,55–1,95)", "Échelle réelle d'un adulte.", 2)
    r.check(abs(min(zs)) <= 0.01, f"Pieds au sol (z min {min(zs):+.3f} m)", "Pieds sur z = 0.", 2)
    ox, oy, oz = lo.matrix_world.translation
    r.check(abs(ox) <= 0.05 and abs(oy) <= 0.05 and abs(oz) <= 0.05, f"Origine en (0, 0, 0) : ({ox:+.2f}, {oy:+.2f}, {oz:+.2f})", "Set Origin vers le curseur 3D à l'origine.", 2)
    # UV
    if not r.check(lo.data.uv_layers.active is not None, "UV présents sur le basse définition", "UV > Smart UV Project, puis Pack Islands.", 4):
        return r.finish()
    P, U = V1.tri_data(lo)
    area3, areau, stretch, dens, ok = V1.metrics(P, U)
    w = area3[ok] / area3[ok].sum()
    sm = float(np.sum(w * stretch[ok]))
    ov, cov = V1.overlap_ratio(U)
    inside = float(np.mean((U >= -1e-4).all(axis=(1, 2)) & (U <= 1 + 1e-4).all(axis=(1, 2))))
    r.check(sm <= 1.35, f"UV : étirement moyen {sm:.2f} (≤ 1,35)", "Plus de coutures ou un autre dépliage.", 3)
    r.check(ov >= 0.98, f"UV : sans chevauchement ({100 * ov:.1f} %)", "Pack Islands.", 3)
    r.check(cov >= 0.35, f"UV : occupation {100 * cov:.0f} % (≥ 35)", "Pack Islands avec Scale.", 2)
    r.check(inside >= 0.99, f"UV : {100 * inside:.0f} % des triangles dans [0,1]²", "Tout dans le carré (hors UDIM).", 2)
    # Bake
    img = bpy.data.images.get(f"T_{nom}_N")
    mat = lo.active_material
    r.check(img is not None, f"Image T_{nom}_N présente", "Créez l'image cible du bake.", 3)
    if img is not None:
        r.check(img.colorspace_settings.name == "Non-Color", f"T_{nom}_N : {img.colorspace_settings.name} (Non-Color)", "Normal map : Non-Color.", 2)
        r.check(img.packed_file is not None, "Image empaquetée", "Image > Pack.", 2)
        chain = False
        if mat and mat.node_tree:
            b = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
            for l in mat.node_tree.links:
                if b is not None and l.to_node == b and l.to_socket.name == "Normal" and l.from_node.type == "NORMAL_MAP" and l.from_node.space == "TANGENT":
                    chain = any(k.from_node.type == "TEX_IMAGE" and k.from_node.image == img for k in l.from_node.inputs["Color"].links)
        r.check(chain, "Image -> Normal Map (Tangent) -> Normal du matériau", "Branchez la normal map.", 3)
        W_, H_ = img.size
        px = np.array(img.pixels[:], np.float32).reshape(H_, W_, 4)[..., :3]
        mask = V7.uv_mask(lo, W_)
        sel = px[mask]
        dev = np.abs(sel - np.array([0.5, 0.5, 1.0])).max(axis=1)
        relief = float((dev > 0.02).mean()) if len(sel) else 0.0
        nn = sel * 2 - 1
        ln = float(np.linalg.norm(nn, axis=1).mean()) if len(sel) else 0.0
        r.check(relief >= 0.05, f"Bake : relief sur {100 * relief:.0f} % des pixels des îlots (≥ 5)", "Bakez HIGH sur LOW (Selected to Active).", 3)
        r.check(0.9 <= ln <= 1.1, f"Normales valides (longueur moyenne {ln:.2f})", "Bake Normal, espace Tangent.", 2)
    # Matériau
    b = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if mat and mat.node_tree else None
    if b is not None:
        rad = tuple(b.inputs["Subsurface Radius"].default_value)
        c = b.inputs["Base Color"].default_value
        r.check(b.inputs["Subsurface Weight"].default_value >= 0.5 and rad[0] > rad[1] > rad[2] and c[0] > c[1] > c[2], f"Peau : Subsurface {b.inputs['Subsurface Weight'].default_value:.2f}, rayon {tuple(round(v, 2) for v in rad)}, Base Color R > V > B", "Voir CH04.10.", 3)
    else:
        r.check(False, "Matériau avec un Principled BSDF", "MAT_CHR_<Nom>.", 3)
    # Planche
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p3_turnaround.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        pxs = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        ok_img = W >= 1600 and pxs.mean() > 0.05 and pxs.std() > 0.05
        msg = f"{W} × {H}, moyenne {pxs.mean():.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche renders/p3_turnaround.png : {msg}", "Quatre vues (face, trois-quarts, profil, dos), ≥ 1600 px de large.", 3)
    if debug:
        print("[DEBUG]", "faces", nh, nl, "quads", quads, "adh", round(mean_d, 4), round(p95, 4), "stretch", round(sm, 3), "ov", round(ov, 3), "cov", round(cov, 3), "inside", round(inside, 3), "relief", round(relief, 3) if img else None, "h", round(h, 3), "zmin", round(min(zs), 4))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
