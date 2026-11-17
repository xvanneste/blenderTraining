"""Crée un starter Blender 5.3 avec les douze débuts du pilote et un calque de dessin."""
import csv
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "SCRIPTS"))
import bcma_lib as L


def main():
    scene = L.reset("Les veilleurs du quai · storyboard")
    scene.frame_end = 2880
    scene.render.fps = 24
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    scene.render.resolution_percentage = 100

    cam = L.camera("CAM_Storyboard", scene.collection, location=(0, -8, 0))
    cam.rotation_euler = Vector((0, 8, 0)).to_track_quat("-Z", "Y").to_euler()
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 6.5
    drawings = bpy.data.grease_pencils.new("Storyboard du pilote")
    board = bpy.data.objects.new("GP_Planches", drawings)
    scene.collection.objects.link(board)
    layer = drawings.layers.new("Vignettes", set_active=True)
    pencil = bpy.data.materials.new("Crayon du storyboard")
    bpy.data.materials.create_gpencil_data(pencil)
    drawings.materials.append(pencil)
    with (HERE / "plans_pilote.csv").open(encoding="utf-8-sig", newline="") as handle:
        for entry in csv.DictReader(handle):
            frame = int(entry["debut"])
            scene.timeline_markers.new(entry["plan"], frame=frame)
            layer.frames.new(frame)
    bpy.context.view_layer.objects.active = board
    board.select_set(True)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"
    L.instructions("Storyboard du pilote. Le calque Vignettes contient 12 dessins vides aux coupes du CSV. "
                   "Dessinez la situation, le geste et sa conséquence avant de construire le layout 3D.")
    L.save(str(HERE / "pilote_timeline.blend"))


if __name__ == "__main__":
    L.run(main)
