"""
build_ch05_06_files.py — « Paramètres et interfaces » (CH05.06).

Un OUTIL paramétrable « Rangée de piliers » (arbre GN_PillarRow) appliqué à un support GEO_Row (plan) :
  Interface (Group Input) : Geometry ; panneau « Dimensions » : Height (Float, 0,2–10, défaut 2), Radius (Float, 0,05–1, défaut 0,2) ;
                            panneau « Layout » : Count (Integer, 1–50, défaut 8), Spacing (Float, 0,3–5, défaut 1,2). Chaque entrée a une description (infobulle).
  Arbre : Mesh Line (Count ; Offset = Combine XYZ (X = Spacing)) -> Instance on Points (Instance = Cylinder (Radius ; Depth = Height) -> Transform (z = Height ÷ 2))
          -> Join Geometry (avec la géométrie d'entrée) -> Set Material (MAT_Pillar) -> Group Output
  STARTER_FILES/ch05_06_parameters_starter.blend : l'arbre fonctionnel mais SANS interface : valeurs codées en dur dans les nœuds.
  COMPLETED_EXAMPLES/ch05_06_parameters_solution.blend (+ _reference.png : deux réglages côte à côte)
  COUNTER_EXAMPLES/ : no_panels, no_description, unused_input (Spacing non branché), hardcoded (Height codé en dur), bad_range (Count 1–100 000 ; Height −5…)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH05.06 — PARAMÈTRES ET INTERFACES (GEO_Row, outil GN_PillarRow) : transformer l'arbre en outil réglable depuis le modificateur
1. Interface de l'arbre (panneau Group) : entrées Height (Float, 0,2–10, défaut 2), Radius (Float, 0,05–1, défaut 0,2), Count (Integer, 1–50, défaut 8), Spacing (Float, 0,3–5, défaut 1,2).
2. Rangez Height et Radius dans un panneau « Dimensions », Count et Spacing dans un panneau « Layout ».
3. Donnez une DESCRIPTION à chaque entrée (infobulle).
4. Branchez chaque entrée aux nœuds : Count → Mesh Line ; Spacing → Offset X ; Radius → Cylinder ; Height → Cylinder Depth et Transform z (Height ÷ 2).
Vérification : SCRIPTS/validate_ch05_06.py -- --exercise parameters (le correcteur CHANGE les paramètres du modificateur et vérifie que la géométrie suit).
"""
PARAMS = [  # nom, type, défaut, min, max, panneau, description
    ("Height", "NodeSocketFloat", 2.0, 0.2, 10.0, "Dimensions", "Hauteur des piliers en mètres"),
    ("Radius", "NodeSocketFloat", 0.2, 0.05, 1.0, "Dimensions", "Rayon des piliers en mètres"),
    ("Count", "NodeSocketInt", 8, 1, 50, "Layout", "Nombre de piliers"),
    ("Spacing", "NodeSocketFloat", 1.2, 0.3, 5.0, "Layout", "Distance entre deux piliers"),
]


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_PillarRow", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    sockets = {}
    if kind != "starter":
        panels = {}
        for name, typ, dv, mn, mx, panel, desc in PARAMS:
            parent = None
            if kind != "no_panels":
                if panel not in panels:
                    panels[panel] = I.new_panel(panel)
                parent = panels[panel]
            s = I.new_socket(name, in_out="INPUT", socket_type=typ, parent=parent)
            s.default_value = dv
            s.min_value = -5 if (kind == "bad_range" and name == "Height") else mn
            s.max_value = 100000 if (kind == "bad_range" and name == "Count") else mx
            s.description = "" if kind == "no_description" else desc
            sockets[name] = s
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-1300, 0)
    out = N.new("NodeGroupOutput"); out.location = (1500, 0)
    line = N.new("GeometryNodeMeshLine"); line.location = (-800, 300)
    line.mode = "OFFSET"
    cyl = N.new("GeometryNodeMeshCylinder"); cyl.location = (-800, -150)
    tr = N.new("GeometryNodeTransform"); tr.location = (-450, -150)
    half = N.new("ShaderNodeMath"); half.location = (-800, -450)
    half.operation = "DIVIDE"
    half.inputs[1].default_value = 2.0
    cz = N.new("ShaderNodeCombineXYZ"); cz.location = (-600, -450)
    cx = N.new("ShaderNodeCombineXYZ"); cx.location = (-1000, 300)
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (0, 150)
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (500, 0)
    sm = N.new("GeometryNodeSetMaterial"); sm.location = (900, 0)
    sm.inputs["Material"].default_value = bpy.data.materials["MAT_Pillar"]

    def src(name, default_setter):
        """Branche Group Input[name] si l'entrée existe ; sinon valeur codée en dur."""
        if name in sockets and not (kind == "unused_input" and name == "Spacing") and not (kind == "hardcoded" and name == "Height"):
            return gi.outputs[name]
        default_setter()
        return None
    # Count
    c = src("Count", lambda: line.inputs["Count"].__setattr__("default_value", 8))
    if c:
        lk(c, line.inputs["Count"])
    # Spacing -> Offset X
    s = src("Spacing", lambda: cx.inputs["X"].__setattr__("default_value", 1.2))
    if s:
        lk(s, cx.inputs["X"])
    lk(cx.outputs["Vector"], line.inputs["Offset"])
    # Radius
    rd = src("Radius", lambda: cyl.inputs["Radius"].__setattr__("default_value", 0.2))
    if rd:
        lk(rd, cyl.inputs["Radius"])
    # Height
    h = src("Height", lambda: (cyl.inputs["Depth"].__setattr__("default_value", 2.0), cz.inputs["Z"].__setattr__("default_value", 1.0)))
    if h:
        lk(h, cyl.inputs["Depth"])
        lk(h, half.inputs[0])
        lk(half.outputs["Value"], cz.inputs["Z"])
    lk(cz.outputs["Vector"], tr.inputs["Translation"])
    lk(cyl.outputs["Mesh"], tr.inputs["Geometry"])
    lk(line.outputs["Mesh"], io.inputs["Points"])
    lk(tr.outputs["Geometry"], io.inputs["Instance"])
    lk(gi.outputs["Geometry"], jn.inputs["Geometry"])
    lk(io.outputs["Instances"], jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], sm.inputs["Geometry"])
    lk(sm.outputs["Geometry"], out.inputs["Geometry"])
    return ng


