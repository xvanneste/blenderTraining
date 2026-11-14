"""
build_ch01_11_files.py — La maison en couleurs (CH01.11 : matériaux simples).

  STARTER_FILES/ch01_11_house_colors_starter.blend
      GEO_House : maison (murs, toit à deux pans, porte = face distincte sur la façade avant),
      un seul matériau gris MAT_Wall sur toutes les faces. GEO_Gutter : gouttière sans
      matériau. GEO_Lantern : lanterne sans matériau.
  COMPLETED_EXAMPLES/ch01_11_house_colors_solution.blend
      MAT_Wall (blanc cassé), MAT_Roof (tuile rouge, rugueux) sur les 2 pans du toit,
      MAT_Door (bois brun) sur la face de porte, MAT_Metal (métal, peu rugueux) sur la
      gouttière, MAT_Lamp_Glow (émissif jaune) sur la lanterne.
Usage : blender -b --factory-startup --python build_ch01_11_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.11 — LA MAISON EN COULEURS (Properties > Material ; vue en Material Preview : Z > 2)
1. GEO_House : renommez son matériau gris en… il s'appelle déjà MAT_Wall : donnez-lui un blanc cassé.
2. Ajoutez un emplacement (+), New, nommez MAT_Roof (rouge tuile, Roughness ≥ 0,6).
   Edit Mode, sélectionnez les 2 pans du toit, Assign.
3. Nouvel emplacement MAT_Door (brun bois) assigné à la face de porte (façade avant).
4. GEO_Gutter : nouveau matériau MAT_Metal : Metallic 1, Roughness ≤ 0,4.
5. GEO_Lantern : MAT_Lamp_Glow : Emission Color jaune, Emission Strength ≥ 5.
"""


def house_mesh():
    me = bpy.data.meshes.new("ME_House")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.translate(bm, vec=(0, 0, 1), verts=bm.verts)
    bm.faces.ensure_lookup_table()
    top = [f for f in bm.faces if f.normal.z > 0.9][0]
    res = bmesh.ops.extrude_face_region(bm, geom=[top])
    for v in [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z += 1.0
        v.co.x = 0.0
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bm.normal_update()
    # Porte : une face distincte (0,8 × 1,4 m) posée 2 mm devant la façade avant (normale -Y)
    vs = [bm.verts.new(co) for co in ((-0.4, -1.002, 0.0), (0.4, -1.002, 0.0), (0.4, -1.002, 1.4), (-0.4, -1.002, 1.4))]
    bm.faces.new(vs)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    return me


def build(solution):
    L.reset("SC_HouseColors")
    cam = L.studio(subject_height=2.5)["camera"]
    cam.location = (5.5, -7.0, 3.2)  # vue de trois quarts : façade + toit
    col = L.collection("HOUSE")
    house = bpy.data.objects.new("GEO_House", house_mesh())
    col.objects.link(house)
    wall = L.material("MAT_Wall", (0.5, 0.5, 0.5), 0.8)
    house.data.materials.append(wall)
    gutter = L.cylinder("GEO_Gutter", col, radius=0.05, depth=2.2, location=(1.05, 0, 2.0), rotation=(1.5708, 0, 0))
    lantern = L.sphere("GEO_Lantern", col, radius=0.12, location=(0.65, -1.15, 1.6))
    if solution:
        wall_b = next(n for n in wall.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        wall_b.inputs["Base Color"].default_value = (0.85, 0.8, 0.7, 1)
        roof = L.material("MAT_Roof", (0.6, 0.12, 0.06), 0.75)
        door = L.material("MAT_Door", (0.35, 0.2, 0.1), 0.6)
        house.data.materials.append(roof)
        house.data.materials.append(door)
        polys = house.data.polygons
        for p in polys:
            if p.normal.z > 0.3 and p.center.z > 2.0:
                p.material_index = 1
        door_poly = min((p for p in polys if p.normal.y < -0.9 and p.center.z < 2.0), key=lambda p: p.area)
        door_poly.material_index = 2
        gutter.data.materials.append(L.material("MAT_Metal", (0.8, 0.8, 0.82), 0.3, 1.0))
        lantern.data.materials.append(L.material("MAT_Lamp_Glow", (1.0, 0.85, 0.4), 0.5,
                                                 emission=(1.0, 0.8, 0.3), emission_strength=8))
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_11_house_colors_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_11_house_colors_solution.blend"))


if __name__ == "__main__":
    L.run(main)
