"""
build_ch02_13_files.py — « La bibliothèque de props » (CH02.13, assets réutilisables).

Réutilise les solutions des chapitres précédents (append) :
  tabouret (CH02.02), boîtier (CH02.05), vase (CH02.03), arbre (CH02.08), caisse et boîte (CH02.11).

  STARTER_FILES/ch02_13_library_starter.blend
      Les 6 props, alignés, SANS marquage d'asset ; aucun fichier de catalogues.
  COMPLETED_EXAMPLES/ch02_13_library_solution.blend + COMPLETED_EXAMPLES/blender_assets.cats.txt
      6 assets marqués : catalogue, description, auteur, licence, ≥ 2 tags, aperçu généré.
  COMPLETED_EXAMPLES/ch02_13_library_reference.png
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_13_files.py
Testé avec : Blender 5.3.0 (les .blend des chapitres CH02.02, 02.03, 02.05, 02.08, 02.11 doivent exister).
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
MOD = os.path.abspath(os.path.join(CH, ".."))
NOTE = """CH02.13 — LA BIBLIOTHÈQUE DE PROPS
Les 6 props de vos chapitres précédents sont dans ce fichier. Transformez-le en bibliothèque :
1. Workspace : ouvrez un éditeur Asset Browser (changez le type d'une zone).
2. Pour chaque prop : Object > Asset > Mark as Asset (ou clic droit dans l'Outliner).
3. Asset Browser, bibliothèque « Current File » : créez des catalogues (+) :
   Props/Mobilier, Props/Accessoires, Props/Nature ; glissez chaque asset dans son catalogue.
4. Panneau latéral de l'Asset Browser (N) : Description, Author, License, au moins 2 Tags.
5. Aperçus : panneau N de l'Asset Browser, icône ⟳ sous l'aperçu (Generate Preview).
6. Enregistrez : Blender écrit blender_assets.cats.txt à côté du fichier (catalogues).
Vérification : SCRIPTS/validate_ch02_13.py -- --exercise library
"""
SOURCES = [
    ("CH02_02_POLY_TOOLS_1/COMPLETED_EXAMPLES/ch02_02_stool_solution.blend", "GEO_Stool", "GEO_Stool", "Mobilier",
     "Tabouret en bois 40 × 40 × 48 cm, traverses, assise creusée.", ["bois", "assise", "intérieur"]),
    ("CH02_05_HARD_SURFACE/COMPLETED_EXAMPLES/ch02_05_device_solution.blend", "GEO_Device", "GEO_Device", "Accessoires",
     "Boîtier de commande 40 × 20 × 50 cm, coins arrondis, écran, 3 boutons.", ["hard surface", "électronique"]),
    ("CH02_03_POLY_TOOLS_2/COMPLETED_EXAMPLES/ch02_03_cutting_solution.blend", "GEO_Profile", "GEO_Vase", "Accessoires",
     "Petit vase tourné (Spin), 32 cm.", ["céramique", "décor"]),
    ("CH02_08_ORGANIC/COMPLETED_EXAMPLES/ch02_08_tree_solution.blend", "GEO_Tree", "GEO_Tree", "Nature",
     "Arbre stylisé (Skin + Subdivision), 2,75 m.", ["végétal", "extérieur"]),
    ("CH02_11_UV_BASICS/COMPLETED_EXAMPLES/ch02_11_uv_solution.blend", "GEO_Crate", "GEO_Crate", "Accessoires",
     "Caisse 60 cm, UV dépliées.", ["caisse", "rangement"]),
    ("CH02_11_UV_BASICS/COMPLETED_EXAMPLES/ch02_11_uv_solution.blend", "GEO_Can", "GEO_Can", "Accessoires",
     "Boîte de conserve Ø 40 cm, UV dépliées.", ["métal", "cuisine"]),
]
CATALOGS = {name: str(uuid.uuid5(uuid.NAMESPACE_URL, "bcma/props/" + name)) for name in ("Mobilier", "Accessoires", "Nature")}


def append_all():
    """Un seul chargement par fichier source : évite les doublons de matériaux (MAT_Checker.001)."""
    by_file = {}
    for path, src_name, *_ in SOURCES:
        by_file.setdefault(path, []).append(src_name)
    got = {}
    for path, names in by_file.items():
        with bpy.data.libraries.load(os.path.join(MOD, path), link=False) as (src, dst):
            dst.objects = list(names)
        for n, ob in zip(names, dst.objects):
            got[(path, n)] = ob
    return got


def build(sol):
    L.reset("SC_Library")
    L.studio(subject_height=1.4)
    col = L.collection("LIBRARY")
    x = -3.0
    objs = []
    got = append_all()
    for path, src_name, new_name, cat, desc, tags in SOURCES:
        ob = got[(path, src_name)]
        for m in list(ob.modifiers):            # dépendances vers des objets absents (cible, armature…)
            if m.type in ("SHRINKWRAP", "ARMATURE", "BOOLEAN"):
                ob.modifiers.remove(m)
        ob.parent = None
        ob.name = new_name
        col.objects.link(ob)
        ob.location = (x, 0, ob.location.z if new_name != "GEO_Vase" else 0)
        x += 1.2
        objs.append((ob, cat, desc, tags))
    if sol:
        for ob, cat, desc, tags in objs:
            ob.asset_mark()
            a = ob.asset_data
            a.description = desc
            a.author = "Blender Cinema Master Academy"
            a.license = "BCMA (usage personnel de formation)"
            a.catalog_id = CATALOGS[cat]
            for t in tags:
                a.tags.new(t)
            ob.asset_generate_preview()
    cam = L.obj("CAM_Main")
    cam.location = (0.0, -7.5, 2.6)
    cam.data.lens = 35
    L.obj("EMP_Target").location = (0, 0, 0.7)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def write_catalogs(folder):
    lines = ["# This is an Asset Catalog Definition file for Blender.", "#",
             "# Empty lines and lines starting with `#` will be ignored.",
             "# The first non-ignored line should be the version indicator.",
             '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"', "", "VERSION 1", ""]
    for name, uid in CATALOGS.items():
        lines.append(f"{uid}:Props/{name}:Props-{name}")
    with open(os.path.join(folder, "blender_assets.cats.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_13_library_starter.blend"))
    build(True)
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    p = L.save(os.path.join(out, "ch02_13_library_solution.blend"))
    write_catalogs(out)
    bpy.context.scene.render.filepath = os.path.join(out, "ch02_13_library_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
