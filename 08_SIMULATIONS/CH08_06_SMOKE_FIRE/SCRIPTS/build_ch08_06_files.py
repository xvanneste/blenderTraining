"""
build_ch08_06_files.py — « Fumée et feu » (CH08.06 : un domaine de gaz alimenté par un foyer, shader de volume).

Scène : FLAME_Domain (boîte de 2 × 2 × 3 m, z de 0 à 3 m) et FLAME_Source (boîte de 0,4 × 0,4 × 0,2 m posée au fond, centre à z = 0,3 m).
  Solution : FLAME_Domain : Fluid > Domain, Domain Type Gas, Resolution Divisions 32, cache modulaire images 1–30 ; matériau MAT_Flame avec un nœud Principled Volume (Density et Emission lus dans les attributs « density » et « flame », via un nœud Attribute)
             relié à la sortie Volume du Material Output ; FLAME_Source : Fluid > Flow, Flow Type Fire + Smoke (« BOTH »), Flow Behavior Inflow (alimentation continue). Plage 1–30.
  Le correcteur COTE le bake (données, dans un dossier temporaire) et mesure la taille des fichiers de cache par image (la grille grossit quand de la fumée est produite).
  Mesures de la solution : 30 fichiers de données ; taille de l'image 1 : 62 Ko environ, de l'image 30 : 145 Ko environ ; sans foyer : 16,7 Ko constants.
  STARTER_FILES/ch08_06_smoke_starter.blend : le domaine et la source comme maillages, sans physique ni matériau. COMPLETED_EXAMPLES/ch08_06_smoke_solution.blend (+ _reference.png : tailles du cache par image : solution, sans foyer)
  COUNTER_EXAMPLES/ : no_flow, smoke_only, low_res, short_cache, no_shader
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.06 — FUMÉE ET FEU (FLAME_Domain, FLAME_Source)
Un foyer posé au fond d'une boîte de 3 m doit produire flammes et fumée.
1. FLAME_Domain : Physics > Fluid > Type Domain ; Domain Type Gas ; Resolution Divisions 32 ; Cache : Type Modular, Frame Start 1, End 30.
2. FLAME_Source : Physics > Fluid > Type Flow ; Flow Type Fire + Smoke ; Flow Behavior Inflow.
3. Matériau du domaine : un Principled Volume relié à la sortie Volume (Density depuis l'attribut « density », Emission depuis l'attribut « flame »).
4. Plage 1–30. Le correcteur cuit lui-même les données (dossier temporaire) et mesure la taille du cache image par image.
Contrôles : domaine gaz modulaire 1–30 à résolution 24–64 ; foyer Fire ou Fire + Smoke en Inflow ; matériau de volume ; 30 fichiers ; taille du cache à l'image 30 au moins 1,8 fois celle de l'image 1.
Vérification : SCRIPTS/validate_ch08_06.py -- --exercise smoke
"""


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def volume_material(dom):
    mat = bpy.data.materials.new("MAT_Flame")
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    ad = nt.nodes.new("ShaderNodeAttribute")
    ad.attribute_name = "density"
    af = nt.nodes.new("ShaderNodeAttribute")
    af.attribute_name = "flame"
    nt.links.new(ad.outputs["Fac"], vol.inputs["Density"])
    nt.links.new(af.outputs["Fac"], vol.inputs["Emission Strength"])
    nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
    dom.data.materials.append(mat)


def build(kind):
    L.reset("SC_SMOKE")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 30
    dom = box("FLAME_Domain", (2, 2, 3), (0, 0, 1.5))
    src = box("FLAME_Source", (0.4, 0.4, 0.2), (0, 0, 0.3))
    if kind != "starter":
        bpy.context.view_layer.objects.active = dom
        dom.select_set(True)
        bpy.ops.object.modifier_add(type="FLUID")
        dom.modifiers["Fluid"].fluid_type = "DOMAIN"
        d = dom.modifiers["Fluid"].domain_settings
        d.domain_type = "GAS"
        d.resolution_max = 8 if kind == "low_res" else 32
        d.cache_type = "MODULAR"
        d.cache_frame_start, d.cache_frame_end = 1, (10 if kind == "short_cache" else 30)
        dom.select_set(False)
        if kind != "no_shader":
            volume_material(dom)
        if kind != "no_flow":
            bpy.context.view_layer.objects.active = src
            src.select_set(True)
            bpy.ops.object.modifier_add(type="FLUID")
            src.modifiers["Fluid"].fluid_type = "FLOW"
            fs = src.modifiers["Fluid"].flow_settings
            fs.flow_type = "SMOKE" if kind == "smoke_only" else "BOTH"
            fs.flow_behavior = "INFLOW"
            src.select_set(False)
    sc.frame_set(1)
    L.instructions(NOTE)
    return dom


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


def sketch(path):
    a = bake_sizes(build("solution"))
    b = bake_sizes(build("no_flow"))
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    top = max(max(a.values()), 1)
    for series, col in ((a, (0.9, 0.55, 0.2)), (b, (0.3, 0.7, 1.0))):
        for f, s in series.items():
            x, y = int(30 + (f - 1) / 29 * 720), int(270 - s / top * 240)
            img[y - 3:y + 4, x - 3:x + 4] = col
    img[270, 20:W - 20] = (0.3, 0.3, 0.3)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print(f"[gas] solution : {a[1]} -> {a[30]} octets ; sans foyer : {b[1]} -> {b[30]}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_06_smoke_starter.blend"))
    for k in ("no_flow", "smoke_only", "low_res", "short_cache", "no_shader"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_06_smoke_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_06_smoke_solution.blend"))
    sketch(os.path.join(out, "ch08_06_smoke_reference.png"))


if __name__ == "__main__":
    L.run(main)
