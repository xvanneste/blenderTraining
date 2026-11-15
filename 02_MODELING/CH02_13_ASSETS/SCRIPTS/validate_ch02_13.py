"""
validate_ch02_13.py — Correcteur « La bibliothèque de props » (CH02.13).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_13.py --python-exit-code 1 -- --exercise library [--render]
Lit les métadonnées d'asset des objets et le fichier blender_assets.cats.txt situé À CÔTÉ du .blend.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def read_catalogs():
    folder = os.path.dirname(bpy.data.filepath)
    path = os.path.join(folder, "blender_assets.cats.txt")
    cats = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("VERSION"):
                continue
            parts = line.split(":")
            if len(parts) >= 2:
                cats[parts[0]] = parts[1]
    return path, cats


def main():
    r = L.Report("CH02.13 — La bibliothèque de props")
    assets = [o for o in bpy.data.objects if o.asset_data is not None]
    r.check(len(assets) >= 5, f"{len(assets)} objet(s) marqué(s) comme assets (≥ 5)", "Clic droit > Mark as Asset.", 3)
    path, cats = read_catalogs()
    r.check(len(cats) >= 2, f"Fichier de catalogues à côté du .blend : {len(cats)} catalogue(s) (≥ 2)",
            "Asset Browser > Current File > + (nouveau catalogue), puis enregistrez le fichier.", 2)
    if assets:
        in_cat = [o for o in assets if o.asset_data.catalog_id in cats]
        r.check(len(in_cat) == len(assets), f"Chaque asset rangé dans un catalogue ({len(in_cat)}/{len(assets)})",
                "Glissez chaque asset sur un catalogue dans l'Asset Browser.", 2)
        used = {o.asset_data.catalog_id for o in in_cat}
        r.check(len(used) >= 2, f"{len(used)} catalogue(s) utilisé(s) (≥ 2)", "Répartissez les props par type.", 1)
        desc = [o for o in assets if o.asset_data.description.strip()]
        r.check(len(desc) == len(assets), f"Descriptions renseignées ({len(desc)}/{len(assets)})",
                "Asset Browser, panneau N : Description.", 2)
        tagged = [o for o in assets if len(o.asset_data.tags) >= 2]
        r.check(len(tagged) == len(assets), f"Au moins 2 tags par asset ({len(tagged)}/{len(assets)})", "Panneau N : Tags, +.", 2)
        lic = [o for o in assets if o.asset_data.license.strip() and o.asset_data.author.strip()]
        r.check(len(lic) == len(assets), f"Auteur et licence renseignés ({len(lic)}/{len(assets)})",
                "Panneau N : Author, License (traçabilité, comme ASSET_MANIFEST.json).", 1)
        prev = [o for o in assets if o.preview is not None]
        r.check(len(prev) == len(assets), f"Aperçus présents ({len(prev)}/{len(assets)})",
                "Asset Browser, panneau N : icône ⟳ sous l'aperçu (Generate Preview).", 1, mandatory=False)
    names = {o.name for o in bpy.data.objects}
    r.check(all(n.startswith(("GEO_", "CAM_", "LGT_", "EMP_")) for n in names), "Nommage conforme (GEO_*, CAM_*, LGT_*…)",
            "Renommez avec les préfixes de CONVENTIONS.md.", 1, mandatory=False)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
