"""
build_p8_reference.py — Scène de référence du projet P8 « Une séquence d'action » (10 s : un mur s'effondre, la poussière et un drapeau suivent le vent).

Assemble les simulations de la phase 8 (mêmes réglages que dans les chapitres) :
  - destruction (CH08.07) : Ground Passive 14 × 14 m ; mur de 24 briques Brick_i_k + 38 contraintes Fixed cassables (seuil 1) ; boulet Wreck_Ball (40 kg, Animated de 1 à 60, lâché à l'image 61) ; monde 30 sous-étapes ;
  - tissu (CH08.03) : Flag (grille 16 × 16 de 1,5 m, plan y–z à x = 3,5 m), arête du haut épinglée par le groupe « pin » ;
  - particules (CH08.04) : Dust (150 particules, images 30–70, vie 120) ;
  - forces (CH08.09) : FORCE_Wind (force 100, vers +X) ; poids : tissu 1, poussière 0,01, monde de corps rigides 0 (le vent ne touche pas le mur) ;
  Images 1–240 (10 s à 24 i/s). Planche renders/p8_contact_sheet.png : images 20, 60, 100 et 180 (Workbench, 480 × 270), côte à côte (1 920 px).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p8_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

OUT = os.path.join(HERE, "REFERENCE")
SHEET_FRAMES = (20, 60, 100, 180)


def box(name, size, loc, color=None):
    sc = bpy.context.scene
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    sc.collection.objects.link(ob)
    ob.location = loc
    if color:
        ob.color = color
    return ob


def sel(*obs, active=None):
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or obs[0]


def build():
    L.reset("SC_P8")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 240
    # --- destruction
    bpy.ops.rigidbody.world_add()
    w = sc.rigidbody_world
    w.substeps_per_frame, w.solver_iterations = 30, 30
    w.point_cache.frame_start, w.point_cache.frame_end = 1, 240
    w.effector_weights.wind = 0.0
    g = box("Ground", (14, 14, 0.2), (0, 0, -0.1), (0.35, 0.36, 0.4, 1))
    sel(g)
    bpy.ops.rigidbody.object_add()
    g.rigid_body.type = "PASSIVE"
    grid = {}
    for i in range(6):
        for k in range(4):
            grid[(i, k)] = box(f"Brick_{i}_{k}", (0.5, 0.3, 0.5), (-1.25 + 0.5 * i, 0, 0.25 + 0.5 * k), (0.9, 0.5, 0.25 + 0.05 * k, 1))
    sel(*grid.values())
    bpy.ops.rigidbody.objects_add(type="ACTIVE")
    for b in grid.values():
        rb = b.rigid_body
        rb.mass, rb.friction, rb.collision_margin, rb.collision_shape = 1.0, 0.6, 0.0, "BOX"
    ball = box("Wreck_Ball", (0.6, 0.6, 0.6), (0, -5, 0.9), (0.15, 0.15, 0.18, 1))
    sel(ball)
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
    for (i, k), b in grid.items():
        for di, dk in ((1, 0), (0, 1)):
            n = grid.get((i + di, k + dk))
            if n:
                sel(b, n, active=b)
                bpy.ops.rigidbody.connect(con_type="FIXED", pivot_type="CENTER", connection_pattern="SELECTED_TO_ACTIVE")
    for o in sc.objects:
        if o.rigid_body_constraint:
            o.rigid_body_constraint.use_breaking = True
            o.rigid_body_constraint.breaking_threshold = 1.0
    # --- drapeau (tissu)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=16, y_segments=16, size=0.75)
    for v in bm.verts:
        v.co = (0, v.co.x, v.co.y)
    me = bpy.data.meshes.new("ME_Flag")
    bm.to_mesh(me)
    bm.free()
    flag = bpy.data.objects.new("Flag", me)
    sc.collection.objects.link(flag)
    flag.location = (3.5, 2.0, 2.0)
    flag.color = (0.2, 0.5, 0.95, 1)
    vg = flag.vertex_groups.new(name="pin")
    for v in me.vertices:
        if v.co.z > 0.74:
            vg.add([v.index], 1.0, "REPLACE")
    cs = flag.modifiers.new("Cloth", "CLOTH").settings
    cs.quality, cs.bending_stiffness, cs.air_damping = 8, 0.4, 1.0
    cs.vertex_group_mass = "pin"
    # --- poussière (particules)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=0.3)
    me = bpy.data.meshes.new("ME_Dust")
    bm.to_mesh(me)
    bm.free()
    dust = bpy.data.objects.new("Dust", me)
    sc.collection.objects.link(dust)
    dust.location = (0, 0, 0.15)
    dust.modifiers.new("Particles", "PARTICLE_SYSTEM")
    st = dust.particle_systems[0].settings
    st.count = 150
    st.frame_start, st.frame_end = 30, 70
    st.lifetime = 120
    st.emit_from = "FACE"
    st.normal_factor = 1.0
    st.physics_type = "NEWTON"
    st.effector_weights.gravity = 0.1
    st.effector_weights.wind = 0.01
    mote = box("DustMote", (0.07, 0.07, 0.07), (0, 0, 0), (0.85, 0.8, 0.7, 1))
    sc.collection.objects.unlink(mote)
    st.render_type = "OBJECT"
    st.instance_object = mote
    st.particle_size = 1.0
    dust.show_instancer_for_render = False
    dust.show_instancer_for_viewport = False
    # --- vent
    bpy.ops.object.effector_add(type="WIND", location=(0, 0, 1), rotation=(0, math.radians(90), 0))
    wd = bpy.context.object
    wd.name = "FORCE_Wind"
    wd.field.strength = 100.0
    # --- caméra (Workbench)
    tgt = bpy.data.objects.new("EMP_Target", None)
    sc.collection.objects.link(tgt)
    tgt.location = (1.8, 0.8, 1.2)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (9.0, -5.5, 3.6)
    cam.data.lens = 35
    c = cam.constraints.new("TRACK_TO")
    c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_P8")
    wo.color = (0.55, 0.68, 0.85)
    sc.world = wo
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 480, 270, 100
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.object.select_all(action="DESELECT")
    return grid


def main():
    build()
    sc = bpy.context.scene
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    tiles = {}
    sc.frame_set(1)
    for f in range(1, max(SHEET_FRAMES) + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in SHEET_FRAMES:
            path = os.path.join(OUT, "renders", f"_tmp_{f}.png")
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
            img = bpy.data.images.load(path)
            tiles[f] = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], 4)
            bpy.data.images.remove(img)
            os.remove(path)
    sheet = np.concatenate([tiles[f] for f in SHEET_FRAMES], axis=1)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0], alpha=False)
    out.pixels = sheet.ravel()
    out.filepath_raw = os.path.join(OUT, "renders", "p8_contact_sheet.png")
    out.file_format = "PNG"
    out.save()
    sc.frame_set(1)
    L.instructions("P8 — scène de référence : voir build_p8_reference.py.")
    L.save(os.path.join(OUT, "p8_scene_reference.blend"))


if __name__ == "__main__":
    L.run(main)
