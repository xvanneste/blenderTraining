"""
build_ch05_07_files.py — « Décors et végétation » (CH05.07).

Un outil « Forêt » (arbre GN_Forest) sur le support GEO_Forest (plan) : terrain de 20 × 20 m déplacé par un bruit, puis arbres dispersés avec CONTRAINTE DE PENTE,
trois variantes d'arbres, échelle aléatoire et trois paramètres exposés (Seed, Density, Max Slope).
  Terrain : Grid (20 × 20 m ; 120 × 120) -> Set Position (Offset z = (Noise [Scale 0,08] − 0,5) × 4) -> Set Material (MAT_Ground)
  Masque  : Normal -> Separate XYZ [Z] -> Math (Greater Than) ← Math (Cosine ← Radians ← Max Slope) -> Density Factor
  Points  : Distribute Points on Faces (Poisson ; Distance Min 0,5 ; Density Max ← Density ; Seed ← Seed ; Density Factor ← masque) sur le terrain déplacé
  Arbres  : trois cônes (rayon/hauteur 0,2/0,8 ; 0,3/1,2 ; 0,4/1,8 ; le nœud Cone a sa BASE à z = 0) -> Set Material -> Geometry to Instance -> Instance on Points
            (Pick Instance ; Instance Index ← Random Value entier 0–2 ; Rotation ← Distribute [Rotation] ; Scale ← Random Value 0,8–1,2)
  Interface : Seed (Integer 0–1000, défaut 0), Density (Float 0,05–2, défaut 0,5), Max Slope (Float 0–90, défaut 30 degrés)
  STARTER_FILES/ch05_07_scattering_starter.blend : terrain déplacé et interface vide ; arbres non dispersés.
  COMPLETED_EXAMPLES/ch05_07_scattering_solution.blend (+ _reference.png)
  COUNTER_EXAMPLES/ : no_slope, no_variation, seed_unused, no_scale, floating
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_07_files.py
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
NOTE = """CH05.07 — DÉCORS ET VÉGÉTATION (GEO_Forest, outil GN_Forest) : une forêt sur un terrain, avec contrainte de pente
1. Terrain : Grid 20 × 20 m (120 × 120) → Set Position (bruit, amplitude 4) → Set Material (MAT_Ground).
2. Masque de pente : Normal → Separate XYZ [Z] → Greater Than (cos de Max Slope) → Density Factor du Distribute (Poisson, Distance Min 0,5).
3. Trois variantes d'arbres (nœuds Cone de 0,8, 1,2 et 1,8 m : leur base est déjà à z = 0, pas de Transform) → Geometry to Instance → Instance on Points (Pick Instance, Instance Index = Random Value entier 0–2, Scale = Random Value 0,8–1,2, Rotation du Distribute).
4. Interface : Seed (Integer), Density (Float), Max Slope (Float, degrés), tous branchés. Join Geometry : terrain + arbres.
Le correcteur règle Seed, Density et Max Slope et mesure : arbres sur la surface, pentes respectées, variantes, variation d'échelle, effet de chaque paramètre.
Vérification : SCRIPTS/validate_ch05_07.py -- --exercise scattering
"""
PARAMS = [("Seed", "NodeSocketInt", 0, 0, 1000, "Graine du tirage aléatoire"),
          ("Density", "NodeSocketFloat", 0.5, 0.05, 2.0, "Densité maximale d'arbres par m²"),
          ("Max Slope", "NodeSocketFloat", 30.0, 0.0, 90.0, "Pente maximale du terrain en degrés")]


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_Forest", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    if kind != "starter":
        for name, typ, dv, mn, mx, desc in PARAMS:
            s = I.new_socket(name, in_out="INPUT", socket_type=typ)
            s.default_value, s.min_value, s.max_value, s.description = dv, mn, mx, desc
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-1800, 0)
    out = N.new("NodeGroupOutput"); out.location = (2300, 0)
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-1500, 300)
    grid.inputs["Size X"].default_value = 20.0
    grid.inputs["Size Y"].default_value = 20.0
    grid.inputs["Vertices X"].default_value = 120
    grid.inputs["Vertices Y"].default_value = 120
    sp = N.new("GeometryNodeSetPosition"); sp.location = (-300, 300)
    lk(grid.outputs["Mesh"], sp.inputs["Geometry"])
    nz = N.new("ShaderNodeTexNoise"); nz.location = (-1500, 0)
    nz.inputs["Scale"].default_value = 0.08
    nz.inputs["Detail"].default_value = 3.0
    sub = N.new("ShaderNodeMath"); sub.location = (-1250, 0)
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = 0.5
    mul = N.new("ShaderNodeMath"); mul.location = (-1050, 0)
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 4.0
    cx = N.new("ShaderNodeCombineXYZ"); cx.location = (-850, 0)
    lk(nz.outputs["Fac"], sub.inputs[0]); lk(sub.outputs["Value"], mul.inputs[0])
    lk(mul.outputs["Value"], cx.inputs["Z"]); lk(cx.outputs["Vector"], sp.inputs["Offset"])
    sg = N.new("GeometryNodeSetMaterial"); sg.location = (0, 300)
    sg.inputs["Material"].default_value = bpy.data.materials["MAT_Ground"]
    lk(sp.outputs["Geometry"], sg.inputs["Geometry"])
    if kind == "starter":
        lk(sg.outputs["Geometry"], out.inputs["Geometry"])
        return ng
    # masque de pente
    nrm = N.new("GeometryNodeInputNormal"); nrm.location = (-300, -250)
    sep = N.new("ShaderNodeSeparateXYZ"); sep.location = (-100, -250)
    rad = N.new("ShaderNodeMath"); rad.location = (-300, -550)
    rad.operation = "RADIANS"
    cos = N.new("ShaderNodeMath"); cos.location = (-100, -550)
    cos.operation = "COSINE"
    gt = N.new("ShaderNodeMath"); gt.location = (100, -400)
    gt.operation = "GREATER_THAN"
    lk(nrm.outputs["Normal"], sep.inputs["Vector"])
    lk(gi.outputs["Max Slope"], rad.inputs[0]); lk(rad.outputs["Value"], cos.inputs[0])
    lk(sep.outputs["Z"], gt.inputs[0]); lk(cos.outputs["Value"], gt.inputs[1])
    ds = N.new("GeometryNodeDistributePointsOnFaces"); ds.location = (300, 200)
    ds.distribute_method = "POISSON"
    ds.inputs["Distance Min"].default_value = 0.5
    lk(sg.outputs["Geometry"], ds.inputs["Mesh"])
    lk(gi.outputs["Density"], ds.inputs["Density Max"])
    if kind != "seed_unused":
        lk(gi.outputs["Seed"], ds.inputs["Seed"])
    if kind != "no_slope":
        lk(gt.outputs["Value"], ds.inputs["Density Factor"])
    # arbres
    variants = [(0.2, 0.8), (0.3, 1.2), (0.4, 1.8)] if kind != "no_variation" else [(0.3, 1.2)]
    gti = N.new("GeometryNodeGeometryToInstance"); gti.location = (300, -200)
    for k, (r_, d_) in enumerate(variants):
        c = N.new("GeometryNodeMeshCone"); c.location = (-300, -800 - 250 * k)
        c.inputs["Radius Bottom"].default_value = r_
        c.inputs["Depth"].default_value = d_
        st = N.new("GeometryNodeSetMaterial"); st.location = (150, -800 - 250 * k)
        st.inputs["Material"].default_value = bpy.data.materials["MAT_Tree"]
        if kind == "floating":                                   # le Cone a sa BASE à z = 0 : aucune translation n'est nécessaire ; ici on le relève à tort
            t = N.new("GeometryNodeTransform"); t.location = (-50, -800 - 250 * k)
            t.inputs["Translation"].default_value = (0, 0, 0.5)
            lk(c.outputs["Mesh"], t.inputs["Geometry"])
            lk(t.outputs["Geometry"], st.inputs["Geometry"])
        else:
            lk(c.outputs["Mesh"], st.inputs["Geometry"])
        lk(st.outputs["Geometry"], gti.inputs["Geometry"])
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (900, 100)
    lk(ds.outputs["Points"], io.inputs["Points"])
    lk(gti.outputs["Instances"], io.inputs["Instance"])
    lk(ds.outputs["Rotation"], io.inputs["Rotation"])
    io.inputs["Pick Instance"].default_value = True
    ri = N.new("FunctionNodeRandomValue"); ri.location = (500, -200)
    ri.data_type = "INT"
    ints = [i for i in ri.inputs if i.enabled and i.type == "INT"]
    ints[0].default_value, ints[1].default_value = 0, max(len(variants) - 1, 0)
    lk([o for o in ri.outputs if o.enabled][0], io.inputs["Instance Index"])
    if kind != "no_scale":
        rs = N.new("FunctionNodeRandomValue"); rs.location = (500, -450)
        rs.data_type = "FLOAT"
        fl = [i for i in rs.inputs if i.enabled and i.type == "VALUE"]
        fl[0].default_value, fl[1].default_value = 0.8, 1.2
        lk([o for o in rs.outputs if o.enabled][0], io.inputs["Scale"])
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (1400, 0)
    lk(sg.outputs["Geometry"], jn.inputs["Geometry"])
    lk(io.outputs["Instances"], jn.inputs["Geometry"])
    lk(gi.outputs["Geometry"], jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], out.inputs["Geometry"])
    return ng


def build(kind):
    L.reset("SC_GN7")
    L.studio(subject_height=2.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -40.0, 17.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.5))
    cam2 = L.camera("CAM_High", c, (20.0, -20.0, 28.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.5))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    me = bpy.data.meshes.new("ME_GEO_Forest")
    me.from_pydata([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("GEO_Forest", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, 3.0)
    mg = bpy.data.materials.new("MAT_Ground")
    mg.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.35, 0.30, 0.18, 1)
    mt = bpy.data.materials.new("MAT_Tree")
    mt.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.10, 0.32, 0.10, 1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_07_scattering_starter.blend"))
    for k in ("no_slope", "no_variation", "seed_unused", "no_scale", "floating"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_07_scattering_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_07_scattering_solution.blend"))
    views(sc, os.path.join(out_dir, "ch05_07_scattering_reference.png"))


if __name__ == "__main__":
    L.run(main)
