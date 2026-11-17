"""
build_ch04_08_files.py — « Relief : bump, normal map, displacement » (CH04.08).

Un sol PROP_Ground (plan 6 x 6 m) et un matériau MAT_Ground : relief de terrain par VRAI displacement (Cycles) :
  Texture Coordinate [Object] -> Noise Texture [Fac] -> Displacement [Height] (Scale 0,25 m ; Midlevel 0,5) -> Material Output [Displacement]
  Material > Settings > Displacement : « Displacement Only » (displacement_method = 'DISPLACEMENT') ;
  Subdivision Surface adaptive (Cycles) ; moteur Cycles.
  STARTER_FILES/ch04_08_relief_starter.blend : plan avec un Principled seul, moteur EEVEE.
  COMPLETED_EXAMPLES/ch04_08_relief_solution.blend (+ _reference.png : deux vues, Cycles)
  COUNTER_EXAMPLES/ : method_bump, no_subdiv, huge_scale, const_height, unlinked, eevee
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_08_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH04.08 — RELIEF (PROP_Ground, matériau MAT_Ground) : vrai displacement avec Cycles
1. Render Properties : moteur Cycles.
2. Matériau : Texture Coordinate [Object] -> Noise Texture [Fac] -> Displacement [Height] ; Scale entre 0,02 et 0,3 m (relief de quelques dizaines de cm) ;
   Displacement [Displacement] -> Material Output [Displacement].
3. Material Properties > Settings : Displacement = « Displacement Only » (ou « Displacement and Bump »).
4. Le plan n'a qu'une face : ajouter un modificateur Subdivision Surface en mode adaptatif (Adaptive Subdivision, Cycles) ou, à défaut, Render >= 6 niveaux.
Vérification : SCRIPTS/validate_ch04_08.py -- --exercise relief
"""


def make_ground(kind):
    bpy.ops.mesh.primitive_plane_add(size=6.0, location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = "PROP_Ground"
    mat = bpy.data.materials.new("MAT_Ground")
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.35, 0.28, 0.20, 1.0)
    b.inputs["Roughness"].default_value = 0.9
    ob.data.materials.append(mat)
    if kind == "starter":
        return ob, mat
    nt = mat.node_tree
    N, lk = nt.nodes, nt.links.new
    tc = N.new("ShaderNodeTexCoord"); tc.location = (-800, -300)
    nz = N.new("ShaderNodeTexNoise"); nz.location = (-550, -300)
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 4.0
    nz.inputs["Roughness"].default_value = 0.55
    ds = N.new("ShaderNodeDisplacement"); ds.location = (-250, -300)
    ds.inputs["Midlevel"].default_value = 0.5
    ds.inputs["Scale"].default_value = 3.0 if kind == "huge_scale" else 0.25
    lk(tc.outputs["Object"], nz.inputs["Vector"])
    if kind != "const_height":
        lk(nz.outputs["Fac"], ds.inputs["Height"])
    if kind != "unlinked":
        lk(ds.outputs["Displacement"], N["Material Output"].inputs["Displacement"])
    mat.displacement_method = "BUMP" if kind == "method_bump" else "DISPLACEMENT"
    if kind != "no_subdiv":
        md = ob.modifiers.new("Subdivision", "SUBSURF")
        md.subdivision_type = "SIMPLE"
        md.levels = 2
        md.render_levels = 2
        md.use_adaptive_subdivision = True
        md.adaptive_object_edge_length = 0.02 if hasattr(md, "adaptive_object_edge_length") else 0.0
    return ob, mat


def sun(name, elev_deg, azim_deg, energy):
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy = energy
    ld.angle = math.radians(3)
    ob = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(90 - elev_deg), 0, math.radians(azim_deg))
    return ob


def build(kind):
    L.reset("SC_RELIEF")
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -6.5, 1.8), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.0))
    cam2 = L.camera("CAM_Low", c, (3.5, -4.8, 0.9), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.0))
    sc = bpy.context.scene
    sc.camera = cam
    sun("SUN_Low", 14, 50, 4.0)                         # soleil rasant : le relief se voit
    L.world((0.30, 0.33, 0.38), 0.6)
    ob, mat = make_ground(kind)
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    if kind in ("starter", "eevee"):
        sc.render.engine = "BLENDER_EEVEE"
    else:
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 24
        sc.cycles.use_denoising = False
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    tiles = []
    for cam in ("CAM_Front", "CAM_Low"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out_path
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out_dir = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_08_relief_starter.blend"))
    for k in ("method_bump", "no_subdiv", "huge_scale", "const_height", "unlinked", "eevee"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_08_relief_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_08_relief_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_08_relief_reference.png"))


if __name__ == "__main__":
    L.run(main)
