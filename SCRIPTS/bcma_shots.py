"""
bcma_shots.py — Outils « langage cinématographique » partagés (phase 18 module C, phase 9).

- mannequin_mesh(name, col, location, mat, facing) : personnage simple de 1,75 m (repères anatomiques
  aux hauteurs standard ci-dessous), en un seul maillage.
- look_at(cam, target) : oriente une caméra vers un point.
- cut_height(scene, cam, base, top=1.9) : hauteur du corps (en m, le long de l'axe vertical du
  personnage) qui tombe sur le BORD BAS de l'image ; None si tout le personnage est au-dessus.
- classify(scene, cam, base) : valeur de plan déduite (PE, PM, PA, PRT, PRP, GP, TGP) + mesures.

Repères (personnage de 1,75 m) : genou 0,50 · mi-cuisse 0,70 · taille 1,05 · poitrine 1,30 ·
menton 1,50 · yeux 1,62 · sommet du crâne 1,75.
Testé avec : Blender 5.3.0.
"""
import math

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

LANDMARKS = {"genou": 0.50, "mi-cuisse": 0.70, "taille": 1.05, "poitrine": 1.30, "menton": 1.50,
             "yeux": 1.62, "crâne": 1.75}
SHOTS = {  # code : (nom, description de la coupe basse)
    "PE": ("Plan d'ensemble", "personnage entier, petit dans le décor (≤ 30 % de la hauteur d'image)"),
    "PM": ("Plan moyen (en pied)", "personnage entier, 55 à 95 % de la hauteur d'image"),
    "PA": ("Plan américain", "coupé entre le genou et la mi-cuisse (0,50–0,85 m)"),
    "PRT": ("Plan rapproché taille", "coupé à la taille (0,90–1,15 m)"),
    "PRP": ("Plan rapproché poitrine", "coupé à la poitrine (1,20–1,40 m)"),
    "GP": ("Gros plan", "le visage : coupé sous le menton (1,40–1,55 m)"),
    "TGP": ("Très gros plan", "une partie du visage : coupé au-dessus du menton (> 1,55 m)"),
    "INS": ("Insert", "un objet ou un détail occupe le cadre"),
}


def mannequin_mesh(name, col, location=(0, 0, 0), mat=None):
    bm = bmesh.new()

    def sphere(c, r, sz=1.0):
        res = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
        for v in res["verts"]:
            v.co = Vector((v.co.x, v.co.y, v.co.z * sz)) + Vector(c)
        return {f for v in res["verts"] for f in v.link_faces}

    def cyl(c, r, h):
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r, depth=h)
        for v in res["verts"]:
            v.co += Vector(c)
    sphere((0, 0, 1.635), 0.115, 1.1)          # tête : sommet ≈ 1,76
    cyl((0, 0, 1.48), 0.05, 0.12)              # cou
    sphere((0, 0, 1.25), 0.2, 1.35)            # torse
    sphere((0, 0, 0.98), 0.17, 0.8)            # bassin
    for s in (-1, 1):
        cyl((0.1 * s, 0, 0.48), 0.07, 0.9)     # jambes
        cyl((0.27 * s, 0, 1.12), 0.05, 0.62)   # bras
    for sx in (-0.045, 0.045):                 # yeux (face à −Y), matériau n° 2
        for f in sphere((sx, -0.1, 1.645), 0.022, 1.0):
            f.material_index = 1
    me = bpy.data.meshes.new(name.replace("CHR_", "ME_"))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location = location
    col.objects.link(ob)
    if mat:
        me.materials.append(mat)
        eye = bpy.data.materials.get("MAT_Eyes") or bpy.data.materials.new("MAT_Eyes")
        eye.diffuse_color = (0.02, 0.02, 0.02, 1)
        bsdf = next((n for n in eye.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if eye.node_tree else None
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.025, 1)
            bsdf.inputs["Roughness"].default_value = 0.2
        me.materials.append(eye)
    return ob


def look_at(cam, target):
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def _proj(scene, cam, p):
    return world_to_camera_view(scene, cam, Vector(p))


def cut_height(scene, cam, base, top=1.9):
    """Hauteur (m) du personnage au bord bas de l'image (y = 0), le long de son axe vertical."""
    bx, by, bz = base
    f = lambda z: _proj(scene, cam, (bx, by, bz + z)).y
    if f(0.0) >= 0.0:
        return None                  # les pieds sont dans l'image
    if f(top) < 0.0:
        return top                   # tout le personnage sous l'image
    lo, hi = 0.0, top
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def classify(scene, cam, base):
    bx, by, bz = base
    pts = {k: _proj(scene, cam, (bx, by, bz + z)) for k, z in (("pieds", 0.0), ("crâne", 1.75), ("yeux", 1.62))}
    info = {"x_yeux": pts["yeux"].x, "devant": pts["yeux"].z > 0}
    cut = cut_height(scene, cam, base)
    info["coupe"] = cut
    if not info["devant"]:
        return None, info
    if cut is None:
        frac = pts["crâne"].y - pts["pieds"].y
        info["fraction"] = frac
        if pts["crâne"].y > 1.0:
            return None, info
        if frac <= 0.30:
            return "PE", info
        if 0.55 <= frac <= 0.95:
            return "PM", info
        return None, info
    for code, lo, hi in (("PA", 0.50, 0.85), ("PRT", 0.90, 1.15), ("PRP", 1.20, 1.40), ("GP", 1.40, 1.55)):
        if lo <= cut < hi:
            return code, info
    if cut >= 1.55:
        return "TGP", info
    return None, info
