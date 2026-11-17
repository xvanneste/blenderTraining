"""
build_ch18_22_files.py — Exemples techniques des 7 projets obligatoires de la phase 18 (CH18.22).

Ces fichiers démontrent la STRUCTURE attendue par le correcteur de chaque projet ; ils réutilisent les
solutions des chapitres (contenu répété ou rallongé) et ne sont PAS des modèles artistiques.
  STARTER_FILES/ch18_22_project_starter.blend  fichier vierge (refusé pour les 7 projets)
  COMPLETED_EXAMPLES/
    ch18_22_p2_dialogue_example.blend   planche de dialogue de 8 cases normées (champ / contrechamp)
    ch18_22_p3_action_example.blend     animatique GP de 30 s, 18 plans (CH18.14 rallongée)
    ch18_22_p4_animatic_example.blend   montage VSE de 60 s, 36 plans, sons, export, notes (CH18.15)
    ch18_22_p5_animation_example.blend  animation GP de 16 s (cycle de marche CH18.17 répété)
    ch18_22_p7_short_example.blend      montage VSE de 3 min, 45 plans, musique, export, notes
  Projets 1 et 6 : les solutions de CH18.13 et CH18.19 servent d'exemples (voir tests.json).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_22_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_board as B  # noqa: E402
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
PH = os.path.dirname(CH)
OUT = os.path.join(CH, "COMPLETED_EXAMPLES")
SRC14 = os.path.join(PH, "CH18_14_ANIMATIC", "COMPLETED_EXAMPLES", "ch18_14_animatic_solution.blend")
SRC15 = os.path.join(PH, "CH18_15_SOUND_EXPORT", "COMPLETED_EXAMPLES", "ch18_15_edit_solution.blend")
SRC17 = os.path.join(PH, "CH18_17_TIMING_CYCLES", "COMPLETED_EXAMPLES", "ch18_17_walk_solution.blend")
PANELS = os.path.join(PH, "CH18_15_SOUND_EXPORT", "ASSETS", "ch18_15_panels")
AUDIO = os.path.join(PH, "CH18_15_SOUND_EXPORT", "ASSETS", "ch18_15_audio")
NOTE = """CH18.22 — PROJETS DE LA PHASE 18
Chaque projet se vérifie avec : SCRIPTS/validate_ch18_22.py -- --exercise p1 … p7
p1 planche 12 cases · p2 dialogue storyboardé (≥ 8 cases) · p3 action 30 s (animatique GP) ·
p4 animatique 1 min (montage son + export) · p5 animation GP 15–30 s · p6 scène hybride 2D/3D ·
p7 storyboard + animatique d'un court de 3–5 min. Voir README et EXERCISES du chapitre.
"""


def starter():
    L.reset("SC_Project")
    L.instructions(NOTE)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_22_project_starter.blend"))


def p2_dialogue():
    L.reset("SC_Dialogue_Board")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Drawing", "USER_Arrows"))
    guide = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    red = G.material(ob, "MAT_GP_Arrow", (0.8, 0.15, 0.1))
    ob.data.layers["GUIDE"].lock = False
    rects = B.page(ob, drw["GUIDE"], guide, 4, 2, 2.5, 0.3, 0.45, (-5.45, 2.6), header_z=2.9)
    ob.data.layers["GUIDE"].lock = True
    d, a = drw["USER_Drawing"], drw["USER_Arrows"]
    ink = L.material("MAT_Text", (0.03, 0.03, 0.04), 0.9)
    plan = [("PE", "fixe", 3), ("PA", "fixe", 2), ("PRP", "fixe", 2.5), ("PRP", "fixe", 2.5),
            ("GP", "fixe", 1.5), ("GP", "fixe", 1.5), ("PRP", "travelling avant", 3), ("PE", "fixe", 3)]
    for i, (x0, z0, x1, z1) in enumerate(rects):
        rect = (x0, z0, x1, z1)
        cx, w, h = (x0 + x1) / 2, x1 - x0, z1 - z0
        val = plan[i][0]
        if val in ("PE", "PA"):
            sc_h = h * (0.45 if val == "PE" else 0.9)
            B.person(d, cx - w * 0.22, z0 + h * 0.1, sc_h, rect, look=1, mat=0)
            B.person(d, cx + w * 0.22, z0 + h * 0.1, sc_h, rect, look=-1, mat=0)
            G.line(d, (x0 + 0.05, z0 + h * 0.1), (x1 - 0.05, z0 + h * 0.1), 0.006, 0)
        else:
            right = i % 2 == 0                    # alternance champ (A, regard à droite) / contrechamp (B)
            big = 3.0 if val == "GP" else 1.6
            head_z = 0.55 if val == "GP" else 0.65            # hauteur du centre de la tête dans la case
            B.person(d, cx + (-1 if right else 1) * w * 0.12, z0 + h * head_z - 0.92 * h * big, h * big, rect,
                     look=1 if right else -1, mat=0)
            G.polyline_clipped(d, B.ellipse_pts(cx + (1 if right else -1) * w * 0.45, z0 + h * 0.35, w * 0.12, h * 0.4), rect, 0.01, 0)
        G.arrow(a, (cx - w * 0.15, z1 - h * 0.12), (cx + w * 0.15, z1 - h * 0.12), 0.01, red)
        code = f"SQ050_SH{(i + 1) * 10:04d}"
        dur = str(plan[i][2]).replace(".", ",")
        B.text(f"TXT_SH{(i + 1) * 10:04d}", f"{code} · {val} · {plan[i][1]} · {dur} s", (x0, -0.02, z0 - 0.3), 0.1, ink)
    B.text("TXT_Header", "La tasse partagée — SQ050 — Page 01", (-5.45, -0.02, 3.05), 0.18, ink)
    L.instructions(NOTE)
    L.save(os.path.join(OUT, "ch18_22_p2_dialogue_example.blend"))


def p3_action():
    bpy.ops.wm.open_mainfile(filepath=SRC14)
    sc = bpy.context.scene
    lay = bpy.data.objects["GP_Animatic"].data.layers["USER_Panels"]
    starts = sorted(m.frame for m in sc.timeline_markers)
    f = sc.frame_end + 1
    for k, src in enumerate(starts[2:8]):                     # 6 plans de plus (dessins réutilisés)
        lay.frames.copy(src, f)
        sc.timeline_markers.new(f"SQ020_SH{(13 + k) * 10:04d}", frame=f)
        f += 44
    sc.frame_end = f - 1                                       # 456 + 6 × 44 = 720 images = 30 s
    L.instructions(NOTE)
    L.save(os.path.join(OUT, "ch18_22_p3_action_example.blend"))


def add_vse_pass(se, start, channel_img, n_frames, prefix):
    files = sorted(os.listdir(PANELS))
    f = start
    for i, name in enumerate(files):
        s = se.strips.new_image(f"{prefix}_{i:02d}", os.path.join(PANELS, name), channel_img, f, fit_method="FIT")
        s.frame_final_duration = n_frames
        f += n_frames
    return f


def p4_animatic():
    bpy.ops.wm.open_mainfile(filepath=SRC15)
    sc = bpy.context.scene
    se = sc.sequence_editor
    f = add_vse_pass(se, 457, 2, 41, "P2")
    f = add_vse_pass(se, f, 2, 41, "P3")
    sc.frame_end = f - 1                                       # 456 + 24 × 41 = 1440 = 60 s
    for k in (1, 2):
        se.strips.new_sound(f"music_{k}", os.path.join(AUDIO, "music_bed.wav"), 5, 1 + 456 * k)
    L.instructions(NOTE)
    L.save(os.path.join(OUT, "ch18_22_p4_animatic_example.blend"))


def p5_animation():
    bpy.ops.wm.open_mainfile(filepath=SRC17)
    sc = bpy.context.scene
    lay = bpy.data.objects["GP_Practice"].data.layers["USER_Walk"]
    base = [fr.frame_number for fr in lay.frames]
    for cyc in range(1, 16):                                   # 16 cycles de 24 images = 16 s
        for f0 in base:
            lay.frames.copy(f0, f0 + 24 * cyc)
    sc.frame_end = 24 * 16
    L.instructions(NOTE)
    L.save(os.path.join(OUT, "ch18_22_p5_animation_example.blend"))


def p7_short():
    sc = L.reset("SC_Short_Edit")
    sc.render.fps, sc.render.fps_base = 24, 1.0
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.view_settings.view_transform = "Standard"
    se = sc.sequence_editor_create()
    f = 1
    for k in range(4):                                         # 4 passages × 12 images (+ 1 plan de fin)
        f = add_vse_pass(se, f, 2, 90 if k < 3 else 94, f"R{k}")
    end_card = se.strips.new_effect("END_Black", "COLOR", 2, f, length=96)
    end_card.color = (0, 0, 0)
    f += 96
    sc.frame_start, sc.frame_end = 1, f - 1                    # 3 × 1080 + 1128 + 96 = 4464 images = 3 min 6 s
    for k in range(10):
        se.strips.new_sound(f"music_{k}", os.path.join(AUDIO, "music_bed.wav"), 5, 1 + 456 * k)
    im = sc.render.image_settings
    im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    ff = sc.render.ffmpeg
    ff.format, ff.codec, ff.audio_codec = "MPEG4", "H264", "AAC"
    L.instructions("# code · image · remarque\nR0_03 · 0300 · plan trop long, couper à 60 images\n"
                   "R1_07 · 1720 · raccord regard à vérifier\nEND_Black · 4400 · ajouter le générique\n", "REVIEW_NOTES")
    L.instructions(NOTE)
    L.save(os.path.join(OUT, "ch18_22_p7_short_example.blend"))


def main():
    starter()
    p2_dialogue()
    p3_action()
    p4_animatic()
    p5_animation()
    p7_short()


if __name__ == "__main__":
    L.run(main)
