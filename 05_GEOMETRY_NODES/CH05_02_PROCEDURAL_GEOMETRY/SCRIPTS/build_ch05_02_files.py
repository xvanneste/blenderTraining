"""
build_ch05_02_files.py — « Géométrie procédurale » (CH05.02).

Une colonne GEO_Column construite par nœuds à partir de primitives : fût (Cylinder), base et chapiteau (Cube), anneau (Curve Circle + Curve to Mesh),
chacun placé par un Transform, puis assemblés par Join Geometry. Dimensions réelles : 3,0 m de haut, pieds sur z = 0, centrée sur l'axe Z.
  Fût      : Cylinder (Radius 0,3 ; Depth 2,6 ; 32 sommets) -> Transform (z = 1,5)             [z de 0,2 à 2,8]
  Base     : Cube (0,9 × 0,9 × 0,2) -> Transform (z = 0,1)                                      [z de 0 à 0,2]
  Chapiteau: Cube (0,9 × 0,9 × 0,2) -> Transform (z = 2,9)                                      [z de 2,8 à 3,0]
  Anneau   : Curve Circle (Radius 0,33 ; 48 points) + Curve Circle (Radius 0,05 ; 8 points) -> Curve to Mesh -> Transform (z = 2,6)
  -> Join Geometry -> Set Shade Smooth -> Set Material -> Group Output
  STARTER_FILES/ch05_02_procedural_starter.blend : arbre avec le seul fût (sans Transform) reliée à la sortie.
  COMPLETED_EXAMPLES/ch05_02_procedural_solution.blend (+ _reference.png : deux vues)
  COUNTER_EXAMPLES/ : no_join (fût seul), no_ring, floating (+0,3 m), short (fût de 1 m), off_center (chapiteau décalé de 0,2 m)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_02_files.py
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
NOTE = """CH05.02 — GÉOMÉTRIE PROCÉDURALE (GEO_Column, arbre GN_Column) : une colonne de 3 m construite à partir de primitives
1. Fût : Cylinder (Radius 0,3 ; Depth 2,6) -> Transform (Translation z = 1,5).
2. Base et chapiteau : Cube (0,9 × 0,9 × 0,2) -> Transform (z = 0,1 et z = 2,9).
3. Anneau : Curve Circle (Radius 0,33) et Curve Circle de profil (Radius 0,05) -> Curve to Mesh -> Transform (z = 2,6).
4. Join Geometry rassemble les quatre pièces -> Set Shade Smooth -> Set Material -> Group Output.
Résultat attendu : hauteur 2,8–3,6 m, pieds sur z = 0, centrée, quatre pièces, maillage fermé.
Vérification : SCRIPTS/validate_ch05_02.py -- --exercise procedural
"""


def tr(ng, geo_out, z, x=0.0):
    t = ng.nodes.new("GeometryNodeTransform")
    t.inputs["Translation"].default_value = (x, 0.0, z)
    ng.links.new(geo_out, t.inputs["Geometry"])
    return t


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Column", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, lk = ng.nodes, ng.links.new
    out = N.new("NodeGroupOutput"); out.location = (1500, 0)
    cyl = N.new("GeometryNodeMeshCylinder"); cyl.location = (-800, 300)
    cyl.inputs["Vertices"].default_value = 32
    cyl.inputs["Radius"].default_value = 0.3
    cyl.inputs["Depth"].default_value = 1.0 if kind == "short" else 2.6
    if kind == "starter":
        lk(cyl.outputs["Mesh"], out.inputs["Geometry"])
        return ng
    parts = []
    t = tr(ng, cyl.outputs["Mesh"], 0.5 if kind == "short" else 1.5); t.location = (-500, 300)
    parts.append(t.outputs["Geometry"])
    if kind != "no_join":
        base = N.new("GeometryNodeMeshCube"); base.location = (-800, 100)
        base.inputs["Size"].default_value = (0.9, 0.9, 0.2)
        tb = tr(ng, base.outputs["Mesh"], 0.1); tb.location = (-500, 100)
        cap = N.new("GeometryNodeMeshCube"); cap.location = (-800, -100)
        cap.inputs["Size"].default_value = (0.9, 0.9, 0.2)
        tc = tr(ng, cap.outputs["Mesh"], 2.9, 0.2 if kind == "off_center" else 0.0); tc.location = (-500, -100)
        parts += [tb.outputs["Geometry"], tc.outputs["Geometry"]]
        if kind != "no_ring":
            c1 = N.new("GeometryNodeCurvePrimitiveCircle"); c1.location = (-800, -350)
            c1.inputs["Radius"].default_value = 0.33
            c1.inputs["Resolution"].default_value = 48
            c2 = N.new("GeometryNodeCurvePrimitiveCircle"); c2.location = (-800, -550)
            c2.inputs["Radius"].default_value = 0.05
            c2.inputs["Resolution"].default_value = 8
            cm = N.new("GeometryNodeCurveToMesh"); cm.location = (-500, -350)
            lk(c1.outputs["Curve"], cm.inputs["Curve"])
            lk(c2.outputs["Curve"], cm.inputs["Profile Curve"])
            tz = tr(ng, cm.outputs["Mesh"], 2.6); tz.location = (-200, -350)
            parts.append(tz.outputs["Geometry"])
        jn = N.new("GeometryNodeJoinGeometry"); jn.location = (300, 0)
        for p in parts:
            lk(p, jn.inputs["Geometry"])
        last = jn.outputs["Geometry"]
    else:
        last = parts[0]
    sm = N.new("GeometryNodeSetShadeSmooth"); sm.location = (700, 0)
    lk(last, sm.inputs["Geometry"])
    sm2 = N.new("GeometryNodeSetMaterial"); sm2.location = (1100, 0)
    sm2.inputs["Material"].default_value = bpy.data.materials["MAT_Column"]
    lk(sm.outputs["Geometry"], sm2.inputs["Geometry"])
    lk(sm2.outputs["Geometry"], out.inputs["Geometry"])
    if kind == "floating":
        for n in list(N):
            if n.bl_idname == "GeometryNodeJoinGeometry":
                t = N.new("GeometryNodeTransform"); t.location = (500, 100)
                t.inputs["Translation"].default_value = (0, 0, 0.3)
                for l in list(ng.links):
                    if l.from_node == n:
                        ng.links.remove(l)
                lk(n.outputs["Geometry"], t.inputs["Geometry"])
                lk(t.outputs["Geometry"], sm.inputs["Geometry"])
    return ng


def build(kind):
    L.reset("SC_GN2")
    L.studio(subject_height=3.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -12.5, 1.9), 50, make_active=True)
    S.look_at(cam, (0, 0, 1.5))
    cam2 = L.camera("CAM_34", c, (7.5, -9.0, 2.6), 50, make_active=False)
    S.look_at(cam2, (0, 0, 1.5))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Column")
    ob = bpy.data.objects.new("GEO_Column", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("MAT_Column")
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.75, 0.72, 0.65, 1)
    b.inputs["Roughness"].default_value = 0.5
    me.materials.append(mat)
    ng = build_tree(kind)
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for cam in ("CAM_Front", "CAM_34"):
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_02_procedural_starter.blend"))
    for k in ("no_join", "no_ring", "floating", "short", "off_center"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_02_procedural_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_02_procedural_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_02_procedural_reference.png"))


if __name__ == "__main__":
    L.run(main)
