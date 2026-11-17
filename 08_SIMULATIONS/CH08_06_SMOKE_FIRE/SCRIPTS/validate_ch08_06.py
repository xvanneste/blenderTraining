"""
validate_ch08_06.py — Correcteur « Fumée et feu » (CH08.06).
Usage : … --python-exit-code 1 --python validate_ch08_06.py -- --exercise smoke [--debug]
Objets : FLAME_Domain (boîte de 2 × 2 × 3 m) et FLAME_Source (petite boîte au fond).
  Configuration : domaine Fluid de type Gas, résolution de 24 à 64, cache modulaire de l'image 1 à au moins 30 ; matériau du domaine avec un Principled Volume relié à la sortie Volume du Material Output ;
                  source Fluid Flow de type Fire ou Fire + Smoke (BOTH), comportement Inflow.
  Bake des données (dossier temporaire ; le fichier n'est pas modifié) : au moins 30 fichiers de données ; taille de l'image 30 au moins 1,8 fois celle de l'image 1 (la grille grossit quand le foyer produit du gaz) ; taille de l'image 30 au moins 80 Ko.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def bake_sizes(dom):
    d = dom.modifiers["Fluid"].domain_settings
    tmp = tempfile.mkdtemp(prefix="bcma_gas_")
    d.cache_directory = tmp
    bpy.context.view_layer.objects.active = dom
    bpy.ops.fluid.bake_data()
    sizes = {}
    for r, _, ff in os.walk(tmp):
        for f in ff:
            if f.endswith(".vdb") and "fluid_data" in f:
                sizes[int(f.split("_")[-1].split(".")[0])] = os.path.getsize(os.path.join(r, f))
    return sizes


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.06 — Fumée et feu (domaine de gaz)")
    dom, src = bpy.data.objects.get("FLAME_Domain"), bpy.data.objects.get("FLAME_Source")
    if not r.check(dom is not None and src is not None, "FLAME_Domain et FLAME_Source présents", "Partez du fichier de départ.", 2):
        return r.finish()
    md = next((m for m in dom.modifiers if m.type == "FLUID" and m.fluid_type == "DOMAIN"), None)
    ms = next((m for m in src.modifiers if m.type == "FLUID" and m.fluid_type == "FLOW"), None)
    if not r.check(md is not None, "FLAME_Domain est un domaine de fluide", "Physics > Fluid > Domain.", 4):
        return r.finish()
    d = md.domain_settings
    r.check(d.domain_type == "GAS" and 24 <= d.resolution_max <= 64 and d.cache_type == "MODULAR" and d.cache_frame_start == 1 and d.cache_frame_end >= 30, f"Domaine : {d.domain_type}, résolution {d.resolution_max} (24–64), cache {d.cache_type} {d.cache_frame_start}–{d.cache_frame_end} (Modular, 1–30 ou plus)", "Gas, Resolution 32, cache Modular 1–30.", 7)
    fs = ms.flow_settings if ms else None
    r.check(fs is not None and fs.flow_type in ("FIRE", "BOTH") and fs.flow_behavior == "INFLOW", f"Foyer : {fs.flow_type + ' / ' + fs.flow_behavior if fs else 'pas un fluide'} (Fire ou Fire + Smoke, Inflow)", "Flow Type Fire + Smoke ; Flow Behavior Inflow.", 6)
    ok = False
    for mat in dom.data.materials:
        if mat and mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "OUTPUT_MATERIAL" and n.inputs["Volume"].links and n.inputs["Volume"].links[0].from_node.type == "PRINCIPLED_VOLUME":
                    ok = True
    r.check(ok, f"Shader de volume : Principled Volume relié à la sortie Volume du domaine : {'oui' if ok else 'non'}", "Matériau du domaine : Principled Volume > Volume.", 5)
    sizes = bake_sizes(dom)
    n = len(sizes)
    s1, s30 = sizes.get(1, 0), sizes.get(30, 0)
    r.check(n >= 30, f"Bake : {n} fichiers de données (≥ 30)", "Cache 1–30 en Modular.", 6)
    r.check(s1 > 0 and s30 >= 1.8 * s1 and s30 >= 80000, f"Taille du cache : {s1 / 1000:.0f} Ko à l'image 1, {s30 / 1000:.0f} Ko à l'image 30 (≥ 1,8 fois et ≥ 80 Ko)", "Source en Inflow, résolution 32 : la grille se remplit de gaz.", 8)
    if debug:
        print("[DEBUG] n", n, "s1", s1, "s30", s30, "ratio", round(s30 / max(s1, 1), 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
