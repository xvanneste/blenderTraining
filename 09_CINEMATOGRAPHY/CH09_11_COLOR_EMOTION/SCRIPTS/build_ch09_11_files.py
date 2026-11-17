"""
build_ch09_11_files.py — « Couleur et émotion » (CH09.11 : teinte, saturation, valeur ; palettes ; color script).

Scène (rendu Workbench FLAT, Standard : les couleurs d'objet s'affichent telles quelles) : un « color script » de cinq cartes carrées de 2 m côte à côte (x = −4, −2, 0, 2, 4), vues du dessus par une caméra orthographique
  (500 × 100) : JOY, SADNESS, ANGER, CALM, FEAR. Chaque carte = un fond BG_<NOM> (plan de 2 × 2 m) et un accent ACC_<NOM> (plan de 0,8 × 0,8 m au centre).
  Consigne : régler Object > Viewport Display > Color de chacun des dix objets pour que la carte exprime son émotion. Mesures (teinte H en degrés, saturation S et valeur V de la couleur AFFICHÉE, médiane sur la zone du fond) :
    JOY : H 20–65, S ≥ 0,6, V ≥ 0,8 ; SADNESS : H 190–250, S 0,15–0,5, V ≤ 0,5 ; ANGER : H ≤ 15 ou ≥ 345, S ≥ 0,7, V 0,35–0,7 ; CALM : H 150–220, S 0,15–0,5, V 0,6–0,85 ; FEAR : V ≤ 0,2 (fond sombre) et accent V ≥ 0,5.
    Les fonds de JOY, SADNESS, ANGER et CALM ont des teintes distinctes (écart ≥ 25° deux à deux) ; sur chaque carte l'accent se détache du fond (écart de valeur ≥ 0,2, ou teintes éloignées d'au moins 120° si les deux couleurs sont saturées).
  Départ : les dix objets sont gris moyen (0,5). Solution (HSV affichées) : JOY fond (45°, 0,75, 0,95) accent (200°, 0,6, 0,9) ; SADNESS fond (220°, 0,35, 0,35) accent (40°, 0,4, 0,8) ;
    ANGER fond (0°, 0,85, 0,55) accent (50°, 0,3, 0,95) ; CALM fond (175°, 0,3, 0,75) accent (30°, 0,3, 0,4) ; FEAR fond (270°, 0,4, 0,12) accent (120°, 0,8, 0,7).
  STARTER_FILES/ch09_11_color_starter.blend ; COMPLETED_EXAMPLES/ch09_11_color_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : wrong_hue_sadness (tristesse verdâtre), saturated_calm (calme très saturé), dim_joy (joie sombre), same_hues (calme et tristesse de même teinte), low_contrast (colère : accent de la valeur du fond), bright_fear (peur sur fond clair)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_11_files.py
Testé avec : Blender 5.3.0.
"""
import colorsys
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
NAMES = ("JOY", "SADNESS", "ANGER", "CALM", "FEAR")
NOTE = """CH09.11 — COULEUR ET ÉMOTION (BG_JOY, ACC_JOY, … BG_FEAR, ACC_FEAR)
Un color script de cinq cartes : chaque carte a un fond (BG_*) et un accent (ACC_*). Au départ tout est gris. Réglez Object > Viewport Display > Color de chaque objet.
JOY : teinte 20–65°, saturation ≥ 0,6, valeur ≥ 0,8 (chaud, vif, clair). SADNESS : teinte 190–250°, saturation 0,15–0,5, valeur ≤ 0,5 (froid, terne, sombre).
ANGER : teinte proche du rouge (≤ 15° ou ≥ 345°), saturation ≥ 0,7, valeur 0,35–0,7. CALM : teinte 150–220°, saturation 0,15–0,5, valeur 0,6–0,85.
FEAR : fond très sombre (valeur ≤ 0,2) et accent clair (valeur ≥ 0,5).
Les fonds de JOY, SADNESS, ANGER, CALM ont des teintes différentes (écart ≥ 25°) ; sur chaque carte l'accent se détache du fond (écart de valeur ≥ 0,2, ou teintes éloignées d'au moins 120° si les deux couleurs sont saturées).
Conseil : réglez une couleur, lancez le correcteur : il affiche les H, S, V réellement RENDUS (la valeur d'une couleur d'objet est linéaire : une valeur affichée de 0,5 donne un gris clair).
Vérification : SCRIPTS/validate_ch09_11.py -- --exercise color
"""

