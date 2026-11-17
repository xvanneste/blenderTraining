"""
build_ch08_09_files.py — « Forces » (CH08.09 : un vent et une turbulence font dériver un nuage de particules).

Scène : EMITTER (grille de 0,5 m à z = 0,3 m, 300 particules émises de l'image 1 à 40, durée de vie 80, Normal 2, gravité à 20 %, pas de rendu des particules).
  Solution : FORCE_Wind (Empty de champ Wind, force 5, tourné de +90° autour de Y : il souffle vers +X) et FORCE_Turb (champ Turbulence, force 5, taille 0,5).
  Mesures de la solution (image 60, 300 particules vivantes) : x moyen 3,9 m (sans vent : 0,01 m ; vent seul : 4,06 m ; vent −90° : −4,04 m) ; écart-type en y 0,30 m (sans turbulence : 0,15 m ; turbulence seule : 0,48 m).
  STARTER_FILES/ch08_09_forces_starter.blend : l'émetteur seul. COMPLETED_EXAMPLES/ch08_09_forces_solution.blend (+ _reference.png : vue de dessus des particules à l'image 60 : sans force, vent seul, vent + turbulence)
  COUNTER_EXAMPLES/ : no_wind, wrong_direction, weak_wind, no_turbulence, ignore_wind
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_09_files.py
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
NOTE = """CH08.09 — FORCES (EMITTER, FORCE_Wind, FORCE_Turb)
Un nuage de 300 particules doit être poussé vers +X par un vent et brassé par une turbulence.
1. Add > Force Field > Wind : nommez-le FORCE_Wind ; Strength 5 ; tournez-le de 90° autour de Y (le vent souffle selon son axe local Z, ici vers +X).
2. Add > Force Field > Turbulence : nommez-le FORCE_Turb ; Strength 5 ; Size 0,5.
3. Particules de EMITTER > Field Weights : Wind et Turbulence à 1 (valeurs par défaut).
4. Images 1–100, lecture dans l'ordre.
Contrôles (image 60) : au moins 280 particules vivantes ; x moyen de 2,5 à 8 m ; écart-type en y d'au moins 0,25 m (turbulence).
Vérification : SCRIPTS/validate_ch08_09.py -- --exercise forces
"""


def build(kind):
    L.reset("SC_FORCES")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 100
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=0.25)
    me = bpy.data.meshes.new("ME_EMITTER")
    bm.to_mesh(me)
    bm.free()
    em = bpy.data.objects.new("EMITTER", me)
    sc.collection.objects.link(em)
    em.location = (0, 0, 0.3)
    em.modifiers.new("Particles", "PARTICLE_SYSTEM")
    st = em.particle_systems[0].settings
    st.count = 300
    st.frame_start, st.frame_end = 1, 40
    st.lifetime = 80
    st.emit_from = "FACE"
    st.normal_factor = 2.0
    st.physics_type = "NEWTON"
    st.render_type = "NONE"
    st.effector_weights.gravity = 0.2
    if kind != "starter":
        if kind != "no_wind":
            rot = -90 if kind == "wrong_direction" else 90
            bpy.ops.object.effector_add(type="WIND", location=(0, 0, 0.3), rotation=(0, math.radians(rot), 0))
            w = bpy.context.object
            w.name = "FORCE_Wind"
            w.field.strength = 0.3 if kind == "weak_wind" else 5.0
        if kind != "no_turbulence":
            bpy.ops.object.effector_add(type="TURBULENCE", location=(0, 0, 0.3))
            t = bpy.context.object
            t.name = "FORCE_Turb"
            t.field.strength, t.field.size = 5.0, 0.5
        if kind == "ignore_wind":
            st.effector_weights.wind = 0.0
    bpy.ops.object.select_all(action="DESELECT")
    sc.frame_set(1)
    L.instructions(NOTE)
    return em


def positions(em, frame):
    sc = bpy.context.scene
    sc.frame_set(1)
    for f in range(1, frame + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return np.array([p.location[:] for p in ev.particle_systems[0].particles if p.alive_state == "ALIVE"])


def sketch(path):
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    for panel, kind in enumerate(("starter", "no_turbulence", "solution")):
        P = positions(build(kind), 60)
        ox, oy = panel * 260 + 60, 150
        img[oy:oy + 1, panel * 260 + 10:panel * 260 + 250] = (0.3, 0.3, 0.3)
        for p in P:
            x, y = int(ox + 24 * p[0]), int(oy - 24 * p[1])
            if 0 <= x < W - 3 and 0 <= y < H - 3:
                img[y:y + 3, x:x + 3] = (0.95, 0.6, 0.25)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_09_forces_starter.blend"))
    for k in ("no_wind", "wrong_direction", "weak_wind", "no_turbulence", "ignore_wind"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch08_09_forces_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch08_09_forces_solution.blend"))
    sketch(os.path.join(out, "ch08_09_forces_reference.png"))


if __name__ == "__main__":
    L.run(main)
