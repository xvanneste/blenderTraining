"""
validate_ch08_05.py — Correcteur « Fluides (Mantaflow) » (CH08.05).
Usage : … --python-exit-code 1 --python validate_ch08_05.py -- --exercise fluid [--debug]
Objets : FLUID_Domain (cube de 2 m centré à z = 1) et FLUID_Source (cube de 0,6 m à z = 1,2).
  Configuration : FLUID_Domain : Fluid Domain, type Liquid, Resolution Divisions de 24 à 64, cache de l'image 1 à au moins 18, maillage activé ; FLUID_Source : Fluid Flow, type Liquid, comportement Geometry (ou Inflow).
  Bake (données puis maillage, dans un dossier temporaire ; le fichier n'est pas modifié) puis lecture des maillages du liquide (repère local du domaine, z de −0,5 à +0,5) :
    au moins 18 maillages ; image 1 : liquide non vide, z maximal ≤ 0,5 et z minimal ≥ −0,15 (dans la région de la source) ;
    image 20 (ou la dernière) : z minimal ≤ −0,40 (le liquide est tombé sur le fond), largeur en X d'au moins 0,7 m (il s'est étalé), au moins 3 fois plus de sommets qu'à l'image 1.
Testé avec : Blender 5.3.0.
"""
import gzip
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def bake_meshes(dom):
    d = dom.modifiers["Fluid"].domain_settings
    tmp = tempfile.mkdtemp(prefix="bcma_fluid_")
    d.cache_directory = tmp
    bpy.context.view_layer.objects.active = dom
    bpy.ops.fluid.bake_data()
    bpy.ops.fluid.bake_mesh()
    out = []
    for q in sorted(os.path.join(r, f) for r, _, ff in os.walk(tmp) for f in ff if f.endswith(".bobj.gz")):
        raw = gzip.open(q).read()
        n = struct.unpack("<i", raw[:4])[0]
        if n == 0:
            out.append((0.0, 0.0, 0.0, 0.0, 0))
            continue
        v = struct.unpack("<%df" % (3 * n), raw[4:4 + 12 * n])
        out.append((min(v[2::3]), max(v[2::3]), min(v[0::3]), max(v[0::3]), n))
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.05 — Fluides (liquide qui tombe)")
    dom, src = bpy.data.objects.get("FLUID_Domain"), bpy.data.objects.get("FLUID_Source")
    if not r.check(dom is not None and src is not None, "FLUID_Domain et FLUID_Source présents", "Partez du fichier de départ.", 2):
        return r.finish()
    md = next((m for m in dom.modifiers if m.type == "FLUID" and m.fluid_type == "DOMAIN"), None)
    ms = next((m for m in src.modifiers if m.type == "FLUID" and m.fluid_type == "FLOW"), None)
    if not r.check(md is not None, "FLUID_Domain est un domaine de fluide", "Physics > Fluid > Domain.", 4):
        return r.finish()
    d = md.domain_settings
    r.check(d.domain_type == "LIQUID" and 24 <= d.resolution_max <= 64 and d.cache_frame_start == 1 and d.cache_frame_end >= 18 and d.use_mesh, f"Domaine : {d.domain_type}, résolution {d.resolution_max} (24–64), cache {d.cache_frame_start}–{d.cache_frame_end} (1–18 ou plus), maillage {'activé' if d.use_mesh else 'désactivé'}", "Liquid, Resolution 32, cache 1–20, Mesh coché.", 7)
    okf = ms is not None and ms.flow_settings.flow_type == "LIQUID" and ms.flow_settings.flow_behavior in ("GEOMETRY", "INFLOW")
    r.check(okf, f"Source : {'Flow ' + ms.flow_settings.flow_type + ' / ' + ms.flow_settings.flow_behavior if ms else 'pas un fluide'} (Flow, Liquid, Geometry ou Inflow)", "Fluid > Flow ; Flow Type Liquid.", 6)
    res = bake_meshes(dom)
    n = len(res)
    r.check(n >= 18 and res[0][4] > 0, f"Bake : {n} maillages (≥ 18), liquide présent à l'image 1 : {'oui' if n and res[0][4] > 0 else 'non'}", "Source Flow liquide dans le domaine ; cache 1–20.", 6)
    if n < 2 or res[0][4] == 0:
        return r.finish()
    first, last = res[0], res[-1]
    r.check(first[1] <= 0.5 and first[0] >= -0.15, f"Image 1 : liquide de z = {first[0]:.2f} à {first[1]:.2f} m (dans la source : −0,15 à 0,5)", "Flow Behavior Geometry, source au milieu du domaine.", 4)
    r.check(last[0] <= -0.40, f"Image {n} : le liquide est tombé : z minimal {last[0]:.2f} m (≤ −0,40)", "Gravité du domaine active.", 6)
    r.check(last[3] - last[2] >= 0.7, f"Image {n} : le liquide s'est étalé : largeur {last[3] - last[2]:.2f} m (≥ 0,7)", "Résolution suffisante.", 4)
    r.check(last[4] >= 3 * first[4], f"Image {n} : {last[4]} sommets, {first[4]} à l'image 1 (≥ 3 fois plus)", "Le liquide éclabousse : maillage plus riche.", 4)
    if debug:
        print("[DEBUG] n", n, "first", [round(x, 3) for x in first], "last", [round(x, 3) for x in last])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
