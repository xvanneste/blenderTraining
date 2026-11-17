"""
build_ch04_05_files.py — « Textures procédurales » (CH04.05).

Un mur de briques PROP_Wall (boîte 3 × 2 × 0,2 m, debout) et son matériau MAT_Brick, entièrement procédural (aucune image) :
  Texture Coordinate [Object] -> Brick Texture (Color1/Color2 : variation de briques, Mortar : joint clair, Scale, Mortar Size, Offset 0,5)
  Brick [Color] -> Base Color ; Brick [Fac] -> Bump [Height] (Invert) -> Normal du Principled (les joints en creux) ; Roughness 0,8.
  STARTER_FILES/ch04_05_procedural_starter.blend : Principled par défaut seul.
  COMPLETED_EXAMPLES/ch04_05_procedural_solution.blend (+ _reference.png : deux vues)
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : no_bump, bump_unlinked, flat_colors, mortar_same, huge_scale, no_stagger
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_05_files.py
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
from mathutils import Matrix  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH04.05 — TEXTURES PROCÉDURALES (PROP_Wall, matériau MAT_Brick)
Un mur de briques SANS image : tout vient de la Brick Texture.
1. Texture Coordinate [Object] -> Brick Texture (Scale entre 3 et 12 ; Mortar Size 0,005–0,1 ; décalage des rangées (Offset) entre 0,3 et 0,7).
2. Color1 et Color2 : deux briques voisines (rouge-brun), assez différentes pour varier ; Mortar : joint clair (luminance supérieure d'au moins 0,15).
3. Brick [Color] -> Base Color ; Roughness ≥ 0,6.
4. Brick [Fac] -> Bump [Height] (Invert, Strength 0,2–1,5) -> Normal du Principled : les joints sont en creux.
5. Aucun nœud orphelin.
Vérification : SCRIPTS/validate_ch04_05.py -- --exercise procedural
"""


def inp(node, ident):
    return next(i for i in node.inputs if i.identifier == ident)


def build_nodes(mat, kind):
    nt = mat.node_tree
    N = nt.nodes
    lk = nt.links.new
    b = N["Principled BSDF"]
    tc = N.new("ShaderNodeTexCoord"); tc.location = (-700, 0)
    br = N.new("ShaderNodeTexBrick"); br.location = (-450, 0)
    br.offset = 0.0 if kind == "no_stagger" else 0.5
    br.inputs["Scale"].default_value = 100.0 if kind == "huge_scale" else 3.0
    br.inputs["Mortar Size"].default_value = 0.03
    br.inputs["Mortar Smooth"].default_value = 0.1
    c1, c2 = (0.35, 0.10, 0.06, 1), (0.22, 0.07, 0.05, 1)
    mortar = (0.55, 0.52, 0.47, 1)
    if kind == "flat_colors":
        c2 = c1
    if kind == "mortar_same":
        mortar = (0.30, 0.10, 0.07, 1)
    br.inputs["Color1"].default_value = c1
    br.inputs["Color2"].default_value = c2
    br.inputs["Mortar"].default_value = mortar
    lk(tc.outputs["Object"], br.inputs["Vector"])
    lk(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.8
    if kind != "no_bump":
        bp = N.new("ShaderNodeBump"); bp.location = (-100, -250)
        bp.invert = kind != "raised_mortar"
        bp.inputs["Strength"].default_value = 0.8
        bp.inputs["Distance"].default_value = 0.02
        if kind != "bump_unlinked":
            lk(br.outputs["Fac"], bp.inputs["Height"])
        lk(bp.outputs["Normal"], b.inputs["Normal"])


def build(kind):
    L.reset("SC_PROC")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -5.5, 1.1), 50, make_active=True)
    S.look_at(cam, (0, 0, 1.0))
    cam2 = L.camera("CAM_Side", c, (4.0, -6.6, 2.4), 50, make_active=False)
    S.look_at(cam2, (0, 0, 1.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    mat = bpy.data.materials.new("MAT_Brick")
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.active_object
    ob.name = "PROP_Wall"
    ob.data.transform(Matrix.Diagonal((3.0, 2.0, 0.2, 1.0)))      # dimensions dans la géométrie : échelle de l'objet = 1
    ob.rotation_euler = (math.pi / 2, 0, 0)                          # debout : le local +z regarde la caméra (−y)
    ob.location = (0, 0, 1.0)
    ob.data.materials.append(mat)
    if kind != "starter":
        build_nodes(mat, kind)
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for cam in ("CAM_Front", "CAM_Side"):
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_05_procedural_starter.blend"))
    for k in ("no_bump", "bump_unlinked", "flat_colors", "mortar_same", "huge_scale", "no_stagger", "raised_mortar"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_05_procedural_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_05_procedural_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_05_procedural_reference.png"))


if __name__ == "__main__":
    L.run(main)
