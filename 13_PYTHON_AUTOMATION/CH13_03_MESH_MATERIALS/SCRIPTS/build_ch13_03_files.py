"""Produit le studio, la solution et les variantes utilisées par le correcteur."""
import runpy
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "SCRIPTS"))
import bcma_lib as L


def setup_studio():
    scene = L.reset("SC_Presentoir")
    studio = L.collection("COL_Studio")
    floor = L.cube("GEO_Fond", studio, size=16, location=(0, 0, -0.12))
    floor.scale.z = 0.015
    floor.data.materials.append(L.material("MAT_Fond", (0.085, 0.10, 0.13)))
    camera = L.camera("CAM_Presentoir", studio, location=(4.1, -6.6, 4.7))
    camera.rotation_euler = (Vector((0, 0.54, 0.36)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 5.7
    for name, location, energy, size in (
        ("LGT_Principale", (-3, -4, 6), 870, 3.0),
        ("LGT_Appoint", (3, -1, 4), 380, 4.0),
        ("LGT_Contour", (1, 4, 5), 900, 3.0),
    ):
        lamp = L.light(name, studio, location=location, energy=energy, size=size)
        lamp.rotation_euler = (Vector((0, 0.5, 0)) - lamp.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 880
    scene.render.resolution_y = 560
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                space = area.spaces.active
                space.region_3d.view_location = (0, 0.5, 0.35)
                space.region_3d.view_distance = 6.0
                space.region_3d.view_rotation = camera.rotation_euler.to_quaternion()
                space.shading.color_type = "MATERIAL"
    L.instructions("CH13.03 · Génération d’un présentoir d’échantillons\n"
                   "Dans l’espace Scripting, créez un texte puis suivez les trois blocs de TUTORIAL.md.")
    return scene


def main():
    prefix = "ch13_03_presentoir"
    starter = CHAPTER / "STARTER_FILES" / f"{prefix}_starter.blend"
    examples = CHAPTER / "COMPLETED_EXAMPLES"
    source = HERE / "generer_presentoir.py"
    scene = setup_studio()
    L.save(str(starter))
    runpy.run_path(str(source))
    L.instructions(source.read_text(encoding="utf-8"), source.name)

    scene.render.filepath = "//ch13_03_presentoir_reference.png"
    solution = examples / f"{prefix}_solution.blend"
    L.save(str(solution))
    bpy.ops.render.render(write_still=True)

    for variant in ("bloc_absent", "hauteur_uniforme", "biseau_absent", "materiau_inverse", "bruit_debranche"):
        bpy.ops.wm.open_mainfile(filepath=str(solution))
        first = bpy.data.objects["GEO_Bloc_1_1"]
        accent = bpy.data.objects["GEO_Bloc_2_3"]
        if variant == "bloc_absent":
            bpy.data.objects.remove(first, do_unlink=True)
        elif variant == "hauteur_uniforme":
            for vertex in accent.data.vertices:
                if vertex.co.z > 0:
                    vertex.co.z = 0.36
            accent.data.update()
        elif variant == "biseau_absent":
            first.modifiers.remove(first.modifiers[0])
        elif variant == "materiau_inverse":
            accent.data.materials[0] = first.data.materials[0]
        elif variant == "bruit_debranche":
            tree = accent.data.materials[0].node_tree
            roughness = next(node for node in tree.nodes if node.type == "BSDF_PRINCIPLED").inputs["Roughness"]
            tree.links.remove(roughness.links[0])
        L.save(str(examples / "COUNTER_EXAMPLES" / f"{prefix}_{variant}.blend"))


if __name__ == "__main__":
    L.run(main)
