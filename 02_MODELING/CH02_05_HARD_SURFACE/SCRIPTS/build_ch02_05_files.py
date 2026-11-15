"""
build_ch02_05_files.py — « Le boîtier de commande » (CH02.05, hard surface).

  STARTER_FILES/ch02_05_device_starter.blend
      GEO_Device : pavé 40 × 20 × 50 cm, arêtes vives, aucun modificateur.
  COMPLETED_EXAMPLES/ch02_05_device_solution.blend (+ _reference.png, + _closeup.png)
      - Bevel Weight = 1 sur les 4 arêtes verticales ; Bevel modificateur n°1 « Weight »
        (2 cm, 4 segments) → coins arrondis ;
      - écran en creux (Inset 3 cm + Extrude −1 cm) sur la face avant ;
      - 3 boutons (cylindres) posés sur le dessus ;
      - Bevel modificateur n°2 « Angle » 30° (3 mm, 2 segments, Harden Normals) → arêtes qui
        accrochent la lumière ; Shade Smooth.
Usage : blender -b --factory-startup --python build_ch02_05_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.05 — LE BOÎTIER DE COMMANDE (GEO_Device, 40 × 20 × 50 cm)
1. Coins arrondis : Edit Mode, sélectionnez les 4 arêtes VERTICALES, Edge > Edge Bevel Weight,
   tapez 1. Object Mode : Add Modifier > Generate > Bevel : Limit Method = Weight,
   Width 0.02, Segments 4.
2. Écran : face avant (-Y), I (Inset) 0.03, puis E -0.01 (creux de 1 cm).
3. Boutons : au moins 3 petits cylindres (Shift+A > Cylinder, rayon 2 cm, hauteur 1,5 cm) posés
   sur le dessus, JOINTS à GEO_Device (Ctrl+J) — ou extrudés depuis le dessus.
4. Finition : 2e modificateur Bevel : Limit Method = Angle (30°), Width 0.003, Segments 2,
   cochez Harden Normals (Shading). Object > Shade Smooth.
Vérification : SCRIPTS/validate_ch02_05.py -- --exercise device
"""
W, D, H = 0.40, 0.20, 0.50


def body(bm):
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * W, v.co.y * D, (v.co.z + 0.5) * H))


def solve(ob):
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    # écran : inset + creux sur la face avant
    front = [f for f in bm.faces if f.normal.y < -0.99]
    bmesh.ops.inset_region(bm, faces=front, thickness=0.03, depth=0.0)
    res = bmesh.ops.extrude_face_region(bm, geom=front)
    inner = [g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, verts=list({v for f in inner for v in f.verts}), vec=(0, 0.01, 0))
    bmesh.ops.delete(bm, geom=front, context="FACES")
    # boutons
    for x in (-0.1, 0.0, 0.1):
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.02, radius2=0.02, depth=0.015,
                              matrix=Matrix.Translation((x, 0.0, H + 0.0075)))
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    # poids de biseau sur les 4 arêtes verticales du corps
    att = me.attributes.get("bevel_weight_edge") or me.attributes.new("bevel_weight_edge", "FLOAT", "EDGE")
    for e in me.edges:
        a, b = me.vertices[e.vertices[0]].co, me.vertices[e.vertices[1]].co
        vertical = abs(a.x - b.x) < 1e-6 and abs(a.y - b.y) < 1e-6 and abs(a.z - b.z) > H * 0.9
        corner = abs(abs(a.x) - W / 2) < 1e-6 and abs(abs(a.y) - D / 2) < 1e-6
        att.data[e.index].value = 1.0 if (vertical and corner) else 0.0
    m1 = ob.modifiers.new("Bevel_Corners", "BEVEL")
    m1.limit_method = "WEIGHT"
    m1.width = 0.02
    m1.segments = 4
    m2 = ob.modifiers.new("Bevel_Edges", "BEVEL")
    m2.limit_method = "ANGLE"
    m2.angle_limit = math.radians(30)
    m2.width = 0.003
    m2.segments = 2
    m2.harden_normals = True
    for p in me.polygons:
        p.use_smooth = True


def build(sol):
    L.reset("SC_Device")
    L.studio(subject_height=0.6)
    col = L.collection("PROPS")
    paint = L.material("MAT_Paint_Yellow", (0.85, 0.6, 0.08), 0.35)
    me = bpy.data.meshes.new("ME_Device")
    bm = bmesh.new()
    body(bm)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Device", me)
    col.objects.link(ob)
    me.materials.append(paint)
    if sol:
        solve(ob)
    cam = L.obj("CAM_Main")
    cam.location = (1.0, -1.7, 1.05)
    cam.data.lens = 50
    L.obj("EMP_Target").location = (0, 0, 0.27)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_05_device_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_05_device_solution.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_05_device_reference.png")
    bpy.ops.render.render(write_still=True)
    cam = L.obj("CAM_Main")
    cam.location = (0.55, -0.6, 0.75)
    cam.data.lens = 70
    L.obj("EMP_Target").location = (0.12, -0.06, 0.47)     # coin supérieur avant droit
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_05_device_closeup.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
