"""
build_ch05_04_files.py — « Distribution » (CH05.04).

Un sol GEO_Field (grille 10 × 10 m, faces) sur lequel on distribue des arbres (cônes instanciés) avec Distribute Points on Faces en méthode POISSON (distance minimale),
et un MASQUE : seule la moitié x > 0 reçoit des arbres.
  Sol      : Grid (Size 10 × 10 ; Vertices 11 × 11) -> Distribute Points on Faces (Poisson ; Distance Min 0,5 ; Density Max 3 ; Density Factor ← masque ; Seed 0)
  Masque   : Position -> Separate XYZ [X] -> Math (Greater Than 0) -> Density Factor
  Arbre    : Cone (Radius 0,2 ; Depth 0,8) -> Transform (z = 0,4) -> Set Material (MAT_Tree)
  Instance on Points (Points ← Distribute ; Instance ← arbre ; Rotation ← Distribute [Rotation]) -> Join Geometry (avec le sol) -> Group Output
  STARTER_FILES/ch05_04_distribution_starter.blend : le sol et l'arbre, SANS distribution.
  COMPLETED_EXAMPLES/ch05_04_distribution_solution.blend (+ _reference.png : deux vues)
  COUNTER_EXAMPLES/ : no_mask, random_method, sparse, wrong_side, orphan
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_04_files.py
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
NOTE = """CH05.04 — DISTRIBUTION (GEO_Field, arbre GN_Field) : des arbres sur la moitié x > 0 d'un sol de 10 × 10 m
1. Sol : Grid (Size 10 × 10 ; Vertices 11 × 11) → Distribute Points on Faces : méthode Poisson Disk, Distance Min 0,5, Density Max 3, Seed 0.
2. Masque : Position → Separate XYZ [X] → Math (Greater Than, 0) → Density Factor (1 si x > 0, sinon 0).
3. Arbre : Cone (Radius 0,2 ; Depth 0,8) → Transform (z = 0,4) → Set Material (MAT_Tree). Instance on Points : Points ← Distribute [Points], Instance ← arbre, Rotation ← Distribute [Rotation].
4. Join Geometry rassemble le sol et les instances → Group Output. Aucun nœud orphelin.
Résultat attendu : 40 à 400 arbres, au moins 95 % avec x > 0, distance minimale entre arbres ≥ 0,45 m.
Vérification : SCRIPTS/validate_ch05_04.py -- --exercise distribution
"""


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Field", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, lk = ng.nodes, ng.links.new
    out = N.new("NodeGroupOutput"); out.location = (1700, 0)
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-900, 0)
    grid.inputs["Size X"].default_value = 10.0
    grid.inputs["Size Y"].default_value = 10.0
    grid.inputs["Vertices X"].default_value = 11
    grid.inputs["Vertices Y"].default_value = 11
    cone = N.new("GeometryNodeMeshCone"); cone.location = (-900, -400)
    cone.inputs["Radius Bottom"].default_value = 0.2
    cone.inputs["Depth"].default_value = 0.8
    tr = N.new("GeometryNodeTransform"); tr.location = (-650, -400)
    tr.inputs["Translation"].default_value = (0, 0, 0.4)
    lk(cone.outputs["Mesh"], tr.inputs["Geometry"])
    sm = N.new("GeometryNodeSetMaterial"); sm.location = (-400, -400)
    sm.inputs["Material"].default_value = bpy.data.materials["MAT_Tree"]
    lk(tr.outputs["Geometry"], sm.inputs["Geometry"])
    if kind == "starter":
        lk(grid.outputs["Mesh"], out.inputs["Geometry"])
        return ng
    ds = N.new("GeometryNodeDistributePointsOnFaces"); ds.location = (-300, 100)
    ds.distribute_method = "RANDOM" if kind == "random_method" else "POISSON"
    if "Distance Min" in ds.inputs:
        ds.inputs["Distance Min"].default_value = 0.5
    dens = 0.1 if kind == "sparse" else 3.0
    for nm in ("Density Max", "Density"):                       # « Density Max » (Poisson) ou « Density » (Random) selon la méthode
        if nm in ds.inputs:
            ds.inputs[nm].default_value = dens
    ds.inputs["Seed"].default_value = 0
    lk(grid.outputs["Mesh"], ds.inputs["Mesh"])
    if kind != "no_mask":
        pos = N.new("GeometryNodeInputPosition"); pos.location = (-900, 300)
        sep = N.new("ShaderNodeSeparateXYZ"); sep.location = (-700, 300)
        gt = N.new("ShaderNodeMath"); gt.location = (-500, 300)
        gt.operation = "LESS_THAN" if kind == "wrong_side" else "GREATER_THAN"
        gt.inputs[1].default_value = 0.0
        lk(pos.outputs["Position"], sep.inputs["Vector"])
        lk(sep.outputs["X"], gt.inputs[0])
        if "Density Factor" in ds.inputs:                        # absent en méthode Random
            lk(gt.outputs["Value"], ds.inputs["Density Factor"])
        else:
            lk(gt.outputs["Value"], ds.inputs["Selection"])        # en Random, le masque passe par Selection
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (300, 100)
    lk(ds.outputs["Points"], io.inputs["Points"])
    lk(sm.outputs["Geometry"], io.inputs["Instance"])
    lk(ds.outputs["Rotation"], io.inputs["Rotation"])
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (900, 0)
    lk(grid.outputs["Mesh"], jn.inputs["Geometry"])
    lk(io.outputs["Instances"], jn.inputs["Geometry"])
    ss = N.new("GeometryNodeSetShadeSmooth"); ss.location = (1200, 0)
    lk(jn.outputs["Geometry"], ss.inputs["Geometry"])
    lk(ss.outputs["Geometry"], out.inputs["Geometry"])
    if kind == "orphan":
        N.new("GeometryNodeMeshCube").location = (0, 500)
    return ng


def build(kind):
    L.reset("SC_GN4")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -15.0, 8.5), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.0))
    cam2 = L.camera("CAM_High", c, (0.01, -0.01, 21.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Field")
    ob = bpy.data.objects.new("GEO_Field", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, 0.02)
    mt = bpy.data.materials.new("MAT_Tree")
    mt.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.12, 0.35, 0.12, 1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_04_distribution_starter.blend"))
    for k in ("no_mask", "random_method", "sparse", "wrong_side", "orphan"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_04_distribution_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_04_distribution_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_04_distribution_reference.png"))


if __name__ == "__main__":
    L.run(main)
