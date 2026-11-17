"""
build_ch08_02_files.py — « Soft Bodies » (CH08.02 : une plaque souple accrochée par un bord, le « goal »).

Une plaque GEO_Plate (grille de 12 × 12 carrés, 2 × 2 m, à z = 2 m, 169 sommets, 312 arêtes) avec un groupe de sommets « pin » (poids 1 sur le bord x = −1, poids 0 ailleurs, explicitement).
  Solution : modificateur Soft Body : Goal coché, groupe « pin », Goal Default 1,0 (les sommets sans poids restent fixes ; les poids explicites 0 les libèrent), Min 0, Max 1 ; masse 1 kg ; Edges coché, Pull 0,9, Push 0,9, Bending 1,0 ;
             la plaque pendue par son bord se balance sans s'étirer.
  Mesures de la solution (simulation de l'image 1 à 100) : bord accroché immobile (0 mm) ; bord libre à z moyen 0,19 m (il pend) ; arête la plus étirée 1,01 fois sa longueur de repos ; plus bas 0,16 m.
  STARTER_FILES/ch08_02_softbody_starter.blend : la plaque et son groupe « pin », sans modificateur. COMPLETED_EXAMPLES/ch08_02_softbody_solution.blend (+ _reference.png : profil de la plaque à l'image 1, 40 et 100)
  COUNTER_EXAMPLES/ : no_goal, no_group, soft_edges, heavy_mass, no_edges
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_02_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.02 — SOFT BODIES (GEO_Plate)
La plaque GEO_Plate (2 × 2 m, à 2 m de haut) a un groupe de sommets « pin » : poids 1 sur son bord gauche (x = −1), poids 0 ailleurs. Rendez-la souple : Physics > Soft Body.
1. Soft Body Goal : coché ; Vertex Group « pin » ; Default 1,0 ; Min 0, Max 1 (les sommets de poids 1 restent accrochés, ceux de poids 0 sont libres).
2. Soft Body Edges : coché ; Pull 0,9, Push 0,9, Bending 1,0 (la plaque ne s'étire pas) ; masse 1 kg.
Lisez la simulation depuis l'image 1 : la plaque pend par son bord et se balance.
Le correcteur configure ET simule (images 1 à 100, pas à pas) : bord accroché immobile, bord libre qui pend, arêtes non étirées (≤ 1,15 fois), rien ne tombe à l'infini.
Vérification : SCRIPTS/validate_ch08_02.py -- --exercise softbody
"""


def build(kind):
    L.reset("SC_SOFT")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 100
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=12, y_segments=12, size=1.0)
    for v in bm.verts:
        v.co.z = 2.0
    me = bpy.data.meshes.new("ME_Plate")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Plate", me)
    sc.collection.objects.link(ob)
    xmin = min(v.co.x for v in me.vertices)
    vg = ob.vertex_groups.new(name="pin")
    for v in me.vertices:
        vg.add([v.index], 1.0 if v.co.x < xmin + 1e-4 else 0.0, "REPLACE")
    if kind != "starter":
        md = ob.modifiers.new("Softbody", "SOFT_BODY")
        s = md.settings
        s.use_goal = kind != "no_goal"
        s.vertex_group_goal = "" if kind == "no_group" else "pin"
        s.goal_default, s.goal_min, s.goal_max = 1.0, 0.0, 1.0
        s.goal_spring, s.goal_friction = 0.9, 0.5
        s.mass = 30.0 if kind == "heavy_mass" else 1.0
        s.use_edges = kind != "no_edges"
        s.bend = 1.0
        s.pull = s.push = 0.02 if kind == "soft_edges" else 0.9
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    for f in range(1, 101):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (1, 40, 100):
            panel = (1, 40, 100).index(f)
            ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
            m = ev.to_mesh()
            for v in m.vertices:
                x, y = int(panel * 260 + 130 + v.co.x * 55), int(40 + (2.0 - v.co.z) * 55)
                if 2 <= x < W - 2 and 2 <= y < H - 2:
                    img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2) if v.co.x > -0.99 else (0.3, 0.8, 0.5)
            ev.to_mesh_clear()
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_02_softbody_starter.blend"))
    for k in ("no_goal", "no_group", "soft_edges", "heavy_mass", "no_edges"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_02_softbody_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_02_softbody_solution.blend"))
    sketch(os.path.join(out, "ch08_02_softbody_reference.png"))


if __name__ == "__main__":
    L.run(main)