def build(kind, view_params=None):
    L.reset("SC_GN6")
    L.studio(subject_height=2.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (5.2, -20.0, 3.5), 50, make_active=True)
    S.look_at(cam, (5.2, 0, 1.3))
    cam2 = L.camera("CAM_Side", c, (-4.0, -12.0, 4.0), 50, make_active=False)
    S.look_at(cam2, (3.0, 0, 1.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Row")
    me.from_pydata([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("GEO_Row", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("MAT_Pillar")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.75, 0.72, 0.65, 1)
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc, ob, md, ng


def set_param(md, ng, name, value):
    item = next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == name)
    md.properties.inputs[item.identifier]["value"] = value   # 5.3 : md[...] n'existe plus ; valeur dans md.properties.inputs[identifiant]["value"]


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    sc, ob, md, ng = None, None, None, None
    return tiles


def main():
    out_dir = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_06_parameters_starter.blend"))
    for k in ("no_panels", "no_description", "unused_input", "hardcoded", "bad_range"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_06_parameters_{k}.blend"))
    sc, ob, md, ng = build("solution")
    L.save(os.path.join(out_dir, "ch05_06_parameters_solution.blend"))
    # référence : deux réglages rendus (défaut puis Height 3,5 / Count 12 / Radius 0,3)
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for params in ({}, {"Height": 3.5, "Count": 12, "Radius": 0.3, "Spacing": 1.0}):
        for k, v in params.items():
            set_param(md, ng, k, v)
        if not params:
            for k, v in (("Height", 2.0), ("Count", 8), ("Radius", 0.2), ("Spacing", 1.2)):
                set_param(md, ng, k, v)
        ob.update_tag()
        bpy.context.view_layer.update()
        p = os.path.join(bpy.app.tempdir, f"r{len(tiles)}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate([tiles[1], tiles[0]], axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = os.path.join(out_dir, "ch05_06_parameters_reference.png")
    img.file_format = "PNG"
    img.save()
    for k, v in (("Height", 2.0), ("Count", 8), ("Radius", 0.2), ("Spacing", 1.2)):
        set_param(md, ng, k, v)
    L.save(os.path.join(out_dir, "ch05_06_parameters_solution.blend"))


if __name__ == "__main__":
    L.run(main)
