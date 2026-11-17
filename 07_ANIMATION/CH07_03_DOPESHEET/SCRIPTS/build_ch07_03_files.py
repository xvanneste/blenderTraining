"""
build_ch07_03_files.py — « Dope Sheet et Action » (CH07.03 : retimer une animation, actions indépendantes, slots).

Deux caisses GEO_CrateA et GEO_CrateB (cubes de 1 m, A à y = 0, B à y = 2) et deux ACTIONS :
  « Slide » (GEO_CrateA) : position X = 0, 2, 4 aux images [1, 25, 49] dans la solution ; le starter l'a aux images [1, 13, 25] (à RETIMER : échelle ×2 du temps autour de l'image 1).
  « Slide_Late » (GEO_CrateB) : la même animation DÉCALÉE de 24 images : images [25, 49, 73], valeurs 0, 2, 4 ; action INDÉPENDANTE (pas la même que « Slide »).
  Chaque action est portée par un SLOT (Blender 5.x : animation_data.action_slot). Plage de la scène : 1–73 à 24 i/s dans la solution (1–25 dans le starter).
  STARTER_FILES/ch07_03_dopesheet_starter.blend (A animée aux images 1, 13, 25 ; B sans animation) ; COMPLETED_EXAMPLES/ch07_03_dopesheet_solution.blend (+ _reference.png : Dope Sheet en numpy)
  COUNTER_EXAMPLES/ : not_retimed, wrong_pivot, shared_action, late_not_shifted, no_range, wrong_values
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_03_files.py
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
VALUES = (0.0, 2.0, 4.0)
NOTE = """CH07.03 — DOPE SHEET ET ACTION (GEO_CrateA, GEO_CrateB)
1. RETIMER : l'action « Slide » de GEO_CrateA a ses clés aux images 1, 13 et 25. Doublez sa durée autour de l'image 1 (Dope Sheet : sélectionnez toutes les clés, curseur sur l'image 1, S pour mettre à l'échelle) :
   les clés doivent tomber aux images 1, 25 et 49. Valeurs inchangées (X = 0, 2, 4).
2. DÉCALER : GEO_CrateB doit faire la même animation 24 images plus tard, avec SA PROPRE action « Slide_Late » (duplication de l'action, puis G pour décaler de 24 images) : clés aux images 25, 49 et 73.
3. Plage de la scène : 1 à 73.
Une action est un bloc de données indépendant ; un slot relie une action à un objet. Deux objets qui partagent une action bougent identiquement.
Le correcteur lit les clés (images et valeurs), les noms des actions, l'indépendance des deux actions et l'animation évaluée.
Vérification : SCRIPTS/validate_ch07_03.py -- --exercise dopesheet
"""


def crate(name, y):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, y, 0)
    return ob


def animate(ob, action_name, frames, values):
    for f, x in zip(frames, values):
        ob.location = (x, ob.location.y, 0)
        ob.keyframe_insert("location", frame=f)
    ob.animation_data.action.name = action_name
    ob.location = (values[0], ob.location.y, 0)


def build(kind):
    L.reset("SC_DOPE")
    sc = bpy.context.scene
    sc.render.fps = 24
    a, b = crate("GEO_CrateA", 0.0), crate("GEO_CrateB", 2.0)
    if kind == "starter":
        animate(a, "Slide", (1, 13, 25), VALUES)
        sc.frame_start, sc.frame_end = 1, 25
        L.instructions(NOTE)
        return a, b
    fa = {"not_retimed": (1, 13, 25), "wrong_pivot": (2, 26, 50)}.get(kind, (1, 25, 49))
    va = tuple(reversed(VALUES)) if kind == "wrong_values" else VALUES
    animate(a, "Slide", fa, va)
    if kind == "shared_action":
        b.animation_data_create()
        b.animation_data.action = a.animation_data.action
        b.animation_data.action_slot = a.animation_data.action.slots[0]
    else:
        fb = (1, 25, 49) if kind == "late_not_shifted" else (25, 49, 73)
        animate(b, "Slide_Late", fb, VALUES)
    sc.frame_start, sc.frame_end = 1, (49 if kind == "no_range" else 73)
    sc.frame_set(1)
    L.instructions(NOTE)
    return a, b


def sketch(path):
    build("solution")
    W, H = 780, 240
    img = np.full((H, W, 3), 0.08, np.float32)

    def fx(f):
        return int(40 + (f - 1) / 72 * (W - 80))
    rows = (((1, 13, 25), 30, (0.5, 0.5, 0.5)), ((1, 25, 49), 100, (0.3, 0.8, 0.5)), ((25, 49, 73), 170, (0.9, 0.55, 0.2)))
    for f in (1, 25, 49, 73):
        img[10:H - 10, fx(f)] = (0.3, 0.3, 0.3)
    for frames, y, col in rows:
        img[y, 30:W - 30] = (0.2, 0.2, 0.2)
        for f in frames:
            x = fx(f)
            for d in range(-9, 10):
                half = 10 - abs(d)
                img[y + d, x - half:x + half + 1] = col
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_03_dopesheet_starter.blend"))
    for k in ("not_retimed", "wrong_pivot", "shared_action", "late_not_shifted", "no_range", "wrong_values"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_03_dopesheet_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_03_dopesheet_solution.blend"))
    sketch(os.path.join(out, "ch07_03_dopesheet_reference.png"))


if __name__ == "__main__":
    L.run(main)
