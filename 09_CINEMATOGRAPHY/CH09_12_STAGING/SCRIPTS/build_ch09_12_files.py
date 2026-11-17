"""
build_ch09_12_files.py — « Mise en scène » (CH09.12 : blocking des acteurs, triangle, étagement des plans, continuité de raccord).

Scène (Workbench plat, couleurs d'objet) : sol gris, table brune (Table) en (0, 0, 0,375), tasse jaune (Cup) en (0,3, 0, 0,8), trois personnages-cylindres de 1,7 m : A rouge, B bleu, C vert ;
  CAM en (0, −9, 1,6) regardant vers +Y, focale 35 mm, rendu 320 × 180. Animation de 72 images (24 i/s) : le MOMENT CLÉ est l'image 36 (fin du plan 1) ; le plan 2 commence à l'image 37 (raccord).
  Départ (à corriger) : A clés 1 (−4, −1,5), 36 (−1,5, 1,0), 37 (−2, −1,5), 72 (−2, −1,5) ; B clés 1 (4, 3), 36 (1,5, 1,0), 72 (1,5, 1,0) ; C clés 1 (0, 5), 36 (0, 1,2), 72 (0, 1,2) ;
  Cup : clés 1 et 36 en (0,3, 0, 0,8), 37 et 72 en (−0,3, 0, 0,8). À l'image 36 les trois personnages sont presque alignés au même niveau (pas de triangle, pas de profondeur) ; A saute de 2,5 m au raccord (37) ; la tasse change de place au raccord.
  Consigne : (1) triangle de blocking à l'image 36 : aire ≥ 2 m² et angle minimal ≥ 30° ; (2) étagement en profondeur : distances à la caméra (selon y) étalées sur ≥ 3 m et d'au moins 1 m entre deux personnages ;
  (3) chacun visible dans le rendu de l'image 36 (≥ 30 pixels) et les centres de A, B, C séparés d'au moins 8 % de la largeur ; (4) continuité : au raccord 36 → 37 chaque personnage bouge de ≤ 0,12 m et la tasse de ≤ 1 cm ;
  (5) aucun personnage ne se déplace de plus de 0,15 m d'une image à l'autre (≈ 3,6 m/s) ; (6) jamais deux personnages à moins de 0,6 m l'un de l'autre.
  Solution : à l'image 36 : A (−2, −1,5), B (2, 0,5), C (0, 3) (aire 7 m², angle min 39°, distances 7,5 / 9,5 / 12 m) ; A clés 1 (−4, −1,5), 36 (−2, −1,5), 72 (−2, −1,5) ; B : 1 (4, 3), 36 (2, 0,5), 72 (2, 0,5) ; C : 1 (0, 5), 36 (0, 3), 72 (0, 3) ; tasse sans mouvement.
  STARTER_FILES/ch09_12_staging_starter.blend ; COMPLETED_EXAMPLES/ch09_12_staging_solution.blend (+ _reference.png : vue de dessus du départ et de la solution)
  COUNTER_EXAMPLES/ : line_up (alignés), flat_depth (triangle mais même profondeur), teleport (A saute au raccord), cup_moved (tasse déplacée au raccord), too_fast (A traverse 2 m en 4 images), occluded (C caché derrière A), collision (B finit à 0,3 m de A)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_12_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH09.12 — MISE EN SCÈNE (A rouge, B bleu, C vert, Table, Cup, CAM)
Une scène de 72 images ; le plan 1 finit à l'image 36 (moment clé), le plan 2 commence à l'image 37. Corrigez le BLOCKING en éditant les clés de position (Location) des personnages et de la tasse.
1. À l'image 36 : A, B, C forment un TRIANGLE (aire ≥ 2 m², angle minimal ≥ 30°) et sont ÉTAGÉS en profondeur (distances à la caméra selon y étalées sur ≥ 3 m, au moins 1 m entre deux personnages).
2. Les trois sont visibles dans le rendu de l'image 36 (≥ 30 pixels chacun, centres séparés d'au moins 8 % de la largeur).
3. Continuité au raccord 36 → 37 : un personnage bouge de ≤ 0,12 m, la tasse de ≤ 1 cm.
4. Pas de téléportation : ≤ 0,15 m par image ; jamais deux personnages à moins de 0,6 m.
Vérification : SCRIPTS/validate_ch09_12.py -- --exercise staging
"""

