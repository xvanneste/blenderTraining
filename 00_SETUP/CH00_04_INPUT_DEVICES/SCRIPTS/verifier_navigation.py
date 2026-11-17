"""Vérifie les actions de navigation et leur effet sur la vue Blender 5.3."""
import bpy


def main():
    prefs = bpy.context.preferences
    assert prefs.inputs.bl_rna.properties["use_emulate_numpad"]
    assert prefs.inputs.bl_rna.properties["use_mouse_emulate_3_button"]
    prefs.view.smooth_view = 0
    window = bpy.context.window_manager.windows[0]
    area = next(area for area in window.screen.areas if area.type == "VIEW_3D")
    region = next(region for region in area.regions if region.type == "WINDOW")
    cube = bpy.context.scene.objects["Cube"]
    camera = bpy.context.scene.camera
    before = (cube.location.copy(), camera.location.copy())
    with bpy.context.temp_override(window=window, area=area, region=region):
        rv3d = area.spaces.active.region_3d
        for axis in ("FRONT", "RIGHT", "TOP", "BACK", "LEFT", "BOTTOM"):
            assert bpy.ops.view3d.view_axis(type=axis) == {"FINISHED"}
            assert rv3d.view_perspective == "ORTHO"
        cube.select_set(True)
        bpy.context.view_layer.objects.active = cube
        assert bpy.ops.view3d.view_selected() == {"FINISHED"}
        assert (rv3d.view_location - before[0]).length < 1e-5
        assert bpy.ops.view3d.view_camera() == {"FINISHED"}
        assert rv3d.view_perspective == "CAMERA"
        bpy.ops.object.mode_set(mode="EDIT")
        assert bpy.ops.mesh.select_mode(type="FACE") == {"FINISHED"}
        assert bpy.context.scene.tool_settings.mesh_select_mode[2]
        bpy.ops.object.mode_set(mode="OBJECT")
    assert cube.location == before[0] and camera.location == before[1]
    print("Six vues orthographiques, cadrage, vue caméra et mode Face vérifiés.")


if __name__ == "__main__":
    main()
