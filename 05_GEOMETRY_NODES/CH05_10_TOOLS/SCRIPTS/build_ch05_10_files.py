"""
build_ch05_10_files.py — « Optimisation et outils » (CH05.10).

Un OUTIL Geometry Nodes publié comme asset : « Scatter Cones » (arbre GN_ScatterCones), modificateur applicable à n'importe quel maillage.
  Interface : Geometry (entrée) · Density (Float 0,05–5, défaut 0,5 par m²) · Seed (Integer 0–1000) · Scale (Float 0,3–3, défaut 1)
  Arbre     : Distribute Points on Faces (Random ; Density ; Seed) sur la géométrie d'entrée -> Instance on Points (Instance = Cone 8 côtés, rayon 0,15, hauteur 0,6 ; Scale ← Scale)
              -> Join Geometry (géométrie d'entrée + instances) -> Group Output          (les instances ne sont PAS réalisées)
  Optimisation : cône à 8 côtés, instances conservées, Density bornée (max 5), valeurs par défaut sûres.
  Publication : is_modifier = True ; asset (description, auteur, licence, 2 tags, catalogue « Tools/Scatter ») ; blender_assets.cats.txt à côté du .blend.
  STARTER_FILES/ch05_10_tools_starter.blend : l'arbre fonctionne mais est LOURD (cône de 64 côtés, instances réalisées, Density sans borne) et n'est pas publié.
  COMPLETED_EXAMPLES/ch05_10_tools_solution.blend (+ blender_assets.cats.txt, _reference.png)
  COUNTER_EXAMPLES/ : heavy_cone, realized, unbounded, not_asset, no_catalog, not_modifier, ignores_input   (+ blender_assets.cats.txt)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch05_10_files.py
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
CAT_ID = "7c1d3e20-0000-4000-8000-0000000000a1"
NOTE = """CH05.10 — OPTIMISATION ET OUTILS (GEO_Base, outil GN_ScatterCones) : alléger puis PUBLIER l'outil
Le fichier de départ contient un outil qui fonctionne mais qui est lourd et non publié. À faire :
1. Alléger : cône à 8 côtés (au lieu de 64) ; supprimer Realize Instances (garder les instances) ; borner Density (min 0,05 ; max 5 ; défaut 0,5).
2. Outil : activer « Modifier » dans les options de l'arbre (is_modifier) ; l'arbre doit utiliser la géométrie d'entrée (Join Geometry avec elle).
3. Publier : Mark as Asset sur l'arbre ; description, auteur, licence, au moins 2 tags ; catalogue (fichier blender_assets.cats.txt à côté du .blend).
Le correcteur mesure : budget de sommets par instance, nombre d'instances par défaut et au maximum de Density, présence de Realize Instances, entrée utilisée, temps d'évaluation, métadonnées d'asset.
Vérification : SCRIPTS/validate_ch05_10.py -- --exercise tools
"""


def build_tree(kind):
    ng = bpy.data.node_groups.new("GN_ScatterCones", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    for name, typ, dv, mn, mx, desc in (("Density", "NodeSocketFloat", 0.5, 0.05, 1000.0 if kind in ("unbounded", "starter") else 5.0, "Nombre maximal de cônes par m²"),
                                       ("Seed", "NodeSocketInt", 0, 0, 1000, "Graine du tirage aléatoire"),
                                       ("Scale", "NodeSocketFloat", 1.0, 0.3, 3.0, "Échelle des cônes")):
        s = I.new_socket(name, in_out="INPUT", socket_type=typ)
        s.default_value, s.min_value, s.max_value, s.description = dv, mn, mx, desc
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-900, 0)
    out = N.new("NodeGroupOutput"); out.location = (1300, 0)
    ds = N.new("GeometryNodeDistributePointsOnFaces"); ds.location = (-500, 100)
    ds.distribute_method = "RANDOM"
    lk(gi.outputs["Geometry"], ds.inputs["Mesh"])
    lk(gi.outputs["Density"], ds.inputs["Density"])
    lk(gi.outputs["Seed"], ds.inputs["Seed"])
    cone = N.new("GeometryNodeMeshCone"); cone.location = (-500, -300)
    cone.inputs["Vertices"].default_value = 64 if kind in ("starter", "heavy_cone") else 8
    cone.inputs["Radius Bottom"].default_value = 0.15
    cone.inputs["Depth"].default_value = 0.6
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (0, 0)
    lk(ds.outputs["Points"], io.inputs["Points"])
    cm = N.new("GeometryNodeSetMaterial"); cm.location = (-250, -300)
    cm.inputs["Material"].default_value = bpy.data.materials["MAT_Cone"]
    lk(cone.outputs["Mesh"], cm.inputs["Geometry"])
    lk(cm.outputs["Geometry"], io.inputs["Instance"])
    lk(gi.outputs["Scale"], io.inputs["Scale"])
    last = io.outputs["Instances"]
    if kind in ("starter", "realized"):
        rz = N.new("GeometryNodeRealizeInstances"); rz.location = (400, 0)
        lk(last, rz.inputs["Geometry"])
        last = rz.outputs["Geometry"]
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (800, 0)
    if kind != "ignores_input":
        lk(gi.outputs["Geometry"], jn.inputs["Geometry"])
    lk(last, jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], out.inputs["Geometry"])
    ng.is_modifier = kind not in ("starter", "not_modifier")
    return ng


def publish(ng, kind):
    if kind in ("starter", "not_asset"):
        return
    ng.asset_mark()
    a = ng.asset_data
    a.description = "Disperse des cônes sur n'importe quel maillage (densité, graine, échelle)"
    a.author = "Blender Cinema Master Academy"
    a.license = "BCMA (usage personnel de formation)"
    a.tags.new("scatter")
    a.tags.new("instances")
    a.catalog_id = "" if kind == "no_catalog" else CAT_ID


def write_cats(folder):
    os.makedirs(folder, exist_ok=True)
    lines = ["# This is an Asset Catalog Definition file for Blender.", "#",
             "# Empty lines and lines starting with `#` will be ignored.",
             "# The first non-ignored line should be the version indicator.",
             '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"', "", "VERSION 1", "", f"{CAT_ID}:Tools/Scatter:Tools-Scatter"]
    with open(os.path.join(folder, "blender_assets.cats.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def build(kind):
    L.reset("SC_GN10")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -26.0, 11.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.0))
    cam2 = L.camera("CAM_High", c, (14.0, -14.0, 20.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, y_subdivisions=20, size=20.0, location=(0, 0, 0.02))
    ob = bpy.context.active_object
    ob.name = "GEO_Base"
    mt = bpy.data.materials.new("MAT_Cone")
    mt.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.10, 0.35, 0.12, 1)
    ng = build_tree(kind)
    publish(ng, kind)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch05_10_tools_starter.blend"))
    write_cats(os.path.join(out_dir, "COUNTER_EXAMPLES"))
    for k in ("heavy_cone", "realized", "unbounded", "not_asset", "no_catalog", "not_modifier", "ignores_input"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch05_10_tools_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch05_10_tools_solution.blend"))
    write_cats(out_dir)
    views(sc, os.path.join(out_dir, "ch05_10_tools_reference.png"))


if __name__ == "__main__":
    L.run(main)
