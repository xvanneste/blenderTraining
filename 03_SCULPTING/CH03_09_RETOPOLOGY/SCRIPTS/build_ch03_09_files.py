"""
build_ch03_09_files.py — « Retopologie personnage » (CH03.09 : boucles faciales, articulations, densité).

Cible : le visage sculpté de CH03.06 (SCULPT_Bust haute densité, ≈ 75 000 faces).
  STARTER_FILES/ch03_09_retopo_starter.blend : le visage sculpté + yeux, sans retopo.
  COMPLETED_EXAMPLES/ch03_09_retopo_solution.blend (+ _reference.png : face, 3/4, profil)
      RETOPO_Face : maillage tout en QUADS, ≈ 1 cm de maille, rangées resserrées autour des deux yeux et de la bouche
      (boucles concentriques), trous aux yeux et à la bouche, projeté sur le sculpt par Shrinkwrap (Project) puis appliqué.
      Construit en 2D (grille + Inset Region) puis projeté : le même principe que le Poly Build + Shrinkwrap de l'interface.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : uniform (grille sans boucles), triangulated, floating (non projeté),
      too_dense (subdivisé), misplaced (boucles décalées de 3 cm)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_09_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "CH03_06_FACES", "COMPLETED_EXAMPLES", "ch03_06_face_solution.blend"))
NOTE = """CH03.09 — LA RETOPOLOGIE DU VISAGE (vues : Num 1 face, Num 3 profil)
But : un maillage léger (≈ 400 quads) qui épouse le sculpt SCULPT_Bust, avec des BOUCLES autour des yeux et de la bouche.
1. Nouvel objet RETOPO_Face (Add > Mesh > Grid ou Poly Build) devant le visage ; vue de face.
2. Faces plus petites et boucles concentriques autour des deux yeux et de la bouche (Inset Faces, Loop Cut) ; des trous aux yeux
   et à la bouche (supprimez les faces centrales).
3. Collez-le au sculpt : modificateur Shrinkwrap (Wrap Method : Project, axe Y coché, Positive coché, cible SCULPT_Bust, Offset 0,002 m)
   puis Apply ; ou accrochage (Snap) sur les faces du sculpt pendant la construction.
4. Tout en quads ; peu de pôles ; ≈ 300–2 500 faces.
Vérification : SCRIPTS/validate_ch03_09.py -- --exercise retopo
"""
EYE_X, EYE_Z, MOUTH_Z = 0.032, 0.385, 0.3085
GX, GZ0, GZ1 = 0.095, 0.25, 0.47
NX, NZ = 25, 30                       # cellules de ≈ 7,5 mm
PLANE_Y = -0.20


def base_scene():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    for n in ("REF_Base",):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    for n in ("README_EXERCICE",):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    return sc


def template(loops=True, holes=True, shift=0.0):
    """Grille 2D de 1 cm, resserrée autour des yeux et de la bouche par Inset Region, puis trous."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=NX, y_segments=NZ, size=0.5)
    # create_grid : [-0.5, 0.5]² -> étirement vers GX × (GZ1-GZ0)/2
    for v in bm.verts:
        v.co.x = v.co.x * 2 * GX
        v.co.z, v.co.y = (GZ0 + GZ1) / 2 + v.co.y * (GZ1 - GZ0), PLANE_Y
    bm.faces.ensure_lookup_table()
    if loops:
        def sel(center, rx, rz):
            return [f for f in bm.faces if abs(f.calc_center_median().x - center[0]) <= rx and abs(f.calc_center_median().z - center[1]) <= rz]
        regions = [sel((EYE_X + shift, EYE_Z), 0.0105, 0.0105), sel((-EYE_X + shift, EYE_Z), 0.0105, 0.0105), sel((shift, MOUTH_Z), 0.0255, 0.0055)]
        centers = []
        for faces in regions:
            if not faces:
                continue
            # inset_region renvoie les faces de l'ANNEAU ; la région d'origine (`faces`) devient le centre : c'est elle qu'on retient
            bmesh.ops.inset_region(bm, faces=faces, thickness=0.0035, depth=0.0, use_even_offset=True, use_boundary=True)
            bmesh.ops.inset_region(bm, faces=faces, thickness=0.0030, depth=0.0, use_even_offset=True, use_boundary=True)
            centers.append(faces)
        if holes:
            for fs in centers:
                bmesh.ops.delete(bm, geom=[f for f in fs if f.is_valid], context="FACES")
    me = bpy.data.meshes.new("ME_RETOPO_Face")
    bm.to_mesh(me)
    bm.free()
    return me


