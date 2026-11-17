"""
build_ch07_11_files.py — « Animation faciale et lip sync » (CH07.11 : visèmes, synchronisation, clignement).

On reprend le rig facial de CH06.09 (GEO_Face, RIG_Face : bones jaw, ctl_smile, ctl_blink ; shape keys smile et blink pilotés par drivers). La piste « sonore » est une liste de phonèmes (dans le texte PHONEMES du fichier) :
  image 1 : M ; 7 : A ; 13 : O ; 19 : E ; 25 : M ; 31 : A ; 37 : E ; 43 : M ; plage 1–48, 24 i/s.
  Visèmes (cibles) : M (bouche FERMÉE : mâchoire 0°, sourire 0) ; A (bouche ouverte : mâchoire −12°) ; O (arrondie : mâchoire −7°) ; E (étirée : mâchoire −4°, sourire 0,04 m).
  Convention : la forme est atteinte UNE image AVANT le son et tenue sur l'image du son : aux images f − 1 et f, la pose égale le visème (mâchoire ± 1,5°, sourire ± 0,008 m ; l'image 1 compte seule).
  Clignement : le curseur ctl_blink monte à 0,05 m et redescend en 3 à 8 images, avec un départ entre les images 17 et 21.
  Contrôle : rotation X de jaw (le sens d'ouverture de CH06.09 : −15° ouvre) ; position X de ctl_smile et ctl_blink (Limit Location : 0 à 0,05 m).
  STARTER_FILES/ch07_11_lipsync_starter.blend : le visage de CH06.09 sans animation, avec le texte PHONEMES. COMPLETED_EXAMPLES/ch07_11_lipsync_solution.blend (+ _reference.png : courbes de la mâchoire et du sourire, visèmes en blanc)
  COUNTER_EXAMPLES/ : late, mouth_open_on_m, no_variety, popping, no_blink, slow_blink
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_11_files.py
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

CH = L.chapter_dir(__file__)
SRC = os.path.join(HERE, "..", "..", "..", "06_RIGGING", "CH06_09_FACIAL", "COMPLETED_EXAMPLES", "ch06_09_facial_solution.blend")
PHON = [(1, "M"), (7, "A"), (13, "O"), (19, "E"), (25, "M"), (31, "A"), (37, "E"), (43, "M")]
VISEME = {"M": (0.0, 0.0), "A": (-12.0, 0.0), "O": (-7.0, 0.0), "E": (-4.0, 0.04)}
NOTE = """CH07.11 — ANIMATION FACIALE ET LIP SYNC (GEO_Face, RIG_Face)
La piste sonore est la liste PHONEMES (éditeur de texte) : 1 M, 7 A, 13 O, 19 E, 25 M, 31 A, 37 E, 43 M (images). Animez le visage pour la suivre :
1. Visèmes : M = bouche FERMÉE (jaw 0°) ; A = bouche ouverte (jaw −12°) ; O = arrondie (jaw −7°) ; E = étirée (jaw −4° et ctl_smile à 0,04 m). Le sens d'ouverture de jaw est celui de CH06.09 (−15° ouvre).
2. Synchronisation : la bouche atteint le visème UNE image avant le son et le tient sur l'image du son : mêmes valeurs aux images f − 1 et f.
3. Continuité : la mâchoire ne saute jamais de plus de 6° d'une image à l'autre.
4. Clignement : ctl_blink monte à 0,05 m et redescend en 3 à 8 images, départ entre les images 17 et 21.
5. Plage 1–48 à 24 i/s.
Le correcteur lit la mâchoire, le curseur de sourire et le curseur de clignement sur les 48 images.
Vérification : SCRIPTS/validate_ch07_11.py -- --exercise lipsync
"""


def key_pose(rig, f, jaw, smile, blink=None):
    pb = rig.pose.bones
    pb["jaw"].rotation_euler = (math.radians(jaw), 0, 0)
    pb["jaw"].keyframe_insert("rotation_euler", index=0, frame=f)
    pb["ctl_smile"].location = (smile, 0, 0)
    pb["ctl_smile"].keyframe_insert("location", index=0, frame=f)


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def build(kind):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(SRC))
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 48
    rig = bpy.data.objects["RIG_Face"]
    pb = rig.pose.bones
    for n in ("jaw", "ctl_smile", "ctl_blink"):
        pb[n].rotation_mode = "XYZ"
        pb[n].location = (0, 0, 0)
        pb[n].rotation_euler = (0, 0, 0)
    for t in list(bpy.data.texts):
        bpy.data.texts.remove(t)
    txt = bpy.data.texts.new("PHONEMES")
    txt.write("\n".join(f"image {f} : {p}" for f, p in PHON) + "\n")
    txt.use_fake_user = True
    L.instructions(NOTE)
    if kind != "starter":
        shift = 3 if kind == "late" else 0
        lst = []
        for f, p in PHON:
            jaw, smile = VISEME[p]
            if kind == "mouth_open_on_m" and p == "M":
                jaw = -4.0
            if kind == "no_variety" and p in ("O", "E"):
                jaw, smile = VISEME["A"]
            lst.append((f, jaw, smile))
        frames = {}
        for f, jaw, smile in lst:
            for ff in (f - 1, f):
                if ff >= 1:
                    frames[ff + shift] = (jaw, smile)
        for f in sorted(frames):
            if f <= 48:
                jaw, smile = frames[f]
                blink = 0.0
                key_pose(rig, f, jaw, smile, blink)
        # clignement : 0 → 0,05 → 0
        if kind != "no_blink":
            span = (19, 29, 39) if kind == "slow_blink" else (19, 21, 23)
            for f, v in zip(span, (0.0, 0.05, 0.0)):
                pb["ctl_blink"].location = (v, 0, 0)
                pb["ctl_blink"].keyframe_insert("location", index=0, frame=f)
        else:
            pass
        # pas de clé de blink parasite : si la courbe existe, elle reste à 0
        act = rig.animation_data.action
        if kind == "popping":
            for fc in fcurves(act):
                if "jaw" in fc.data_path or "ctl_smile" in fc.data_path:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"
        for n in ("jaw", "ctl_smile", "ctl_blink"):
            pb[n].location = (0, 0, 0)
            pb[n].rotation_euler = (0, 0, 0)
    sc.frame_set(1)
    return rig


def sketch(path):
    rig = build("solution")
    sc = bpy.context.scene
    W, H = 800, 320
    img = np.full((H, W, 3), 0.08, np.float32)
    img[160, 20:W - 20] = (0.25, 0.25, 0.25)

    def x(f):
        return int(20 + (f - 1) / 47 * (W - 40))
    for f, p in PHON:
        img[10:H - 10, x(f)] = (0.25, 0.25, 0.25)
        jaw, smile = VISEME[p]
        y = int(160 + (-jaw) / 15 * 120)
        img[y - 5:y + 6, x(f) - 1:x(f) + 2] = (1, 1, 1)
        img[y - 1:y + 2, x(f) - 5:x(f) + 6] = (1, 1, 1)
    for f in range(1, 49):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        pb = rig.pose.bones
        for v, col in ((-math.degrees(pb["jaw"].rotation_euler.x) / 15 * 120 + 160, (0.9, 0.55, 0.2)), (160 - pb["ctl_smile"].location.x / 0.05 * 100, (0.3, 0.8, 0.5)), (160 - pb["ctl_blink"].location.x / 0.05 * 100, (0.3, 0.7, 1.0))):
            yy = int(v)
            img[yy - 2:yy + 3, x(f) - 2:x(f) + 3] = col
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_11_lipsync_starter.blend"))
    for k in ("late", "mouth_open_on_m", "no_variety", "popping", "no_blink", "slow_blink"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_11_lipsync_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_11_lipsync_solution.blend"))
    sketch(os.path.join(out, "ch07_11_lipsync_reference.png"))


if __name__ == "__main__":
    L.run(main)
