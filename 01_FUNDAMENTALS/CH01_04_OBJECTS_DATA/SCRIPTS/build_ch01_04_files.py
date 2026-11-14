"""
build_ch01_04_files.py — La ferme : objets, données, duplication, jointure (CH01.04).

  STARTER_FILES/ch01_04_farm_starter.blend
      GEO_Post_01 (un piquet de clôture) ; une table en 5 morceaux (GEO_TableTop,
      GEO_TableLeg_1..4) ; GEO_Rocks (un seul objet contenant deux rochers séparés).
  COMPLETED_EXAMPLES/ch01_04_farm_solution.blend
      8 piquets GEO_Post_01..08 partageant le même maillage (Alt+D) sauf GEO_Post_08
      rendu unique et modifié (piquet cassé) ; table jointe en un objet GEO_Table ;
      rochers séparés en deux objets GEO_Rock_A et GEO_Rock_B.
Usage : blender -b --factory-startup --python build_ch01_04_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.04 — LA FERME
1. Clôture : à partir de GEO_Post_01, créez 7 piquets de plus avec Alt+D (duplication
   LIÉE), espacés de 1 m sur X : GEO_Post_02 … GEO_Post_08.
2. Rendez GEO_Post_08 unique (Object Data > nombre d'utilisateurs > Make Single User,
   ou Object > Relations > Make Single User > Object & Data) puis cassez-le :
   en Edit Mode, abaissez les sommets du haut de 0,4 m.
3. Table : joignez les 5 morceaux en UN objet nommé GEO_Table (Ctrl+J, plateau actif).
4. Rochers : séparez GEO_Rocks en deux objets (Edit Mode > P > By Loose Parts) nommés
   GEO_Rock_A et GEO_Rock_B.
"""


def post_mesh():
    me = bpy.data.meshes.new("ME_Post")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.1
        v.co.y *= 0.1
        v.co.z = (v.co.z + 0.5) * 1.2
    bm.to_mesh(me)
    bm.free()
    return me


def build(solution):
    L.reset("SC_Farm")
    L.studio(subject_height=1.0)
    fence, table_c, rocks_c = L.collection("FENCE"), L.collection("TABLE"), L.collection("ROCKS")
    wood = L.material("MAT_Wood", (0.45, 0.3, 0.15), 0.7)
    me = post_mesh()
    me.materials.append(wood)
    n = 8 if solution else 1
    for i in range(n):
        o = bpy.data.objects.new(f"GEO_Post_{i + 1:02d}", me)
        o.location = (-4 + i, -1, 0)
        fence.objects.link(o)
    if solution:
        p8 = bpy.data.objects["GEO_Post_08"]
        p8.data = me.copy()
        p8.data.name = "ME_Post_Broken"
        for v in p8.data.vertices:
            if v.co.z > 1.0:
                v.co.z -= 0.4
    top = L.cube("GEO_TableTop", table_c, wood, size=1, location=(2, 1, 0.75), scale=(1.2, 0.7, 0.05))
    legs = [L.cube(f"GEO_TableLeg_{i + 1}", table_c, wood, size=1, location=(2 + x, 1 + y, 0.36),
                   scale=(0.06, 0.06, 0.72))
            for i, (x, y) in enumerate([(-.5, -.28), (.5, -.28), (-.5, .28), (.5, .28)])]
    if solution:
        bpy.ops.object.select_all(action="DESELECT")
        for o in legs + [top]:
            o.select_set(True)
        bpy.context.view_layer.objects.active = top
        bpy.ops.object.join()
        top.name = "GEO_Table"
        top.data.name = "ME_Table"
    stone = L.material("MAT_Stone", (0.4, 0.4, 0.38), 0.8)
    rme = bpy.data.meshes.new("ME_Rocks")
    bm = bmesh.new()
    for cx in (-0.6, 0.6):
        res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.35)
        bmesh.ops.translate(bm, vec=(cx, 0, 0.3), verts=res["verts"])
    bm.to_mesh(rme)
    bm.free()
    rme.materials.append(stone)
    rocks = bpy.data.objects.new("GEO_Rocks", rme)
    rocks.location = (-2, 2, 0)
    rocks_c.objects.link(rocks)
    if solution:
        bpy.ops.object.select_all(action="DESELECT")
        rocks.select_set(True)
        bpy.context.view_layer.objects.active = rocks
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.separate(type="LOOSE")
        bpy.ops.object.mode_set(mode="OBJECT")
        parts = sorted(rocks_c.objects, key=lambda o: o.name)
        for o, nm in zip(parts, ("GEO_Rock_A", "GEO_Rock_B")):
            o.name = nm
            o.data.name = nm.replace("GEO_", "ME_")
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_04_farm_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_04_farm_solution.blend"))


if __name__ == "__main__":
    L.run(main)
