"""
build_ch02_10_files.py — « Alléger sans abîmer » (CH02.10, optimisation).

  STARTER_FILES/ch02_10_optim_starter.blend
      GEO_Statue      : Suzanne subdivisée niveau 3 appliqué (31 488 faces), à alléger ;
      GEO_Statue_REF  : copie identique, cachée et non rendue (référence du correcteur, à ne pas toucher) ;
      GEO_Imported    : modèle « importé » sale : faces détachées (sommets en double),
                        30 sommets et 10 arêtes isolés.
  COMPLETED_EXAMPLES/ch02_10_optim_solution.blend (+ _reference.png)
      GEO_Statue : Decimate Collapse 0,2 ; GEO_Statue_LOD1 (0,08) et GEO_Statue_LOD2 (0,015) en
      copies LIÉES (Alt+D) dans la collection LOD ; GEO_Imported nettoyé (By Distance, Delete Loose).
Usage : blender -b --factory-startup --python build_ch02_10_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.10 — ALLÉGER SANS ABÎMER (Statistics activées)
1. GEO_Statue (31 488 faces) : Add Modifier > Generate > Decimate, Collapse, Ratio 0.2
   (≤ 25 % des faces). Comparez à l'œil : la silhouette ne doit pas changer.
2. LOD : Alt+D (copie liée) de GEO_Statue deux fois → GEO_Statue_LOD1 (Decimate Ratio ≤ 0.1)
   et GEO_Statue_LOD2 (Ratio ≤ 0.02), rangées dans une collection LOD, décalées en X (x = -1,3 et 0).
3. GEO_Imported : Edit Mode, A, M > By Distance ; puis Mesh > Clean Up > Delete Loose.
NE TOUCHEZ PAS GEO_Statue_REF (cachée) : elle sert à mesurer l'écart.
Vérification : SCRIPTS/validate_ch02_10.py -- --exercise optim
"""


def monkey(level):
    bpy.ops.mesh.primitive_monkey_add(size=1.2)
    ob = bpy.context.active_object
    if level:
        m = ob.modifiers.new("s", "SUBSURF")
        m.levels = level
        bpy.ops.object.modifier_apply(modifier=m.name)
    ob.rotation_euler = (0, 0, 0)
    return ob


def build(sol):
    L.reset("SC_Optim")
    L.studio(subject_height=1.0)
    col = L.collection("ASSETS")
    bronze = L.material("MAT_Bronze", (0.55, 0.38, 0.2), 0.35, metallic=1.0)
    clay = L.material("MAT_Clay", (0.75, 0.72, 0.68), 0.6)
    st = monkey(3)
    st.name, st.data.name = "GEO_Statue", "ME_Statue"
    st.location = (-2.6, 0, 0.65)
    L.move_to(st, col)
    st.data.materials.append(bronze)
    for p in st.data.polygons:
        p.use_smooth = True
    ref = st.copy()
    ref.data = st.data.copy()
    ref.name, ref.data.name = "GEO_Statue_REF", "ME_Statue_REF"
    refcol = L.collection("REFERENCE")
    refcol.objects.link(ref)
    ref.hide_viewport = ref.hide_render = True
    ref.hide_select = True
    im = monkey(1)
    im.name, im.data.name = "GEO_Imported", "ME_Imported"
    im.location = (2.0, 0, 0.65)
    L.move_to(im, col)
    im.data.materials.append(clay)
    bm = bmesh.new()
    bm.from_mesh(im.data)
    bmesh.ops.split_edges(bm, edges=bm.edges[:])
    rnd = random.Random(3)
    loose = [bm.verts.new((rnd.uniform(-0.6, 0.6), rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5))) for _ in range(30)]
    for i in range(10):
        a = bm.verts.new((rnd.uniform(-0.6, 0.6), 0.7, rnd.uniform(-0.4, 0.4)))
        b = bm.verts.new((a.co.x + 0.05, 0.72, a.co.z))
        bm.edges.new((a, b))
    if sol:
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)
        wires = [v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm, geom=wires, context="VERTS")
    bm.to_mesh(im.data)
    bm.free()
    if sol:
        d = st.modifiers.new("Decimate", "DECIMATE")
        d.decimate_type = "COLLAPSE"
        d.ratio = 0.2
        lodcol = L.collection("LOD")
        for name, ratio, x in (("GEO_Statue_LOD1", 0.08, -1.3), ("GEO_Statue_LOD2", 0.015, 0.0)):
            lod = st.copy()                      # copie LIÉE : même maillage (Alt+D)
            lod.name = name
            lod.location.x = x
            lodcol.objects.link(lod)
            lod.modifiers["Decimate"].ratio = ratio
    cam = L.obj("CAM_Main")
    cam.location = (-0.3, -6.5, 1.8)
    cam.data.lens = 32
    L.obj("EMP_Target").location = (-0.3, 0, 0.6)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_10_optim_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_10_optim_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_10_optim_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
