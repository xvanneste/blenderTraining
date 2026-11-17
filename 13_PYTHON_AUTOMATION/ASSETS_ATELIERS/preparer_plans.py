"""Blender 5.3. Prépare deux plans depuis la scène du présentoir CH13.03."""
import bpy
from mathutils import Vector

scene = bpy.context.scene
if bpy.data.collections.get("COL_Plans"):
    raise RuntimeError("Repartez d’une copie du présentoir CH13.03.")
plans = bpy.data.collections.new("COL_Plans")
scene.collection.children.link(plans)
for name, position, target, scale, start in (
    ("PLAN_010", (4.1, -6.6, 4.7), (0, .55, .4), 5.7, 1),
    ("PLAN_020", (2.9, -2.8, 2.4), (1.12, 1.12, .52), 2.2, 25),
):
    data = bpy.data.cameras.new(name)
    data.type = "ORTHO"
    data.ortho_scale = scale
    camera = bpy.data.objects.new(name, data)
    plans.objects.link(camera)
    camera.location = position
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    marker = scene.timeline_markers.new(name, frame=start)
    marker.camera = camera
scene.camera = plans.objects["PLAN_010"]
scene.frame_start, scene.frame_end = 1, 48
scene.render.fps = 24
scene.render.resolution_x, scene.render.resolution_y = 640, 360
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.frame_set(1)
