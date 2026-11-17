"""
build_ch03_02_files.py — « Premier sculpt : un visage simple » (CH03.02, Sculpt Mode).

  STARTER_FILES/ch03_02_face_starter.blend
      SCULPT_Head : sphère quadrangulée de 1 m de rayon (cube subdivisé ×6 projeté, 24 576 faces),
      positions d'origine mémorisées dans l'attribut « bcma_orig » (pour mesurer le sculpt) ;
      visage tourné vers −Y (vue de face Num 1) ; caméra et lumière de studio.
  COMPLETED_EXAMPLES/ch03_02_face_solution.blend (+ _reference.png)
      Visage stylisé : nez (relief +12 cm), arcades, orbites creusées (−6 cm), pommettes, sillon de
      bouche ; parfaitement symétrique en X (Mirror X activé) ; arrière du crâne MASQUÉ (.sculpt_mask = 1)
      et intact ; 3 Face Sets (visage, côtés, arrière).
NOTE : la solution livrée est sculptée à la brosse (Blender 5.2 via MCP, marqueur .sculpted_with_mcp). Ce script ne produit qu'un repli scripté : en 5.3 -b les opérateurs de sculpture plantent, la version de repli est donc
générée par des déplacements calculés le long de la normale (équivalents aux brosses Draw / Clay Strips,
inversées pour creuser) et par écriture directe des attributs de masque et de Face Sets.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_02_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH03.02 — PREMIER SCULPT : UN VISAGE SIMPLE (SCULPT_Head, Sculpt Mode : Ctrl+Tab)
Le visage regarde vers −Y (vue de face : Num 1).
1. En-tête : Mirror X activé (symétrie).
2. Masque : brosse Mask (M) ou B (rectangle) — masquez TOUT l'arrière du crâne pour le protéger.
3. Sculptez : un NEZ en relief (Draw V, Clay Strips C), deux ORBITES creusées (Ctrl + Draw), des
   arcades, des pommettes, un sillon de bouche (Crease Polish Shift+C) ; lissez avec Shift.
   Rayon : F, force : Shift+F. Ne touchez pas à la densité (pas de DynTopo / Remesh dans ce chapitre).
4. Face Sets : au moins 2 zones (Face Set Paint, ou Face Sets > Initialize Face Sets).
Vérification : SCRIPTS/validate_ch03_02.py -- --exercise face
"""
FEATURES = [  # direction (visage vers −Y), amplitude (m), largeur angulaire (rad), étirement en x
    ((0.0, -0.99, -0.08), 0.12, 0.16, 1.0),     # nez
    ((0.0, -0.96, 0.05), 0.04, 0.12, 1.0),      # arête du nez
    ((0.30, -0.88, 0.32), 0.045, 0.14, 1.6),    # arcade
    ((0.33, -0.88, 0.17), -0.06, 0.12, 1.2),    # orbite
    ((0.46, -0.80, -0.12), 0.04, 0.18, 1.0),    # pommette
    ((0.0, -0.93, -0.36), -0.025, 0.07, 3.5),   # sillon de bouche
    ((0.0, -0.88, -0.47), 0.03, 0.12, 2.0),     # menton
]


def quad_sphere():
    bpy.ops.mesh.primitive_cube_add(size=2)
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_Head", "ME_SCULPT_Head"
    m = ob.modifiers.new("Subdivision", "SUBSURF")
    m.levels = 6
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    me = ob.data
    co = np.zeros(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co /= np.linalg.norm(co, axis=1)[:, None]
    me.vertices.foreach_set("co", co.ravel())
    a = me.attributes.new("bcma_orig", "FLOAT_VECTOR", "POINT")
    a.data.foreach_set("vector", co.ravel())
    for p in me.polygons:
        p.use_smooth = True
    me.update()
    return ob, co


def sculpt(ob, orig):
    me = ob.data
    n = orig                                         # sphère de rayon 1 : normale = position
    disp = np.zeros(len(n))
    for d, amp, width, sx in FEATURES:
        for side in ((1, -1) if d[0] != 0 else (1,)):
            v = np.array((d[0] * side, d[1], d[2]))
            v /= np.linalg.norm(v)
            # distance angulaire, étirée horizontalement (sx > 1 = forme allongée en x)
            dx = (n[:, 0] - v[0]) / sx
            dist = np.sqrt(dx ** 2 + (n[:, 1] - v[1]) ** 2 + (n[:, 2] - v[2]) ** 2)
            disp += amp * np.exp(-(dist / width) ** 2)
    mask = np.clip((n[:, 1] - 0.05) / 0.25, 0, 1)   # arrière (y > 0,3) entièrement masqué
    disp *= (1 - mask)
    co = n * (1 + disp)[:, None]
    me.vertices.foreach_set("co", co.ravel())
    m = me.attributes.new(".sculpt_mask", "FLOAT", "POINT")
    m.data.foreach_set("value", mask)
    fs = me.attributes.new(".sculpt_face_set", "INT", "FACE")
    vals = []
    for p in me.polygons:
        c = p.center
        vals.append(1 if c.y < -0.35 else (3 if c.y > 0.3 else 2))
    fs.data.foreach_set("value", vals)
    me.use_mirror_x = True
    me.update()


def build(sol):
    sc = L.reset("SC_Sculpt")
    ob, orig = quad_sphere()
    ob.data.materials.append(L.material("MAT_Clay", (0.72, 0.55, 0.45), 0.55))
    if sol:
        sculpt(ob, orig)
    ob.location.z = 1.1                              # posée au-dessus du sol du studio
    L.studio(subject_height=1.8)
    cam = L.camera("CAM_Face", L.collection("CAMERAS"), (1.5, -3.6, 1.6), 50, make_active=True)
    S.look_at(cam, (0, 0, 1.05))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    sc.render.resolution_x = sc.render.resolution_y = 1080
    L.instructions(NOTE)
    return sc


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_02_face_starter.blend"))
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] solution sculptée à la brosse (Blender 5.2 via MCP) conservée : non régénérée")
        return
    sc = build(True)          # version SCRIPTÉE (repli) : n'est utilisée que si la solution sculptée est absente
    L.save(os.path.join(out, "ch03_02_face_solution.blend"))
    sc.render.filepath = os.path.join(out, "ch03_02_face_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
