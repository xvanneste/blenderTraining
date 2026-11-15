"""
build_ch18_17_files.py — « Timing, exposition, cycle de marche 2D » (CH18.17, phase 18 module E).

  STARTER_FILES/ch18_17_xsheet_starter.blend
      Calque USER_Turn : 8 dessins A…H d'une tête qui tourne, tous « en un » (images 1 à 8) ;
      texte XSHEET : la feuille d'exposition à appliquer (image de début de chaque dessin, fin 18).
  COMPLETED_EXAMPLES/ch18_17_xsheet_solution.blend : les 8 dessins re-minutés selon la feuille.
  STARTER_FILES/ch18_17_walk_starter.blend
      Feuille 16:9, GUIDE (sol, axe vertical, repères de hauteur), calque USER_Walk vide,
      cycle de 24 images (24 i/s), onion skinning sans « Show Start Frame ».
  COMPLETED_EXAMPLES/ch18_17_walk_solution.blend (+ _reference.png : planche des 12 dessins)
      Marche sur place, de profil, en deux (12 dessins) : contacts 1 et 13, bas 3 et 15, passages
      7 et 19, hauts 9 et 21 ; pieds posés au sol et glissant vers l'arrière, jambe libre en arc,
      bras en opposition, rebond du bassin ; onion « Show Start Frame » activé.
Génération : trajectoires des pieds + rebond du bassin + cinématique inverse à 2 segments.
Usage : blender -b --factory-startup --python build_ch18_17_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
GROUND = -2.9
THIGH = SHIN = 0.8
TORSO, HEAD_R, FOOT = 1.0, 0.24, 0.28
UPPER, FORE = 0.55, 0.5
STRIDE, LIFT, HIP0, BOB = 1.0, 0.25, 1.58, 0.05
CYCLE = 24
XSHEET = [("A", 1), ("B", 4), ("C", 6), ("D", 7), ("E", 8), ("F", 9), ("G", 10), ("H", 12)]
XS_END = 18

NOTE_X = """CH18.17 — LA FEUILLE D'EXPOSITION (GP_Practice, calque USER_Turn)
Les 8 dessins A…H d'une tête qui tourne sont posés « en un » (images 1 à 8) : trop rapide, mécanique.
Appliquez la feuille d'exposition du texte XSHEET : chaque dessin commence à l'image indiquée et dure
jusqu'au suivant (ex. A en trois : 1–3 ; B en deux : 4–5 ; C, D, E, F en un ; G en deux ; H tenu).
Dope Sheet (mode Grease Pencil) : sélectionnez une clé (ou plusieurs), G pour déplacer, saisissez le
décalage. Travaillez de la DERNIÈRE clé vers la première pour ne pas les superposer.
Output Properties > Frame Range : End = 18.
Vérification : SCRIPTS/validate_ch18_17.py -- --exercise xsheet
"""
NOTE_W = """CH18.17 — LE CYCLE DE MARCHE 2D (GP_Practice, calque USER_Walk, images 1–24)
Marche SUR PLACE, de profil, vers la droite, « en deux » (un dessin aux images 1, 3, 5 … 23).
Poses : CONTACT (1 et 13 : jambes écartées, talon avant au sol), BAS (3 et 15 : genou d'appui fléchi,
corps au plus bas), PASSAGE (7 et 19 : jambes croisées, pied libre levé), HAUT (9 et 21 : corps au
plus haut, poussée sur l'orteil arrière). Le pied d'appui GLISSE vers l'arrière au sol (marche sur
place) ; bras en opposition aux jambes. Le dessin 13 = le 1 avec les jambes inversées.
Onion skinning : Object Data > Onion Skinning > Display > Show Start Frame (voir l'image 1 après la 23).
Vérification : SCRIPTS/validate_ch18_17.py -- --exercise walk
"""


# --- cycle de marche ------------------------------------------------------------------------

def ik(hip, foot, l1=THIGH, l2=SHIN):
    """Genou d'une jambe à 2 segments (genou vers l'avant, +x)."""
    dx, dz = foot[0] - hip[0], foot[1] - hip[1]
    d = min(math.hypot(dx, dz), l1 + l2 - 1e-4)
    a = math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))
    base = math.atan2(dz, dx)
    ang = base + a                                   # coude du genou orienté vers l'avant
    return (hip[0] + l1 * math.cos(ang), hip[1] + l1 * math.sin(ang))


def foot_at(psi):
    """Position du pied (x relatif au bassin, hauteur) et soulèvement du talon pour la phase psi."""
    psi %= 1.0
    if psi < 0.5:                                    # appui : glisse de l'avant vers l'arrière
        u = psi / 0.5
        heel = max(0.0, (u - 0.55) / 0.45) * 0.18      # le talon décolle en fin d'appui (poussée)
        return STRIDE / 2 - STRIDE * u, 0.0, heel
    u = (psi - 0.5) / 0.5                            # vol : revient vers l'avant en arc
    x = -STRIDE / 2 + STRIDE * (1 - math.cos(math.pi * u)) / 2
    return x, LIFT * math.sin(math.pi * u), 0.0


def pose(f):
    phi = (f - 1) / CYCLE
    hip = (0.0, GROUND + HIP0 + BOB * math.cos(4 * math.pi * (phi - 0.375)))
    parts = {}
    for side, off in (("R", 0.0), ("L", 0.5)):
        fx, fz, heel = foot_at(phi + off)
        ankle = (hip[0] + fx, GROUND + 0.08 + fz + heel)
        knee = ik(hip, ankle)
        toe = (ankle[0] + FOOT * math.cos(-0.15 - heel * 2.5), ankle[1] + FOOT * math.sin(-0.15 - heel * 2.5) - 0.02)
        toe = (toe[0], max(toe[1], GROUND + 0.0))
        parts["leg" + side] = [hip, knee, ankle, toe]
    neck = (hip[0] + 0.06, hip[1] + TORSO)
    parts["torso"] = [hip, neck]
    parts["head"] = (neck[0] + 0.04, neck[1] + 0.06 + HEAD_R)
    for side, off in (("R", 0.5), ("L", 0.0)):     # bras opposé à la jambe
        sw = math.radians(28) * math.cos(2 * math.pi * (phi + off))
        sh = (neck[0], neck[1] - 0.12)
        el = (sh[0] + UPPER * math.sin(sw), sh[1] - UPPER * math.cos(sw))
        hand = (el[0] + FORE * math.sin(sw + 0.35), el[1] - FORE * math.cos(sw + 0.35))
        parts["arm" + side] = [sh, el, hand]
    return parts


def draw_pose(d, parts, near, far):
    G.polyline(d, parts["legL"], 0.03, far)
    G.polyline(d, parts["armL"], 0.025, far)
    G.polyline(d, parts["torso"], 0.035, near)
    G.circle(d, parts["head"], HEAD_R, 0.025, near, n=32)
    hx, hz = parts["head"]
    G.line(d, (hx + 0.1, hz + 0.04), (hx + 0.14, hz + 0.04), 0.02, near)   # œil : direction du regard
    G.polyline(d, parts["legR"], 0.03, near)
    G.polyline(d, parts["armR"], 0.025, near)


def walk(sol):
    L.reset("SC_Walk")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Walk",))
    guide = G.material(ob, "MAT_GP_Guide", (0.35, 0.45, 0.7))
    gl = ob.data.layers["GUIDE"]
    gl.lock = False
    g = drw["GUIDE"]
    G.line(g, (-5.9, GROUND), (5.9, GROUND), 0.012, guide)
    G.line(g, (0, GROUND - 0.2), (0, GROUND + 3.6), 0.004, guide)
    for z in (HIP0, HIP0 + TORSO + 0.06 + 2 * HEAD_R):
        G.line(g, (-0.4, GROUND + z), (0.4, GROUND + z), 0.004, guide)
    gl.lock = True
    sc = bpy.context.scene
    sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, CYCLE
    gp = ob.data
    gp.onion_mode = "RELATIVE"
    gp.ghost_before_range = gp.ghost_after_range = 2
    gp.use_onion_loop = False
    near = G.material(ob, "MAT_GP_Near", (0.05, 0.05, 0.08))
    far = G.material(ob, "MAT_GP_Far", (0.55, 0.55, 0.62))
    if sol:
        for f in range(1, CYCLE + 1, 2):
            d = G.layer(ob, "USER_Walk", frame=f)
            draw_pose(d, pose(f), near, far)
        gp.use_onion_loop = True
        lay = ob.data.layers["USER_Walk"]
        for fr in lay.frames:
            fr.keyframe_type = "KEYFRAME" if fr.frame_number in (1, 13) else (
                "EXTREME" if fr.frame_number in (3, 7, 9, 15, 19, 21) else "BREAKDOWN")
    L.instructions(NOTE_W)
    return sc, ob


def walk_sheet(out):
    """Planche de contrôle : les 12 dessins côte à côte (rendus un par un, 6 × 2)."""
    sc = bpy.context.scene
    cam = sc.camera
    cam.data.ortho_scale, cam.location.z = 6.6, GROUND + 1.65    # recadré sur le personnage
    sc.render.resolution_percentage = 25
    W, H = sc.render.resolution_x // 4, sc.render.resolution_y // 4
    frames = list(range(1, CYCLE + 1, 2))
    sheet = np.zeros((2 * H, 6 * W, 4), dtype=np.float32)
    for i, f in enumerate(frames):
        sc.frame_set(f)
        p = os.path.join(bpy.app.tempdir, f"walk_{f}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
        r, c = i // 6, i % 6
        sheet[(1 - r) * H:(2 - r) * H, c * W:(c + 1) * W] = px
    img = bpy.data.images.new("walk_sheet", 6 * W, 2 * H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


# --- feuille d'exposition --------------------------------------------------------------------

def head_turn(d, k, ink):
    """Dessin k (0…7) d'une tête qui tourne de profil gauche vers profil droit."""
    t = k / 7
    cx, cz = 0.0, 0.0
    G.circle(d, (cx, cz), 1.3, 0.025, ink, n=48)
    nx = -1.25 + 2.5 * t                              # axe du visage qui glisse
    G.line(d, (nx, 0.25), (nx + (0.25 if t > 0.5 else -0.25), -0.2), 0.03, ink)       # nez
    for e in (-0.35, 0.35):
        ex = nx + e * math.sin(math.pi * max(0.15, min(0.85, t)))
        if abs(ex) < 1.15:
            G.circle(d, (ex, 0.45), 0.09 + 0.01 * k, 0.02, ink, n=16)                # yeux (taille = signature)
    G.line(d, (nx - 0.3, -0.7), (nx + 0.3, -0.7), 0.025, ink)                        # bouche


