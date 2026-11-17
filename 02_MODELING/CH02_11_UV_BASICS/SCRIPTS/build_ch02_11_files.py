"""
build_ch02_11_files.py — « Déplier une caisse et une boîte de conserve » (CH02.11).

  STARTER_FILES/ch02_11_uv_starter.blend
      GEO_Crate (cube 60 cm subdivisé, sans UV) et GEO_Can (cylindre 32 côtés, sans UV),
      matériau MAT_Checker (texture « UV Grid » générée) déjà assigné.
  COMPLETED_EXAMPLES/ch02_11_uv_solution.blend (+ _reference.png)
      GEO_Crate : Smart UV Project ; GEO_Can : coutures (1 arête verticale + 2 cercles des
      couvercles) puis Unwrap (Angle Based) ; Pack Islands. Opérateurs de l'interface.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_11_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.11 — DÉPLIER (UV) — le damier doit être régulier, sans étirement
GEO_Crate et GEO_Can n'ont pas d'UV : le damier est mal appliqué. Material Preview (Z).
1. GEO_Crate : Edit Mode, A, U > Smart UV Project (Angle Limit 66°, Island Margin 0.02).
2. GEO_Can : mode arête ; sélectionnez UNE arête verticale + les 2 cercles des couvercles
   (Alt+clic), Edge > Mark Seam (rouge). Puis A, U > Unwrap (Angle Based).
   Dans l'UV Editor : UV > Pack Islands (Margin 0.02).
3. Contrôle : les carrés du damier sont carrés et de même taille partout.
Vérification : SCRIPTS/validate_ch02_11.py -- --exercise uv
"""


def mk(name, col, mat, bm, loc):
    me = bpy.data.meshes.new(name.replace("GEO_", "ME_"))
    bm.to_mesh(me)
    bm.free()
    for uv in list(me.uv_layers):
        me.uv_layers.remove(uv)
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    col.objects.link(ob)
    me.materials.append(mat)
    return ob


def checker_material():
    mat = L.material("MAT_Checker", (0.8, 0.8, 0.8), 0.6)
    img = bpy.data.images.get("IMG_UVGrid") or bpy.data.images.new("IMG_UVGrid", 1024, 1024)
    img.generated_type = "UV_GRID"
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.location = (-350, 250)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def edit_ops(ob, fn):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    fn()
    bpy.ops.object.mode_set(mode="OBJECT")


def build(sol):
    L.reset("SC_UV")
    L.studio(subject_height=0.8)
    col = L.collection("PROPS")
    mat = checker_material()
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.6)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    for v in bm.verts:
        v.co.z += 0.3
    crate = mk("GEO_Crate", col, mat, bm, (-0.6, 0, 0))
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.2, radius2=0.2, depth=0.5)
    for v in bm.verts:
        v.co.z += 0.25
    can = mk("GEO_Can", col, mat, bm, (0.6, 0, 0))
    for p in can.data.polygons:
        p.use_smooth = abs(p.normal.z) < 0.5
    if sol:
        def crate_ops():
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
        edit_ops(crate, crate_ops)
        # coutures : une arête verticale + arêtes des deux couvercles
        me = can.data
        verts = me.vertices
        vert_edge = None
        for e in me.edges:
            a, b = verts[e.vertices[0]].co, verts[e.vertices[1]].co
            horizontal = abs(a.z - b.z) < 1e-5
            on_cap_rim = horizontal and abs(a.xy.length - 0.2) < 1e-4 and abs(b.xy.length - 0.2) < 1e-4
            e.use_seam = on_cap_rim
            if not horizontal and vert_edge is None and a.x > 0.19 and abs(a.y) < 0.03:
                vert_edge = e
        vert_edge.use_seam = True

        def can_ops():
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.02)
            bpy.ops.uv.pack_islands(margin=0.02)
        edit_ops(can, can_ops)
    cam = L.obj("CAM_Main")
    cam.location = (0.0, -2.6, 1.4)
    cam.data.lens = 45
    L.obj("EMP_Target").location = (0, 0, 0.3)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_11_uv_starter.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_11_uv_starter_view.png")
    bpy.ops.render.render(write_still=True)
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_11_uv_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_11_uv_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
