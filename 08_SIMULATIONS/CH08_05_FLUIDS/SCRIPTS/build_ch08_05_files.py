"""
build_ch08_05_files.py — « Fluides (Mantaflow) » (CH08.05 : un cube de liquide qui tombe dans un domaine et s'étale).

Scène : FLUID_Domain (cube de 2 m de côté centré à z = 1 m) et FLUID_Source (cube de 0,6 m centré à z = 1,2 m, au milieu du domaine).
  Solution : FLUID_Domain : Fluid > Type Domain, Domain Type Liquid, Resolution Divisions 32, cache modulaire, images 1–20, maillage (Mesh) activé ;
             FLUID_Source : Fluid > Type Flow, Flow Type Liquid, Flow Behavior Geometry (le liquide remplit le volume de l'objet à l'image 1). Plage 1–20.
  Le correcteur COTE le bake (données puis maillage, en arrière-plan, dans un dossier temporaire) et lit les maillages du liquide (fichiers .bobj.gz).
  Mesures de la solution : 20 maillages ; image 1 : liquide de z −0,06 à 0,27 m (repère local du domaine) ; image 20 : z de −0,475 à −0,006 m, x de −0,475 à 0,475 m (étalé sur le fond), 18 594 sommets (3 066 à l'image 1).
  STARTER_FILES/ch08_05_fluid_starter.blend : le domaine et la source comme maillages, sans physique. COMPLETED_EXAMPLES/ch08_05_fluid_solution.blend (+ _reference.png : profil du liquide aux images 1, 10 et 20, lu dans le cache)
  COUNTER_EXAMPLES/ : no_flow, gas_flow, low_res, short_cache
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_05_files.py
Testé avec : Blender 5.3.0.
"""
import gzip
import os
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.05 — FLUIDES (FLUID_Domain, FLUID_Source)
Un cube de liquide de 0,6 m, suspendu à 1,2 m dans un domaine de 2 m, doit tomber et s'étaler sur le fond.
1. FLUID_Domain : Physics > Fluid > Type Domain ; Domain Type Liquid ; Resolution Divisions 32 ; Cache : Type Modular, Frame Start 1, End 20 ; Mesh : coché.
2. FLUID_Source : Physics > Fluid > Type Flow ; Flow Type Liquid ; Flow Behavior Geometry.
3. Plage 1–20. (Le correcteur bake lui-même, dans un dossier temporaire : vous n'avez pas à cuire dans ce chapitre ; CH08.10 traite les caches.)
Mesures : 18 maillages au moins ; liquide dans la source à l'image 1 ; image 20 : liquide tombé sur le fond (z ≤ −0,40 local) et étalé (largeur ≥ 0,7 m) ; au moins 3 fois plus de sommets qu'à l'image 1.
Vérification : SCRIPTS/validate_ch08_05.py -- --exercise fluid
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


def build(kind):
    L.reset("SC_FLUID")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 20
    dom = box("FLUID_Domain", (2, 2, 2), (0, 0, 1))
    src = box("FLUID_Source", (0.6, 0.6, 0.6), (0, 0, 1.2))
    if kind != "starter":
        bpy.context.view_layer.objects.active = dom
        dom.select_set(True)
        bpy.ops.object.modifier_add(type="FLUID")
        dom.modifiers["Fluid"].fluid_type = "DOMAIN"
        d = dom.modifiers["Fluid"].domain_settings
        d.domain_type = "LIQUID"
        d.resolution_max = 8 if kind == "low_res" else 32
        d.cache_type = "MODULAR"
        d.cache_frame_start, d.cache_frame_end = 1, (5 if kind == "short_cache" else 20)
        d.use_mesh = True
        dom.select_set(False)
        if kind != "no_flow":
            bpy.context.view_layer.objects.active = src
            src.select_set(True)
            bpy.ops.object.modifier_add(type="FLUID")
            src.modifiers["Fluid"].fluid_type = "FLOW"
            fs = src.modifiers["Fluid"].flow_settings
            fs.flow_type = "SMOKE" if kind == "gas_flow" else "LIQUID"
            fs.flow_behavior = "GEOMETRY"
            src.select_set(False)
    sc.frame_set(1)
    L.instructions(NOTE)
    return dom


def bake_meshes(dom):
    """Cuit données puis maillage dans un dossier temporaire ; renvoie la liste (image, z min, z max, x min, x max, nombre de sommets)."""
    d = dom.modifiers["Fluid"].domain_settings
    tmp = tempfile.mkdtemp(prefix="bcma_fluid_")
    d.cache_directory = tmp
    bpy.context.view_layer.objects.active = dom
    bpy.ops.fluid.bake_data()
    bpy.ops.fluid.bake_mesh()
    out = []
    files = sorted(os.path.join(r, f) for r, _, ff in os.walk(tmp) for f in ff if f.endswith(".bobj.gz"))
    for q in files:
        raw = gzip.open(q).read()
        n = struct.unpack("<i", raw[:4])[0]
        if n == 0:
            out.append((len(out) + 1, 0.0, 0.0, 0.0, 0.0, 0))
            continue
        v = struct.unpack("<%df" % (3 * n), raw[4:4 + 12 * n])
        out.append((len(out) + 1, min(v[2::3]), max(v[2::3]), min(v[0::3]), max(v[0::3]), n))
    return out


def sketch(path):
    dom = build("solution")
    res = bake_meshes(dom)
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    for panel, i in enumerate((0, 9, 19)):
        f, zmin, zmax, xmin, xmax, n = res[i]
        x0, x1 = int(panel * 260 + 130 + xmin * 100), int(panel * 260 + 130 + xmax * 100)
        y0, y1 = int(150 - zmax * 100), int(150 - zmin * 100)
        img[y0:y1, x0:x1] = (0.3, 0.6, 0.9)
        img[200:204, panel * 260 + 30:panel * 260 + 230] = (0.3, 0.3, 0.3)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_05_fluid_starter.blend"))
    for k in ("no_flow", "gas_flow", "low_res", "short_cache"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_05_fluid_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_05_fluid_solution.blend"))
    sketch(os.path.join(out, "ch08_05_fluid_reference.png"))


if __name__ == "__main__":
    L.run(main)
