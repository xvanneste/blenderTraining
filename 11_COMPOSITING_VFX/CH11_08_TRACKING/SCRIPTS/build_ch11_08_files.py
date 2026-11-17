"""
build_ch11_08_files.py — « Tracking et matchmoving » (CH11.08 : suivre des points dans un plan, résoudre la caméra).

Données : une séquence de 40 images PNG (320 × 180, « ch11_08_clip/frame_0001.png … 0040 ») RENDUE par le script (Workbench) : 48 petites sphères blanches (rayon 8 cm) semées en 3D devant la caméra (x de −5 à 5, y de 5 à 14, z de 0 à 3 m) sur fond noir ;
  la caméra (focale 35 mm, capteur 36 mm) avance en translation de x = −1 m à x = +1 m (image 1 à 40) à hauteur 1,5 m, regard fixe vers +Y : il y a de la PARALLAXE (les points proches bougent plus que les lointains), ce qui permet de résoudre la caméra.
  Le fichier contient le clip (movieclips « ch11_08 », source séquence d'images, chemin RELATIF) et la scène.
  Consigne (éditeur Movie Clip, mode Tracking) :
    1. régler la caméra du clip : Focal Length 35 mm (tracking.camera.focal_length), capteur 36 mm ;
    2. détecter des points (Detect Features) à l'image 1 et les suivre sur toute la séquence (Track Markers, vers l'avant) : au moins 12 pistes d'au moins 30 marqueurs ;
    3. résoudre la caméra (Solve Camera Motion) : reconstruction valide, erreur de reprojection moyenne ≤ 1,0 pixel.
  Le correcteur contrôle les pistes et la reconstruction ENREGISTRÉES ; il relance lui-même Solve Camera Motion avec les pistes de l'élève (via un éditeur de clip temporaire) pour confirmer que l'erreur annoncée est reproductible.
  Départ : clip chargé, aucune piste, focale 24 mm. Solution : focale 35 mm, 8 à 20 pistes suivies (Detect Features, Track Markers), caméra résolue (mesuré : voir calibrage).
  STARTER_FILES/ch11_08_tracking_starter.blend (+ dossier ch11_08_clip/) ; COMPLETED_EXAMPLES/ch11_08_tracking_solution.blend (+ ch11_08_clip/) (+ _reference.png : image 1 avec les pistes)
  COUNTER_EXAMPLES/ : no_tracks (départ), short_tracks (suivi sur 8 images seulement), wrong_focal (focale 100 mm), not_solved (pistes sans résolution), few_tracks (4 pistes)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_08_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.08 — TRACKING ET MATCHMOVING (clip « ch11_08 », 40 images)
La caméra qui a filmé ces points s'est déplacée en translation (x de −1 m à +1 m, focale 35 mm, capteur 36 mm). Retrouvez son mouvement dans l'éditeur Movie Clip :
1. Camera de clip : Focal Length 35 mm.
2. Detect Features à l'image 1, puis Track Markers vers l'avant sur toute la séquence : au moins 12 pistes d'au moins 30 marqueurs.
3. Solve Camera Motion : reconstruction valide, erreur moyenne ≤ 1,0 pixel.
Vérification : SCRIPTS/validate_ch11_08.py -- --exercise tracking
"""
N_FR, W, H = 40, 320, 180
LAST = {}


def render_clip(folder):
    os.makedirs(folder, exist_ok=True)
    L.reset("SC_CLIPGEN")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light, sc.display.shading.color_type = "FLAT", "OBJECT"
    sc.view_settings.view_transform = "Standard"
    wo = bpy.data.worlds.new("WO_Black")
    wo.color = (0, 0, 0)
    sc.world = wo
    rng = np.random.RandomState(11)
    for i in range(48):
        x, y, z = rng.uniform(-5, 5), rng.uniform(5, 14), rng.uniform(0, 3)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x, y, z), segments=10, ring_count=6)
        o = bpy.context.object
        o.name = f"P_{i:02d}"
        o.color = (1, 1, 1, 1)
    cam = bpy.data.objects.new("CAMGEN", bpy.data.cameras.new("CAMGEN"))
    sc.collection.objects.link(cam)
    cam.data.lens, cam.data.sensor_width = 35, 36
    cam.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    for f in range(1, N_FR + 1):
        cam.location = (-1.0 + 2.0 * (f - 1) / (N_FR - 1), 0.0, 1.5)
        sc.render.filepath = os.path.join(folder, f"frame_{f:04d}")
        bpy.ops.render.render(write_still=True)


