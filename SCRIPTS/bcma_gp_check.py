"""
bcma_gp_check.py — Vérificateur générique des exercices Grease Pencil (phase 18).

Chaque chapitre fournit SCRIPTS/gp_spec.json :
{
  "title": "CH18.01 — Formes et volumes",
  "exercises": {
    "volumes": {
      "object": "GP_Practice",
      "layers": {"USER_Boxes": {"min_strokes": 20, "min_points": 200, "min_width": 2.0,
                                "min_frames": 1, "max_frames": null,
                                "hint": "Dessinez 10 boîtes sur le calque USER_Boxes"}},
      "camera": {"name": "CAM_Sheet", "ortho": true},
      "materials_min": 1,
      "fill_layers": ["USER_Values"]          (optionnel : au moins un trait rempli)
      (dans "layers", "min_fills": n exige n traits remplis sur ce calque)
    }
  }
}
Ce que le correcteur PEUT vérifier : présence et quantité de dessin, emplacement, nombre
d'images (animation), remplissages, caméras. Ce qu'il NE PEUT PAS juger : la qualité
artistique — elle s'évalue avec la grille d'auto-évaluation du chapitre.

Usage (dans un validate_ch18_xx.py) :
    import bcma_gp_check as C ; C.main(__file__)
Testé avec : Blender 5.3.0.
"""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402


def check_exercise(r, ex):
    ob = L.obj(ex["object"])
    if not r.check(ob is not None and ob.type == "GREASEPENCIL", f"Objet Grease Pencil {ex['object']} présent",
                   "Ne renommez pas l'objet de dessin.", 1):
        return
    for lname, spec in ex.get("layers", {}).items():
        st = G.layer_stats(ob, lname)
        if not r.check(st is not None, f"Calque {lname} présent", spec.get("hint", ""), 1):
            continue
        frames, strokes, points = st
        r.check(strokes >= spec.get("min_strokes", 1), f"{lname} : {strokes} traits (≥ {spec.get('min_strokes', 1)})",
                spec.get("hint", ""), 2)
        if "min_points" in spec:
            r.check(points >= spec["min_points"], f"{lname} : {points} points (≥ {spec['min_points']})",
                    "Des traits trop courts ou trop peu nombreux : dessinez davantage.", 1)
        if "min_width" in spec or "min_height" in spec:
            bb = G.strokes_bbox(ob, lname)
            w = (bb[1] - bb[0]) if bb else 0
            h = (bb[3] - bb[2]) if bb else 0
            r.check(w >= spec.get("min_width", 0) and h >= spec.get("min_height", 0),
                    f"{lname} : dessin de {w:.1f} × {h:.1f} m (≥ {spec.get('min_width', 0)} × {spec.get('min_height', 0)})",
                    "Utilisez toute la zone de travail indiquée par le cadre.", 1)
        if "min_fills" in spec:
            lay = next((l for l in ob.data.layers if l.name == lname), None)
            nf = 0
            for fr in (lay.frames if lay else []):
                a = fr.drawing.attributes.get("fill_id")
                nf += sum(1 for d in a.data if d.value != 0) if a else 0
            r.check(nf >= spec["min_fills"], f"{lname} : {nf} trait(s) rempli(s) (≥ {spec['min_fills']})",
                    "Outil Fill (clic dans une zone fermée) ou pinceau en mode Fill/Both.", 2)
        if "min_frames" in spec:
            r.check(frames >= spec["min_frames"], f"{lname} : {frames} image(s) clé(s) (≥ {spec['min_frames']})",
                    "Ajoutez des images clés (Dope Sheet / nouvelle image puis dessin).", 2)
    for lname in ex.get("fill_layers", []):
        lay = next((l for l in ob.data.layers if l.name == lname), None)
        filled = False
        if lay:
            for fr in lay.frames:
                a = fr.drawing.attributes.get("fill_id")   # 5.3 : remplissage porté par le trait
                if a and any(d.value != 0 for d in a.data):
                    filled = True
        r.check(filled, f"{lname} : au moins une forme remplie (matériau avec Fill)",
                "Pinceau en mode Fill ou Both (en-tête Draw Mode), outil Fill, ou Edit Mode > Set Stroke Type.", 1)
    if "materials_min" in ex:
        r.check(len(ob.data.materials) >= ex["materials_min"],
                f"{len(ob.data.materials)} matériau(x) GP (≥ {ex['materials_min']})", "Créez des matériaux GP distincts.", 1)
    cam_spec = ex.get("camera")
    if cam_spec:
        cam = L.obj(cam_spec["name"])
        ok = cam is not None and (not cam_spec.get("ortho") or cam.data.type == "ORTHO")
        r.check(ok, f"Caméra {cam_spec['name']} conservée", "Ne supprimez pas la caméra de la feuille.", 1)
    for cname, cspec in ex.get("cameras", {}).items():
        cams = [o for o in bpy.context.scene.objects if o.type == "CAMERA" and o.name.startswith(cname)]
        r.check(len(cams) >= cspec.get("min", 1), f"{len(cams)} caméra(s) {cname}* (≥ {cspec.get('min', 1)})",
                cspec.get("hint", ""), 2)
    for mname, mspec in ex.get("markers", {}).items():
        mk = [m for m in bpy.context.scene.timeline_markers if m.name.startswith(mname)]
        r.check(len(mk) >= mspec.get("min", 1), f"{len(mk)} marqueur(s) {mname}* (≥ {mspec.get('min', 1)})",
                mspec.get("hint", ""), 2)
        if mspec.get("bound"):
            r.check(all(m.camera is not None for m in mk) and mk, "Marqueurs liés à des caméras (Ctrl+B)",
                    "Timeline : sélectionnez caméra + marqueur, Marker > Bind Camera to Markers.", 2)


def main(validator_file):
    sdir = os.path.dirname(os.path.abspath(validator_file))
    spec = json.load(open(os.path.join(sdir, "gp_spec.json"), encoding="utf-8"))
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ex_name = argv[argv.index("--exercise") + 1] if "--exercise" in argv else next(iter(spec["exercises"]))
    r = L.Report(f"{spec['title']} — {ex_name}")
    check_exercise(r, spec["exercises"][ex_name])
    if "--render" in argv:
        lum = L.quick_render(15, 8)
        r.check(0.05 < lum, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()
