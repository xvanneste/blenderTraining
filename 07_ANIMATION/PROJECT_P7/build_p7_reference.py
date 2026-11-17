"""
build_p7_reference.py — Produit la RÉFÉRENCE du projet P7 « Une scène animée » (16,7 s : jeu d'acteur, dialogue, deux caméras).

La référence ASSEMBLE les résultats des chapitres de la phase :
  - le mannequin (CHR_Mannequin, RIG_Mannequin) et l'action de jeu d'acteur de CH07.10 (72 images : idle, remarque, maintien, anticipation) ;
  - le cycle de marche de CH07.08 (24 images) et le saut de CH07.09 (40 images) ;
  - le montage NLA de CH07.13 : cinq strips sur deux pistes alternées (ACTING 1–73, WALK ×6 de 67 à 211, JUMP 205–245, ACTING 239–311, WALK ×4 305–401), chaque strip en fondu d'entrée de 6 images sur la fin du précédent ; plage 1–401 à 24 i/s (16,7 s) ;
  - deux caméras (CH07.12) : CAM_A (travelling avant lent, Track To) et CAM_B (plan de côté, objectif 40 mm, Track To, léger Noise), avec des MARQUEURS LIÉS aux caméras (coupe à l'image 201) ;
  - le dialogue : texte DIALOGUE (deux répliques) et marqueurs line_1 (image 14) et line_2 (image 253), alignés sur la remarque du personnage (la tête tourne 7 images après le début de la réplique) ;
  - la planche renders/p7_contact_sheet.png : quatre images (14, 100, 225, 330) rendues par la caméra active (EEVEE, 480 × 270), côte à côte (1 920 px de large).
Sources : COMPLETED_EXAMPLES des chapitres CH07.08, CH07.09 et CH07.10 (regénérez-les d'abord si vous les modifiez).
Limites (dites) : le mannequin marche SUR PLACE et reste au même endroit ; pas de lip sync ; pas de décor ; la qualité artistique du plan n'est pas jugée.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p7_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

OUT = os.path.join(HERE, "REFERENCE")
CH = os.path.join(HERE, "..")
SRC_ACT = os.path.join(CH, "CH07_10_ACTING", "COMPLETED_EXAMPLES", "ch07_10_acting_solution.blend")
SRC_WALK = os.path.join(CH, "CH07_08_WALK", "COMPLETED_EXAMPLES", "ch07_08_walk_solution.blend")
SRC_JUMP = os.path.join(CH, "CH07_09_RUN_JUMP", "COMPLETED_EXAMPLES", "ch07_09_jump_solution.blend")
DIALOGUE = [(14, "Tiens, qu'est-ce que c'est ?"), (253, "Je crois qu'on peut y aller.")]
SHEET_FRAMES = (14, 100, 225, 330)


def load_actions(path, name, objects=False):
    before = set(bpy.data.actions)
    with bpy.data.libraries.load(os.path.abspath(path), link=False) as (src, dst):
        dst.actions = list(src.actions)
        if objects:
            dst.objects = ["CHR_Mannequin", "RIG_Mannequin"]
    new = [a for a in bpy.data.actions if a not in before]
    act = new[0]
    act.name = name
    act.use_fake_user = True
    return act


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = "SC_P7"
    sc.render.fps = 24
    act_a = load_actions(SRC_ACT, "ACT_acting", objects=True)
    act_w = load_actions(SRC_WALK, "ACT_walk")
    act_j = load_actions(SRC_JUMP, "ACT_jump")
    for o in ("CHR_Mannequin", "RIG_Mannequin"):
        sc.collection.objects.link(bpy.data.objects[o])
    rig, body = bpy.data.objects["RIG_Mannequin"], bpy.data.objects["CHR_Mannequin"]
    body.parent = rig
    for n in rig.pose.bones.keys():
        rig.pose.bones[n].rotation_mode = "XYZ"
    ad = rig.animation_data_create()
    ad.action = None
    t1, t2 = ad.nla_tracks.new(), ad.nla_tracks.new()
    t1.name, t2.name = "T1", "T2"
    plan = [(t1, "ACTING_1", 1, act_a, 1, 0), (t2, "WALK_1", 67, act_w, 6, 6), (t1, "JUMP", 205, act_j, 1, 6), (t2, "ACTING_2", 239, act_a, 1, 6), (t1, "WALK_2", 305, act_w, 4, 6)]
    for tr, name, start, act, rep, bi in plan:
        s = tr.strips.new(name, start, act)
        s.repeat = rep
        s.blend_in = float(bi)
    sc.frame_start, sc.frame_end = 1, 401
    # scène : sol, lumières, cible de visée
    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "GEO_Floor"
    tgt = bpy.data.objects.new("EMP_Target", None)
    tgt.location = (0, 0, 1.0)
    sc.collection.objects.link(tgt)
    sd = bpy.data.lights.new("LGT_Sun", "SUN")
    sd.energy = 3.0
    sun = bpy.data.objects.new("LGT_Sun", sd)
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))
    sc.collection.objects.link(sun)
    sc.world = bpy.data.worlds.new("W")
    sc.world.color = (0.35, 0.37, 0.4)

    def camera(name, loc0, loc1, f0, f1, lens, noise=0.0):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        cd.clip_end = 100
        cam = bpy.data.objects.new(name, cd)
        sc.collection.objects.link(cam)
        for f, p in ((f0, loc0), (f1, loc1)):
            cam.location = p
            cam.keyframe_insert("location", frame=f)
        c = cam.constraints.new("TRACK_TO")
        c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
        if noise:
            for fc in L.fcurves(cam.animation_data.action) if hasattr(L, "fcurves") else []:
                pass
            act = cam.animation_data.action
            try:
                fcs = list(act.fcurves)
            except AttributeError:
                fcs = [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]
            for fc in fcs:
                if fc.array_index in (0, 2):
                    m = fc.modifiers.new("NOISE")
                    m.scale, m.strength, m.phase = 8.0, noise, 1.0 + 3.0 * fc.array_index
        return cam
    cam_a = camera("CAM_A", Vector((0.4, -6.0, 1.4)), Vector((0.2, -4.4, 1.4)), 1, 200, 35)
    cam_b = camera("CAM_B", Vector((1.6, -4.6, 1.3)), Vector((1.2, -4.0, 1.3)), 201, 401, 40, noise=0.08)
    for name, f, cam in (("cam_A", 1, cam_a), ("cam_B", 201, cam_b)):
        m = sc.timeline_markers.new(name, frame=f)
        m.camera = cam
    sc.camera = cam_a
    txt = bpy.data.texts.new("DIALOGUE")
    txt.write("\n".join(f"image {f} : {t}" for f, t in DIALOGUE) + "\n")
    txt.use_fake_user = True
    for i, (f, t) in enumerate(DIALOGUE, 1):
        sc.timeline_markers.new(f"line_{i}", frame=f)
    # planche de contact
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 480, 270, 100
    sc.render.image_settings.file_format = "PNG"
    tiles = []
    for f in SHEET_FRAMES:
        sc.frame_set(f)
        path = os.path.join(OUT, "renders", f"_tmp_{f}.png")
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(path)
        tiles.append(np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], 4))
        bpy.data.images.remove(img)
        os.remove(path)
    sheet = np.concatenate(tiles, axis=1)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0], alpha=False)
    out.pixels = sheet.ravel()
    out.filepath_raw = os.path.join(OUT, "renders", "p7_contact_sheet.png")
    out.file_format = "PNG"
    out.save()
    sc.frame_set(1)
    L.instructions("P7 — scène de référence : voir build_p7_reference.py.")
    L.save(os.path.join(OUT, "p7_scene_reference.blend"))


if __name__ == "__main__":
    L.run(main)
