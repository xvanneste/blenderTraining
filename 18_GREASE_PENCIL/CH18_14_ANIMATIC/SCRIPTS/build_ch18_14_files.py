"""
build_ch18_14_files.py — « Du scénario à l'animatique » (CH18.14, phase 18 module D).

  STARTER_FILES/ch18_14_animatic_starter.blend
      Feuille 16:9 (12 × 6,75 m, caméra orthographique CAM_Sheet), calque USER_Panels vide,
      liste de plans dans le texte interne SHOTLIST (code;valeur;mouvement;durée en s),
      scène à 24 i/s mais fin à 250, aucun marqueur, aucune animation de caméra.
  COMPLETED_EXAMPLES/ch18_14_animatic_solution.blend (+ _contact.png)
      Les 12 cases de la planche CH18.13 (« La tasse tombe ») recopiées, agrandies, une image clé
      GP par plan (dessin tenu jusqu'au plan suivant), 12 marqueurs SQ020_SH0010…, fin de scène
      = durée totale (456 images = 19 s), zoom arrière animé (ortho_scale) dans le dernier plan,
      incrustation (Metadata > Burn Into Image : Marker, Frame).
  STARTER_FILES/ch18_14_layout_starter.blend
      Décor de dialogue de CH18.11 (A à gauche, B à droite), aucune caméra ni marqueur,
      liste de plans SHOTLIST (code;valeur;sujet;durée).
  COMPLETED_EXAMPLES/ch18_14_layout_solution.blend (+ _contact.png)
      6 caméras dont la valeur de plan mesurée (bcma_shots.classify) correspond à la liste,
      6 marqueurs liés aux caméras aux images calculées depuis les durées.
Dépend de : COMPLETED_EXAMPLES de CH18.13 (planche source) et du script de CH18.11 (décor).
Usage : blender -b --factory-startup --python build_ch18_14_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
PHASE = os.path.dirname(CH)
SRC_BOARD = os.path.join(PHASE, "CH18_13_COMPLEX_BOARDS", "COMPLETED_EXAMPLES", "ch18_13_action_solution.blend")
SRC_SET = os.path.join(PHASE, "CH18_11_CONTINUITY", "SCRIPTS", "build_ch18_11_files.py")
FPS = 24

ANIM_SHOTS = [("SQ020_SH0010", "PE", "fixe", 3), ("SQ020_SH0020", "PM", "fixe", 1.5),
              ("SQ020_SH0030", "INS", "fixe", 1), ("SQ020_SH0040", "GP", "fixe", 0.8),
              ("SQ020_SH0050", "INS", "fixe", 0.5), ("SQ020_SH0060", "PA", "pano", 1),
              ("SQ020_SH0070", "TGP", "fixe", 0.7), ("SQ020_SH0080", "INS", "fixe", 1),
              ("SQ020_SH0090", "PRP", "fixe", 2), ("SQ020_SH0100", "PM", "fixe", 2),
              ("SQ020_SH0110", "GP", "fixe", 1.5), ("SQ020_SH0120", "PE", "travelling arrière", 4)]

LAYOUT_SHOTS = [("SQ030_SH0010", "PE", "A", 3), ("SQ030_SH0020", "PM", "A", 2),
                ("SQ030_SH0030", "PRP", "B", 2), ("SQ030_SH0040", "PRP", "A", 2),
                ("SQ030_SH0050", "GP", "B", 1.5), ("SQ030_SH0060", "PE", "B", 3)]
A, B = (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)
# position de la caméra, point visé, plage de focales cherchée pour la valeur voulue
LAYOUT_CAMS = [((0.0, -14.0, 1.6), (0.0, 0.0, 1.0)), ((0.6, -3.6, 1.2), (-1.0, 0.0, 0.9)),
               ((-0.2, -1.9, 1.6), (1.0, 0.0, 1.55)), ((0.2, -1.9, 1.6), (-1.0, 0.0, 1.55)),
               ((0.35, -1.0, 1.62), (1.0, 0.0, 1.62)), ((3.0, -13.0, 2.2), (0.5, 0.0, 1.0))]

NOTE_ANIM = """CH18.14 — L'ANIMATIQUE IMAGE PAR IMAGE (GP_Animatic, Num 0)
La liste de plans est dans le texte SHOTLIST (code;valeur;mouvement;durée en secondes).
1. Durées → images : à 24 i/s, image de début du plan n = 1 + somme des durées précédentes × 24
   (arrondies). Exemple : 3 s = 72 images, donc SH0020 commence à l'image 73.
