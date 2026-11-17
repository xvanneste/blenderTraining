"""
build_ch08_08_files.py — « Cheveux et fourrure » (CH08.08 : un système de particules de type Hair sur une tête, avec enfants, mèches et dynamique).

Scène : Head (UV sphère de 1 m de rayon, 32 × 16) avec un groupe de sommets « scalp » (sommets de z > 0,3 : la calotte).
  Solution : système de particules « Hair » : Type Hair, Number 300, Hair Length 0,5 m, Segments (hair_step) 6, densité par le groupe « scalp » (Vertex Groups > Density),
             Children : Interpolated, 10 enfants par cheveu (Display Amount), Clumping 0,5 (mèches), Hair Dynamics activée (ps.use_hair_dynamics).
  Mesures de la solution (images 1 → 30, lues une à une) : 300 racines, toutes à z ≥ 0,23 ; longueur 0,5 m ; 3 000 enfants ; distance moyenne enfant–parent (extrémités, 5e étape) 0,0385 m (0,073 sans mèches, 0 avec Clumping 1) ;
             hauteur moyenne des pointes 0,96 m à l'image 1, 0,28 m à l'image 30 (les cheveux retombent).
  STARTER_FILES/ch08_08_hair_starter.blend : la tête et son groupe « scalp ». COMPLETED_EXAMPLES/ch08_08_hair_solution.blend (+ _reference.png : cheveux parents vus de face aux images 1 et 30)
  COUNTER_EXAMPLES/ : no_group, no_children, no_clump, no_dynamics, short, too_few
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_08_files.py
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
NOTE = """CH08.08 — CHEVEUX ET FOURRURE (Head)
Une tête de 1 m de rayon doit porter 300 cheveux de 0,5 m, uniquement sur la calotte (groupe de sommets « scalp »), regroupés en mèches, qui retombent sous la pesanteur.
1. Head : Physics ou Particles > + : nouveau système ; Type Hair ; Number 300 ; Hair Length 0,5 m ; Segments 6.
2. Vertex Groups > Density : « scalp ».
3. Children : Interpolated ; Display Amount 10 ; Clumping : 0,5.
4. Hair Dynamics : coché. Images 1–30 (à lire dans l'ordre).
Contrôles : racines sur la calotte (z ≥ 0,15) ; longueur 0,4–0,6 m ; au moins 2 000 enfants ; mèches (distance enfant–parent ≤ 0,055 m) ; les pointes descendent d'au moins 0,3 m entre l'image 1 et l'image 30.
Vérification : SCRIPTS/validate_ch08_08.py -- --exercise hair
"""


def head():
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    me = bpy.data.meshes.new("ME_Head")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Head", me)
    bpy.context.scene.collection.objects.link(ob)
    vg = ob.vertex_groups.new(name="scalp")
    for v in me.vertices:
        if v.co.z > 0.3:
            vg.add([v.index], 1.0, "REPLACE")
    return ob


def build(kind):
    L.reset("SC_HAIR")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 30
    ob = head()
    if kind != "starter":
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.particle_system_add()
        ps = ob.particle_systems[0]
        ps.name = "Hair"
        s = ps.settings
        s.name = "HairSettings"
        s.type = "HAIR"
        s.count = 50 if kind == "too_few" else 300
        s.hair_length = 0.15 if kind == "short" else 0.5
        s.hair_step = 6
        if kind != "no_group":
            ps.vertex_group_density = "scalp"
        if kind != "no_children":
            s.child_type = "INTERPOLATED"
            s.child_percent = 10
        s.clump_factor = 0.0 if kind == "no_clump" else 0.5
        ps.use_hair_dynamics = kind != "no_dynamics"
        ob.select_set(False)
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def parents_at(ob, frame):
    sc = bpy.context.scene
    sc.frame_set(1)
    for f in range(1, frame + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    eps = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).particle_systems[0]
    return [[k.co[:] for k in p.hair_keys] for p in eps.particles]


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    sc.frame_set(1)
    a = parents_at(ob, 1)
    b = parents_at(ob, 30)
    W, H = 780, 330
    img = np.full((H, W, 3), 0.08, np.float32)
    S = 100
    for panel, hairs in enumerate((a, b)):
        ox, oy = panel * 390 + 195, 270
        for r in range(-30, 30):
            for c in range(-30, 30):
                if r * r + c * c <= 900 and 0 <= oy - 0 - r < H:
                    pass
        for hair in hairs:
            for key in hair:
                x, y = int(ox + S * key[0]), int(oy - S * key[2])
                if 0 <= x < W - 2 and 0 <= y < H - 2:
                    img[y:y + 2, x:x + 2] = (0.95, 0.6, 0.25)
        img[int(oy):int(oy) + 2, panel * 390 + 20:panel * 390 + 370] = (0.3, 0.3, 0.3)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_08_hair_starter.blend"))
    for k in ("no_group", "no_children", "no_clump", "no_dynamics", "short", "too_few"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_08_hair_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_08_hair_solution.blend"))
    sketch(os.path.join(out, "ch08_08_hair_reference.png"))


if __name__ == "__main__":
    L.run(main)
