"""
build_ch08_01_files.py — « Rigid Bodies » (CH08.01 : un mur de briques qu'une boule fait s'effondrer).

Scène : GEO_Ground (dalle 60 × 60 × 1 m, face supérieure à z = 0), 30 briques BRICK_rc (6 rangs × 5 colonnes, 0,3 × 0,6 × 0,3 m, rangs impairs décalés de 0,3 m, mur au centre, le long de Y),
        BALL_Impact (cube de 0,8 m de côté, centre à z = 0,9) qui arrive de x = −6 vers x = −1 (images 1 → 21, animé) puis est LÂCHÉE : elle continue sur sa lancée et heurte le mur.
  Solution : monde de corps rigides (images 1–150, substeps 10) ; sol PASSIVE (forme Box) ; briques ACTIVE (masse 1 kg, friction 0,6, forme Box, marge 0) ; boule ACTIVE (masse 20 kg, forme Box) avec « Animated » (kinematic)
             coché à l'image 1 et décoché à l'image 21 (clés sur rigid_body.kinematic).
  Mesures de la solution : avant l'impact (image 12) les briques ont bougé de 8 mm au plus ; après 150 images 21 briques sur 30 ont bougé de plus de 0,6 m.
  STARTER_FILES/ch08_01_rigid_starter.blend : les objets sans physique (la boule a sa trajectoire animée). COMPLETED_EXAMPLES/ch08_01_rigid_solution.blend (+ _reference.png : vue de dessus du mur avant et après l'effondrement)
  COUNTER_EXAMPLES/ : no_ground, passive_bricks, light_ball, no_release, low_friction, no_world_frames
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_01_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.01 — CORPS RIGIDES (mur de briques et boule)
Rendez la scène physique : Physics > Rigid Body.
1. GEO_Ground : Passive, forme Box. 2. Les 30 briques BRICK_* : Active, masse 1 kg, friction 0,6, forme Box, marge 0 (Collisions > Margin : cochée à 0). 3. BALL_Impact : Active, masse 20 kg, forme Box ;
   « Animated » (Dynamics) coché à l'image 1 puis décoché à l'image 21 (clés) : la boule suit sa trajectoire animée puis est lâchée et heurte le mur.
4. Monde (Scene > Rigid Body World) : images 1 à 150, au moins 10 sous-étapes par image.
Le correcteur configure ET SIMULE (images 1 à 150 pas à pas) : mur stable avant l'impact, effondrement après, aucune brique sous le sol, boule en mouvement, mur au repos à la fin.
Vérification : SCRIPTS/validate_ch08_01.py -- --exercise rigid
"""


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def rb(ob, typ, **kw):
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.rigidbody.object_add(type=typ)
    for k, v in kw.items():
        setattr(ob.rigid_body, k, v)
    ob.select_set(False)


def build(kind):
    L.reset("SC_RIGID")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 150
    ground = box("GEO_Ground", (60, 60, 1), (0, 0, -0.5))
    bricks = []
    for row in range(6):
        for col in range(5):
            off = 0.3 if row % 2 else 0.0
            bricks.append(box(f"BRICK_{row}{col}", (0.3, 0.6, 0.3), (0, (col - 2) * 0.6 + off, 0.15 + row * 0.3)))
    ball = box("BALL_Impact", (0.8, 0.8, 0.8), (-6, 0, 0.9))
    ball.location = (-6, 0, 0.9)
    ball.keyframe_insert("location", frame=1)
    ball.location = (-1.0 if kind != "no_release" else -4.0, 0, 0.9)
    ball.keyframe_insert("location", frame=21)
    ball.location = (-6, 0, 0.9)
    if kind == "starter":
        L.instructions(NOTE)
        return
    if kind != "no_ground":
        rb(ground, "PASSIVE", collision_shape="BOX", friction=0.6)
    for b in bricks:
        rb(b, "PASSIVE" if kind == "passive_bricks" else "ACTIVE", mass=1.0, friction=0.05 if kind == "low_friction" else 0.6, collision_shape="BOX", use_margin=True, collision_margin=0.0)
    rb(ball, "ACTIVE", mass=0.3 if kind == "light_ball" else 20.0, collision_shape="BOX", kinematic=True)
    ball.rigid_body.keyframe_insert("kinematic", frame=1)
    ball.rigid_body.kinematic = kind == "no_release"
    ball.rigid_body.keyframe_insert("kinematic", frame=21)
    sc.rigidbody_world.substeps_per_frame = 10
    if kind == "no_world_frames":
        sc.rigidbody_world.point_cache.frame_end = 60
    sc.frame_set(1)
    L.instructions(NOTE)


def sketch(path):
    build("solution")
    sc = bpy.context.scene
    bricks = [o for o in bpy.data.objects if o.name.startswith("BRICK_")]
    ball = bpy.data.objects["BALL_Impact"]
    W, H = 760, 300
    img = np.full((H, W, 3), 0.08, np.float32)

    def px(p, panel):
        return int(panel * 380 + 190 + p.x * 14), int(150 - p.y * 14)
    for f in range(1, 151):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (1, 150):
            panel = 0 if f == 1 else 1
            for o in bricks:
                x, y = px(o.matrix_world.translation, panel)
                if 3 <= x < W - 3 and 3 <= y < H - 3:
                    img[y - 3:y + 4, x - 2:x + 3] = (0.9, 0.55, 0.2)
            x, y = px(ball.matrix_world.translation, panel)
            if 5 <= x < W - 5 and 5 <= y < H - 5:
                img[y - 5:y + 6, x - 5:x + 6] = (0.3, 0.7, 1.0)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_01_rigid_starter.blend"))
    for k in ("no_ground", "passive_bricks", "light_ball", "no_release", "low_friction", "no_world_frames"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_01_rigid_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_01_rigid_solution.blend"))
    sketch(os.path.join(out, "ch08_01_rigid_reference.png"))


if __name__ == "__main__":
    L.run(main)
