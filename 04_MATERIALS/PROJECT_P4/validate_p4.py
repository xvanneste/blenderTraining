"""
validate_p4.py — Correcteur du projet P4 « La bibliothèque de matériaux ».
Usage : blender -b --factory-startup <p4_materials.blend> --python-exit-code 1 --python validate_p4.py [-- --debug]
Le fichier .blend est accompagné de blender_assets.cats.txt (même dossier) et de renders/p4_contact_sheet.png.
Contrôles (tous obligatoires sauf mention) :
  Assets   : ≥ 25 matériaux marqués asset ; noms MAT_<Catégorie>_<Nom> uniques ; description non vide ; ≥ 2 tags ; auteur et licence ;
             catalogue présent dans blender_assets.cats.txt ; ≥ 5 catégories de ≥ 3 matériaux ; aperçus (non obligatoire).
  Matériau : Principled BSDF relié à Surface ; aucun nœud orphelin ; ≤ 30 nœuds ; aucune image (bibliothèque autonome, procédurale) ;
             Metallic non relié ∈ [0 ; 0,05] ∪ [0,9 ; 1] ; Base Color non reliée : métal ≥ 0,4 de luminance, diélectrique opaque 0,02–0,9.
  Variété  : ≥ 15 matériaux dont Base Color, Roughness ou Normal est piloté par une texture ; ≥ 20 signatures (couleur, rugosité, métal) distinctes ;
             verres (catégorie Glass) : Transmission Weight ≥ 0,9.
  Rendu    : renders/p4_contact_sheet.png d'au moins 1600 px de large, non noir et contrasté.
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def has_tex_upstream(sock, seen=None):
    seen = set() if seen is None else seen
    for l in sock.links:
        n = l.from_node
        if n.name in seen:
            continue
        seen.add(n.name)
        if n.type.startswith("TEX_"):
            return True
        if any(has_tex_upstream(i, seen) for i in n.inputs):
            return True
    return False


def read_catalogs():
    folder = os.path.dirname(bpy.data.filepath)
    path = os.path.join(folder, "blender_assets.cats.txt")
    cats = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("VERSION"):
                p = line.split(":")
                if len(p) >= 2:
                    cats[p[0]] = p[1]
    return cats


def main():
    debug = L.flag("--debug")
    r = L.Report("Projet P4 — La bibliothèque de matériaux")
    mats = [m for m in bpy.data.materials if m.asset_data is not None]
    r.check(len(mats) >= 25, f"{len(mats)} matériaux marqués asset (≥ 25)", "Clic droit sur le matériau > Mark as Asset.", 6)
    pat = re.compile(r"^MAT_([A-Za-z]+)_([A-Za-z0-9]+)$")
    bad_names = [m.name for m in mats if not pat.match(m.name)]
    r.check(not bad_names, f"Nommage MAT_<Catégorie>_<Nom> ({len(bad_names)} hors norme : {bad_names[:4]})", "Ex. MAT_Metal_Gold.", 3)
    cats_of = {}
    for m in mats:
        mm = pat.match(m.name)
        if mm:
            cats_of.setdefault(mm.group(1), []).append(m)
    big = {c: len(v) for c, v in cats_of.items() if len(v) >= 3}
    r.check(len(big) >= 5, f"{len(big)} catégories de ≥ 3 matériaux ({big})", "Au moins 5 familles de 3 matériaux.", 4)
    r.check(all((m.asset_data.description or "").strip() for m in mats), "Chaque asset a une description", "Panneau d'asset : Description.", 3)
    r.check(all(len(m.asset_data.tags) >= 2 for m in mats), "Chaque asset a au moins 2 tags", "Panneau d'asset : Tags.", 3)
    r.check(all((m.asset_data.author or "").strip() and (m.asset_data.license or "").strip() for m in mats), "Auteur et licence renseignés", "Panneau d'asset : Author, License.", 2)
    cats = read_catalogs()
    r.check(len(cats) >= 5, f"Fichier de catalogues : {len(cats)} catalogue(s) (≥ 5)", "Asset Browser : créer les catalogues puis enregistrer.", 3)
    r.check(all(m.asset_data.catalog_id in cats for m in mats), "Chaque asset est rangé dans un catalogue existant", "Glissez chaque matériau sur son catalogue.", 3)
    r.check(all(m.preview is not None for m in mats), "Aperçus présents", "Panneau d'asset : générer l'aperçu.", 1, mandatory=False)
    # Contrôles par matériau
    problems = {"principled": [], "orphan": [], "size": [], "image": [], "metal": [], "albedo": [], "glass": []}
    textured, sigs = 0, set()
    for m in mats:
        nt = m.node_tree
        if nt is None:
            problems["principled"].append(m.name)
            continue
        out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
        b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        ok = out is not None and b is not None and any(l.from_node == b and l.to_node == out and l.to_socket.name == "Surface" for l in nt.links)
        if not ok:
            problems["principled"].append(m.name)
            continue
        if any(n.type not in ("OUTPUT_MATERIAL", "FRAME") and not any(o.links for o in n.outputs) for n in nt.nodes):
            problems["orphan"].append(m.name)
        if len([n for n in nt.nodes if n.type != "FRAME"]) > 30:
            problems["size"].append(m.name)
        if any(n.type == "TEX_IMAGE" for n in nt.nodes):
            problems["image"].append(m.name)
        gi = lambda k: b.inputs[k]  # noqa: E731
        met = gi("Metallic")
        mv = 1.0 if met.links else met.default_value
        if not met.links and not (mv <= 0.05 or mv >= 0.9):
            problems["metal"].append(m.name)
        bc = gi("Base Color")
        trans = gi("Transmission Weight").default_value
        if not bc.links:
            L_ = lum(bc.default_value)
            if mv >= 0.9 and L_ < 0.4:
                problems["albedo"].append(m.name)
            if mv <= 0.05 and trans < 0.9 and not (0.02 <= L_ <= 0.9):
                problems["albedo"].append(m.name)
        mm = pat.match(m.name)
        if mm and mm.group(1) == "Glass" and trans < 0.9:
            problems["glass"].append(m.name)
        if any(has_tex_upstream(gi(k)) for k in ("Base Color", "Roughness", "Normal")):
            textured += 1
        bcv = tuple(round(v, 1) for v in bc.default_value[:3]) if not bc.links else "tex"
        rv = round(gi("Roughness").default_value, 1) if not gi("Roughness").links else "tex"
        sigs.add((bcv, rv, round(mv, 1), m.name.split("_")[1] if mm else ""))
    r.check(not problems["principled"], f"Principled BSDF relié à Surface ({problems['principled'] or 'tous OK'})", "Chaque matériau : Principled -> Material Output.", 4)
    r.check(not problems["orphan"], f"Aucun nœud orphelin ({problems['orphan'] or 'aucun'})", "Supprimez les nœuds inutilisés.", 3)
    r.check(not problems["size"], f"Graphes de ≤ 30 nœuds ({problems['size'] or 'tous OK'})", "Simplifiez ou groupez.", 1)
    r.check(not problems["image"], f"Bibliothèque autonome : aucune image ({problems['image'] or 'aucune'})", "Procédural uniquement dans ce projet.", 3)
    r.check(not problems["metal"], f"Metallic proche de 0 ou 1 ({problems['metal'] or 'tous OK'})", "Binaire : 0 ou 1.", 3)
    r.check(not problems["albedo"], f"Albedos plausibles ({problems['albedo'] or 'tous OK'})", "Métal ≥ 0,4 ; diélectrique 0,02–0,9.", 3)
    r.check(not problems["glass"], f"Verres transmissifs ({problems['glass'] or 'tous OK'})", "Transmission Weight 1.", 2)
    r.check(textured >= 15, f"{textured} matériaux pilotés par une texture (≥ 15)", "Au moins 15 matériaux avec une variation.", 4)
    r.check(len(sigs) >= 20, f"{len(sigs)} signatures distinctes (≥ 20)", "Évitez les doublons.", 3)
    # Planche contact
    folder = os.path.dirname(bpy.data.filepath)
    sheet = os.path.join(folder, "renders", "p4_contact_sheet.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        mean, std = float(px.mean()), float(px.std())
        ok_img = W >= 1600 and mean > 0.05 and std > 0.05
        msg = f"{W} × {H}, moyenne {mean:.2f}, écart-type {std:.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche contact renders/p4_contact_sheet.png : {msg}", "Grille de sphères, ≥ 1600 px de large, non noire.", 4)
    if debug:
        print("[DEBUG]", {k: v for k, v in problems.items() if v}, "textured", textured, "sigs", len(sigs), "cats", len(cats))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
