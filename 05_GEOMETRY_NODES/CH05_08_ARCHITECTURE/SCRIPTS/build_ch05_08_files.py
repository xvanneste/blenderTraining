"""
build_ch05_08_files.py — « Architecture procédurale » (CH05.08).

Un outil « Immeuble » (arbre GN_Building) sur le support GEO_Building (plan), cinq paramètres :
  Floors (Integer 1–10, défaut 4) · Bays (Integer 1–12, défaut 5) · Floor Height (Float 2,5–4, défaut 3) · Bay Width (Float 1,5–4, défaut 2,5) · Depth (Float 4–15, défaut 8)
  Corps    : Cube (X = Bays × Bay Width ; Y = Depth ; Z = Floors × Floor Height) -> Transform (z = hauteur ÷ 2) -> Set Material (MAT_Wall)
  Fenêtres : Grid (Size X = (Bays − 1) × Bay Width ; Size Y = (Floors − 1) × Floor Height ; Vertices X = Bays ; Vertices Y = Floors) -> Transform (rotation x = 90°, y = −Depth ÷ 2,
             z = (Floors − 1) × Floor Height ÷ 2 + 0,55 × Floor Height) -> Instance on Points (Instance = Cube 1,2 × 0,12 × 1,4 -> Set Material (MAT_Window))
  Join Geometry (corps + fenêtres + entrée) -> Group Output
  Résultat : une façade régulière de Bays × Floors fenêtres, une fenêtre au centre de chaque travée et de chaque étage.
  STARTER_FILES/ch05_08_architecture_starter.blend : corps et fenêtres en dur (5 × 4, 2,5 m, 3 m, 8 m), SANS interface.
  COMPLETED_EXAMPLES/ch05_08_architecture_solution.blend (+ _reference.png : deux immeubles)
  COUNTER_EXAMPLES/ : fixed_count, body_height_fixed, bad_spacing, off_facade
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_08_files.py
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
NOTE = """CH05.08 — ARCHITECTURE PROCÉDURALE (GEO_Building, outil GN_Building) : un immeuble modulaire à cinq paramètres
Interface : Floors (Integer, 1–10, défaut 4) ; Bays (Integer, 1–12, défaut 5) ; Floor Height (Float, 2,5–4, défaut 3) ; Bay Width (Float, 1,5–4, défaut 2,5) ; Depth (Float, 4–15, défaut 8).
1. Corps : Cube (X = Bays × Bay Width ; Y = Depth ; Z = Floors × Floor Height) → Transform (z = hauteur ÷ 2).
2. Fenêtres : Grid (Size X = (Bays − 1) × Bay Width ; Size Y = (Floors − 1) × Floor Height ; Vertices X = Bays ; Vertices Y = Floors) → Transform (rotation X 90°, y = −Depth ÷ 2,
   z = (Floors − 1) × Floor Height ÷ 2 + 0,55 × Floor Height) → Instance on Points (fenêtre : Cube 1,2 × 0,12 × 1,4).
