"""Teste GLB, USD, OBJ, FBX et Alembic avec une boîte asymétrique dans Blender 5.3."""
import tempfile
from pathlib import Path

import bpy


def create_source():
    obj = bpy.context.scene.objects["Cube"]
    obj.name = "GEO_Boite_Echange"
    obj.scale = (.4, .6, .9)
    material = bpy.data.materials.new("MAT_Rouge_Echange")
    red = (.62, .03, .02, 1)
    shader = next(n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    shader.inputs["Base Color"].default_value = red
    material.diffuse_color = red
    obj.data.materials.clear()
    obj.data.materials.append(material)


def importer(importer_op, filepath, *, material_expected=True, **options):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    assert importer_op(filepath=str(filepath), **options) == {"FINISHED"}
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    assert len(meshes) == 1
    obj = meshes[0]
    world_points = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
    size = tuple(max(p[i] for p in world_points) - min(p[i] for p in world_points) for i in range(3))
    assert all(abs(value - expected) < 1e-4 for value, expected in zip(size, (.8, 1.2, 1.8))), (filepath, size)
    label = "géométrie seule contrôlée"
    if material_expected:
        assert any(m and "MAT_Rouge_Echange" in m.name for m in obj.data.materials)
        label = "nom du matériau conservé"
    print(f"{filepath.suffix}: dimensions monde {tuple(round(v, 2) for v in size)}, {label}")



def main():
    bpy.ops.wm.read_factory_settings()
    create_source()
    with tempfile.TemporaryDirectory(prefix="bcma_echange_") as directory:
        folder = Path(directory)
        glb, usd, obj, fbx, abc = (folder / f"test.{ext}" for ext in ("glb", "usda", "obj", "fbx", "abc"))
        assert bpy.ops.export_scene.gltf(filepath=str(glb), use_selection=True, export_format="GLB") == {"FINISHED"}
        assert bpy.ops.wm.usd_export(filepath=str(usd), selected_objects_only=True, export_materials=True) == {"FINISHED"}
        assert bpy.ops.wm.obj_export(filepath=str(obj), export_selected_objects=True, export_materials=True) == {"FINISHED"}
        assert obj.with_suffix(".mtl").is_file()
        assert bpy.ops.export_scene.fbx(filepath=str(fbx), use_selection=True) == {"FINISHED"}
        assert bpy.ops.wm.alembic_export(filepath=str(abc), selected=True, start=1, end=1,
                                          as_background_job=False) == {"FINISHED"}
        importer(bpy.ops.import_scene.gltf, glb)
        importer(bpy.ops.wm.usd_import, usd)
        importer(bpy.ops.wm.obj_import, obj)
        importer(bpy.ops.import_scene.fbx, fbx)
        try:
            importer(bpy.ops.wm.alembic_import, abc, material_expected=False, as_background_job=False)
        finally:
            # La scène peut conserver un lecteur de cache et garder le fichier ouvert.
            bpy.ops.wm.read_factory_settings(use_empty=True)


if __name__ == "__main__":
    main()
