"""
build_ch05_05_files.py — « Attributs » (CH05.05).

Le terrain de CH05.01, colorié par la HAUTEUR : l'arbre calcule la hauteur (z après déplacement), la STOCKE dans un attribut nommé « height » (point, flottant)
et le matériau LIT cet attribut (nœud Attribute) pour choisir la couleur.
  Arbre   : Grid (10 × 10 m ; 100 × 100) -> Set Position (Offset z = (Noise − 0,5) × 2) -> Store Named Attribute (Name « height » ; Point ; Float ; Value = Position.z)
            -> Set Shade Smooth -> Set Material (MAT_Height) -> Group Output
  Matériau: Attribute (type Geometry, nom « height ») [Fac] -> Map Range (−0,5…0,5 -> 0…1) -> Color Ramp (bleu -> vert -> blanc) -> Base Color
  STARTER_FILES/ch05_05_attributes_starter.blend : terrain déplacé et lissé, sans attribut ; matériau MAT_Height à couleur unie.
  COMPLETED_EXAMPLES/ch05_05_attributes_solution.blend (+ _reference.png : deux vues)
  COUNTER_EXAMPLES/ : no_store, wrong_name (« altitude »), wrong_domain (face), shader_unlinked, constant (valeur 0,5), orphan
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_05_files.py
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
NOTE = """CH05.05 — ATTRIBUTS (GEO_Terrain, arbre GN_Terrain, matériau MAT_Height) : colorier le terrain par la hauteur
1. Dans l'arbre, après Set Position : Store Named Attribute — Data Type Float, Domain Point, Name « height », Value = Position → Separate XYZ [Z].
2. Dans le matériau MAT_Height : nœud Attribute (Type Geometry, Name « height ») [Fac] → Map Range (From Min −0,5, From Max 0,5) → Color Ramp (bleu, vert, blanc) → Base Color.
3. Le nom doit être IDENTIQUE des deux côtés (« height »).
Résultat attendu : l'attribut « height » existe sur les points de la géométrie évaluée, varie (écart-type ≥ 0,05) et le matériau en dépend.
Vérification : SCRIPTS/validate_ch05_05.py -- --exercise attributes
"""


def build_material(kind):
    mat = bpy.data.materials.new("MAT_Height")
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.8
    b.inputs["Base Color"].default_value = (0.4, 0.4, 0.4, 1)
    if kind == "starter":
        return mat
    if kind != "shader_unlinked":
        at = nt.nodes.new("ShaderNodeAttribute"); at.location = (-900, 0)
        at.attribute_type = "GEOMETRY"
        at.attribute_name = "height"
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.location = (-650, 0)
        mr.inputs["From Min"].default_value = -0.5
        mr.inputs["From Max"].default_value = 0.5
        cr = nt.nodes.new("ShaderNodeValToRGB"); cr.location = (-350, 0)
        cr.color_ramp.elements[0].position = 0.25
        cr.color_ramp.elements[0].color = (0.05, 0.15, 0.45, 1)
        mid = cr.color_ramp.elements.new(0.5)
        mid.color = (0.12, 0.40, 0.12, 1)
        cr.color_ramp.elements[2].position = 0.85
        cr.color_ramp.elements[2].color = (0.95, 0.95, 0.95, 1)
        nt.links.new(at.outputs["Fac"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], cr.inputs["Fac"])
        nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    return mat


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Terrain", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, lk = ng.nodes, ng.links.new
    out = N.new("NodeGroupOutput"); out.location = (1700, 0)
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-900, 0)
    grid.inputs["Size X"].default_value = 10.0
    grid.inputs["Size Y"].default_value = 10.0
    grid.inputs["Vertices X"].default_value = 100
    grid.inputs["Vertices Y"].default_value = 100
    sp = N.new("GeometryNodeSetPosition"); sp.location = (100, 0)
    lk(grid.outputs["Mesh"], sp.inputs["Geometry"])
    nz = N.new("ShaderNodeTexNoise"); nz.location = (-900, -350)
    nz.inputs["Scale"].default_value = 0.35
    nz.inputs["Detail"].default_value = 5.0
    sub = N.new("ShaderNodeMath"); sub.location = (-650, -350)
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = 0.5
    mul = N.new("ShaderNodeMath"); mul.location = (-450, -350)
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 2.0
    cx = N.new("ShaderNodeCombineXYZ"); cx.location = (-250, -350)
    lk(nz.outputs["Fac"], sub.inputs[0])
    lk(sub.outputs["Value"], mul.inputs[0])
    lk(mul.outputs["Value"], cx.inputs["Z"])
    lk(cx.outputs["Vector"], sp.inputs["Offset"])
    last = sp.outputs["Geometry"]
    if kind != "starter" and kind != "no_store":
        st = N.new("GeometryNodeStoreNamedAttribute"); st.location = (500, 0)
        st.data_type = "FLOAT"
        st.domain = "FACE" if kind == "wrong_domain" else "POINT"
        st.inputs["Name"].default_value = "altitude" if kind == "wrong_name" else "height"
        lk(last, st.inputs["Geometry"])
        val = [i for i in st.inputs if i.name == "Value" and i.enabled][0]
        if kind == "constant":
            val.default_value = 0.5
        else:
            pos = N.new("GeometryNodeInputPosition"); pos.location = (100, -250)
            sep = N.new("ShaderNodeSeparateXYZ"); sep.location = (300, -250)
            lk(pos.outputs["Position"], sep.inputs["Vector"])
            lk(sep.outputs["Z"], val)
        last = st.outputs["Geometry"]
    sm = N.new("GeometryNodeSetShadeSmooth"); sm.location = (900, 0)
    lk(last, sm.inputs["Geometry"])
    sm2 = N.new("GeometryNodeSetMaterial"); sm2.location = (1250, 0)
    sm2.inputs["Material"].default_value = bpy.data.materials["MAT_Height"]
    lk(sm.outputs["Geometry"], sm2.inputs["Geometry"])
    lk(sm2.outputs["Geometry"], out.inputs["Geometry"])
    if kind == "orphan":
        N.new("GeometryNodeMeshCube").location = (-900, 400)
    return ng


def build(kind):
    L.reset("SC_GN5")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -17.0, 7.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.8))
    cam2 = L.camera("CAM_High", c, (9.5, -9.5, 10.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.8))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Terrain")
    ob = bpy.data.objects.new("GEO_Terrain", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, 0.8)
    build_material(kind)
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for cam in ("CAM_Front", "CAM_High"):
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_05_attributes_starter.blend"))
    for k in ("no_store", "wrong_name", "wrong_domain", "shader_unlinked", "constant", "orphan"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_05_attributes_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_05_attributes_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_05_attributes_reference.png"))


if __name__ == "__main__":
    L.run(main)
