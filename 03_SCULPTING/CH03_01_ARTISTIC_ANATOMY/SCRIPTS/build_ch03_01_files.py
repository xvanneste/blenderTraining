"""
build_ch03_01_files.py — « Les masses du corps et le canon » (CH03.01, anatomie artistique).

  STARTER_FILES/ch03_01_proportions_starter.blend
      Toise de 1,75 m (GUIDES) : 7,5 graduations « tête » et repères anatomiques nommés (menton,
      épaules, mamelons, nombril, entrejambe, bout des doigts, genoux, chevilles) ; caméras de face et de
      profil ; collection MASSES vide.
  COMPLETED_EXAMPLES/ch03_01_adult_solution.blend (+ _reference.png, face et profil)
      Adulte de 7,5 têtes construit en 16 masses simples (tête, cage thoracique, bassin, bras, avant-bras,
      mains, cuisses, jambes, pieds) aux repères du canon.
  COMPLETED_EXAMPLES/ch03_01_child_solution.blend  enfant d'environ 5 têtes (1,10 m).
  COMPLETED_EXAMPLES/ch03_01_gesture_solution.blend (+ _reference.png)
      Contrapposto : bassin et cage inclinés en sens opposés, tête au-dessus du pied d'appui.
Usage : blender -b --factory-startup --python build_ch03_01_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Euler, Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
H = 1.75
LANDMARKS = [("Menton", 0.87), ("Épaules", 0.82), ("Mamelons", 0.72), ("Coudes / nombril", 0.62),
             ("Entrejambe", 0.50), ("Bout des doigts", 0.38), ("Genoux", 0.28), ("Chevilles", 0.045)]
NOTE = """CH03.01 — LES MASSES DU CORPS (collection MASSES, vues : Num 1 face, Num 3 profil)
Construisez un adulte de 1,75 m, canon 7,5 têtes, avec des primitives (Add > Mesh) renommées :
MASS_Head, MASS_Ribcage, MASS_Pelvis, MASS_UpperArm_L/R, MASS_Forearm_L/R, MASS_Hand_L/R,
MASS_Thigh_L/R, MASS_Shin_L/R, MASS_Foot_L/R (16 masses ; _L = côté +X, _R = côté −X).
Calez-les sur les repères de la toise (GUIDES) : menton 0,87 H, entrejambe 0,50 H, genoux 0,28 H,
coudes 0,62 H, bout des doigts 0,38 H (bras le long du corps), pieds au sol (z = 0).
Côtés symétriques (Ctrl+M pour un miroir, ou Mirror Modifier puis application).
Vérification : SCRIPTS/validate_ch03_01.py -- --exercise adult  (child, gesture : voir EXERCISES)
"""


def guides():
    g = L.collection("GUIDES")
    mat = L.material("MAT_Guide", (0.05, 0.25, 0.75), 0.9)
    txt = L.material("MAT_Label", (0.05, 0.05, 0.08), 0.9)
    hu = H / 7.5
    for i in range(8):
        L.cube(f"GUIDE_Head_{i}", g, mat, size=1, location=(-0.55, 0, H - i * hu), scale=(0.25, 0.01, 0.004))
    L.cube("GUIDE_Pole", g, mat, size=1, location=(-0.68, 0, H / 2), scale=(0.01, 0.01, H))
    for name, f in LANDMARKS:
        L.cube(f"GUIDE_{name}", g, mat, size=1, location=(0.55, 0, f * H), scale=(0.3, 0.01, 0.003))
        t = L.text_note(f"{name} {f:.2f} H", f"TXT_{name}", g, (0.72, -0.02, f * H - 0.015), 0.045)
        t.rotation_euler.x = math.radians(90)          # face à la vue de face
        t.data.materials.append(txt)
    for o in g.objects:
        o.hide_select = True


def cams():
    c = L.collection("CAMERAS")
    front = L.camera("CAM_Front", c, (0, -6, 0.9), 50, make_active=True)
    front.rotation_euler = (math.radians(90), 0, 0)
    front.data.type, front.data.ortho_scale = "ORTHO", 2.3
    side = L.camera("CAM_Side", c, (6, 0, 0.9), 50, make_active=False)
    side.rotation_euler = (math.radians(90), 0, math.radians(90))
    side.data.type, side.data.ortho_scale = "ORTHO", 2.3


def ellipsoid(name, col, mat, c, r):
    return L.sphere(name, col, mat, radius=1, location=c, scale=r)


def capsule(name, col, mat, top, bottom, radius):
    """Cylindre lissé entre deux points (axe local Z), pour les segments des membres."""
    a, b = Vector(top), Vector(bottom)
    d = a - b
    o = L.cylinder(name, col, mat, radius=radius, depth=d.length, vertices=16, location=(a + b) / 2)
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def ik_knee(hip, ankle, l1, l2, forward=-1.0):
    """Genou d'une jambe à 2 segments, dans le plan contenant la hanche, la cheville et l'axe Y (avant = −Y)."""
    hip, ankle = Vector(hip), Vector(ankle)
    d = ankle - hip
    L_ = min(d.length, l1 + l2 - 1e-4)
    a = math.acos(max(-1, min(1, (l1 * l1 + L_ * L_ - l2 * l2) / (2 * l1 * L_))))
    axis = d.normalized()
    side = axis.cross(Vector((0, forward, 0))).normalized()
    if side.length < 1e-6:
        side = Vector((1, 0, 0))
    bend = side.cross(axis).normalized()          # perpendiculaire dans le plan de la jambe, vers l'avant
    if bend.y * forward < 0:
        bend = -bend
    return hip + axis * (l1 * math.cos(a)) + bend * (l1 * math.sin(a))


def rot_y(v, ang):
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return Vector((v.x * c + v.z * s_, v.y, -v.x * s_ + v.z * c))


def figure(s=1.0, head_scale=1.0, child=False, pelvis_tilt=0.0, chest_tilt=0.0, gesture=False):
    """Masses d'un personnage debout, construites entre des POINTS ARTICULAIRES (squelette simple).
    pelvis_tilt / chest_tilt (degrés, vue de face) : inclinaisons du bassin et de la cage."""
    col = L.collection("MASSES")
    skin = L.material("MAT_Mass", (0.78, 0.62, 0.52), 0.6)
    h = H * s
    hh = H / 7.5 * s * head_scale
    crotch = (0.45 if child else 0.50) * h
    knee_z, ankle_z = (0.25 if child else 0.28) * h, 0.045 * h
    thigh, shin = crotch + 0.04 * h - knee_z, knee_z - ankle_z
    hip_dx = 0.052 * h
    # bassin : centre, au-dessus de la jambe d'appui (R) en geste
    pel_c = Vector((0, 0, crotch + 0.055 * h))
    if gesture:
        pel_c.x = -hip_dx * 0.85
    hips = {sd: pel_c + rot_y(Vector((sx * hip_dx, 0, -0.015 * h)), pelvis_tilt) for sd, sx in (("L", 1), ("R", -1))}
    ankles = {"L": Vector((hip_dx, 0, ankle_z)), "R": Vector((-hip_dx, 0, ankle_z))}
    if gesture:                                    # jambe libre : pied en avant, talon levé
        ankles["L"] = Vector((hip_dx * 1.6, -0.07 * h, ankle_z + 0.03 * h))
    # tronc : taille au-dessus du bassin, cage inclinée à l'opposé
    waist = pel_c + rot_y(Vector((0, 0, 0.055 * h)), pelvis_tilt)
    neck_z = h - hh - 0.055 * h                    # le crâne touche exactement la taille h
    rib_len = neck_z - waist.z - 0.03 * h
    rib_c = waist + rot_y(Vector((0, 0, 0.03 * h + rib_len / 2)), chest_tilt)
    neck = waist + rot_y(Vector((0, 0, 0.03 * h + rib_len)), chest_tilt)
    head_c = Vector((neck.x, 0, h - hh / 2))
    if gesture:                                    # tête recentrée au-dessus du pied d'appui
        head_c.x = ankles["R"].x
    ellipsoid("MASS_Head", col, skin, head_c, (hh * 0.34, hh * 0.42, hh / 2))
    rib = ellipsoid("MASS_Ribcage", col, skin, rib_c, (0.09 * h, 0.065 * h, rib_len / 2))
    pel = ellipsoid("MASS_Pelvis", col, skin, pel_c, (0.095 * h, 0.065 * h, 0.055 * h))
    rib.rotation_euler.y = math.radians(chest_tilt)
    pel.rotation_euler.y = math.radians(pelvis_tilt)
    elbow_z, wrist_z, tips_z = [f * h for f in ((0.62, 0.48, 0.38) if not child else (0.60, 0.45, 0.36))]
    for side, sx in (("L", 1), ("R", -1)):
        hip, ank = hips[side], ankles[side]
        kn = ik_knee(hip, ank, thigh, shin)
        capsule(f"MASS_Thigh_{side}", col, skin, hip, kn, 0.04 * h)
        capsule(f"MASS_Shin_{side}", col, skin, kn, ank, 0.03 * h)
        foot = L.cube(f"MASS_Foot_{side}", col, skin, size=1, location=(ank.x, ank.y - 0.035 * h, ank.z - ankle_z / 2),
                      scale=(0.055 * h, 0.15 * h, ankle_z))
        if gesture and side == "L":
            foot.rotation_euler.x = math.radians(-18)
            foot.location.z = 0.045 * h
        sh = neck + rot_y(Vector((sx * hh * 0.95, 0, -0.01 * h)), chest_tilt)   # articulation ≈ 0,80 H
        dz = sh.z - (neck_z - 0.01 * h)            # décalage de l'épaule dû à l'inclinaison de la cage
        el = Vector((sh.x + sx * 0.006 * h, 0, elbow_z + dz))
        wr = Vector((el.x + sx * 0.006 * h, -0.01 * h, wrist_z + dz))
        tip = Vector((wr.x, wr.y, tips_z + dz))
        capsule(f"MASS_UpperArm_{side}", col, skin, sh, el, 0.027 * h)
        capsule(f"MASS_Forearm_{side}", col, skin, el, wr, 0.022 * h)
        ellipsoid(f"MASS_Hand_{side}", col, skin, (wr + tip) / 2, (0.013 * h, 0.03 * h, (wr - tip).length / 2))
    return col


def build(kind):
    L.reset("SC_Anatomy")
    guides()
    cams()
    L.light("LGT_Key", L.collection("LIGHTS"), "SUN", (2, -4, 5), 3.5, rotation=(45, 0, 35))
    L.world((0.6, 0.62, 0.66), 0.7, "WO_Studio")
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1080
    if kind == "adult":
        figure()
    elif kind == "child":
        figure(s=1.10 / 1.75, head_scale=1.5, child=True)       # 1,10 m, tête 0,22 m = 5 têtes
    elif kind == "gesture":
        figure(pelvis_tilt=8.0, chest_tilt=-6.0, gesture=True)   # appui R : hanche R haute, épaule R basse
    else:
        L.collection("MASSES")
    L.instructions(NOTE)
    return sc


def render_views(sc, out):
    tiles = []
    for cam in ("CAM_Front", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, Hh = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(Hh, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("views", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(None)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_01_proportions_starter.blend"))
    for kind in ("adult", "child", "gesture"):
        sc = build(kind)
        L.save(os.path.join(out, f"ch03_01_{kind}_solution.blend"))
        if kind != "child":
            render_views(sc, os.path.join(out, f"ch03_01_{kind}_reference.png"))


if __name__ == "__main__":
    L.run(main)
