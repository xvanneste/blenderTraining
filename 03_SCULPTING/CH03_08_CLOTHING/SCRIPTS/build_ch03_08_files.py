"""
build_ch03_08_files.py — « Vêtements » (CH03.08 : plis, tension, workflow de simulation de tissu).

Workflow enseigné (et exécuté ici en arrière-plan) :
  1. un corps (le buste de CH03.05) + un COLLIDER simplifié (Decimate) avec le modificateur Collision ; le sol collisionne aussi ;
  2. un tissu = grille trouée (col du cou) à 1,6 cm de maille, posée au-dessus des épaules ;
  3. modificateur Cloth (masse, rigidités, distance de collision, auto-collision) ; on joue la simulation ; on APPLIQUE le
     modificateur à l'image où le tissu est au repos ;
  4. on contrôle : pas de pénétration, tissu non étiré, couvre les épaules, plis.
  STARTER_FILES/ch03_08_poncho_starter.blend : buste + COLLIDER + tissu PLAT (sans simulation).
  COMPLETED_EXAMPLES/ch03_08_poncho_solution.blend (+ _reference.png : face, 3/4, profil)
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : penetrating, smoothed, stretched, tiny (+ le starter plat)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_08_files.py
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
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402

CH = L.chapter_dir(__file__)
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "CH03_05_REALISTIC", "COMPLETED_EXAMPLES", "ch03_05_bust_solution.blend"))
NOTE = """CH03.08 — LE PONCHO (simulation de tissu)
1. COLLIDER (corps simplifié, modificateur Collision) et sol (Collision) sont prêts. CLOTH_Poncho est un tissu plat troué au col.
2. Sur CLOTH_Poncho : Physics > Cloth. Quality Steps 12 ; Physical Properties : Vertex Mass 0,3, Air Viscosity 2 ;
   Stiffness : Tension 15, Compression 15, Shear 5, Bending 0,4 ; Damping : Tension 5, Compression 5, Shear 5, Bending 0,5 ;
   Collisions : Quality 5 ; Object Collisions : Distance 0,005 ; Self Collisions DÉCOCHÉES (elles font vibrer).
3. Lancez l'animation (Espace) jusqu'à l'image 120 : le tissu tombe sur les épaules et se pose au sol.
4. À l'image 120 : Object > Apply > Visual Geometry to Mesh, ou Ctrl+A sur le modificateur Cloth (APPLIQUEZ-le).
5. Vérification : SCRIPTS/validate_ch03_08.py -- --exercise poncho
"""
SIZE = 0.27            # demi-côté du tissu (m)
SEG = 33               # segments par côté -> maille 1,6 cm
REST = 2 * SIZE / SEG
HOLE = 0.07
FRAMES = 120


def base_scene():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    for n in ("GP_Guide", "README_EXERCICE"):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    bust = bpy.data.objects["SCULPT_Bust"]
    col = bust.copy()
    col.data = bust.data.copy()
    col.name, col.data.name = "COLLIDER", "ME_COLLIDER"
    sc.collection.objects.link(col)
    bpy.context.view_layer.objects.active = col
    m = col.modifiers.new("dec", "DECIMATE")
    m.ratio = 0.08
    bpy.ops.object.modifier_apply(modifier="dec")
    col.modifiers.new("Collision", "COLLISION")
    col.collision.thickness_outer = 0.002
    col.hide_render = True
    col.display_type = "WIRE"      # PAS hide_viewport : un objet masqué dans la vue n'est pas évalué, donc ne collisionne pas
    floor = bpy.data.objects["GEO_Floor"]
    floor.modifiers.new("Collision", "COLLISION")
    for n in ("EYE_L_Iris", "EYE_R_Iris"):
        pass
    sc.frame_start, sc.frame_end = 1, FRAMES
    sc.frame_set(1)
    return sc


def make_cloth(half=SIZE, seg=SEG, hole=HOLE, z=0.20):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=seg, y_segments=seg, size=half)
    bm.faces.ensure_lookup_table()
    kill = [f for f in bm.faces if math.hypot(f.calc_center_median().x, f.calc_center_median().y) < hole]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    me = bpy.data.meshes.new("ME_CLOTH_Poncho")
    bm.to_mesh(me)
    bm.free()
    cl = bpy.data.objects.new("CLOTH_Poncho", me)
    bpy.context.scene.collection.objects.link(cl)
    cl.location = (0, 0.01, z)
    cl["rest_edge"] = 2 * half / seg
    me.materials.append(L.material("MAT_Cloth", (0.55, 0.1, 0.08), 0.85))
    for p in me.polygons:
        p.use_smooth = True
    return cl


def simulate(cl):
    cm = cl.modifiers.new("Cloth", "CLOTH")
    s = cm.settings
    s.quality = 12
    s.mass = 0.3
    s.tension_stiffness = 15
    s.compression_stiffness = 15
    s.shear_stiffness = 5
    s.bending_stiffness = 0.4
    s.air_damping = 2.0
    s.tension_damping = 5.0
    s.compression_damping = 5.0
    s.shear_damping = 5.0
    s.bending_damping = 0.5
    cm.collision_settings.distance_min = 0.005
    cm.collision_settings.collision_quality = 5
    cm.collision_settings.use_self_collision = False
    sc = bpy.context.scene
    for f in range(1, FRAMES + 1):
        sc.frame_set(f)
    bpy.ops.object.select_all(action="DESELECT")
    cl.select_set(True)
    bpy.context.view_layer.objects.active = cl
    bpy.ops.object.modifier_apply(modifier="Cloth")
    for p in cl.data.polygons:
        p.use_smooth = True
    bpy.context.scene.frame_set(1)


def world_verts(o):
    return np.array([o.matrix_world @ v.co for v in o.data.vertices])


def set_verts(o, P):
    inv = o.matrix_world.inverted()
    for v, p in zip(o.data.vertices, P):
        v.co = inv @ Vector(p)
    o.data.update()


def body_bvh():
    b = bpy.data.objects["COLLIDER"]
    return BVHTree.FromPolygons([b.matrix_world @ v.co for v in b.data.vertices], [tuple(p.vertices) for p in b.data.polygons])


def variant_penetrating(cl):
    """Tissu repoussé de 1,5 cm vers l'intérieur du corps (pénétration)."""
    P = world_verts(cl)
    bvh = body_bvh()
    for i, p in enumerate(P):
        loc, nor, _i, d = bvh.find_nearest(Vector(p))
        if loc is not None and d < 0.05:
            P[i] = np.array(p) - np.array(nor) * 0.015 - (np.array(p) - np.array(loc)) * 0.0
            # on enfonce le point d'1,5 cm sous la surface la plus proche
            P[i] = np.array(loc) - np.array(nor) * 0.015
    set_verts(cl, P)


