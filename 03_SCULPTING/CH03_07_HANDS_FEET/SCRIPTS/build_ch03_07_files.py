"""
build_ch03_07_files.py — « Mains et pieds » (CH03.07 : structure, articulations).

  STARTER_FILES/ch03_07_hand_starter.blend  et  ch03_07_foot_starter.blend
      Studio, 3 caméras, guide de proportions (Grease Pencil) ; aucun membre.
  COMPLETED_EXAMPLES/ch03_07_hand_solution.blend / ch03_07_foot_solution.blend (+ _reference.png)
      Main (SCULPT_Hand) : paume, poignet, quatre doigts de trois phalanges, pouce, articulations, doigts écartés.
      Pied (SCULPT_Foot) : talon, cheville, voûte plantaire, avant-pied, cinq orteils, semelle plane.
      Orientation : bout des doigts / orteils vers +Y ; main à plat (paume vers −Z) ; pied posé sur z = 0.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : fused_fingers, four_fingers, equal_fingers, no_thumb, tiny (main)
                                         fused_toes, four_toes, flat_foot, short_big_toe, tiny (pied)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_07_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH03_05_REALISTIC", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import build_ch03_05_files as B5  # noqa: E402  (taubin)
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE_HAND = """CH03.07 — LA MAIN (vues : Num 7 dessus, Num 1 face)
Main à plat, doigts vers +Y, pouce vers +X. 20 cm du poignet au bout du majeur.
1. Paume (≈ 9 × 10 cm, épaisseur 3 cm) et poignet (≈ 6 cm de large) ; 2. quatre doigts de TROIS phalanges
(proportions ≈ 45 / 30 / 25 %), le majeur le plus long, l'auriculaire le plus court ; 3. pouce : deux phalanges + un
métacarpien épais qui part du poignet, à ≈ 50° ; 4. articulations marquées, doigts légèrement écartés (pas de moufle).
Vérification : SCRIPTS/validate_ch03_07.py -- --exercise hand
"""
NOTE_FOOT = """CH03.07 — LE PIED (vues : Num 3 profil, Num 7 dessus)
Pied posé sur z = 0, orteils vers +Y, gros orteil vers +X. ≈ 27 cm du talon au gros orteil.
1. Talon, cheville ; 2. VOÛTE plantaire (le milieu du pied ne touche pas le sol) ; 3. avant-pied (« balle ») ;
4. cinq orteils : le gros orteil est le plus long et le plus épais, puis ils décroissent ; 5. semelle plane sous le
talon et la balle.
Vérification : SCRIPTS/validate_ch03_07.py -- --exercise foot
"""

# --- main --------------------------------------------------------------------------------------------------------
PALM_TOP = 0.10
FINGERS = [  # nom, x de la base, longueur totale, angle (°, + vers +X), rayon de base
    ("Index", 0.037, 0.070, 8, 0.0095),
    ("Middle", 0.0125, 0.080, 1, 0.0100),
    ("Ring", -0.0125, 0.073, -6, 0.0092),
    ("Pinky", -0.0375, 0.057, -14, 0.0080),
]
PHALANX = (0.45, 0.30, 0.25)


def seg(name, col, mat, base, ang_deg, start, length, radius, flat=1.0):
    """Un ellipsoïde allongé le long de la direction (sin a, cos a) à partir de `base`."""
    a = math.radians(ang_deg)
    d = Vector((math.sin(a), math.cos(a), 0))
    c = Vector((base[0], base[1], base[2])) + d * (start + length / 2)
    return L.sphere(name, col, mat, radius=1, location=tuple(c), scale=(radius, length / 2 * 1.40, radius * flat), rotation=(0, 0, -a))


def finger_parts(name, col, mat, base, ang, length, r0, joints=True):
    out, off = [], 0.0
    for i, f in enumerate(PHALANX):
        ln = length * f
        r = r0 * (1 - 0.07 * i)
        out.append(seg(f"{name}_P{i}", col, mat, base, ang, off, ln, r))
        off += ln
        if joints and i < 2:           # articulation : léger renflement
            out.append(seg(f"{name}_J{i}", col, mat, base, ang, off - 0.003, 0.006, r * 1.05))
    return out


def hand_parts(col, mat, variant):
    parts = [L.sphere("Palm", col, mat, radius=1, location=(0, 0.045, 0), scale=(0.052, 0.056, 0.015)),
             L.sphere("Wrist", col, mat, radius=1, location=(0, -0.01, 0), scale=(0.031, 0.045, 0.02))]
    for name, bx, ln, ang, r0 in FINGERS:
        if variant == "four_fingers" and name == "Pinky":
            continue
        if variant == "equal_fingers":
            ln = 0.075
        parts += finger_parts(name, col, mat, (bx, PALM_TOP - 0.005, 0), ang, ln, r0, joints=False)
    if variant != "no_thumb":
        base = (0.046, 0.025, 0)
        parts.append(seg("Thumb_M", col, mat, base, 50, 0.0, 0.042, 0.0145, 0.85))
        parts.append(seg("Thumb_P0", col, mat, base, 50, 0.040, 0.032, 0.0125))
        parts.append(seg("Thumb_J", col, mat, base, 50, 0.069, 0.006, 0.0130))
        parts.append(seg("Thumb_P1", col, mat, base, 50, 0.071, 0.026, 0.0108))
    if variant == "fused_fingers":     # moufle : un bloc entre les doigts
        parts.append(L.sphere("Mitten", col, mat, radius=1, location=(0, 0.14, 0), scale=(0.052, 0.045, 0.0085)))
    return parts


def build_hand(variant="solution"):
    col = L.collection("SCULPT")
    skin = L.material("MAT_Skin", (0.72, 0.58, 0.5), 0.6)
    parts = hand_parts(col, skin, variant)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_Hand", "ME_SCULPT_Hand"
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = type(ob.matrix_world)()
    ob.data.remesh_voxel_size = 0.0025
    bpy.ops.object.voxel_remesh()
    B5.taubin(ob, 14)
    # poignet : coupe plane en y = −0,04 (Bisect + Fill)
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, -0.04, 0), plane_no=(0, 1, 0), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    ob.location.z = 0.02
    for p in ob.data.polygons:
        p.use_smooth = True
    if variant == "tiny":
        ob.data.transform(__import__("mathutils").Matrix.Scale(0.5, 4))
    print(f"[BCMA] SCULPT_Hand ({variant}) : {len(ob.data.vertices)} sommets")
    return ob


# --- pied --------------------------------------------------------------------------------------------------------
TOE_SPECS = [  # nom, longueur, rayon (le gros orteil est le plus long et le plus épais)
    ("Toe1", 0.052, 0.0120), ("Toe2", 0.044, 0.0090), ("Toe3", 0.039, 0.0083), ("Toe4", 0.033, 0.0077), ("Toe5", 0.027, 0.0070)]
TOE_GAP = 0.005


def toe_layout():
    """Positions x calculées à partir des rayons, avec un écart fixe : des orteils séparés, pas une masse."""
    out, x_edge = [], 0.054
    for name, ln, r in TOE_SPECS:
        c = x_edge - r
        out.append((name, c, ln, r))
        x_edge = c - r - TOE_GAP
    return out


TOES = toe_layout()


def foot_parts(col, mat, variant):
    arch_z = 0.050 if variant != "flat_foot" else 0.027
    arch_rz = 0.027
    parts = [L.sphere("Heel", col, mat, radius=1, location=(0, 0.035, 0.030), scale=(0.033, 0.043, 0.034)),
             L.sphere("HeelPad", col, mat, radius=1, location=(0, 0.035, 0.0), scale=(0.032, 0.042, 0.016)),
             L.sphere("Ankle", col, mat, radius=1, location=(0, 0.018, 0.095), scale=(0.032, 0.033, 0.060)),
             L.sphere("Instep", col, mat, radius=1, location=(0, 0.105, arch_z), scale=(0.036, 0.078, arch_rz)),
             L.sphere("Ball", col, mat, radius=1, location=(0, 0.19, 0.016), scale=(0.056, 0.045, 0.020)),
             L.sphere("BallPad", col, mat, radius=1, location=(0, 0.19, 0.0), scale=(0.052, 0.044, 0.016)),
             L.sphere("Forefoot", col, mat, radius=1, location=(0, 0.16, 0.026), scale=(0.050, 0.04, 0.022))]
    for name, x, ln, r in TOES:
        if variant == "four_toes" and name == "Toe5":
            continue
        if variant == "short_big_toe" and name == "Toe1":
            ln = 0.030
        zc = max(0.016, r * 0.95)
        parts.append(L.sphere(name + "_a", col, mat, radius=1, location=(x, 0.208 + ln * 0.30, zc), scale=(r, ln * 0.30 * 1.2, r * 0.92)))
        parts.append(L.sphere(name + "_b", col, mat, radius=1, location=(x, 0.208 + ln * 0.74, zc), scale=(r * 0.95, ln * 0.26 * 1.2, r * 0.88)))
    if variant == "fused_toes":
        parts.append(L.sphere("Block", col, mat, radius=1, location=(0, 0.235, 0.015), scale=(0.052, 0.022, 0.011)))
    return parts


def build_foot(variant="solution"):
    col = L.collection("SCULPT")
    skin = L.material("MAT_Skin", (0.72, 0.58, 0.5), 0.6)
    parts = foot_parts(col, skin, variant)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_Foot", "ME_SCULPT_Foot"
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = type(ob.matrix_world)()
    ob.data.remesh_voxel_size = 0.0025
    bpy.ops.object.voxel_remesh()
    B5.taubin(ob, 4)
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0.0), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0.14), plane_no=(0, 0, 1), clear_outer=True)   # jambe : coupe plane
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    for p in ob.data.polygons:
        p.use_smooth = True
    if variant == "tiny":
        ob.data.transform(__import__("mathutils").Matrix.Scale(0.5, 4))
    print(f"[BCMA] SCULPT_Foot ({variant}) : {len(ob.data.vertices)} sommets")
    return ob


# --- scène -------------------------------------------------------------------------------------------------------
def studio(kind):
    L.studio(subject_height=0.3)
    c = L.collection("CAMERAS")
    if kind == "hand":
        top = L.camera("CAM_Top", c, (0.04, 0.07, 0.62), 75, make_active=True)
        S.look_at(top, (0.04, 0.07, 0.02))
        side = L.camera("CAM_Side", c, (0.6, 0.08, 0.1), 75, make_active=False)
        S.look_at(side, (0, 0.08, 0.03))
        tq = L.camera("CAM_34", c, (0.32, -0.25, 0.35), 75, make_active=False)
        S.look_at(tq, (0.02, 0.08, 0.02))
    else:
        top = L.camera("CAM_Top", c, (0.0, 0.11, 0.75), 75, make_active=False)
        S.look_at(top, (0, 0.11, 0.02))
        side = L.camera("CAM_Side", c, (0.62, 0.115, 0.075), 75, make_active=True)
        S.look_at(side, (0, 0.115, 0.075))
        tq = L.camera("CAM_34", c, (0.38, -0.3, 0.26), 75, make_active=False)
        S.look_at(tq, (0, 0.12, 0.07))
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.camera = bpy.data.objects["CAM_Top"] if kind == "hand" else bpy.data.objects["CAM_Side"]
    return sc


def guide(kind):
    """Guide à plat (plan XY, vue de dessus Num 7). bcma_gp écrit les points en (x, 0, z) : une rotation de −90° autour de X
    les couche dans le plan XY (z -> y). Repères : main = poignet, crête du poignet, articulations de la paume, bout du majeur ;
    pied = arrière du talon, milieu de la voûte, balle, bout du gros orteil."""
    ob = G.new_object("GP_Guide", L.collection("GUIDE"))
    ob.rotation_euler.x = math.radians(-90)
    ob.location = (0, 0, 0.0)
    ink = G.material(ob, "MAT_GP_Ink", (0.05, 0.05, 0.08))
    red = G.material(ob, "MAT_GP_Eye", (0.8, 0.1, 0.1))
    d = G.layer(ob, "GUIDE")
    ob.data.layers["GUIDE"].use_lights = False
    ys = (-0.04, 0.0, 0.10, 0.18) if kind == "hand" else (-0.015, 0.105, 0.19, 0.27)
    x0, x1 = (-0.07, 0.14) if kind == "hand" else (-0.07, 0.07)
    for i, y in enumerate(ys):
        G.polyline(d, [(x0, y), (x1, y)], 0.0010, red if i == len(ys) - 1 else ink)
    return ob


def build(kind, variant=None, with_model=True):
    L.reset("SC_" + kind)
    sc = studio(kind)
    guide(kind)
    if with_model:
        (build_hand if kind == "hand" else build_foot)(variant or "solution")
    L.instructions(NOTE_HAND if kind == "hand" else NOTE_FOOT)
    return sc


def views(sc, out, kind):
    tiles = []
    sc.render.resolution_x, sc.render.resolution_y = 600, 600
    for cam in ("CAM_Top", "CAM_34", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    variants = {"hand": ("fused_fingers", "four_fingers", "equal_fingers", "no_thumb", "tiny"),
                "foot": ("fused_toes", "four_toes", "flat_foot", "short_big_toe", "tiny")}
    for kind in ("hand", "foot"):
        build(kind, with_model=False)
        L.save(os.path.join(CH, "STARTER_FILES", f"ch03_07_{kind}_starter.blend"))
        for v in variants[kind]:
            build(kind, v)
            L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_07_{kind}_{v}.blend"))
        sc = build(kind)
        L.save(os.path.join(out, f"ch03_07_{kind}_solution.blend"))
        for o in bpy.data.objects:
            if o.name == "GP_Guide":
                o.hide_render = True
        views(sc, os.path.join(out, f"ch03_07_{kind}_reference.png"), kind)


if __name__ == "__main__":
    L.run(main)
