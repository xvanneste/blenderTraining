"""Captures d’interface. Lancer dans une instance Blender dédiée au premier plan."""
import traceback
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
JOBS = (("pilote_timeline.blend", "timeline_pilote.png"),
        ("SQ020_SH020_override.blend", "balise_override.png"))
state = iter(JOBS)


def capture(name, image, frame=0):
    window = bpy.context.window_manager.windows[0]
    area = max(window.screen.areas, key=lambda ui: ui.width * ui.height)
    with bpy.context.temp_override(window=window, area=area):
        if frame:
            assert bpy.ops.screen.screenshot(filepath=str(HERE / image)) == {"FINISHED"}
            print(image, flush=True)
            return next_scene
        if name == JOBS[0][0]:
            area.type = "DOPESHEET_EDITOR"
            area.spaces.active.mode = "DOPESHEET"
            region = next(region for region in area.regions if region.type == "WINDOW")
            with bpy.context.temp_override(region=region):
                if bpy.ops.action.view_all.poll():
                    bpy.ops.action.view_all()
        else:
            area.type = "VIEW_3D"
            region = area.spaces.active.region_3d
            region.view_location = (1.25, 0, .67)
            region.view_distance = 2.85
            region.view_rotation = Vector((2, -4, 1.8)).to_track_quat("Z", "Y")
            region.view_perspective = "ORTHO"
            area.spaces.active.shading.color_type = "MATERIAL"
            obj = bpy.context.scene.objects["GEO_A03_Coffret"]
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            outliner = next(ui for ui in window.screen.areas if ui.type == "OUTLINER")
            outliner.spaces.active.display_mode = "LIBRARIES"
    bpy.app.timers.register(lambda: step(name, image, 1), first_interval=.8, persistent=True)


def step(name, image, frame=0):
    try:
        callback = capture(name, image, frame)
        if callback:
            bpy.app.timers.register(callback, first_interval=.4, persistent=True)
    except Exception:
        traceback.print_exc()
        bpy.ops.wm.quit_blender()


def next_scene():
    try:
        name, image = next(state)
    except StopIteration:
        bpy.ops.wm.quit_blender()
        return None
    bpy.ops.wm.open_mainfile(filepath=str(HERE / name), load_ui=False)
    bpy.app.timers.register(lambda: step(name, image), first_interval=.8, persistent=True)


bpy.app.timers.register(next_scene, first_interval=1, persistent=True)
