"""Crée le corrigé P1 à partir du corrigé CH01.14 ouvert par la commande du README."""
from pathlib import Path
from math import cos, pi, sin

import bpy


def open_cup(cup):
    profile = [(0.074, -0.06), (0.078, -0.057), (0.089, 0.053), (0.089, 0.06),
               (0.081, 0.06), (0.081, 0.053), (0.070, -0.047)]
    sections = 64
    vertices = [(radius * cos(2 * pi * i / sections), radius * sin(2 * pi * i / sections), z)
                for radius, z in profile for i in range(sections)]
    faces = [tuple(reversed(range(sections)))]
    for section in range(len(profile) - 1):
        start = section * sections
        for i in range(sections):
            next_i = (i + 1) % sections
            faces.append((start + i, start + next_i, start + sections + next_i, start + sections + i))
    faces.append(tuple(range(len(vertices) - sections, len(vertices))))
    mesh = bpy.data.meshes.new("ME_Cup_Wall")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    mesh.materials.append(cup.data.materials[0])
    cup.modifiers.clear()
    cup.data = mesh
    for face in mesh.polygons:
        face.use_smooth = len(face.vertices) == 4


def add_handle(collection, name, material, location, radius, thickness):
    bpy.ops.mesh.primitive_torus_add(location=location, rotation=(pi / 2, 0, 0),
                                    major_segments=48, minor_segments=12,
                                    major_radius=radius, minor_radius=thickness)
    handle = bpy.context.object
    for old_collection in list(handle.users_collection):
        old_collection.objects.unlink(handle)
    collection.objects.link(handle)
    handle.name = name
    handle.data.materials.append(material)
    for face in handle.data.polygons:
        face.use_smooth = True


def main():
    project = Path(__file__).resolve().parent
    source = project.parent / "CH01_14_FIRST_RENDERS" / "COMPLETED_EXAMPLES" / "ch01_14_final_render_solution.blend"
    if Path(bpy.data.filepath).resolve() != source.resolve():
        raise RuntimeError("Ouvrez le corrigé CH01.14 avant de lancer le script.")

    scene = bpy.context.scene
    props = bpy.data.collections["PROPS"]
    apple = props.objects["GEO_Apple_1"]
    apple.location.y = -0.23
    second_apple = props.objects["GEO_Apple_2"]
    second_apple.data = apple.data
    second_apple.location.y = -0.25
    cup = props.objects["GEO_Cup"]
    open_cup(cup)
    add_handle(props, "GEO_Cup_Handle", cup.data.materials[0], (-0.445, -0.10, 0.269), 0.035, 0.008)
    teapot = props.objects["GEO_Teapot"]
    add_handle(props, "GEO_Teapot_Handle", teapot.data.materials[0], (-0.055, 0.25, 0.39), 0.105, 0.015)
    for index in range(1, 4):
        props.objects[f"GEO_Book_{index}"].location.x -= 0.13
    book = props.objects["GEO_Book_3"]
    paper = bpy.data.materials.new("MAT_Book_Paper")
    paper.use_nodes = True
    shader = paper.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (0.78, 0.67, 0.48, 1)
    shader.inputs["Roughness"].default_value = 0.8
    book.data.materials.append(paper)
    for face in book.data.polygons:
        if abs(face.normal.z) < 0.5:
            face.material_index = len(book.data.materials) - 1
    bevel = book.modifiers.new("Arêtes de la couverture", "BEVEL")
    bevel.width, bevel.segments = 0.002, 3
    book.modifiers.new("Normales pondérées", "WEIGHTED_NORMAL")

    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35
    camera = scene.camera
    distance = (teapot.location - camera.location).length
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = distance
    camera.data.dof.aperture_fstop = 5.6
    scene.render.resolution_percentage = 100
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.eevee.taa_render_samples = 32
    note = bpy.data.texts.get("README_EXERCICE") or bpy.data.texts.new("README_EXERCICE")
    note.clear()
    note.write("P1 — Nature morte de référence\nComparez les données partagées des pommes, les matériaux du livre supérieur et les deux moteurs de rendu.\n")
    note.use_fake_user = True

    reference = project / "REFERENCE"
    (reference / "renders").mkdir(parents=True, exist_ok=True)
    for engine, name in (("CYCLES", "p1_cycles"), ("BLENDER_EEVEE", "p1_eevee")):
        scene.render.engine = engine
        scene.render.filepath = str(reference / "renders" / f"{name}.png")
        bpy.ops.render.render(write_still=True)
    scene.render.engine = "CYCLES"
    scene.render.filepath = "//renders/p1_cycles.png"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(reference / "p1_nature_morte_reference.blend"))


if __name__ == "__main__":
    main()
