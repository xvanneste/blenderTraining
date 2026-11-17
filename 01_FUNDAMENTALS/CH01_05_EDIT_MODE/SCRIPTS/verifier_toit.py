"""Vérifie l’extrusion, la fusion du faîtage et les normales sur la maison de départ."""
import bmesh
import bpy


def main():
    house = bpy.context.scene.objects["GEO_House"]
    bm = bmesh.new()
    try:
        bm.from_mesh(house.data)
        inv = house.matrix_world.inverted()
        top = max(bm.faces, key=lambda f: (house.matrix_world @ f.calc_center_median()).z)
        raised = bmesh.ops.extrude_face_region(bm, geom=[top])
        crest = [v for v in raised["geom"] if isinstance(v, bmesh.types.BMVert)]
        assert len(crest) == 4
        # Une extrusion de région via BMesh conserve la face de départ si elle n’est pas reliée.
        # Les opérateurs de mode Édition traitent le retrait de cette face automatiquement.
        if top.is_valid:
            bmesh.ops.delete(bm, geom=[top], context="FACES_ONLY")
        new_x = sum((house.matrix_world @ v.co).x for v in crest) / len(crest)
        for vertex in crest:
            world = house.matrix_world @ vertex.co
            world.z += 1.0
            world.x = new_x
            vertex.co = inv @ world
        bmesh.ops.remove_doubles(bm, verts=crest, dist=0.0001)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        assert len(bm.faces) == 9, len(bm.faces)
        assert all(edge.is_manifold for edge in bm.edges)
        assert all(face.calc_area() > 0.0001 for face in bm.faces)
        assert bm.calc_volume(signed=True) > 0
        assert abs(max((house.matrix_world @ v.co).z for v in bm.verts) - 3.0) < 0.001
        print("Faîtage vérifié à 3 m, 9 faces, maillage fermé et orienté.")
    finally:
        bm.free()


if __name__ == "__main__":
    main()