def with_clip_area(fn):
    wm = bpy.context.window_manager
    win = wm.windows[0]
    area = win.screen.areas[0]
    keep = area.type
    area.type = "CLIP_EDITOR"
    sp = area.spaces.active
    reg = [r for r in area.regions if r.type == "WINDOW"][0]
    try:
        with bpy.context.temp_override(window=win, area=area, region=reg, space_data=sp):
            return fn(sp)
    finally:
        area.type = keep


def build(kind, rel_prefix):
    L.reset("SC_TRACKING")
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    sc.frame_start, sc.frame_end = 1, N_FR
    clip = bpy.data.movieclips.load(os.path.join(CH, "tmp_clip", "frame_0001.png"))
    clip.name = "ch11_08"
    sc.active_clip = clip
    trk = clip.tracking
    trk.camera.sensor_width = 36.0
    trk.camera.focal_length = 24.0 if kind == "starter" else (100.0 if kind == "wrong_focal" else 35.0)
    if kind in ("starter", "no_tracks"):
        clip.filepath = rel_prefix + "frame_0001.png"
        sc.frame_set(1)
        L.instructions(NOTE)
        return clip
    ntr = 4 if kind == "few_tracks" else 20

    def work(sp):
        sp.clip = clip
        sc.frame_set(1)
        bpy.ops.clip.detect_features(placement="FRAME", margin=10, threshold=0.2, min_distance=15)
        names = [t.name for t in trk.tracks]
        for i, t in enumerate(trk.tracks):
            t.select = i < ntr
        if kind == "short_tracks":
            sc.frame_end = 8
        bpy.ops.clip.track_markers(backwards=False, sequence=True)
        sc.frame_end = N_FR
        sc.frame_set(1)
        for t in trk.tracks:
            t.select = True
        if kind not in ("not_solved", "short_tracks", "few_tracks"):
            bpy.ops.clip.solve_camera()
    with_clip_area(work)
    LAST.clear()
    LAST.update(stats())  # AVANT de changer le chemin (un chemin relatif non résolu dans la session non enregistrée vide le clip : 256 × 256)
    clip.filepath = rel_prefix + "frame_0001.png"  # chemin RELATIF à l'emplacement du .blend enregistré
    sc.frame_set(1)
    L.instructions(NOTE)
    return clip


def stats():
    clip = bpy.data.movieclips["ch11_08"]
    trk = clip.tracking
    lens = [len(t.markers) for t in trk.tracks]
    return {"tracks": len(lens), "long": sum(1 for n in lens if n >= 30), "valid": bool(trk.reconstruction.is_valid), "error": float(trk.reconstruction.average_error), "focal": trk.camera.focal_length}


def calibrate():
    for kind in ("solution", "short_tracks", "wrong_focal", "not_solved", "few_tracks"):
        build(kind, "//../ch11_08_clip/")
        print("[trk]", kind, LAST)


def sketch(path):
    """Image 1 du clip avec les pistes (croix) : tracé numpy."""
    build("solution", "//ch11_08_clip/")
    clip = bpy.data.movieclips["ch11_08"]
    im = bpy.data.images.load(os.path.join(CH, "tmp_clip", "frame_0001.png"))
    px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    img = np.repeat(np.repeat(px[::-1], 2, axis=0), 2, axis=1)  # haut en premier
    for t in clip.tracking.tracks:
        m = t.markers.find_frame(1)
        if m:
            cx, cy = int(m.co[0] * W * 2), int((1 - m.co[1]) * H * 2)
            for d in range(-6, 7):
                for (yy, xx) in ((cy + d, cx), (cy, cx + d)):
                    if 0 <= yy < img.shape[0] and 0 <= xx < img.shape[1]:
                        img[yy, xx] = (1, 0.2, 0.2)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    tmp = os.path.join(CH, "tmp_clip")
    for d in (tmp,):
        if os.path.isdir(d):
            shutil.rmtree(d)
    render_clip(tmp)
    for sub in ("STARTER_FILES", "COMPLETED_EXAMPLES"):
        dst = os.path.join(CH, sub, "ch11_08_clip")
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(tmp, dst)
    calibrate()
    build("starter", "//ch11_08_clip/")
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_08_tracking_starter.blend"))
    for k, rel in (("short_tracks", "//../ch11_08_clip/"), ("wrong_focal", "//../ch11_08_clip/"), ("not_solved", "//../ch11_08_clip/"), ("few_tracks", "//../ch11_08_clip/")):
        build(k, rel)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_08_tracking_{k}.blend"))
    sketch(os.path.join(out, "ch11_08_tracking_reference.png"))
    build("solution", "//ch11_08_clip/")
    L.save(os.path.join(out, "ch11_08_tracking_solution.blend"))
    shutil.rmtree(tmp)


if __name__ == "__main__":
    L.run(main)
