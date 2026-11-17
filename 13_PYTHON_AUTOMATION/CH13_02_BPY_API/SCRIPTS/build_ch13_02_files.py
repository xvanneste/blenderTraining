"""Construit la scène, le corrigé et les contre-exemples de CH13.02."""
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "SCRIPTS"))
import bcma_lib as L


def build(variant):
    L.reset("SC_Atelier")
    scene = bpy.context.scene
    props = L.collection("COL_Props")
    props.color_tag = "COLOR_04"
    original = L.cube("GEO_Crate_A", props, size=1.4, location=(-1.7, 0, 0.7))
    original.data.materials.append(L.material("MAT_Blue", (0.06, 0.27, 0.74)))
    hero = original.copy()
    hero.name = "GEO_Crate_B"
    hero.location.x = 0
    props.objects.link(hero)

    if variant != "starter":
        if variant != "shared_mesh":
            hero.data = hero.data.copy()
        hero.data.materials[0] = L.material("MAT_Orange", (0.85, 0.25, 0.055))
        if variant != "missing_marker":
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=16, ring_count=8, radius=0.3,
                location=(1.7, 0, 1.0 if variant == "marker_high" else 0.3),
            )
            marker = bpy.context.object
            marker.name = "GEO_Marker"
            L.move_to(marker, props)

    bpy.ops.object.select_all(action="DESELECT")
    active = original if variant in {"starter", "wrong_active"} else hero
    active.select_set(True)
    bpy.context.view_layer.objects.active = active
    camera = L.camera("CAM_Atelier", scene.collection, location=(4, -9, 5))
    camera.rotation_euler = (Vector((0, 0, 0.6)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 6.6
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    L.instructions(
        "CH13.02 — L'API bpy\n"
        "GEO_Crate_A et GEO_Crate_B partagent le même maillage au départ. "
        "Isolez la caisse B, rendez-la orange, ajoutez le repère et enregistrez B comme objet actif."
    )
    return scene


def main():
    ch = HERE.parent
    out = ch / "COMPLETED_EXAMPLES"
    for variant in ("starter", "solution", "shared_mesh", "missing_marker", "marker_high", "wrong_active"):
        scene = build(variant)
        if variant == "starter":
            path = ch / "STARTER_FILES" / "ch13_02_bpy_starter.blend"
        elif variant == "solution":
            path = out / "ch13_02_bpy_solution.blend"
        else:
            path = out / "COUNTER_EXAMPLES" / f"ch13_02_bpy_{variant}.blend"
        L.save(str(path))
        if variant == "solution":
            scene.render.filepath = str(out / "ch13_02_bpy_reference.png")
            bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
