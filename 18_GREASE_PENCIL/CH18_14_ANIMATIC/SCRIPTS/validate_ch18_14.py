"""
validate_ch18_14.py — Correcteur « Du scénario à l'animatique » (CH18.14).
Usage : … --python-exit-code 1 --python validate_ch18_14.py -- --exercise animatic|layout [--render]
  animatic : liste SHOTLIST → images de début ; une image clé GP (≥ 3 traits) par plan sur USER_Panels,
             dessins différents d'un plan à l'autre ; un marqueur nommé par plan à la bonne image ;
             fin de scène = durée totale ; caméra animée dans le dernier plan ; incrustation Marker/Frame.
  layout   : une caméra par plan liée à son marqueur (bonne image), valeur de plan mesurée
             (bcma_shots.classify) = valeur demandée sur le sujet, règle des 180° (caméras en y < 0).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402

SUBJECTS = {"A": (-1.0, 0.0, 0.0), "B": (1.0, 0.0, 0.0)}


def read_shotlist():
    t = bpy.data.texts.get("SHOTLIST")
    if t is None:
        return []
    rows = []
    for line in t.as_string().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(";")]
        if len(parts) >= 4:
            rows.append((parts[0], parts[1], parts[2], float(parts[3].replace(",", "."))))
    return rows


def starts(rows, fps, first):
    out, f = [], first
    for r in rows:
        out.append(f)
        f += round(r[3] * fps)
    return out, f - 1


def marker_for(sc, code):
    short = code.split("_")[-1]
    return [m for m in sc.timeline_markers if code in m.name or m.name.endswith(short)]


def fcurve_keys(idblock):
    ad = getattr(idblock, "animation_data", None)
    if not ad or not ad.action:
        return []
    keys = []
    act = ad.action
    curves = []
    if hasattr(act, "fcurves"):
        try:
            curves = list(act.fcurves)
        except Exception:
            curves = []
    if not curves and hasattr(act, "layers"):              # actions par couches (Blender ≥ 4.4)
        for lay in act.layers:
            for strip in lay.strips:
                for bag in getattr(strip, "channelbags", []):
                    curves.extend(bag.fcurves)
    for fc in curves:
        keys.append([(k.co.x, k.co.y) for k in fc.keyframe_points])
    return keys


def common(r, sc, rows):
    if not r.check(len(rows) >= 4, f"Liste de plans SHOTLIST lue ({len(rows)} plans)", "Ne supprimez pas le texte SHOTLIST.", 1):
        return None
    fps = sc.render.fps / sc.render.fps_base
    r.check(abs(fps - 24) < 1e-6, f"Cadence {fps:g} i/s (24)", "Output Properties > Format > Frame Rate.", 1)
    st, end = starts(rows, 24, sc.frame_start)
    r.check(sc.frame_end == end, f"Fin de scène {sc.frame_end} (attendu {end} = {sum(x[3] for x in rows):g} s)",
            "Frame Range > End = début + somme des durées × 24 − 1.", 2)
    bad = []
    for (code, *_x), f in zip(rows, st):
        ms = marker_for(sc, code)
        if not any(m.frame == f for m in ms):
            bad.append(f"{code}→{f} (trouvé : {[m.frame for m in ms] or 'aucun'})")
    r.check(not bad, f"Marqueurs nommés aux images de début ({len(rows) - len(bad)}/{len(rows)})",
            "Écarts : " + "; ".join(bad[:4]), 3)
    return st, end


def animatic(r, sc):
    rows = read_shotlist()
    res = common(r, sc, rows)
    if res is None:
        return
    st, end = res
    ob = bpy.data.objects.get("GP_Animatic")
    lay = None
    if ob and ob.type == "GREASEPENCIL":
        lay = next((l for l in ob.data.layers if l.name == "USER_Panels"), None)
    if not r.check(lay is not None, "Calque USER_Panels présent", "Gardez l'objet GP_Animatic du starter.", 1):
        return
    frames = {f.frame_number: f.drawing for f in lay.frames}
    missing = [f for f in st if f not in frames]
    r.check(not missing, f"Une image clé GP au début de chaque plan ({len(st) - len(missing)}/{len(st)})",
            f"Images manquantes : {missing[:6]}", 3)
    thin = [f for f in st if f in frames and len(frames[f].strokes) < 3]
    r.check(not thin and not missing, "Chaque image clé contient un dessin (≥ 3 traits)", f"Trop vides : {thin[:6]}", 2)
    sigs = []
    for f in st:
        d = frames.get(f)
        if d is None:
            continue
        sigs.append((len(d.strokes), round(sum(p.position.x + p.position.z for s in d.strokes for p in s.points), 2)))
    same = sum(1 for a, b in zip(sigs, sigs[1:]) if a == b)
    r.check(same == 0 and sigs, f"Dessins différents d'un plan au suivant ({same} doublon(s))",
            "Chaque plan a son propre dessin.", 2)
    extra = [f for f in frames if f > end]
    r.check(not extra, "Aucune image clé après la fin de la scène", f"Hors durée : {extra[:4]}", 1)
    cam = sc.camera
    moved = False
    if cam is not None:
        for idb in (cam, cam.data):
            for keys in fcurve_keys(idb):
                inside = [v for f, v in keys if st[-1] <= f <= end]
                if len(inside) >= 2 and max(inside) - min(inside) > 1e-4:
                    moved = True
    r.check(moved, "Mouvement de caméra animé dans le dernier plan (≥ 2 clés différentes)",
            "Animez Orthographic Scale (ou la position) de CAM_Sheet entre le début et la fin du dernier plan.", 2)
    rd = sc.render
    r.check(rd.use_stamp and rd.use_stamp_marker and rd.use_stamp_frame,
            "Incrustation Marker + Frame (Burn Into Image)", "Output Properties > Metadata.", 1)
    if L.flag("--render"):
        sc.frame_set(st[len(st) // 2])
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)


def layout(r, sc):
    rows = read_shotlist()
    res = common(r, sc, rows)
    if res is None:
        return
    st, _end = res
    cams, wrong, side = [], [], []
    for (code, value, subj, _d), f in zip(rows, st):
        m = next((m for m in marker_for(sc, code) if m.frame == f), None)
        if m is None or m.camera is None:
            wrong.append(f"{code} : pas de caméra liée")
            continue
        cams.append(m.camera)
        base = SUBJECTS.get(subj.upper())
        got, info = S.classify(sc, m.camera, base) if base else (None, {})
        if got != value:
            cut = info.get("coupe")
            wrong.append(f"{code} : {got or '?'} au lieu de {value} sur {subj} (coupe {cut if cut is None else round(cut, 2)})")
        if m.camera.matrix_world.translation.y >= 0:
            side.append(m.camera.name)
    r.check(len(cams) == len(rows) and len(set(c.name for c in cams)) == len(rows),
            f"Une caméra distincte liée à chaque marqueur ({len(set(c.name for c in cams))}/{len(rows)})",
            "Sélection caméra puis marqueur, Marker > Bind Camera to Markers (Ctrl+B).", 3)
    r.check(not wrong, f"Valeurs de plans conformes à la liste ({len(rows) - len(wrong)}/{len(rows)})",
            " ; ".join(wrong[:4]), 4)
    r.check(cams and not side, "Règle des 180° : caméras du côté y < 0", f"De l'autre côté : {side}", 2)
    if L.flag("--render"):
        sc.frame_set(st[0])
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)


def main():
    ex = L.opt("--exercise", "animatic")
    sc = bpy.context.scene
    r = L.Report(f"CH18.14 — Animatique ({ex})")
    {"animatic": animatic, "layout": layout}[ex](r, sc)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