2. Calque USER_Panels : à l'image de début de CHAQUE plan, une image clé (dessin du plan, ≥ 3 traits).
   Le dessin est tenu jusqu'à l'image clé suivante. Astuce : partez de votre planche CH18.13.
3. Timeline : un marqueur (M) par plan, à son image de début, renommé (F2) avec son code SQ020_SH0010…
4. Output Properties > Frame Range : End = durée totale en images.
5. Dernier plan (travelling arrière) : animez la caméra CAM_Sheet (Orthographic Scale, I sur le champ)
   entre le début et la fin du plan.
6. Output Properties > Metadata : cochez Marker et Frame, puis Burn Into Image.
Vérification : SCRIPTS/validate_ch18_14.py -- --exercise animatic
"""
NOTE_LAYOUT = """CH18.14 — L'ANIMATIQUE 3D À CAMÉRAS MULTIPLES
Liste de plans : texte SHOTLIST (code;valeur;sujet;durée en s). A = rouge (gauche), B = bleu (droite).
1. Une caméra par plan (CAM_SH0010…), cadrée sur le SUJET avec la valeur demandée
   (PE, PM, PRP, GP : repères de CH18.10 ; le correcteur mesure la coupe).
2. Règle des 180° : toutes les caméras du côté y < 0 (devant la table).
3. Timeline : un marqueur par plan à son image de début (calculée depuis les durées, à 24 i/s),
   lié à sa caméra : sélectionnez la caméra, puis le marqueur, Marker > Bind Camera to Markers (Ctrl+B).
