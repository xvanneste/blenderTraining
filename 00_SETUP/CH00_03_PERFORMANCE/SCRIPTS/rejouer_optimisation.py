"""Rejoue le partage des maillages et les deux plafonds du tutoriel sur le starter."""
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
from bcma_scene_cost import scene_cost
from validate_ch00_03 import main as validate


def main():
    scene = bpy.context.scene
    bpy.ops.object.select_all(action="DESELECT")
    props = scene.collection.children["PROPS"]
    pebbles = [obj for obj in props.objects if obj.name.startswith("GEO_Pebble_")]
    positions = {obj.name: obj.location.copy() for obj in pebbles}
    for obj in pebbles:
        obj.select_set(True)
    active = props.objects["GEO_Pebble_000"]
    bpy.context.view_layer.objects.active = active

    baseline = scene_cost(scene)
    assert (baseline["unique_meshes"], baseline["render_faces_est"]) == (202, 16_384_002)
    assert bpy.ops.object.make_links_data(type="OBDATA") == {"FINISHED"}
    linked = scene_cost(scene)
    assert (linked["unique_meshes"], linked["render_faces_est"]) == (3, 16_384_002)

    for obj in pebbles:
        modifier = next(mod for mod in obj.modifiers if mod.type == "SUBSURF")
        modifier.levels, modifier.render_levels = 1, 2
        assert obj.location == positions[obj.name]
    assert scene_cost(scene)["render_faces_est"] == 256_002
    scene.render.use_simplify = True
    scene.render.simplify_subdivision = 1
    scene.render.simplify_subdivision_render = 2
    next(mod for mod in active.modifiers if mod.type == "SUBSURF").render_levels = 5
    assert scene_cost(scene)["render_faces_est"] == 256_002
    assert validate() == 0

    active.hide_render = True
    assert validate() == 1, "Le correcteur doit refuser la disparition d’un galet."
    active.hide_render = False
    props.hide_render = True
    assert validate() == 1, "Le correcteur doit refuser une collection masquée au rendu."


if __name__ == "__main__":
    main()
