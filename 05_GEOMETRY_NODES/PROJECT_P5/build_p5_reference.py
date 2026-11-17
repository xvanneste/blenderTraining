"""
build_p5_reference.py — Outil de RÉFÉRENCE du projet P5 : « Mini-ville » (arbre GN_City), publié comme asset.
Écrit dans 05_GEOMETRY_NODES/PROJECT_P5/REFERENCE/ :
  p5_tool_reference.blend (+ blender_assets.cats.txt, renders/p5_turnaround.png : trois réglages côte à côte)
Interface : Seed (Integer 0–1000) · Density (Float 0–1, défaut 0,7) · Style (Integer 0–2 : 0 immeubles, 1 tours, 2 barres) · Lots (Integer 3–20, défaut 10) · Lot Size (Float 5–30, défaut 12)
Arbre : Grid de Lots × Lots points (espacement Lot Size) -> Instance on Points
          (Selection ← Random Value booléen (Probability = Density ; Seed) ; Pick Instance ; Instance Index ← Style ;
           Scale ← Random Value vecteur (1, 1, 0,6 à 1,6 ; Seed) ; Rotation 0)
        Instance = Geometry to Instance de trois bâtiments (immeuble 8 × 8 × 12 m ; tour 5 × 5 × 28 m ; barre 14 × 5 × 8 m, bases à z = 0)
        -> Join Geometry (avec la géométrie d'entrée) -> Group Output (instances conservées)
Publication : is_modifier ; asset (description, auteur, licence, 2 tags, catalogue « Tools/City »).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p5_reference.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

OUT = os.path.join(HERE, "REFERENCE")
CAT_ID = "7c1d3e20-0000-4000-8000-0000000000b5"
PARAMS = [("Seed", "NodeSocketInt", 0, 0, 1000, "Graine du tirage aléatoire"),
          ("Density", "NodeSocketFloat", 0.7, 0.0, 1.0, "Proportion de parcelles construites"),
          ("Style", "NodeSocketInt", 0, 0, 2, "Style de bâtiment : 0 immeubles, 1 tours, 2 barres"),
          ("Lots", "NodeSocketInt", 10, 3, 20, "Nombre de parcelles par côté"),
          ("Lot Size", "NodeSocketFloat", 12.0, 5.0, 30.0, "Côté d'une parcelle en mètres")]


def enabled(node, kind):
    return [i for i in node.inputs if i.enabled and i.type == kind]


def build_tree():
    ng = bpy.data.node_groups.new("GN_City", "GeometryNodeTree")
    I = ng.interface
    I.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    I.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    for name, typ, dv, mn, mx, desc in PARAMS:
        s = I.new_socket(name, in_out="INPUT", socket_type=typ)
        s.default_value, s.min_value, s.max_value, s.description = dv, mn, mx, desc
    N, lk = ng.nodes, ng.links.new
    gi = N.new("NodeGroupInput"); gi.location = (-1800, 0)
    out = N.new("NodeGroupOutput"); out.location = (1700, 0)
    # parcelles : Grid centrée, espacement Lot Size
    grid = N.new("GeometryNodeMeshGrid"); grid.location = (-1300, 300)
    lm1 = N.new("ShaderNodeMath"); lm1.location = (-1600, 400); lm1.operation = "SUBTRACT"; lm1.inputs[1].default_value = 1.0
    sz = N.new("ShaderNodeMath"); sz.location = (-1450, 400); sz.operation = "MULTIPLY"
    lk(gi.outputs["Lots"], lm1.inputs[0]); lk(lm1.outputs["Value"], sz.inputs[0]); lk(gi.outputs["Lot Size"], sz.inputs[1])
    lk(sz.outputs["Value"], grid.inputs["Size X"]); lk(sz.outputs["Value"], grid.inputs["Size Y"])
    lk(gi.outputs["Lots"], grid.inputs["Vertices X"]); lk(gi.outputs["Lots"], grid.inputs["Vertices Y"])
    # bâtiments
    gti = N.new("GeometryNodeGeometryToInstance"); gti.location = (-700, -300)
    mat = bpy.data.materials["MAT_Building"]
    for k, (w_, d_, h_) in enumerate(((14, 5, 8), (5, 5, 28), (8, 8, 12))):   # ordre INVERSÉ : une multi-entrée est lue en sens inverse (indice 0 = immeuble)
        cb = N.new("GeometryNodeMeshCube"); cb.location = (-1300, -300 - 220 * k)
        cb.inputs["Size"].default_value = (w_, d_, h_)
        tr = N.new("GeometryNodeTransform"); tr.location = (-1050, -300 - 220 * k)
        tr.inputs["Translation"].default_value = (0, 0, h_ / 2)
        sm = N.new("GeometryNodeSetMaterial"); sm.location = (-850, -300 - 220 * k)
        sm.inputs["Material"].default_value = mat
        lk(cb.outputs["Mesh"], tr.inputs["Geometry"]); lk(tr.outputs["Geometry"], sm.inputs["Geometry"]); lk(sm.outputs["Geometry"], gti.inputs["Geometry"])
    io = N.new("GeometryNodeInstanceOnPoints"); io.location = (300, 100)
    lk(grid.outputs["Mesh"], io.inputs["Points"])
    lk(gti.outputs["Instances"], io.inputs["Instance"])
    io.inputs["Pick Instance"].default_value = True
    lk(gi.outputs["Style"], io.inputs["Instance Index"])
    # sélection : Random Value booléen (Probability = Density)
    rb = N.new("FunctionNodeRandomValue"); rb.location = (-200, -150)
    rb.data_type = "BOOLEAN"
    pr = [i for i in rb.inputs if i.enabled and i.type == "VALUE"][0]
    lk(gi.outputs["Density"], pr)
    lk(gi.outputs["Seed"], [i for i in rb.inputs if i.enabled and i.name == "Seed"][0])
    lk([o for o in rb.outputs if o.enabled][0], io.inputs["Selection"])
    # échelle verticale aléatoire 0,6–1,6 (vecteur)
    rv = N.new("FunctionNodeRandomValue"); rv.location = (-200, -450)
    rv.data_type = "FLOAT_VECTOR"
    vv = enabled(rv, "VECTOR")
    vv[0].default_value, vv[1].default_value = (1.0, 1.0, 0.6), (1.0, 1.0, 1.6)
    lk(gi.outputs["Seed"], [i for i in rv.inputs if i.enabled and i.name == "Seed"][0])
    lk([o for o in rv.outputs if o.enabled][0], io.inputs["Scale"])
    jn = N.new("GeometryNodeJoinGeometry"); jn.location = (1000, 0)
    lk(gi.outputs["Geometry"], jn.inputs["Geometry"])
    lk(io.outputs["Instances"], jn.inputs["Geometry"])
    lk(jn.outputs["Geometry"], out.inputs["Geometry"])
    ng.is_modifier = True
    ng.asset_mark()
    a = ng.asset_data
    a.description = "Mini-ville procédurale : parcelles, densité, style de bâtiment, graine"
    a.author = "Blender Cinema Master Academy"
    a.license = "BCMA (usage personnel de formation)"
    a.tags.new("ville")
    a.tags.new("procédural")
    a.catalog_id = CAT_ID
    return ng


def write_cats(folder):
    lines = ["# This is an Asset Catalog Definition file for Blender.", "#",
             "# Empty lines and lines starting with `#` will be ignored.",
             "# The first non-ignored line should be the version indicator.",
             '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"', "", "VERSION 1", "", f"{CAT_ID}:Tools/City:Tools-City"]
    with open(os.path.join(folder, "blender_assets.cats.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def set_param(md, ng, name, value):
    item = next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == name)
    md.properties.inputs[item.identifier]["value"] = value


def main():
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    L.reset("SC_P5")
    L.studio(subject_height=20.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_High", c, (140.0, -140.0, 120.0), 35, make_active=True)
    cam.data.clip_end = 2000.0                           # la ville fait ≈ 110 m : au-delà du clip par défaut (100 m)
    S.look_at(cam, (0, 0, 0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 640, 360
    sc.render.resolution_percentage = 100
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = "GEO_City"
    mb = bpy.data.materials.new("MAT_Building")
    mb.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.62, 0.58, 0.52, 1)
    ng = build_tree()
    md = ob.modifiers.new("GeometryNodes", "NODES")
    md.node_group = ng
    L.instructions("P5 — référence : outil « Mini-ville » (voir build_p5_reference.py)")
    L.save(os.path.join(OUT, "p5_tool_reference.blend"))
    write_cats(OUT)
    tiles = []
    for params in ({"Style": 0, "Density": 0.7, "Seed": 0}, {"Style": 1, "Density": 0.35, "Seed": 3}, {"Style": 2, "Density": 0.9, "Seed": 8}):
        for k, v in params.items():
            set_param(md, ng, k, v)
        ob.update_tag()
        bpy.context.view_layer.update()
        p = os.path.join(bpy.app.tempdir, f"c{len(tiles)}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = os.path.join(OUT, "renders", "p5_turnaround.png")
    img.file_format = "PNG"
    img.save()
    for k, v in (("Style", 0), ("Density", 0.7), ("Seed", 0)):
        set_param(md, ng, k, v)
    L.save(os.path.join(OUT, "p5_tool_reference.blend"))


if __name__ == "__main__":
    L.run(main)