def add_retopo(kind):
    sc = bpy.context.scene
    me = template(loops=kind not in ("uniform",), holes=kind not in ("uniform",), shift=0.03 if kind == "misplaced" else 0.0)
    bust = bpy.data.objects["SCULPT_Bust"]
    # on ne garde que les faces dont les 4 sommets tombent sur une surface tournée vers l'avant (normale vers −Y) :
    # sinon des quads s'étirent entre le plan de départ et le côté de la tête
    from mathutils.bvhtree import BVHTree
    bvh = BVHTree.FromPolygons([bust.matrix_world @ v.co for v in bust.data.vertices], [tuple(p.vertices) for p in bust.data.polygons])
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    def protected(x, z):          # yeux et bouche : on garde même si la paroi est inclinée
        return (math.hypot(x - EYE_X, z - EYE_Z) < 0.032 or math.hypot(x + EYE_X, z - EYE_Z) < 0.032
                or (abs(x) < 0.040 and abs(z - MOUTH_Z) < 0.016))
    good = {}
    for v in bm.verts:
        loc, nor, _i, _d = bvh.ray_cast(Vector(v.co), Vector((0, 1, 0)))
        inside = (v.co.x / 0.070) ** 2 + ((v.co.z - 0.36) / 0.112) ** 2 <= 1.0
        core = (v.co.x / 0.056) ** 2 + ((v.co.z - 0.36) / 0.098) ** 2 <= 1.0       # cœur du visage (nez, joues) : pas de filtre d'inclinaison
        good[v.index] = loc is not None and inside and (nor.y < -0.45 or core or protected(v.co.x, v.co.z))
    bad_faces = [f for f in bm.faces if not all(good[v.index] for v in f.verts)]
    bmesh.ops.delete(bm, geom=bad_faces, context="FACES")
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("RETOPO_Face", me)
    sc.collection.objects.link(ob)
    if kind != "floating":
        sw = ob.modifiers.new("Shrinkwrap", "SHRINKWRAP")
        sw.target = bust
        sw.wrap_method = "PROJECT"
        sw.use_project_x = sw.use_project_z = False
        sw.use_project_y = True
        sw.use_negative_direction = False
        sw.use_positive_direction = True
        sw.cull_face = "OFF"
        sw.offset = 0.002
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.ops.object.modifier_apply(modifier="Shrinkwrap")
    if kind == "triangulated":
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        bm.to_mesh(ob.data)
        bm.free()
    if kind == "too_dense":
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        for _ in range(2):
            bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
        bm.to_mesh(ob.data)
        bm.free()
    ob.data.materials.append(L.material("MAT_Retopo", (0.2, 0.5, 0.9), 0.5))
    wm = ob.modifiers.new("Wire", "WIREFRAME") if False else None
    ob.show_wire = True
    ob.show_in_front = False
    return ob


def views(out):
    sc = bpy.context.scene
    cam = bpy.data.objects["CAM_Front"]
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 600, 600
    sc.render.resolution_percentage = 100
    for n in ("GP_Guide",):
        o = bpy.data.objects.get(n)
        if o:
            o.hide_render = True
    bust = bpy.data.objects["SCULPT_Bust"]
    bust.hide_render = False
    # rendu de référence uniquement (après la sauvegarde) : copie en fil de fer du retopo pour voir les boucles
    rt = bpy.data.objects["RETOPO_Face"]
    wv = rt.copy()
    wv.data = rt.data.copy()
    wv.name = "WIRE_VIEW"
    sc.collection.objects.link(wv)
    wm = wv.modifiers.new("Wire", "WIREFRAME")
    wm.thickness = 0.0007
    wv.data.materials.clear()
    wv.data.materials.append(L.material("MAT_WireView", (0.05, 0.35, 0.95), 0.4))
    rt.hide_render = True
    tiles = []
    for loc in ((0, -0.62, 0.36), (0.43, -0.45, 0.38), (0.62, 0, 0.36)):
        cam.location = loc
        cam.rotation_euler = (Vector((0, 0, 0.36)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 85
        p = os.path.join(bpy.app.tempdir, "v.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def save(path):
    L.instructions(NOTE)
    L.save(path)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    base_scene()
    save(os.path.join(CH, "STARTER_FILES", "ch03_09_retopo_starter.blend"))
    for kind in ("uniform", "triangulated", "floating", "too_dense", "misplaced"):
        base_scene()
        add_retopo(kind)
        save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_09_retopo_{kind}.blend"))
    base_scene()
    add_retopo("solution")
    save(os.path.join(out, "ch03_09_retopo_solution.blend"))
    views(os.path.join(out, "ch03_09_retopo_reference.png"))


if __name__ == "__main__":
    L.run(main)