def variant_smoothed(cl):
    """Plis effacés par un lissage laplacien répété (tissu « en plastique »)."""
    me = cl.data
    n = len(me.vertices)
    P = world_verts(cl)
    E = np.empty(len(me.edges) * 2, dtype=np.int32)
    me.edges.foreach_get("vertices", E)
    a, b = E[0::2], E[1::2]
    deg = np.bincount(np.concatenate([a, b]), minlength=n).astype(float)
    deg[deg == 0] = 1
    border = np.zeros(n, bool)
    for e in bmesh_border(me):
        border[list(e)] = True
    for _ in range(60):
        acc = np.zeros_like(P)
        np.add.at(acc, a, P[b])
        np.add.at(acc, b, P[a])
        Q = acc / deg[:, None]
        P = np.where(border[:, None], P, P + 0.5 * (Q - P))
    # on repousse hors du corps pour ne pas introduire une pénétration
    bvh = body_bvh()
    for i, p in enumerate(P):
        loc, nor, _i, d = bvh.find_nearest(Vector(p))
        if loc is not None and (Vector(p) - loc).dot(nor) < 0.003:
            P[i] = np.array(loc) + np.array(nor) * 0.003
    set_verts(cl, P)


def bmesh_border(me):
    bm = bmesh.new()
    bm.from_mesh(me)
    out = [tuple(v.index for v in e.verts) for e in bm.edges if e.is_boundary]
    bm.free()
    return out


def variant_stretched(cl):
    P = world_verts(cl)
    P[:, 0] *= 1.6
    P[:, 1] *= 1.6
    set_verts(cl, P)


def views(out):
    sc = bpy.context.scene
    for n in ("COLLIDER",):
        bpy.data.objects[n].hide_render = True
    cam = bpy.data.objects["CAM_Front"]
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 500, 500
    sc.render.resolution_percentage = 100
    tiles = []
    for loc, tgt in (((0, -1.3, 0.35), (0, 0, 0.2)), ((0.9, -0.9, 0.55), (0, 0, 0.18)), ((1.3, 0, 0.3), (0, 0, 0.15))):
        cam.location = loc
        cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 50
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
    make_cloth()
    save(os.path.join(CH, "STARTER_FILES", "ch03_08_poncho_starter.blend"))
    for v in ("penetrating", "smoothed", "stretched", "tiny"):
        base_scene()
        if v == "tiny":
            cl = make_cloth(half=0.14, seg=17)
        else:
            cl = make_cloth()
        simulate(cl)
        {"penetrating": variant_penetrating, "smoothed": variant_smoothed, "stretched": variant_stretched, "tiny": lambda c: None}[v](cl)
        save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_08_poncho_{v}.blend"))
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] poncho retouché à la brosse (Blender 5.2 via MCP) conservé : non régénéré")
        return
    base_scene()              # repli : simulation seule, sans retouche
    cl = make_cloth()
    simulate(cl)
    save(os.path.join(out, "ch03_08_poncho_solution.blend"))
    views(os.path.join(out, "ch03_08_poncho_reference.png"))


if __name__ == "__main__":
    L.run(main)
