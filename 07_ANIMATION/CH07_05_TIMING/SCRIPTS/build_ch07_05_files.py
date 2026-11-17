"""
build_ch07_05_files.py — « Timing et spacing » (CH07.05 : la balle rebondissante crédible).

Une balle GEO_Ball (rayon 0,25 m, origine à sa base) qui tombe et rebondit, 72 images à 24 i/s ; gravité g = 9,81 m/s² = 0,01703 m/image².
  Solution (images clés de position Z, 7 clés, poignées exactes) : 1 : 2,759 m (lâcher) ; 19 : 0 (contact 1) ; 31,5 : 1,3305 m (sommet 1) ; 44 : 0 (contact 2) ; 53 : 0,6897 m (sommet 2) ; 62 : 0 (contact 3, la balle s'arrête) ; 72 : 0.
  Les durées et les hauteurs obéissent à la gravité : h = g·T²/8 pour un vol de T images (T en secondes), chute depuis le repos : h = g·t²/2 ; restitution : hauteur ×0,48 puis ×0,52 ; durée de vol 25 puis 18 images (×0,72).
  Courbe : sommets aux poignées horizontales, contacts aux poignées raides (pente de la parabole) : l'ESPACEMENT (distance parcourue par image) reproduit la gravité.
  STARTER_FILES/ch07_05_bounce_starter.blend : la balle avec deux clés (image 1 : 2,759 m ; image 72 : 0), interpolation Bezier par défaut (elle flotte jusqu'au sol, sans rebond).
  COMPLETED_EXAMPLES/ch07_05_bounce_solution.blend (+ _reference.png : courbe de hauteur et chronophotographie, un point par image)
  COUNTER_EXAMPLES/ : linear, floaty, no_decay, same_time, no_rest, below_floor
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_05_files.py
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
G_FRAME = 9.81 / 576.0
IDEAL = [(1, 2.759), (19, 0.0), (31.5, 1.3305), (44, 0.0), (53, 0.6897), (62, 0.0), (72, 0.0)]
NOTE = """CH07.05 — TIMING ET SPACING (GEO_Ball)
Une balle lâchée de 2,76 m doit rebondir trois fois puis s'arrêter, avec la gravité de la Terre (24 images par seconde).
Le TIMING, ce sont les images des contacts ; le SPACING, la distance parcourue entre deux images : la balle accélère en tombant (écarts de plus en plus grands vers le sol) et ralentit en montant.
Repères : contacts aux images 19, 44, 62 ; sommets aux images 31,5 (1,33 m) et 53 (0,69 m) ; la balle est au repos à partir de l'image 62.
Dans le Graph Editor : sommets en poignées horizontales (Auto Clamped), contacts en poignées « Vector » ou raides : une parabole, pas une sinusoïde.
Le correcteur mesure : 3 contacts, décroissance des hauteurs (×0,35 à ×0,65) et des durées de vol (×0,55 à ×0,85), cohérence avec la gravité (accélération 0,0128 à 0,0213 m/image²),
espacement parabolique (accélération médiane de chaque segment), balle au repos à la fin, jamais sous le sol, au plus 12 clés.
Vérification : SCRIPTS/validate_ch07_05.py -- --exercise bounce
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def make_ball():
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.25)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.25))
    me = bpy.data.meshes.new("ME_Ball")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("GEO_Ball", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def exact_handles(kp_list):
    """Poignées exactes d'une parabole par morceaux (sommets : horizontales ; contacts : pente 2h/τ)."""
    pts = [(k.co[0], k.co[1]) for k in kp_list]
    hl, hr = {}, {}
    for i, (t, z) in enumerate(pts):
        hl[i] = (t - 1.0, z)
        hr[i] = (t + 1.0, z)
    # (indice, côté) : (écart en images, valeur)
    spec = {(0, "r"): (6.0, 2.759), (1, "l"): (13.0, 2 * 2.759 / 3), (1, "r"): (19 + 12.5 / 3, 2 * 1.3305 / 3), (2, "l"): (31.5 - 12.5 / 3, 1.3305), (2, "r"): (31.5 + 12.5 / 3, 1.3305),
            (3, "l"): (44 - 12.5 / 3, 2 * 1.3305 / 3), (3, "r"): (47.0, 2 * 0.6897 / 3), (4, "l"): (50.0, 0.6897), (4, "r"): (56.0, 0.6897), (5, "l"): (59.0, 2 * 0.6897 / 3), (5, "r"): (62 + 10 / 3, 0.0),
            (6, "l"): (72 - 10 / 3, 0.0), (6, "r"): (72 + 10 / 3, 0.0)}
    for (i, side), (t, z) in spec.items():
        if side == "l":
            hl[i] = (t, z) if i != 0 else hl[i]
        else:
            hr[i] = (t if i != 0 else 1 + 6.0, z)
    hl[0] = (1 - 6.0, 2.759)
    for i, k in enumerate(kp_list):
        k.handle_left_type = k.handle_right_type = "FREE"
        k.handle_left = hl[i]
        k.handle_right = hr[i]


def build(kind):
    L.reset("SC_BOUNCE")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 72
    ob = make_ball()
    if kind == "starter":
        keys = [(1, 2.759), (72, 0.0)]
    elif kind == "no_decay":
        keys = [(1, 2.759), (19, 0.0), (31.5, 2.759), (44, 0.0), (56.5, 2.759), (69, 0.0), (72, 0.0)]
    elif kind == "same_time":
        keys = [(1, 2.759), (19, 0.0), (31.5, 1.3305), (44, 0.0), (56.5, 0.6897), (69, 0.0), (72, 0.0)]
    elif kind == "no_rest":
        keys = [(1, 2.759), (19, 0.0), (31.5, 1.3305), (44, 0.0), (53, 0.6897), (62, 0.0), (72, 0.5)]
    elif kind == "below_floor":
        keys = [(1, 2.759), (19, -0.12), (31.5, 1.3305), (44, -0.12), (53, 0.6897), (62, -0.12), (72, 0.0)]
    else:
        keys = IDEAL
    for f, z in keys:
        ob.location = (0, 0, z)
        ob.keyframe_insert("location", index=2, frame=f)
    ob.location = (0, 0, keys[0][1])
    fc = next(f for f in fcurves(ob.animation_data.action) if f.array_index == 2)
    kps = list(fc.keyframe_points)
    if kind == "linear":
        for k in kps:
            k.interpolation = "LINEAR"
    elif kind == "floaty" or kind == "starter":
        for k in kps:
            k.interpolation = "BEZIER"
            k.handle_left_type = k.handle_right_type = "AUTO_CLAMPED"
    elif kind == "solution":
        for k in kps:
            k.interpolation = "BEZIER"
        exact_handles(kps)
    else:                                                  # no_decay, same_time, no_rest, below_floor : contacts en poignées Vector, sommets Auto Clamped
        for k in kps:
            k.interpolation = "BEZIER"
            contact = k.co[1] <= 0.01 and 1 < k.co[0] < 72
            k.handle_left_type = k.handle_right_type = "VECTOR" if contact else "AUTO_CLAMPED"
    fc.update()
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    W, H = 780, 340
    img = np.full((H, W, 3), 0.08, np.float32)

    def px(f, z):
        return int(20 + (f - 1) / 71 * (W - 40)), int(H - 20 - z / 2.9 * (H - 40))
    img[H - 20, 20:W - 20] = (0.3, 0.3, 0.3)
    pts = []
    for f10 in range(10, 721):
        f = f10 / 10
        sc.frame_set(int(f), subframe=f - int(f))
        bpy.context.view_layer.update()
        pts.append(px(f, ob.location.z))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0)) + 1
        for k in range(n + 1):
            x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
            img[y, x] = (0.9, 0.55, 0.2)
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        x, y = px(f, ob.location.z)
        img[y - 3:y + 4, x - 3:x + 4] = (0.3, 0.8, 0.5)
    for f, z in IDEAL:
        x, y = px(f, z)
        img[y - 5:y + 6, x - 1:x + 2] = (1, 1, 1)
        img[y - 1:y + 2, x - 5:x + 6] = (1, 1, 1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_05_bounce_starter.blend"))
    for k in ("linear", "floaty", "no_decay", "same_time", "no_rest", "below_floor"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_05_bounce_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_05_bounce_solution.blend"))
    sketch(os.path.join(out, "ch07_05_bounce_reference.png"))


if __name__ == "__main__":
    L.run(main)
