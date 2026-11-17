"""
build_ch08_03_files.py — « Cloth » (CH08.03 : un tissu qui drape une sphère et se pose sur le sol).

Scène : CLOTH_Sheet (grille de 40 × 40 carrés, 2,4 × 2,4 m, à z = 1,2 m, 1 681 sommets), COL_Ball (sphère de rayon 0,5 m centrée à l'origine), COL_Floor (plan de 6 × 6 m à z = −0,5 m, tangent à la sphère).
  Solution : CLOTH_Sheet : modificateur Cloth (Quality 12, Bending 0,4, Air Damping 5) ; Collisions : activées, Quality 5, Distance 5 mm, auto-collision désactivée ;
             COL_Ball et COL_Floor : modificateur Collision. Plage 1–120.
  Mesures de la solution (simulation de l'image 1 à 120) : sommet central posé sur la sphère à z = 0,525 m ; aucun sommet à moins de 0,52 m du centre de la sphère ; point le plus bas −0,475 m (le tissu repose sur le sol à −0,5 m, épaisseur comprise) ; au repos (9 mm entre les images 110 et 120).
  STARTER_FILES/ch08_03_cloth_starter.blend : les trois objets sans physique. COMPLETED_EXAMPLES/ch08_03_cloth_solution.blend (+ _reference.png : profil du tissu aux images 1, 30 et 120)
  COUNTER_EXAMPLES/ : no_ball_collision, no_floor_collision, low_quality, no_gravity
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_03_files.py
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
NOTE = """CH08.03 — CLOTH (CLOTH_Sheet, COL_Ball, COL_Floor)
Un drap de 2,4 m doit tomber sur une sphère et se poser sur le sol. Physics :
1. CLOTH_Sheet : Cloth ; Quality 12 ; Bending Stiffness 0,4 ; Air Damping 5 ; Collisions : cochées, Quality 5, Distance 5 mm (0,005), Self Collisions décochées.
2. COL_Ball et COL_Floor : Collision (obstacles du tissu).
3. Plage 1–120 ; lisez depuis l'image 1.
Le correcteur configure ET simule (images 1 à 120, pas à pas) : le drap repose sur la sphère (z central 0,50 à 0,58 m), n'entre pas dans la sphère (≥ 0,49 m du centre), ne traverse pas le sol (z ≥ −0,505 m), est immobile à la fin (≤ 2 cm entre les images 110 et 120).
Vérification : SCRIPTS/validate_ch08_03.py -- --exercise cloth
"""


def mesh_obj(name, bm, loc=(0, 0, 0)):
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def build(kind):
    L.reset("SC_CLOTH")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 120
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=40, y_segments=40, size=1.2)
    for v in bm.verts:
        v.co.z = 1.2
    cloth = mesh_obj("CLOTH_Sheet", bm)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.5)
    ball = mesh_obj("COL_Ball", bm)
    for p in ball.data.polygons:
        p.use_smooth = True
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=3.0)
    floor = mesh_obj("COL_Floor", bm, (0, 0, -0.5))
    if kind != "starter":
        if kind != "no_ball_collision":
            ball.modifiers.new("Collision", "COLLISION")
        if kind != "no_floor_collision":
            floor.modifiers.new("Collision", "COLLISION")
        md = cloth.modifiers.new("Cloth", "CLOTH")
        s = md.settings
        s.quality = 1 if kind == "low_quality" else 12
        s.bending_stiffness = 0.4
        s.air_damping = 5.0
        c = md.collision_settings
        c.use_collision = True
        c.collision_quality = 1 if kind == "low_quality" else 5
        c.distance_min = 0.05 if kind == "low_quality" else 0.005
        c.use_self_collision = False
        if kind == "no_gravity":
            s.effector_weights.gravity = 0.0
    sc.frame_set(1)
    L.instructions(NOTE)
    return cloth


def sketch(path):
    cloth = build("solution")
    sc = bpy.context.scene
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    for f in range(1, 121):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (1, 30, 120):
            panel = (1, 30, 120).index(f)
            ev = cloth.evaluated_get(bpy.context.evaluated_depsgraph_get())
            m = ev.to_mesh()
            for v in m.vertices:
                if abs(v.co.y) < 0.04:
                    x, y = int(panel * 260 + 130 + v.co.x * 80), int(200 - v.co.z * 80)
                    if 2 <= x < W - 2 and 2 <= y < H - 2:
                        img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2)
            ev.to_mesh_clear()
            for t in np.linspace(0, 6.2832, 120):
                x, y = int(panel * 260 + 130 + 0.5 * 80 * np.cos(t)), int(200 - 0.5 * 80 * np.sin(t))
                img[y, x] = (0.3, 0.7, 1.0)
            img[240, panel * 260 + 10:panel * 260 + 250] = (0.3, 0.3, 0.3)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_03_cloth_starter.blend"))
    for k in ("no_ball_collision", "no_floor_collision", "low_quality", "no_gravity"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_03_cloth_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_03_cloth_solution.blend"))
    sketch(os.path.join(out, "ch08_03_cloth_reference.png"))


if __name__ == "__main__":
    L.run(main)
