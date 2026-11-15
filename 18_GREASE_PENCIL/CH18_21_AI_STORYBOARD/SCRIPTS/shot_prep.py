"""
shot_prep.py — Préparation automatique des plans à partir du texte SHOTLIST (CH18.21).

Écrit avec l'aide d'une IA (Claude), puis relu et testé par le correcteur du chapitre : c'est
l'exemple même d'un outil « assisté et contrôlé ». Il NE vérifie PAS la liste : c'est votre rôle.

Format de SHOTLIST (une ligne par plan, « # » = commentaire) :
    code;valeur;sujet;côté;durée_s;note
    valeur : PE, PM, PA, PRT, PRP, GP, TGP · sujet : A ou B · côté : face (y < 0) ou dos (y > 0)
Pour chaque plan : une caméra CAM_<SHxxxx> cadrée sur le sujet (focale cherchée jusqu'à obtenir la
valeur demandée, mesurée par bcma_shots.classify), un marqueur lié à l'image de début (24 i/s), un
board GP vide (cadre) enfant de la caméra, la note dans la propriété « note » de la caméra.
La fin de scène = somme des durées. Les caméras CAM_SH* existantes sont d'abord supprimées.

Utilisation : Text Editor > shot_prep.py > Run Script (fichier enregistré dans STARTER_FILES), ou
    blender -b fichier.blend --python SCRIPTS/shot_prep.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

import bpy

for base in (os.path.dirname(bpy.data.filepath), os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ""):
    if base:
        p = os.path.normpath(os.path.join(base, "..", "..", "..", "SCRIPTS"))
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)
import bcma_shots as S  # noqa: E402

SUBJECTS = {"A": (-1.0, 0.0, 0.0), "B": (1.0, 0.0, 0.0)}
FACING = {"A": (0.55, -0.83), "B": (-0.55, -0.83)}      # direction caméra depuis le sujet (côté face)
DIST = {"PE": 12.0, "PM": 4.5, "PA": 2.6, "PRT": 1.9, "PRP": 1.4, "GP": 0.9, "TGP": 0.6}
AIM = {"PE": 1.0, "PM": 0.95, "PA": 1.2, "PRT": 1.45, "PRP": 1.58, "GP": 1.62, "TGP": 1.64}


def read_shotlist(text_name="SHOTLIST"):
    rows = []
    t = bpy.data.texts.get(text_name)
    for line in (t.as_string().splitlines() if t else []):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = [x.strip() for x in line.split(";")]
        if len(p) >= 6:
            rows.append({"code": p[0], "value": p[1].upper(), "subject": p[2].upper(), "side": p[3].lower(),
                         "dur": float(p[4].replace(",", ".")), "note": p[5]})
    return rows


def fit_lens(sc, cam, base, value):
    ok = []
    for lens in range(14, 301):
        cam.data.lens = lens
        bpy.context.view_layer.update()
        if S.classify(sc, cam, base)[0] == value:
            ok.append(lens)
    if ok:
        cam.data.lens = ok[0] + min(20, (ok[-1] - ok[0]) // 2)   # milieu de la plage, sans dépasser +20 mm
        return cam.data.lens
    return None


def board(cam, code):
    gp = bpy.data.grease_pencils.new("GPD_BOARD_" + code)
    ob = bpy.data.objects.new("BOARD_" + code, gp)
    col = bpy.data.collections.get("BOARDS") or bpy.data.collections.new("BOARDS")
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    col.objects.link(ob)
    ob.parent = cam
    ob.hide_render = True
    lay = gp.layers.new("Board")
    lay.use_lights = False
    d = lay.frames.new(1).drawing
    w = 0.5 * math.tan(cam.data.angle_x / 2)
    h = w * 9 / 16
    d.add_strokes([5])
    s = d.strokes[0]
    for pt, (x, y) in zip(s.points, [(-w, -h), (w, -h), (w, h), (-w, h), (-w, -h)]):
        pt.position = (x * 0.95, y * 0.95, -0.5)
        pt.radius = 0.0008
    return ob


def build(sc=None):
    sc = sc or bpy.context.scene
    rows = read_shotlist()
    for ob in [o for o in bpy.data.objects if o.name.startswith(("CAM_SH", "BOARD_SH"))]:
        bpy.data.objects.remove(ob, do_unlink=True)
    sc.timeline_markers.clear()
    cams = bpy.data.collections.get("CAMERAS") or bpy.data.collections.new("CAMERAS")
    if cams.name not in sc.collection.children:
        sc.collection.children.link(cams)
    sc.render.fps, sc.render.fps_base = 24, 1.0
    f = sc.frame_start
    report = []
    for r in rows:
        short = r["code"].split("_")[-1]
        cd = bpy.data.cameras.new("CAM_" + short)
        cam = bpy.data.objects.new("CAM_" + short, cd)
        cams.objects.link(cam)
        bx, by, _bz = SUBJECTS.get(r["subject"], SUBJECTS["A"])
        dx, dy = FACING.get(r["subject"], FACING["A"])
        if r["side"] == "dos":
            dy = -dy
        dist = DIST.get(r["value"], 3.0)
        cam.location = (bx + dx * dist, by + dy * dist, 1.55)
        S.look_at(cam, (bx, by, AIM.get(r["value"], 1.2)))
        lens = fit_lens(sc, cam, (bx, by, 0.0), r["value"])
        cam["note"] = r["note"]
        m = sc.timeline_markers.new(r["code"], frame=f)
        m.camera = cam
        board(cam, short)
        report.append(f"{r['code']} {r['value']} {r['subject']} image {f} focale {lens}")
        f += max(1, round(r["dur"] * 24))
    sc.frame_end = f - 1
    first = sc.timeline_markers and min(sc.timeline_markers, key=lambda m: m.frame)
    if first:
        sc.camera = first.camera
    for line in report:
        print("[shot_prep]", line)
    return report


if __name__ == "__main__":
    build()