COLORS = {"A": (1, 0, 0, 1), "B": (0, 0, 1, 1), "C": (0, 1, 0, 1)}
FRAMES = {"starter": None}


def prism(sc, name, size, loc, col, cyl=False):
    bm = bmesh.new()
    if cyl:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=size[0], radius2=size[0], depth=size[2])
    else:
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.location = loc
    o.color = col
    return o


def keys(ob, table):
    """table : {image: (x, y)} ; z reste fixe."""
    z = ob.location.z
    for f, (x, y) in table.items():
        ob.location = (x, y, z)
        ob.keyframe_insert("location", frame=f)
    act = ob.animation_data.action
    for fc in [fc for la in act.layers for st in la.strips for cb in st.channelbags for fc in cb.fcurves]:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def build(kind):
    L.reset("SC_STAGING")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    wo = bpy.data.worlds.new("WO_Dark")
    wo.color = (0.1, 0.1, 0.1)
    sc.world = wo
    g = prism(sc, "Floor", (10, 10, 1), (0, 0, 0), (0.35, 0.35, 0.35, 1))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=30)
    bm.to_mesh(g.data)
    bm.free()
    prism(sc, "Table", (1.2, 0.8, 0.75), (0, 0, 0.375), (0.4, 0.25, 0.1, 1))
    cup = prism(sc, "Cup", (0.06, 0.06, 0.1), (0.3, 0, 0.8), (1, 1, 0, 1), cyl=True)
    act = {n: prism(sc, n, (0.25, 0.25, 1.7), (0, 0, 0.85), COLORS[n], cyl=True) for n in "ABC"}
    # positions clés
    A = {1: (-4, -1.5), 36: (-1.5, 1.0), 37: (-2, -1.5), 72: (-2, -1.5)}
    B = {1: (4, 3), 36: (1.5, 1.0), 72: (1.5, 1.0)}
    C = {1: (0, 5), 36: (0, 1.2), 72: (0, 1.2)}
    cupk = {1: (0.3, 0), 36: (0.3, 0), 37: (-0.3, 0), 72: (-0.3, 0)}
    if kind != "starter":
        A = {1: (-4, -1.5), 36: (-2, -1.5), 72: (-2, -1.5)}
        B = {1: (4, 3), 36: (2, 0.5), 72: (2, 0.5)}
        C = {1: (0, 5), 36: (0, 3), 72: (0, 3)}
        cupk = None
    if kind == "line_up":
        A, B, C = {1: (-4, -1.5), 36: (-2, 1.0), 72: (-2, 1.0)}, {1: (4, 3), 36: (2, 1.0), 72: (2, 1.0)}, {1: (0, 5), 36: (0, 1.0), 72: (0, 1.0)}
    elif kind == "flat_depth":
        A, B, C = {1: (-4, -1.5), 36: (-2, 1.0), 72: (-2, 1.0)}, {1: (4, 3), 36: (2, 0.0), 72: (2, 0.0)}, {1: (0, 5), 36: (0, 2.0), 72: (0, 2.0)}
    elif kind == "teleport":
        A = {1: (-4, -1.5), 36: (-2, -1.5), 37: (-4, -1.5), 72: (-4, -1.5)}
    elif kind == "cup_moved":
        cupk = {1: (0.3, 0), 36: (0.3, 0), 37: (-0.3, 0), 72: (-0.3, 0)}
    elif kind == "too_fast":
        A = {1: (-4, -1.5), 5: (-2, -1.5), 36: (-2, -1.5), 72: (-2, -1.5)}
    elif kind == "collision":
        B = {1: (4, 3), 36: (2, 0.5), 72: (-1.8, -1.2)}
    elif kind == "occluded":
        A = {1: (-4, -1.5), 36: (0, -1.5), 72: (0, -1.5)}
    for n, t in (("A", A), ("B", B), ("C", C)):
        keys(act[n], t)
    if cupk:
        keys(cup, cupk)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -9, 1.6)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    sc.frame_start, sc.frame_end = 1, 72
    sc.render.fps = 24
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.frame_set(36)
    L.instructions(NOTE)


