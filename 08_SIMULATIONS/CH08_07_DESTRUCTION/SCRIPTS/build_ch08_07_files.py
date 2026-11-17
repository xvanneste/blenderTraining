"""
build_ch08_07_files.py — « Destruction » (CH08.07 : un mur de briques relié par des contraintes cassables, frappé par un boulet).

Scène : Ground (dalle de 12 × 12 m, Passive), 24 briques Brick_i_k (6 colonnes i × 4 rangées k, 0,5 × 0,3 × 0,5 m, Active, masse 1, friction 0,6, Box, marge 0),
        Wreck_Ball (cube de 0,6 m, 40 kg, Animated 1 → 60, déplacé de y = −5 à y = 2 entre les images 1 et 60, puis lâché à l'image 61).
  Monde : images 1–120, 30 sous-étapes, 30 itérations du solveur (une boule trop rapide ou trop peu de sous-étapes FAIT EXPLOSER le mur : mesuré, voir THEORY).
  Solution : 38 contraintes « Fixed » (Physics > Rigid Body > Connect, une paire de briques voisines à la fois : horizontales et verticales),
             chacune avec Breaking cochée et un seuil (Breaking Threshold) de 1,0.
  Mesures de la solution : 12 à 13 liaisons sur 38 cassées à l'image 120 (distance entre voisines modifiée de plus de 10 cm) ; seuil 5 ou plus : 0 liaison cassée (le mur est poussé d'un bloc).
  STARTER_FILES/ch08_07_destruction_starter.blend : sol, briques actives, boulet animé, monde réglé ; AUCUNE contrainte.
  COMPLETED_EXAMPLES/ch08_07_destruction_solution.blend (+ _reference.png : vue de dessus des briques à l'image 120, solution à gauche, seuil trop haut à droite)
  COUNTER_EXAMPLES/ : no_breaking, high_threshold, no_constraints, no_ground
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_07_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.07 — DESTRUCTION (Ground, Brick_i_k, Wreck_Ball)
Un mur de 24 briques doit être relié par des contraintes cassables ; un boulet de 40 kg le frappe : le mur doit se fracturer en morceaux (sans tout disperser).
1. Sélectionnez deux briques voisines (la seconde active) : Physics > Rigid Body > Connect (menu Object > Rigid Body > Connect), Type Fixed, Location Center, Connection Pattern Selected to Active. Répétez pour chaque paire voisine (horizontale et verticale : 38 paires).
2. Pour chaque contrainte : onglet Physics de l'objet Constraint > Settings : Breaking coché, Threshold 1.
3. Ne touchez pas au monde (30 sous-étapes, images 1–120) ni au boulet.
Le correcteur simule 120 images : liaisons cassées entre 8 et 30 sur 38, aucune brique sous le sol.
Vérification : SCRIPTS/validate_ch08_07.py -- --exercise destruction
"""


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def select_only(*obs, active=None):
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or obs[0]


def build(kind):
    L.reset("SC_DESTRUCTION")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 120
    bpy.ops.rigidbody.world_add()
    w = sc.rigidbody_world
    w.substeps_per_frame, w.solver_iterations = 30, 30
    w.point_cache.frame_start, w.point_cache.frame_end = 1, 120
    ground = box("Ground", (12, 12, 0.2), (0, 0, -0.1))
    if kind != "no_ground":
        select_only(ground)
        bpy.ops.rigidbody.object_add()
        ground.rigid_body.type = "PASSIVE"
    grid = {}
    for i in range(6):
        for k in range(4):
            grid[(i, k)] = box(f"Brick_{i}_{k}", (0.5, 0.3, 0.5), (-1.25 + 0.5 * i, 0, 0.25 + 0.5 * k))
    select_only(*grid.values())
    bpy.ops.rigidbody.objects_add(type="ACTIVE")
    for b in grid.values():
        rb = b.rigid_body
        rb.mass, rb.friction, rb.collision_margin, rb.collision_shape = 1.0, 0.6, 0.0, "BOX"
    ball = box("Wreck_Ball", (0.6, 0.6, 0.6), (0, -5, 0.9))
    select_only(ball)
    bpy.ops.rigidbody.object_add()
    ball.rigid_body.mass, ball.rigid_body.collision_shape = 40.0, "BOX"
    ball.rigid_body.kinematic = True
    ball.rigid_body.keyframe_insert("kinematic", frame=1)
    ball.location = (0, -5, 0.9)
    ball.keyframe_insert("location", frame=1)
    ball.location = (0, 2.0, 0.9)
    ball.keyframe_insert("location", frame=60)
    ball.rigid_body.kinematic = False
    ball.rigid_body.keyframe_insert("kinematic", frame=61)
    if kind not in ("starter", "no_constraints"):
        for (i, k), b in grid.items():
            for di, dk in ((1, 0), (0, 1)):
                n = grid.get((i + di, k + dk))
                if n:
                    select_only(b, n, active=b)
                    bpy.ops.rigidbody.connect(con_type="FIXED", pivot_type="CENTER", connection_pattern="SELECTED_TO_ACTIVE")
        for o in sc.objects:
            rc = o.rigid_body_constraint
            if rc:
                rc.use_breaking = kind != "no_breaking"
                rc.breaking_threshold = 20.0 if kind == "high_threshold" else 1.0
    bpy.ops.object.select_all(action="DESELECT")
    sc.frame_set(1)
    L.instructions(NOTE)
    return grid


def simulate(grid, last=120):
    sc = bpy.context.scene
    sc.frame_set(1)
    for f in range(1, last + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    return {key: b.matrix_world.translation.copy() for key, b in grid.items()}


def sketch(path):
    a = simulate(build("solution"))
    b = simulate(build("high_threshold"))
    W, H = 780, 360
    img = np.full((H, W, 3), 0.08, np.float32)
    S = 50
    for panel, pos in enumerate((a, b)):
        ox, oy = panel * 390 + 195, 40
        for (i, k), p in pos.items():
            r0 = Vector((-1.25 + 0.5 * i, 0, 0))
            x0, y0 = int(ox + S * r0.x), int(oy + S * r0.y)
            img[max(y0 - 4, 0):y0 + 5, max(x0 - 12, 0):x0 + 13] = (0.35, 0.35, 0.35)
            x1, y1 = int(ox + S * p.x), int(oy + S * p.y)
            col = (0.95, 0.55, 0.2) if p.z < 0.3 else (0.4, 0.8, 1.0)
            if 0 <= x1 < W - 13 and 0 <= y1 < H - 13:
                img[y1 - 4:y1 + 5, max(x1 - 12, 0):x1 + 13] = col
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_07_destruction_starter.blend"))
    for k in ("no_breaking", "high_threshold", "no_constraints", "no_ground"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_07_destruction_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_07_destruction_solution.blend"))
    sketch(os.path.join(out, "ch08_07_destruction_reference.png"))


if __name__ == "__main__":
    L.run(main)