4. Frame Range : End = durée totale en images.
Vérification : SCRIPTS/validate_ch18_14.py -- --exercise layout
"""


def stamp(sc, camera=False):
    """Incrustation : seulement Marker, Frame (et Camera) ; les autres champs, cochés par défaut, décochés."""
    r = sc.render
    for k in dir(r):
        if k.startswith("use_stamp_") and k not in ("use_stamp_labels",):
            setattr(r, k, False)
    r.use_stamp = True
    r.use_stamp_marker = r.use_stamp_frame = True
    r.use_stamp_camera = camera
    r.stamp_font_size = 22


def starts(shots, fps=FPS):
    out, f = [], 1
    for s in shots:
        out.append(f)
        f += round(s[3] * fps)
    return out, f - 1


def shotlist(lines, header):
    t = L.instructions(header + "\n" + "\n".join(";".join(str(x) for x in s) for s in lines) + "\n", "SHOTLIST")
    return t


def harvest_board():
    """Lit les traits de la planche CH18.13, rangés par case (centre du trait dans la case)."""
    bpy.ops.wm.open_mainfile(filepath=SRC_BOARD)
    sc = bpy.context.scene
    rects = json.loads(sc["bcma_panels"])
    ob = bpy.data.objects["GP_Practice"]
    mats = [(m.name, tuple(m.grease_pencil.color[:3])) for m in ob.data.materials]
    panels = [[] for _ in rects]
    for lay in ob.data.layers:
        if lay.name not in ("USER_Drawing", "USER_Arrows"):
            continue
        for fr in lay.frames:
            for s in fr.drawing.strokes:
                pts = [(p.position.x, p.position.z) for p in s.points]
                cx, cz = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
                for i, (x0, z0, x1, z1) in enumerate(rects):
                    if x0 <= cx <= x1 and z0 <= cz <= z1:
                        panels[i].append({"pts": pts, "r": [p.radius for p in s.points],
                                          "mat": mats[s.material_index], "cyclic": s.cyclic})
                        break
    return rects, panels


def animatic(sol, rects=None, panels=None):
    L.reset("SC_Animatic")
    ob, cam, drw = G.sheet("GP_Animatic", 12.0, 6.75, ("GUIDE",), ("USER_Panels",))
    guide = G.material(ob, "MAT_GP_Guide", (0.6, 0.6, 0.65))
    ob.data.layers["GUIDE"].lock = False
    G.rect(drw["GUIDE"], -5.98, -3.36, 5.98, 3.36, 0.01, guide)       # bord du cadre 16:9
    ob.data.layers["GUIDE"].lock = True
    sc = bpy.context.scene
    sc.render.fps, sc.render.fps_base = FPS, 1.0
    sc.frame_start, sc.frame_end = 1, 250
    shotlist(ANIM_SHOTS, "# code;valeur;mouvement;durée_s")
    st, end = starts(ANIM_SHOTS)
    if sol:
        for i, (code, *_r) in enumerate(ANIM_SHOTS):
            x0, z0, x1, z1 = rects[i]
            cx, cz, k = (x0 + x1) / 2, (z0 + z1) / 2, 11.96 / (x1 - x0)
            d = G.layer(ob, "USER_Panels", frame=st[i])
            for s in panels[i]:
                mi = G.material(ob, s["mat"][0], s["mat"][1])
                pts = [((x - cx) * k, (z - cz) * k) for x, z in s["pts"]]
                st_ = G.polyline(d, pts, 1.0, mi, cyclic=s["cyclic"], fill=False)
                for p, r in zip(st_.points, s["r"]):
                    p.radius = r * k * 0.55
            sc.timeline_markers.new(code, frame=st[i])
        sc.frame_end = end
        last = st[-1]
        cam.data.ortho_scale = 10.0
        cam.data.keyframe_insert("ortho_scale", frame=last)
        cam.data.ortho_scale = 12.0
        cam.data.keyframe_insert("ortho_scale", frame=end)
        stamp(sc)
    sc.frame_set(1)
    L.instructions(NOTE_ANIM)
    return sc


def load_set_builder():
    spec = importlib.util.spec_from_file_location("b1811", SRC_SET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fit_lens(sc, cam, base, value):
    """Cherche la focale (18–300 mm) qui donne la valeur voulue, au milieu de la plage trouvée."""
    ok = []
    for lens in range(18, 301):
        cam.data.lens = lens
        bpy.context.view_layer.update()
        if S.classify(sc, cam, base)[0] == value:
            ok.append(lens)
    if not ok:
        raise RuntimeError(f"aucune focale ne donne {value} pour {cam.name}")
    cam.data.lens = ok[len(ok) // 2]
    return cam.data.lens


def layout(sol, mod):
    sc = mod.scene(False)
    sc.name = "SC_Layout"
    sc.render.fps, sc.render.fps_base = FPS, 1.0
    sc.frame_start, sc.frame_end = 1, 288
    shotlist(LAYOUT_SHOTS, "# code;valeur;sujet;durée_s")
    st, end = starts(LAYOUT_SHOTS)
    if sol:
        cam_c = L.collection("CAMERAS")
        for i, (code, value, subj, _d) in enumerate(LAYOUT_SHOTS):
            loc, tgt = LAYOUT_CAMS[i]
            c = L.camera("CAM_" + code.split("_")[1], cam_c, loc, 50, make_active=False)
            S.look_at(c, tgt)
            lens = fit_lens(sc, c, A if subj == "A" else B, value)
            print(f"[BCMA] {c.name} {value} sur {subj} : focale {lens} mm")
            m = sc.timeline_markers.new(code, frame=st[i])
            m.camera = c
        sc.frame_end = end
        sc.camera = L.obj("CAM_SH0010")
        stamp(sc, camera=True)
    sc.frame_set(1)
    L.instructions(NOTE_LAYOUT)
    return sc


def contact(sc, frames, cols, out, percent=25):
    sc.render.resolution_percentage = percent
    W = sc.render.resolution_x * percent // 100
    H = sc.render.resolution_y * percent // 100
    rows = math.ceil(len(frames) / cols)
    sheet = np.full((rows * H, cols * W, 4), 0.1, dtype=np.float32)
    sheet[..., 3] = 1.0
    for i, f in enumerate(frames):
        sc.frame_set(f)
        p = os.path.join(bpy.app.tempdir, f"anim_{f}.png")
        sc.render.filepath = p
        sc.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
        r, c = i // cols, i % cols
        y0 = (rows - 1 - r) * H                     # les images Blender commencent en bas
        sheet[y0:y0 + H, c * W:(c + 1) * W] = px
    img = bpy.data.images.new("contact", cols * W, rows * H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    print(f"[BCMA] contact {out}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    rects, panels = harvest_board()
    print("[BCMA] traits par case :", [len(p) for p in panels])
    animatic(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_14_animatic_starter.blend"))
    sc = animatic(True, rects, panels)
    L.save(os.path.join(out, "ch18_14_animatic_solution.blend"))
    st, end = starts(ANIM_SHOTS)
    mids = [s + (round(d[3] * FPS) // 2) for s, d in zip(st, ANIM_SHOTS)]
    mids[-1] = end                                   # fin du zoom arrière
    contact(sc, mids, 4, os.path.join(out, "ch18_14_animatic_contact.png"))
    mod = load_set_builder()
    layout(False, mod)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_14_layout_starter.blend"))
    sc = layout(True, mod)
    L.save(os.path.join(out, "ch18_14_layout_solution.blend"))
    st, _e = starts(LAYOUT_SHOTS)
    contact(sc, [s + 1 for s in st], 3, os.path.join(out, "ch18_14_layout_contact.png"))


if __name__ == "__main__":
    L.run(main)
