"""Check the delivered scenes in Blender 5.3. Run with --python-exit-code 1."""
import math
import tempfile
from pathlib import Path

import bmesh
import bpy


ASSETS = Path(__file__).resolve().parent / "assets"


def open_asset(name):
    bpy.ops.wm.open_mainfile(filepath=str(ASSETS / f"{name}.blend"))
    return bpy.context.scene


def closed(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    result = bool(bm.faces) and all(edge.is_manifold for edge in bm.edges)
    bm.free()
    return result


def extent(ob, axis):
    points = [ob.matrix_world @ v.co for v in ob.data.vertices]
    return min(p[axis] for p in points), max(p[axis] for p in points)


def main():
    open_asset("caisse")
    cuve = bpy.data.objects["Cuve creuse"]
    assert closed(cuve.data), "La cuve doit avoir une coque fermée."
    assert any(math.isclose(v.co.z, .04, abs_tol=1e-6) for v in cuve.data.vertices)
    assert not any(len(p.vertices) > 3 and all(cuve.data.vertices[i].co.z > .37 for i in p.vertices)
                   and p.area > .12 for p in cuve.data.polygons), "Pas de face qui bouche l'ouverture."

    for name,top,expected in (("table","Plateau",.74),("chaise","Assise",.45)):
        open_asset(name)
        feet = [ob for ob in bpy.context.scene.objects if ob.name.startswith("Pied")]
        assert len(feet) == 4 and all(abs(extent(f, 2)[0]) < .00001 for f in feet)
        assert math.isclose(extent(bpy.data.objects[top], 2)[1], expected, abs_tol=.00001)

    open_asset("epee")
    blade = bpy.data.objects["Demi-lame · Mirror"]
    assert blade.modifiers[0].type == "MIRROR" and blade.modifiers[0].use_clip
    sym = blade.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    assert closed(sym), "La lame évaluée doit avoir une couture fermée."

    open_asset("coffre")
    chest = bpy.data.objects["Cuve"]
    lid = bpy.data.objects["Couvercle"]
    pivot = lid.parent
    assert closed(chest.data) and pivot.name == "Axe du couvercle"
    assert extent(lid, 2)[1] > .60
    pivot.rotation_euler.x = 0
    bpy.context.view_layer.update()
    assert math.isclose(extent(lid, 2)[0], .32, abs_tol=.00001)

    open_asset("maison")
    assert closed(bpy.data.objects["Toit à deux versants"].data)
    assert sum(o.name.startswith("Cadre fenêtre") for o in bpy.context.scene.objects) == 2

    scene = open_asset("cage_humain")
    ob = bpy.data.objects["GEO_Cage_Humaine"]
    rig = bpy.data.objects["RIG_Atelier"]
    assert ob.parent is rig and closed(ob.data)
    assert all(abs(sum(g.weight for g in v.groups)-1) < .00001 for v in ob.data.vertices)
    def positions(frame):
        scene.frame_set(frame)
        return [v.co.copy() for v in ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
    rest, bent, back = (positions(frame) for frame in (1, 25, 49))
    assert max((a-b).length for a,b in zip(rest,bent)) > .12
    assert max((a-b).length for a,b in zip(rest,back)) < .00001

    with tempfile.TemporaryDirectory(prefix="bcma-modeling-") as tmp:
        target = str(Path(tmp) / "atelier.glb")
        scene.frame_set(1)
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        rig.select_set(True)
        bpy.ops.export_scene.gltf(filepath=target, export_format="GLB", use_selection=True)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=target)
        skeleton = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
        imported = next(o for o in bpy.context.scene.objects if o.type == "MESH")
        assert len(skeleton.data.bones) == 16
        assert imported.data.materials and any(m.type == "ARMATURE" for m in imported.modifiers)
        assert len(bpy.data.actions) > 0
    print("6 accessoires, cage, déformation et réimport GLB : validés.")


if __name__ == "__main__":
    main()
