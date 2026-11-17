"""Rejoue en mémoire Grid Fill et la réparation du cylindre du starter CH02.01."""
import bmesh
import bpy


def edit_object(name):
    bpy.ops.object.select_all(action="DESELECT")
    obj = bpy.data.objects[name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    return obj


def check_octagon():
    obj = edit_object("GEO_Ngon")
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_all(action="SELECT")
    contour = {tuple(vertex.co) for vertex in bmesh.from_edit_mesh(obj.data).verts}
    assert len(contour) == 8
    bpy.ops.mesh.delete(type="ONLY_FACE")
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.select_all(action="SELECT")
    assert bpy.ops.mesh.fill_grid() == {"FINISHED"}
    mesh = bmesh.from_edit_mesh(obj.data)
    assert len(mesh.faces) >= 3 and all(len(face.verts) == 4 for face in mesh.faces)
    assert {tuple(vertex.co) for edge in mesh.edges if edge.is_boundary for vertex in edge.verts} == contour
    bpy.ops.object.mode_set(mode="OBJECT")


def check_cylinder():
    obj = edit_object("GEO_Hole")
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.mesh.select_non_manifold(extend=False)
    mesh = bmesh.from_edit_mesh(obj.data)
    opening = [edge for edge in mesh.edges if edge.select]
    assert len(opening) == 16 and all(edge.is_boundary for edge in opening)
    assert bpy.ops.mesh.edge_face_add() == {"FINISHED"}
    assert all(edge.is_manifold for edge in bmesh.from_edit_mesh(obj.data).edges)
    bpy.ops.object.mode_set(mode="OBJECT")


check_octagon()
check_cylinder()
print("Octogone rempli en quads, contour conserve et cylindre ferme.")
