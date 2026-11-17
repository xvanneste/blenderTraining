"""
build_ch05_01_files.py — « Geometry Nodes : principes » (CH05.01).

Un terrain procédural GEO_Terrain : maillage vide + modificateur Geometry Nodes (arbre GN_Terrain). La GÉOMÉTRIE circule de gauche à droite ;
un CHAMP (le bruit, évalué en chaque point) pilote le déplacement.
  Solution : Grid (10 x 10 m, 100 x 100 sommets) -> Set Position [Offset = Combine XYZ (Z = (Noise [Fac] − 0,5) × 2)] -> Set Shade Smooth -> Set Material (MAT_Terrain) -> Group Output
  STARTER_FILES/ch05_01_principles_starter.blend : arbre avec la seule Grid (3 x 3 sommets) reliée à la sortie.
  COMPLETED_EXAMPLES/ch05_01_principles_solution.blend (+ _reference.png : deux vues)
  COUNTER_EXAMPLES/ : flat (Offset non alimenté), no_smooth, no_material (sans Set Material), coarse (Grid 8 x 8), huge_amp (amplitude 20), orphan (nœud inutilisé)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_01_files.py
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
NOTE = """CH05.01 — PRINCIPES DE GEOMETRY NODES (GEO_Terrain, arbre GN_Terrain)
La géométrie circule de gauche à droite ; un CHAMP est une valeur calculée en chaque point/face au moment où un nœud la lit.
1. Grid : Size 10 x 10 m, Vertices 100 x 100.
2. Set Position : Offset alimenté par un champ : Noise Texture [Fac] -> Math (Subtract 0,5) -> Math (Multiply 2) -> Combine XYZ [Z] -> Offset.
3. Set Shade Smooth après le déplacement, puis Set Material (MAT_Terrain : la géométrie générée n'hérite pas des matériaux du maillage d'origine) ; Group Output [Geometry] relié.
4. Aucun nœud inutilisé ; 5 à 15 nœuds.
Vérification : SCRIPTS/validate_ch05_01.py -- --exercise principles
"""


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Terrain", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, lk = ng.nodes, ng.links.new
    out = N.new("NodeGroupOutput"); out.location = (1000, 0)
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-700, 0)
    if kind == "starter":
        lk(grid.outputs["Mesh"], out.inputs["Geometry"])
        return ng
    grid.inputs["Size X"].default_value = 10.0
    grid.inputs["Size Y"].default_value = 10.0
    v = 8 if kind == "coarse" else 100
    grid.inputs["Vertices X"].default_value = v
    grid.inputs["Vertices Y"].default_value = v
    sp = N.new("GeometryNodeSetPosition"); sp.location = (200, 0)
    lk(grid.outputs["Mesh"], sp.inputs["Geometry"])
    if kind != "flat":
        nz = N.new("ShaderNodeTexNoise"); nz.location = (-700, -350)
        nz.inputs["Scale"].default_value = 0.35
        nz.inputs["Detail"].default_value = 5.0
        sub = N.new("ShaderNodeMath"); sub.location = (-450, -350)
        sub.operation = "SUBTRACT"
        sub.inputs[1].default_value = 0.5
        mul = N.new("ShaderNodeMath"); mul.location = (-250, -350)
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = 20.0 if kind == "huge_amp" else 2.0
        cx = N.new("ShaderNodeCombineXYZ"); cx.location = (-50, -350)
        lk(nz.outputs["Fac"], sub.inputs[0])
        lk(sub.outputs["Value"], mul.inputs[0])
        lk(mul.outputs["Value"], cx.inputs["Z"])
        lk(cx.outputs["Vector"], sp.inputs["Offset"])
    last = sp.outputs["Geometry"]
    if kind != "no_smooth":
        sm = N.new("GeometryNodeSetShadeSmooth"); sm.location = (450, 0)
        lk(last, sm.inputs["Geometry"])
        last = sm.outputs["Geometry"]
    if kind != "no_material":
        sm2 = N.new("GeometryNodeSetMaterial"); sm2.location = (700, 0)
        sm2.inputs["Material"].default_value = bpy.data.materials["MAT_Terrain"]
        lk(last, sm2.inputs["Geometry"])
        last = sm2.outputs["Geometry"]
    lk(last, out.inputs["Geometry"])
    if kind == "orphan":
        N.new("GeometryNodeMeshCube").location = (-700, 350)
    return ng


def build(kind):
    L.reset("SC_GN1")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -17.0, 6.5), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.0))
    cam2 = L.camera("CAM_Low", c, (9.0, -9.0, 2.2), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Terrain")
    ob = bpy.data.objects.new("GEO_Terrain", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("MAT_Terrain")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.35, 0.28, 0.20, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    me.materials.append(mat)
    ob.location = (0, 0, 0.8)                             # relief au-dessus du sol du studio
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_01_principles_starter.blend"))
    for k in ("flat", "no_smooth", "no_material", "coarse", "huge_amp", "orphan"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_01_principles_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_01_principles_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_01_principles_reference.png"))


if __name__ == "__main__":
    L.run(main)