def render_px():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0912.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure():
    sc = bpy.context.scene
    obs = {n: bpy.data.objects[n] for n in "ABC"}
    cup = bpy.data.objects["Cup"]
    pos = {}
    for f in range(1, 73):
        sc.frame_set(f)
        pos[f] = ({n: obs[n].matrix_world.translation.copy() for n in "ABC"}, cup.matrix_world.translation.copy())
    sc.frame_set(36)
    P = [obs[n].matrix_world.translation for n in "ABC"]
    ax, bx, cx = [(p.x, p.y) for p in P]
    area = 0.5 * abs((bx[0] - ax[0]) * (cx[1] - ax[1]) - (cx[0] - ax[0]) * (bx[1] - ax[1]))
    def ang(p, q, r):
        v1, v2 = (q[0] - p[0], q[1] - p[1]), (r[0] - p[0], r[1] - p[1])
        d = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2) + 1e-12)
        return math.degrees(math.acos(max(-1, min(1, d))))
    amin = min(ang(ax, bx, cx), ang(bx, ax, cx), ang(cx, ax, bx))
    depth = sorted(p.y + 9 for p in P)
    spread, gap = depth[-1] - depth[0], min(depth[1] - depth[0], depth[2] - depth[1])
    jump = max((pos[37][0][n] - pos[36][0][n]).length for n in "ABC")
    cupj = (pos[37][1] - pos[36][1]).length
    step = max((pos[f + 1][0][n] - pos[f][0][n]).length for f in range(1, 72) for n in "ABC")
    px = render_px()
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    masks = {"A": (R > 0.7) & (G < 0.3) & (B < 0.3), "B": (B > 0.7) & (R < 0.3) & (G < 0.3), "C": (G > 0.7) & (R < 0.3) & (B < 0.3)}
    cnt = {n: int(m.sum()) for n, m in masks.items()}
    cxs = {n: (np.nonzero(m)[1].mean() / 320.0 if m.sum() else -9) for n, m in masks.items()}
    sep = min(abs(cxs["A"] - cxs["B"]), abs(cxs["A"] - cxs["C"]), abs(cxs["B"] - cxs["C"]))
    return {"area": area, "amin": amin, "spread": spread, "gap": gap, "jump": jump, "cup": cupj, "step": step, "px": cnt, "sep": sep}


def calibrate():
    for kind in ("starter", "solution", "line_up", "flat_depth", "teleport", "cup_moved", "too_fast", "occluded", "collision"):
        build(kind)
        m = measure()
        print("[stage]", kind, {k: (round(v, 3) if not isinstance(v, dict) else v) for k, v in m.items()})


def sketch(path):
    W, H = 760, 330
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution")):
        build(kind)
        sc = bpy.context.scene
        sc.frame_set(36)
        x0, y0 = 20 + i * 370, 15
        img[y0:y0 + 300, x0:x0 + 330, :] = 0.15
        # vue de dessus : x ∈ [−5, 5] -> 330 px ; y ∈ [−4, 6] -> 300 px (haut = +y)
        def to(p):
            return int(x0 + (p[0] + 5) * 33), int(y0 + 300 - (p[1] + 4) * 30)
        for n in "ABC":
            c = to(bpy.data.objects[n].matrix_world.translation)
            col = np.array(COLORS[n][:3], np.float32)
            for dy in range(-8, 9):
                for dx in range(-8, 9):
                    if dx * dx + dy * dy <= 64 and 0 <= c[1] + dy < H and 0 <= c[0] + dx < W:
                        img[c[1] + dy, c[0] + dx, :] = col
        t = to((0, 0))
        img[t[1] - 5:t[1] + 6, t[0] - 8:t[0] + 9, :] = (0.5, 0.3, 0.1)
        cam = to((0, -9)) if False else (x0 + 165, y0 + 300 - 2)
        img[cam[1] - 4:cam[1] + 1, cam[0] - 10:cam[0] + 11, :] = (1, 1, 1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_12_staging_starter.blend"))
    for k in ("line_up", "flat_depth", "teleport", "cup_moved", "too_fast", "occluded", "collision"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_12_staging_{k}.blend"))
    sketch(os.path.join(out, "ch09_12_staging_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_12_staging_solution.blend"))


if __name__ == "__main__":
    L.run(main)