def signature(drawing):
    return [len(drawing.strokes), round(sum(p.position.x for s in drawing.strokes for p in s.points), 2)]


def xsheet(sol):
    L.reset("SC_XSheet")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Turn",))
    sc = bpy.context.scene
    sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, 8
    lay = ob.data.layers["USER_Turn"]
    sigs = {}
    for k, (name, target) in enumerate(XSHEET):
        f = target if sol else k + 1
        d = G.layer(ob, "USER_Turn", frame=f)
        head_turn(d, k, 0)
        sigs[name] = signature(d)
    sc["bcma_xsheet_sigs"] = json.dumps(sigs)
    if sol:
        sc.frame_end = XS_END
    rows = ["# dessin;image de début;exposition"]
    for i, (name, f) in enumerate(XSHEET):
        nxt = XSHEET[i + 1][1] if i + 1 < len(XSHEET) else XS_END + 1
        rows.append(f"{name};{f};{nxt - f} image(s)")
    rows.append(f"FIN;{XS_END};")
    L.instructions("\n".join(rows) + "\n", "XSHEET")
    L.instructions(NOTE_X)
    return sc


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    xsheet(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_17_xsheet_starter.blend"))
    xsheet(True)
    L.save(os.path.join(out, "ch18_17_xsheet_solution.blend"))
    walk(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_17_walk_starter.blend"))
    walk(True)
    L.save(os.path.join(out, "ch18_17_walk_solution.blend"))
    walk_sheet(os.path.join(out, "ch18_17_walk_reference.png"))


if __name__ == "__main__":
    L.run(main)
