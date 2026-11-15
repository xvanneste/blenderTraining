"""
build_ch02_08_files.py — « L'arbre au modificateur Skin » (CH02.08, modélisation organique).

  STARTER_FILES/ch02_08_tree_starter.blend
      GEO_Tree : un objet maillage réduit à UN sommet (à l'origine), aucun modificateur.
  COMPLETED_EXAMPLES/ch02_08_tree_solution.blend (+ _reference.png, + _skeleton.png)
      Squelette de sommets/arêtes (tronc, 3 branches, 3 racines, rameaux), rayons Skin
      décroissants (18 cm à la base → 2,5 cm aux pointes), modificateur Skin puis Subdivision
      (Levels 1 / Render 2), Shade Smooth.
Usage : blender -b --factory-startup --python build_ch02_08_files.py --python-exit-code 1
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
NOTE = """CH02.08 — L'ARBRE AU MODIFICATEUR SKIN
GEO_Tree ne contient qu'UN sommet. Edit Mode (Tab), mode sommet (1) :
1. Tronc : E Z 0.8, puis E Z 0.7 (hauteur 1,5 m).
2. Branches : depuis le sommet du haut, E plusieurs fois dans 3 directions (≈ 0,8 m chacune),
   puis des rameaux. Racines : depuis le sommet du bas, 3 extrusions courtes vers l'extérieur.
3. Object Mode : Add Modifier > Generate > Skin, puis Subdivision Surface (Levels 1, Render 2).
4. Edit Mode : Ctrl+A (Skin Resize) pour épaissir la base (≈ 18 cm) et affiner les pointes
   (≈ 2–3 cm). Le premier sommet est la racine par défaut (sinon : bouton du modificateur Skin
   ou F3 > Skin Root Mark).
5. Object > Shade Smooth. Hauteur totale ≥ 1,5 m.
Vérification : SCRIPTS/validate_ch02_08.py -- --exercise tree
"""
# (position, rayon) ; arêtes = liste de chemins
NODES = {
    "base": ((0, 0, 0.0), 0.18), "mid": ((0, 0, 0.8), 0.13), "top": ((0, 0, 1.5), 0.10),
    "b1a": ((0.45, 0.1, 1.95), 0.07), "b1b": ((0.85, 0.15, 2.45), 0.035),
    "b2a": ((-0.4, 0.25, 2.0), 0.07), "b2b": ((-0.7, 0.5, 2.5), 0.035),
    "b3a": ((0.05, -0.45, 2.05), 0.065), "b3b": ((0.1, -0.7, 2.6), 0.03),
    "b4": ((0.0, 0.0, 2.2), 0.06), "b4b": ((0.05, 0.05, 2.75), 0.025),
    "t1": ((1.1, 0.0, 2.7), 0.025), "t2": ((-0.95, 0.6, 2.65), 0.025),
    "r1": ((0.35, 0.05, 0.02), 0.06), "r2": ((-0.25, 0.3, 0.02), 0.06), "r3": ((-0.1, -0.35, 0.02), 0.06),
}
PATHS = [("base", "mid", "top", "b1a", "b1b", "t1"), ("top", "b2a", "b2b", "t2"), ("top", "b3a", "b3b"),
         ("top", "b4", "b4b"), ("base", "r1"), ("base", "r2"), ("base", "r3")]


def build(sol):
    L.reset("SC_Tree")
    L.studio(subject_height=2.5)
    col = L.collection("PROPS")
    bark = L.material("MAT_Bark", (0.32, 0.22, 0.14), 0.85)
    me = bpy.data.meshes.new("ME_Tree")
    bm = bmesh.new()
    if not sol:
        bm.verts.new((0, 0, 0))
    else:
        idx = {}
        for k, (co, _r) in NODES.items():
            idx[k] = bm.verts.new(co)
        for path in PATHS:
            for a, b in zip(path, path[1:]):
                bm.edges.new((idx[a], idx[b]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Tree", me)
    col.objects.link(ob)
    me.materials.append(bark)
    if sol:
        sk = ob.modifiers.new("Skin", "SKIN")
        sk.branch_smoothing = 0.6
        names = list(NODES.keys())
        layer = me.skin_vertices[0].data
        for i, k in enumerate(names):
            r = NODES[k][1]
            layer[i].radius = (r, r)
            layer[i].use_root = (k == "base")
        ss = ob.modifiers.new("Subdivision", "SUBSURF")
        ss.levels, ss.render_levels = 1, 2
        # Shade Smooth via l'opérateur (le Skin génère la géométrie)
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.shade_smooth()
    cam = L.obj("CAM_Main")
    cam.location = (0, -6.5, 2.0)
    cam.data.lens = 40
    L.obj("EMP_Target").location = (0, 0, 1.35)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)
    return ob


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_08_tree_starter.blend"))
    ob = build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_08_tree_solution.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_08_tree_reference.png")
    bpy.ops.render.render(write_still=True)
    # image du squelette seul (modificateurs désactivés, fil de fer épais) — non enregistré
    for m in ob.modifiers:
        m.show_render = False
    w = ob.modifiers.new("Wire", "SKIN")
    for v in ob.data.skin_vertices[0].data:
        v.radius = (0.012, 0.012)
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_08_tree_skeleton.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
