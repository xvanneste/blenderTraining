"""
build_ch01_05_files.py — De la boîte à la maison (CH01.05, Edit Mode).

  STARTER_FILES/ch01_05_house_starter.blend
      GEO_House : un cube de 2 m (base au sol, z de 0 à 2) ; GEO_Practice : une grille
      5×5 pour s'entraîner à la sélection de sommets/arêtes/faces et à l'édition
      proportionnelle.
  COMPLETED_EXAMPLES/ch01_05_house_solution.blend
      GEO_House avec un toit à deux pans : face du haut extrudée de 1 m puis mise à
      l'échelle 0 sur X et fusionnée (faîtage parallèle à Y à z = 3) ; GEO_Practice avec une « colline »
      (sommet central monté de 1 m en édition proportionnelle).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch01_05_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.05 — DE LA BOÎTE À LA MAISON
GEO_House (Tab pour entrer en Edit Mode) :
1. Mode face (3), cliquez la face du haut.
2. E (extruder) puis 1 Entrée : la face monte de 1 m.
3. S X 0 Entrée : la face s'écrase en une arête -> un toit à deux pans, faîtage à z = 3.
4. Mode sommet, M > By Distance pour fusionner les sommets du faîtage. A puis Shift+N.
5. Tab pour revenir en Object Mode.
GEO_Practice (grille) : sélectionnez le sommet central, activez l'édition proportionnelle
(O), G Z 1 Entrée en réglant le rayon à la molette pendant le déplacement -> une colline.
"""


def build(solution):
    L.reset("SC_House")
    L.studio(subject_height=2.5)
    col = L.collection("HOUSE")
    house = L.cube("GEO_House", col, L.material("MAT_Wall", (0.85, 0.8, 0.7), 0.8), size=2, location=(0, 0, 1))
    grid = L.mesh(bpy.ops.mesh.primitive_grid_add, "GEO_Practice", col, L.material("MAT_Grass", (0.25, 0.5, 0.2), 0.9),
                  x_subdivisions=5, y_subdivisions=5, size=4, location=(4, 0, 0.01))
    if solution:
        bm = bmesh.new()
        bm.from_mesh(house.data)
        top = [f for f in bm.faces if f.normal.z > 0.9][0]
        res = bmesh.ops.extrude_face_region(bm, geom=[top])
        verts = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
        if top.is_valid:
            bmesh.ops.delete(bm, geom=[top], context="FACES_ONLY")
        for v in verts:
            v.co.z += 1.0
            v.co.x = 0.0
        bmesh.ops.remove_doubles(bm, verts=verts, dist=0.0001)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(house.data)
        bm.free()
        # colline : sommet central +1 m, voisins atténués (édition proportionnelle, lissage)
        for v in grid.data.vertices:
            d = (v.co.x ** 2 + v.co.y ** 2) ** 0.5
            if d < 1.6:
                t = 1 - d / 1.6
                v.co.z += t * t * (3 - 2 * t)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_05_house_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_05_house_solution.blend"))


if __name__ == "__main__":
    L.run(main)
