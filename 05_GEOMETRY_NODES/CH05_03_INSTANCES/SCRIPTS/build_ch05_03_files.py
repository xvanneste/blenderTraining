"""
build_ch05_03_files.py — « Instances » (CH05.03).

Un champ de piquets GEO_Posts : une grille de 21 × 21 points (8 × 8 m) reçoit un piquet INSTANCIÉ en chaque point, avec rotation et échelle aléatoires.
  Piquet  : Cylinder (Radius 0,05 ; Depth 1) -> Transform (z = 0,5 : base sur le point) -> Set Material (MAT_Post)
  Points  : Grid (Size 8 × 8 ; Vertices 21 × 21)
  Instance on Points [Points ← Grid ; Instance ← piquet ; Rotation ← Random Value (vecteur, Max z = 2π) ; Scale ← Random Value (flottant 0,6–1,4)] -> Group Output
  (les instances ne sont PAS réalisées : l'arbre produit 441 instances d'une même géométrie)
  STARTER_FILES/ch05_03_instances_starter.blend : arbre avec le seul piquet (sans Transform ni matériau) relié à la sortie.
  COMPLETED_EXAMPLES/ch05_03_instances_solution.blend (+ _reference.png : deux vues)
  COUNTER_EXAMPLES/ : realized (Realize Instances), no_random, sunk (piquet non relevé), sparse (Grid 4 × 4), too_dense (Grid 60 × 60), no_material
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_03_files.py
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
NOTE = """CH05.03 — INSTANCES (GEO_Posts, arbre GN_Posts) : un champ de piquets
1. Piquet : Cylinder (Radius 0,05 ; Depth 1) -> Transform (Translation z = 0,5, pour que la base soit à l'origine) -> Set Material (MAT_Post).
2. Points : Grid (Size 8 × 8 ; Vertices 21 × 21).
3. Instance on Points : Points ← Grid ; Instance ← piquet ; Rotation ← Random Value (type Vector, Max z = 6,283) ; Scale ← Random Value (type Float, Min 0,6, Max 1,4).
4. Ne PAS utiliser Realize Instances : on garde des instances (légères). Group Output relié ; aucun nœud orphelin.
Résultat attendu : 100 à 1 600 instances, emprise 7–8,5 m, échelles variées (0,4–1,8), orientations réparties, bases à z = 0.
Vérification : SCRIPTS/validate_ch05_03.py -- --exercise instances
"""


def enabled(node, kind):
    return [i for i in node.inputs if i.enabled and i.type == kind]


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Posts", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, lk = ng.nodes, ng.links.new
    out = N.new("NodeGroupOutput"); out.location = (1300, 0)
    cyl = N.new("GeometryNodeMeshCylinder"); cyl.location = (-900, 250)
    cyl.inputs["Radius"].default_value = 0.05
    cyl.inputs["Depth"].default_value = 1.0
    if kind == "starter":
        lk(cyl.outputs["Mesh"], out.inputs["Geometry"])
        return ng
    last = cyl.outputs["Mesh"]
    if kind != "sunk":
        tr = N.new("GeometryNodeTransform"); tr.location = (-650, 250)
        tr.inputs["Translation"].default_value = (0, 0, 0.5)
        lk(last, tr.inputs["Geometry"])
        last = tr.outputs["Geometry"]
    if kind != "no_material":
        sm = N.new("GeometryNodeSetMaterial"); sm.location = (-400, 250)
        sm.inputs["Material"].default_value = bpy.data.materials["MAT_Post"]
        lk(last, sm.inputs["Geometry"])
        last = sm.outputs["Geometry"]
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-650, -50)
    grid.inputs["Size X"].default_value = 8.0
    grid.inputs["Size Y"].default_value = 8.0
    v = {"sparse": 4, "too_dense": 60}.get(kind, 21)
    grid.inputs["Vertices X"].default_value = v
    grid.inputs["Vertices Y"].default_value = v
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (300, 0)
    lk(grid.outputs["Mesh"], io.inputs["Points"])
    lk(last, io.inputs["Instance"])
    if kind != "no_random":
        rv = N.new("FunctionNodeRandomValue"); rv.location = (-200, -300)
        rv.data_type = "FLOAT_VECTOR"
        enabled(rv, "VECTOR")[1].default_value = (0.0, 0.0, 6.283185)
        rs = N.new("FunctionNodeRandomValue"); rs.location = (-200, -550)
        rs.data_type = "FLOAT"
        f = enabled(rs, "VALUE")
        f[0].default_value, f[1].default_value = 0.6, 1.4
        lk([o for o in rv.outputs if o.enabled][0], io.inputs["Rotation"])
        lk([o for o in rs.outputs if o.enabled][0], io.inputs["Scale"])
    lastg = io.outputs["Instances"]
    if kind == "realized":
        rz = N.new("GeometryNodeRealizeInstances"); rz.location = (700, 0)
        lk(lastg, rz.inputs["Geometry"])
        lastg = rz.outputs["Geometry"]
    lk(lastg, out.inputs["Geometry"])
    return ng


def build(kind):
    L.reset("SC_GN3")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -15.0, 6.5), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.3))
    cam2 = L.camera("CAM_High", c, (9.5, -9.5, 10.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.3))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Posts")
    ob = bpy.data.objects.new("GEO_Posts", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("MAT_Post")
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.55, 0.38, 0.22, 1)
    b.inputs["Roughness"].default_value = 0.6
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_03_instances_starter.blend"))
    for k in ("realized", "no_random", "sunk", "sparse", "too_dense", "no_material"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_03_instances_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_03_instances_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_03_instances_reference.png"))


if __name__ == "__main__":
    L.run(main)