3. Join Geometry (corps + fenêtres + entrée) → Group Output.
Le correcteur règle les paramètres (deux réglages) et mesure : nombre de fenêtres, dimensions du corps, régularité de la façade.
Vérification : SCRIPTS/validate_ch05_08.py -- --exercise architecture
"""
PARAMS = [("Floors", "NodeSocketInt", 4, 1, 10, "Nombre d'étages"),
          ("Bays", "NodeSocketInt", 5, 1, 12, "Nombre de travées (fenêtres par étage)"),
          ("Floor Height", "NodeSocketFloat", 3.0, 2.5, 4.0, "Hauteur d'un étage en mètres"),
          ("Bay Width", "NodeSocketFloat", 2.5, 1.5, 4.0, "Largeur d'une travée en mètres"),
          ("Depth", "NodeSocketFloat", 8.0, 4.0, 15.0, "Profondeur de l'immeuble en mètres")]


class B:
    """Petit assistant pour construire des opérations mathématiques."""

    def __init__(self, ng):
        self.ng, self.x = ng, -1400

    def _n(self, kind):
        n = self.ng.nodes.new(kind)
        n.location = (self.x, -600 - 120 * (len(self.ng.nodes) % 14))
        self.x += 40
        return n

    def math(self, op, a, b=None):
        n = self._n("ShaderNodeMath")
        n.operation = op
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = float(v)
            else:
                self.ng.links.new(v, n.inputs[i])
        return n.outputs["Value"]


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Building", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    if kind != "starter":
        for name, typ, dv, mn, mx, desc in PARAMS:
            s = I.new_socket(name, in_out="INPUT", socket_type=typ)
            s.default_value, s.min_value, s.max_value, s.description = dv, mn, mx, desc
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-1800, 0)
    out = N.new("NodeGroupOutput"); out.location = (2000, 0)
    m = B(ng)

    def P(name, const):
        """Paramètre de l'interface (socket) ou, pour le starter, constante."""
        return gi.outputs[name] if kind != "starter" else const
    floors, bays, fh, bw, depth = P("Floors", 4.0), P("Bays", 5.0), P("Floor Height", 3.0), P("Bay Width", 2.5), P("Depth", 8.0)
    # corps
    width = m.math("MULTIPLY", bays, bw)
    height = m.math("MULTIPLY", floors, 3.0 if kind == "body_height_fixed" else fh)
    cube = N.new("GeometryNodeMeshCube"); cube.location = (-700, 400)
    vec = N.new("ShaderNodeCombineXYZ"); vec.location = (-900, 400)
    for k, v in (("X", width), ("Y", depth), ("Z", height)):
        if isinstance(v, float):
            vec.inputs[k].default_value = v
        else:
            lk(v, vec.inputs[k])
    lk(vec.outputs["Vector"], cube.inputs["Size"])
    tb = N.new("GeometryNodeTransform"); tb.location = (-400, 400)
    zc = N.new("ShaderNodeCombineXYZ"); zc.location = (-600, 250)
    hh = m.math("DIVIDE", height, 2.0)
    lk(hh, zc.inputs["Z"])
    lk(zc.outputs["Vector"], tb.inputs["Translation"])
    lk(cube.outputs["Mesh"], tb.inputs["Geometry"])
    sw = N.new("GeometryNodeSetMaterial"); sw.location = (-150, 400)
    sw.inputs["Material"].default_value = bpy.data.materials["MAT_Wall"]
    lk(tb.outputs["Geometry"], sw.inputs["Geometry"])
    # fenêtres
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-700, -100)
    bm1 = m.math("SUBTRACT", bays, 1.0)
    fm1 = m.math("SUBTRACT", floors, 1.0)
    gx = m.math("MULTIPLY", bm1, bw)
    spacing_y = m.math("DIVIDE", fh, 2.0) if kind == "bad_spacing" else fh
    gy = m.math("MULTIPLY", fm1, spacing_y)
    if kind == "fixed_count":
        grid.inputs["Vertices X"].default_value = 5
        grid.inputs["Vertices Y"].default_value = 4
    else:
        for v_, k_ in ((bays, "Vertices X"), (floors, "Vertices Y")):
            if isinstance(v_, float):
                grid.inputs[k_].default_value = int(v_)
            else:
                lk(v_, grid.inputs[k_])
    lk(gx, grid.inputs["Size X"])
    lk(gy, grid.inputs["Size Y"])
    tg = N.new("GeometryNodeTransform"); tg.location = (-400, -100)
    tg.inputs["Rotation"].default_value = (math.pi / 2, 0, 0)
    tv = N.new("ShaderNodeCombineXYZ"); tv.location = (-600, -300)
    ny = m.math("MULTIPLY", depth, -0.5 if kind != "off_facade" else 0.0)
    cz = m.math("ADD", m.math("DIVIDE", gy, 2.0), m.math("MULTIPLY", spacing_y, 0.55))
    lk(ny, tv.inputs["Y"])
    lk(cz, tv.inputs["Z"])
    lk(tv.outputs["Vector"], tg.inputs["Translation"])
    lk(grid.outputs["Mesh"], tg.inputs["Geometry"])
    win = N.new("GeometryNodeMeshCube"); win.location = (-400, -450)
    win.inputs["Size"].default_value = (1.2, 0.12, 1.4)
    sm = N.new("GeometryNodeSetMaterial"); sm.location = (-150, -450)
    sm.inputs["Material"].default_value = bpy.data.materials["MAT_Window"]
    lk(win.outputs["Mesh"], sm.inputs["Geometry"])
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (200, -100)
    lk(tg.outputs["Geometry"], io.inputs["Points"])
    lk(sm.outputs["Geometry"], io.inputs["Instance"])
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (800, 0)
    lk(sw.outputs["Geometry"], jn.inputs["Geometry"])
    lk(io.outputs["Instances"], jn.inputs["Geometry"])
    lk(gi.outputs["Geometry"], jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], out.inputs["Geometry"])
    return ng


def set_param(md, ng, name, value):
    item = next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == name)
    md.properties.inputs[item.identifier]["value"] = value


def build(kind):
    L.reset("SC_GN8")
    L.studio(subject_height=12.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (10.0, -72.0, 11.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 11.0))
    cam2 = L.camera("CAM_34", c, (50.0, -58.0, 16.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 11.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Building")
    me.from_pydata([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("GEO_Building", me)
    bpy.context.scene.collection.objects.link(ob)
    mw = bpy.data.materials.new("MAT_Wall")
    mw.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.75, 0.55, 0.40, 1)
    mw.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    mwi = bpy.data.materials.new("MAT_Window")
    b = mwi.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.10, 0.18, 0.28, 1)
    b.inputs["Roughness"].default_value = 0.1
    b.inputs["Metallic"].default_value = 0.0
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc, ob, md, ng


def render_to(sc, path_idx):
    p = os.path.join(bpy.app.tempdir, f"r{path_idx}.png")
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_08_architecture_starter.blend"))
    for k in ("fixed_count", "body_height_fixed", "bad_spacing", "off_facade"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_08_architecture_{k}.blend"))
    sc, ob, md, ng = build("solution")
    L.save(os.path.join(out_dir, "ch05_08_architecture_solution.blend"))
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for params in ({}, {"Floors": 7, "Bays": 3, "Floor Height": 3.4, "Bay Width": 3.2, "Depth": 10.0}):
        for k, v in params.items():
            set_param(md, ng, k, v)
        ob.update_tag()
        bpy.context.view_layer.update()
        for cam in ("CAM_Front", "CAM_34"):
            sc.camera = bpy.data.objects[cam]
            tiles.append(render_to(sc, len(tiles)))
    # planche 2 x 2 : haut = réglage B, bas = défaut (origine de l'image en bas)
    top = np.concatenate([tiles[2], tiles[3]], axis=1)
    bot = np.concatenate([tiles[0], tiles[1]], axis=1)
    sheet = np.concatenate([bot, top], axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = os.path.join(out_dir, "ch05_08_architecture_reference.png")
    img.file_format = "PNG"
    img.save()
    for k, v in (("Floors", 4), ("Bays", 5), ("Floor Height", 3.0), ("Bay Width", 2.5), ("Depth", 8.0)):
        set_param(md, ng, k, v)
    sc.camera = bpy.data.objects["CAM_Front"]
    L.save(os.path.join(out_dir, "ch05_08_architecture_solution.blend"))


if __name__ == "__main__":
    L.run(main)
