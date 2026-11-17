"""
build_ch05_09_files.py — « Boucles et simulation » (CH05.09 : Repeat Zone).

Un outil « Escalier en colimaçon » (arbre GN_Spiral) : une ZONE DE RÉPÉTITION construit les marches une à une.
  Interface : Steps (Integer 3–60, défaut 16) · Angle (Float 5–45, défaut 22,5 degrés) · Rise (Float 0,05–0,5, défaut 0,18 m) · Radius (Float 0,5–3, défaut 1,2 m)
  Repeat Input [Iterations ← Steps ; Geometry : vide au départ]
    marche = Cube (1,0 × 0,4 × 0,1) -> Transform (x = Radius) -> Transform (rotation z = Iteration × Angle ; z = 0,05 + Iteration × Rise)
    Join Geometry (état précédent + marche) -> Repeat Output [Geometry]
  -> Set Material (MAT_Step) -> Group Output
  STARTER_FILES/ch05_09_loops_starter.blend : une seule marche (sans zone de répétition ni interface).
  COMPLETED_EXAMPLES/ch05_09_loops_solution.blend (+ _reference.png : deux réglages)
  COUNTER_EXAMPLES/ : fixed_steps, no_rotation, no_rise, no_accumulate, radius_ignored
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_09_files.py
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
NOTE = """CH05.09 — BOUCLES ET SIMULATION (GEO_Spiral, outil GN_Spiral) : un escalier en colimaçon construit par une zone de répétition (Repeat Zone)
Interface : Steps (Integer 3–60, défaut 16) ; Angle (Float 5–45, défaut 22,5 degrés) ; Rise (Float 0,05–0,5, défaut 0,18 m) ; Radius (Float 0,5–3, défaut 1,2 m).
1. Repeat Input : Iterations ← Steps ; la géométrie de départ reste vide.
2. Dans la zone : Cube (1,0 × 0,4 × 0,1) → Transform (Translation x = Radius) → Transform (Rotation z = Iteration × Angle en radians ; Translation z = 0,05 + Iteration × Rise).
3. Join Geometry reçoit la géométrie de l'itération précédente ET la nouvelle marche → Repeat Output [Geometry].
4. Set Material (MAT_Step) → Group Output.
Le correcteur règle les paramètres (deux réglages) et mesure les marches : nombre, hauteur de contremarche, angle entre marches, rayon.
Vérification : SCRIPTS/validate_ch05_09.py -- --exercise loops
"""
PARAMS = [("Steps", "NodeSocketInt", 16, 3, 60, "Nombre de marches"),
          ("Angle", "NodeSocketFloat", 22.5, 5.0, 45.0, "Angle entre deux marches en degrés"),
          ("Rise", "NodeSocketFloat", 0.18, 0.05, 0.5, "Hauteur d'une marche en mètres"),
          ("Radius", "NodeSocketFloat", 1.2, 0.5, 3.0, "Distance du centre de la marche à l'axe en mètres")]


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Spiral", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    if kind != "starter":
        for name, typ, dv, mn, mx, desc in PARAMS:
            s = I.new_socket(name, in_out="INPUT", socket_type=typ)
            s.default_value, s.min_value, s.max_value, s.description = dv, mn, mx, desc
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-1800, 0)
    out = N.new("NodeGroupOutput"); out.location = (1800, 0)
    cube = N.new("GeometryNodeMeshCube"); cube.location = (-900, -300)
    cube.inputs["Size"].default_value = (1.0, 0.4, 0.1)
    t1 = N.new("GeometryNodeTransform"); t1.location = (-600, -300)
    t2 = N.new("GeometryNodeTransform"); t2.location = (-300, -300)
    lk(cube.outputs["Mesh"], t1.inputs["Geometry"])
    lk(t1.outputs["Geometry"], t2.inputs["Geometry"])
    if kind == "starter":
        t1.inputs["Translation"].default_value = (1.2, 0, 0)
        t2.inputs["Translation"].default_value = (0, 0, 0.05)
        lk(t2.outputs["Geometry"], out.inputs["Geometry"])
        return ng
    ri = N.new("GeometryNodeRepeatInput"); ri.location = (-1200, 100)
    ro = N.new("GeometryNodeRepeatOutput"); ro.location = (700, 100)
    ri.pair_with_output(ro)
    if kind == "fixed_steps":
        ri.inputs["Iterations"].default_value = 16
    else:
        lk(gi.outputs["Steps"], ri.inputs["Iterations"])
    # étape : placement
    cx = N.new("ShaderNodeCombineXYZ"); cx.location = (-900, -550)
    if kind == "radius_ignored":
        cx.inputs["X"].default_value = 1.2
    else:
        lk(gi.outputs["Radius"], cx.inputs["X"])
    lk(cx.outputs["Vector"], t1.inputs["Translation"])
    it = ri.outputs["Iteration"]
    # rotation = Iteration × radians(Angle)
    rad = N.new("ShaderNodeMath"); rad.location = (-1100, -650)
    rad.operation = "RADIANS"
    lk(gi.outputs["Angle"], rad.inputs[0])
    mulr = N.new("ShaderNodeMath"); mulr.location = (-900, -700)
    mulr.operation = "MULTIPLY"
    lk(it, mulr.inputs[0]); lk(rad.outputs["Value"], mulr.inputs[1])
    rot = N.new("ShaderNodeCombineXYZ"); rot.location = (-700, -700)
    if kind != "no_rotation":
        lk(mulr.outputs["Value"], rot.inputs["Z"])
    lk(rot.outputs["Vector"], t2.inputs["Rotation"])
    # montée = 0,05 + Iteration × Rise
    mulz = N.new("ShaderNodeMath"); mulz.location = (-1100, -850)
    mulz.operation = "MULTIPLY"
    lk(it, mulz.inputs[0])
    if kind == "no_rise":
        mulz.inputs[1].default_value = 0.0
    else:
        lk(gi.outputs["Rise"], mulz.inputs[1])
    addz = N.new("ShaderNodeMath"); addz.location = (-900, -850)
    addz.operation = "ADD"
    addz.inputs[1].default_value = 0.05
    lk(mulz.outputs["Value"], addz.inputs[0])
    tz = N.new("ShaderNodeCombineXYZ"); tz.location = (-700, -850)
    lk(addz.outputs["Value"], tz.inputs["Z"])
    lk(tz.outputs["Vector"], t2.inputs["Translation"])
    # accumulation
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (300, 100)
    if kind != "no_accumulate":
        lk(ri.outputs["Geometry"], jn.inputs["Geometry"])
    lk(t2.outputs["Geometry"], jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], ro.inputs["Geometry"])
    sm = N.new("GeometryNodeSetMaterial"); sm.location = (1100, 100)
    sm.inputs["Material"].default_value = bpy.data.materials["MAT_Step"]
    lk(ro.outputs["Geometry"], sm.inputs["Geometry"])
    lk(sm.outputs["Geometry"], out.inputs["Geometry"])
    return ng


def set_param(md, ng, name, value):
    item = next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == name)
    md.properties.inputs[item.identifier]["value"] = value


def build(kind):
    L.reset("SC_GN9")
    L.studio(subject_height=4.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -17.0, 4.5), 50, make_active=True)
    S.look_at(cam, (0, 0, 2.3))
    cam2 = L.camera("CAM_High", c, (11.0, -11.0, 12.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 1.8))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Spiral")
    me.from_pydata([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("GEO_Spiral", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("MAT_Step")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.65, 0.45, 0.28, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc, ob, md, ng


def render_to(sc, i):
    p = os.path.join(bpy.app.tempdir, f"r{i}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    W, H = im.size
    a = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
    bpy.data.images.remove(im)
    return a


def main():
    out_dir = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_09_loops_starter.blend"))
    for k in ("fixed_steps", "no_rotation", "no_rise", "no_accumulate", "radius_ignored"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_09_loops_{k}.blend"))
    sc, ob, md, ng = build("solution")
    L.save(os.path.join(out_dir, "ch05_09_loops_solution.blend"))
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for params in ({}, {"Steps": 30, "Angle": 15.0, "Rise": 0.12, "Radius": 2.0}):
        for k, v in params.items():
            set_param(md, ng, k, v)
        ob.update_tag()
        bpy.context.view_layer.update()
        for cam in ("CAM_Front", "CAM_High"):
            sc.camera = bpy.data.objects[cam]
            tiles.append(render_to(sc, len(tiles)))
    top = np.concatenate([tiles[2], tiles[3]], axis=1)
    bot = np.concatenate([tiles[0], tiles[1]], axis=1)
    sheet = np.concatenate([bot, top], axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = os.path.join(out_dir, "ch05_09_loops_reference.png")
    img.file_format = "PNG"
    img.save()
    for k, v in (("Steps", 16), ("Angle", 22.5), ("Rise", 0.18), ("Radius", 1.2)):
        set_param(md, ng, k, v)
    sc.camera = bpy.data.objects["CAM_Front"]
    L.save(os.path.join(out_dir, "ch05_09_loops_solution.blend"))


if __name__ == "__main__":
    L.run(main)
