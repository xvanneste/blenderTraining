"""
build_ch08_04_files.py — « Particules et distribution » (CH08.04 : une fontaine de particules qui retombent et rebondissent sur le sol).

Scène : EMITTER (grille de 2 × 2 carrés, 0,5 m de côté, à z = 1 m, normales vers le haut) et COL_Floor (plan de 6 × 6 m à z = 0).
  Solution : système de particules sur EMITTER : 200 particules, émises de l'image 1 à 30 depuis les faces, durée de vie 60 images, vitesse normale 3, physique Newtonienne, gravité 1,
             rendu « None » (les particules ne sont que simulées) ; COL_Floor : modificateur Collision (amortissement 0,5). Plage 1–120.
  Mesures de la solution (simulation de l'image 1 à 100) : image 15 : 97 particules vivantes (49 % de 200) ; image 30 : 200 ; sommet 1,46 m ; image 75 : 103 vivantes ; image 90 : 0 ; plus bas 0,01 m.
  STARTER_FILES/ch08_04_particles_starter.blend : l'émetteur et le sol sans physique. COMPLETED_EXAMPLES/ch08_04_particles_solution.blend (+ _reference.png : nuage de particules vu de côté aux images 10, 20, 40, 60)
  COUNTER_EXAMPLES/ : no_floor, short_life, no_gravity, too_few, burst, static
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_04_files.py
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
NOTE = """CH08.04 — PARTICULES (EMITTER, COL_Floor)
L'émetteur (EMITTER, à 1 m de haut) doit lancer une fontaine de particules :
1. EMITTER : Physics/Particles > Particle System : Emitter ; Number 200 ; Frame Start 1, End 30 ; Lifetime 60 ; Emit From Faces ; Velocity > Normal 3 ; Physics Newtonian ; Gravity 1 (Field Weights) ; Render As None.
2. COL_Floor : Physics > Collision (les particules rebondissent : Damping 0,5).
3. Plage 1–120.
Le correcteur configure ET simule (images 1 à 100, pas à pas) : émission étalée sur 30 images (moitié environ à l'image 15, tout à l'image 30), sommet de la fontaine entre 1,3 et 3 m, aucune particule sous le sol, toutes mortes à l'image 95.
Vérification : SCRIPTS/validate_ch08_04.py -- --exercise particles
"""


def mesh_obj(name, bm, loc):
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def build(kind):
    L.reset("SC_PARTICLES")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 120
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=0.5)
    em = mesh_obj("EMITTER", bm, (0, 0, 1))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=6.0)
    floor = mesh_obj("COL_Floor", bm, (0, 0, 0))
    if kind != "starter":
        if kind != "no_floor":
            floor.modifiers.new("Collision", "COLLISION")
            floor.collision.damping = 0.5
        em.modifiers.new("Particles", "PARTICLE_SYSTEM")
        st = em.particle_systems[0].settings
        st.count = 40 if kind == "too_few" else 200
        st.frame_start, st.frame_end = 1, (5 if kind == "burst" else 30)
        st.lifetime = 20 if kind == "short_life" else 60
        st.emit_from = "FACE"
        st.use_emit_random = True
        st.normal_factor = 0.0 if kind == "static" else 3.0
        st.physics_type = "NEWTON"
        st.render_type = "NONE"
        st.effector_weights.gravity = 0.0 if kind == "no_gravity" else 1.0
    sc.frame_set(1)
    L.instructions(NOTE)
    return em


def sketch(path):
    em = build("solution")
    sc = bpy.context.scene
    W, H = 800, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    img[250, 10:W - 10] = (0.3, 0.3, 0.3)
    for f in range(1, 61):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (10, 20, 40, 60):
            panel = (10, 20, 40, 60).index(f)
            ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
            for q in ev.particle_systems[0].particles:
                if q.alive_state == "ALIVE":
                    x, y = int(panel * 200 + 100 + q.location.x * 60), int(250 - q.location.z * 90)
                    if 2 <= x < W - 2 and 2 <= y < H - 2:
                        img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_04_particles_starter.blend"))
    for k in ("no_floor", "short_life", "no_gravity", "too_few", "burst", "static"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_04_particles_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_04_particles_solution.blend"))
    sketch(os.path.join(out, "ch08_04_particles_reference.png"))


if __name__ == "__main__":
    L.run(main)