SOL = {"JOY": ((45, .75, .95), (200, .6, .9)), "SADNESS": ((220, .35, .35), (40, .4, .8)), "ANGER": ((0, .85, .55), (50, .3, .95)),
       "CALM": ((175, .3, .75), (30, .3, .4)), "FEAR": ((270, .4, .12), (120, .8, .7))}


def lin(hsv):
    """HSV AFFICHÉE (teinte en degrés) -> couleur d'objet linéaire."""
    r, g, b = colorsys.hsv_to_rgb(hsv[0] / 360.0, hsv[1], hsv[2])
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b), 1.0)


def plane(sc, name, x, size, z):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.location = (x, 0, z)
    return o


def build(kind):
    L.reset("SC_COLORSCRIPT")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    wo = bpy.data.worlds.new("WO_Black")
    wo.color = (0, 0, 0)
    sc.world = wo
    sol = {k: [list(v[0]), list(v[1])] for k, v in SOL.items()}
    if kind == "wrong_hue_sadness":
        sol["SADNESS"][0] = [100, .35, .35]
    elif kind == "saturated_calm":
        sol["CALM"][0] = [175, .9, .75]
    elif kind == "dim_joy":
        sol["JOY"][0] = [45, .75, .5]
    elif kind == "same_hues":
        sol["CALM"][0] = [200, .3, .75]
    elif kind == "low_contrast":
        sol["ANGER"][1] = [0, .85, .55]
    elif kind == "bright_fear":
        sol["FEAR"][0] = [270, .4, .5]
    for i, n in enumerate(NAMES):
        x = (i - 2) * 2.0
        bg = plane(sc, "BG_" + n, x, 2.0, 0.0)
        ac = plane(sc, "ACC_" + n, x, 0.8, 0.05)
        if kind == "starter":
            bg.color = ac.color = (0.5, 0.5, 0.5, 1)
        else:
            bg.color, ac.color = lin(sol[n][0]), lin(sol[n][1])
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 5)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 10
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 500, 100, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0911.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(100, 500, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def hsv_of(px, r0, r1, c0, c1):
    m = np.median(px[r0:r1, c0:c1].reshape(-1, 3), axis=0)
    h, s, v = colorsys.rgb_to_hsv(*[float(t) for t in m])
    return round(h * 360, 1), round(s, 3), round(v, 3)


def measure(px):
    out = {}
    for i, n in enumerate(NAMES):
        c0 = i * 100
        out[n] = (hsv_of(px, 5, 25, c0 + 10, c0 + 90), hsv_of(px, 40, 60, c0 + 40, c0 + 60))
    return out


def calibrate():
    for kind in ("starter", "solution"):
        build(kind)
        print("[color]", kind, measure(render()))


def sketch(path):
    img = np.zeros((260, 540, 3), np.float32)
    for row, kind in enumerate(("starter", "solution")):
        build(kind)
        px = render()
        y0 = 15 + row * 125
        img[y0:y0 + 100, 20:520, :] = px
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 540, 260)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_11_color_starter.blend"))
    for k in ("wrong_hue_sadness", "saturated_calm", "dim_joy", "same_hues", "low_contrast", "bright_fear"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_11_color_{k}.blend"))
    sketch(os.path.join(out, "ch09_11_color_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_11_color_solution.blend"))


if __name__ == "__main__":
    L.run(main)
