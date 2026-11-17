"""
build_ch09_08_files.py — « Objectifs et focales » (CH09.08 : focale, capteur, champ de vision, compression de la perspective).

Scène (rendu Workbench, lumière plate, couleurs d'objet) : Ground (gris), ciel = couleur du monde (bleu),
  Subject (cylindre rouge de 1,8 m en (-0,4, 8, 0,9)) et Backdrop (cylindre vert identique en (0,4, 16, 0,9)),
  CAM à (0, 0, 0,9) regardant vers +Y (rotation X = 90°), capteur 36 mm (Fit AUTO), rendu 160 × 90 (16:9), focale 35 mm au départ.
  Consigne : « compresser » la perspective SANS déplacer les cylindres : en reculant la caméra et en allongeant la focale,
  - le fond (vert) doit paraître au moins 75 % aussi haut que le sujet (au départ : 50 %, car il est deux fois plus loin) ;
  - le sujet doit garder une hauteur de 40 % de l'image (± 5 %) ;
  - la focale doit être d'au moins 70 mm (téléobjectif).
  Calcul : hauteur apparente ∝ 1 / distance. Reculer la caméra de c mètres : rapport = (8 + c) / (16 + c) ; il faut c ≥ 16. Hauteur du sujet dans l'image = 1,8 × f / ((8 + c) × 20,25).
  Solution : c = 24 m (caméra en y = −24), focale 144 mm (mesuré : rapport 0,80 ; hauteur du sujet 40 %).
  STARTER_FILES/ch09_08_lenses_starter.blend ; COMPLETED_EXAMPLES/ch09_08_lenses_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : wide (départ : rapport 0,50), moved_only (caméra reculée mais focale 35 : sujet minuscule), zoomed_only (focale 70 sans reculer : sujet trop grand, rapport 0,50),
    short_lens (reculé de 24 m, focale 75 : rapport bon, hauteur 21 % : trop petit), subject_moved (sujet reculé à y = 16 pour tricher)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_08_files.py
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
NOTE = """CH09.08 — OBJECTIFS ET FOCALES (Subject, Backdrop, Ground, CAM)
Deux cylindres identiques de 1,8 m : le rouge (Subject) à 8 m de la caméra, le vert (Backdrop) à 16 m. Le fond paraît deux fois plus petit : perspective forte (focale 35 mm).
Consigne : compressez la perspective sans toucher aux cylindres, en ne modifiant que la caméra (CAM).
1. Reculez la caméra (Location Y) : la hauteur apparente est proportionnelle à 1 / distance.
2. Allongez la focale (Camera > Lens > Focal Length) pour que le sujet reste à 40 % de la hauteur de l'image (± 5 %).
3. Cible : le fond fait au moins 75 % de la hauteur du sujet ; focale ≥ 70 mm.
Vérification : SCRIPTS/validate_ch09_08.py -- --exercise lenses
"""


def cyl(sc, name, x, y, col):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.25, radius2=0.25, depth=1.8)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.location = (x, y, 0.9)
    o.color = col
    return o


def build(kind):
    L.reset("SC_LENSES")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    wo = bpy.data.worlds.new("WO_Sky")
    wo.color = (0.4, 0.6, 1.0)
    sc.world = wo
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=200)
    me = bpy.data.meshes.new("ME_Ground")
    bm.to_mesh(me)
    bm.free()
    g = bpy.data.objects.new("Ground", me)
    sc.collection.objects.link(g)
    g.color = (0.35, 0.35, 0.35, 1)
    s = cyl(sc, "Subject", -0.4, 8.0, (1, 0, 0, 1))
    cyl(sc, "Backdrop", 0.4, 16.0, (0, 1, 0, 1))
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.sensor_width = 36
    cam.data.sensor_fit = "AUTO"
    sc.camera = cam
    back, f = {"starter": (0, 35), "wide": (0, 35), "solution": (24, 144), "moved_only": (24, 35), "zoomed_only": (0, 70), "short_lens": (24, 75), "subject_moved": (24, 144)}[kind]
    cam.location = (0, -back, 0.9)
    cam.data.lens = f
    if kind == "subject_moved":
        s.location.y = 16.0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0908.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def analyse(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    red = (R > 0.7) & (G < 0.3) & (B < 0.3)
    green = (G > 0.7) & (R < 0.3) & (B < 0.3)
    H = red.shape[0]

    def height(m):
        ys = np.nonzero(m)[0]
        return (ys.max() + 1 - ys.min()) / H if len(ys) else 0.0
    hs, hb = height(red), height(green)
    return {"subject_h": hs, "backdrop_h": hb, "ratio": (hb / hs) if hs > 0 else 0.0, "red_px": int(red.sum()), "green_px": int(green.sum())}


def calibrate():
    for kind in ("starter", "solution", "moved_only", "zoomed_only", "short_lens", "subject_moved"):
        build(kind)
        a = analyse(render())
        print(f"[lens] {kind:14s}", {k: round(float(v), 3) for k, v in a.items()})


def sketch(path):
    W, H = 780, 230
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution")):
        build(kind)
        px = render()
        tile = np.kron(px, np.ones((2, 2, 1), np.float32))  # 180 × 320
        y0, x0 = 25, 30 + i * 380
        img[y0:y0 + 180, x0:x0 + 320, :] = tile
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_08_lenses_starter.blend"))
    for k in ("wide", "moved_only", "zoomed_only", "short_lens", "subject_moved"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_08_lenses_{k}.blend"))
    sketch(os.path.join(out, "ch09_08_lenses_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_08_lenses_solution.blend"))


if __name__ == "__main__":
    L.run(main)
