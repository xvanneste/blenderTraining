"""
validate_ch18_12.py — Correcteur de « La planche normée » (CH18.12).
Usage : … --python-exit-code 1 --python validate_ch18_12.py -- --exercise board [--render]
Vérifie : dessin dans chacune des 6 cases, ≥ 3 flèches, 6 annotations conformes à la norme
« SQnnn_SHnnnn · valeur · mouvement · durée » placées sous des cases différentes, un en-tête de page.
Testé avec : Blender 5.3.0.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CODE = re.compile(r"SQ\d{3}_SH\d{4}")
VALUE = re.compile(r"\b(PE|PM|PA|PRT|PRP|GP|TGP|INS)\b")
MOVE = re.compile(r"(fixe|pano|travelling|zoom|grue|steadicam|épaule|tilt|dolly)", re.I)
DUR = re.compile(r"\d+(?:[.,]\d+)?\s?s\b")


def main():
    r = L.Report("CH18.12 — La planche normée")
    sc = bpy.context.scene
    ob = L.obj("GP_Practice")
    rects = json.loads(sc.get("bcma_panels", "[]"))
    note_h = float(sc.get("bcma_note_h", 0.6))
    if not r.check(ob is not None and len(rects) == 6, "Gabarit de planche (6 cases) présent", "Repartez du starter.", 1):
        return r.finish()
    lay = {l.name: l for l in ob.data.layers}
    counts = [0] * 6
    if "USER_Drawing" in lay:
        for fr in lay["USER_Drawing"].frames:
            for s in fr.drawing.strokes:
                xs = [p.position.x for p in s.points]; zs = [p.position.z for p in s.points]
                cx, cz = sum(xs) / len(xs), sum(zs) / len(zs)
                for i, (x0, z0, x1, z1) in enumerate(rects):
                    if x0 <= cx <= x1 and z0 <= cz <= z1:
                        counts[i] += 1
    r.check(all(c >= 3 for c in counts), f"Dessin dans chaque case (traits par case : {counts} ; ≥ 3)",
            "Calque USER_Drawing : remplissez les 6 cases.", 3)
    na = sum(len(fr.drawing.strokes) for fr in lay["USER_Arrows"].frames) if "USER_Arrows" in lay else 0
    r.check(na >= 3, f"{na} trait(s) de flèches sur USER_Arrows (≥ 3)", "Flèches de mouvement caméra/personnage.", 2)
    texts = [o for o in bpy.data.objects if o.type == "FONT"]
    notes, used = [], set()
    for t in texts:
        body = t.data.body
        if CODE.search(body):
            x, z = t.matrix_world.translation.x, t.matrix_world.translation.z
            panel = next((i for i, (x0, z0, x1, z1) in enumerate(rects) if x0 - 0.2 <= x <= x1 and z0 - note_h - 0.05 <= z <= z0), None)
            ok = bool(VALUE.search(body) and MOVE.search(body) and DUR.search(body))
            notes.append((t.name, ok, panel))
            if ok and panel is not None:
                used.add(panel)
    r.check(len(notes) >= 6, f"{len(notes)} annotation(s) avec un code SQnnn_SHnnnn (≥ 6)", "Add > Text ; format SQ010_SH0010.", 2)
    bad = [n for n, ok, _ in notes if not ok]
    r.check(notes and not bad, "Annotations complètes : valeur · mouvement · durée" + (f" (incomplètes : {', '.join(bad)})" if bad else ""),
            "Ex. : SQ010_SH0020 · PM · travelling avant · 4 s", 3)
    r.check(len(used) >= 6, f"Une annotation sous chaque case ({len(used)}/6)", "Placez chaque texte dans le bandeau sous sa case.", 2)
    header = [t for t in texts if re.search(r"page\s*\d+", t.data.body, re.I)]
    r.check(header, "En-tête de page (« … Page 01 »)", "Un texte en haut de la planche avec le numéro de page.", 1)
    codes = sorted(CODE.search(t.data.body).group(0) for t in texts if CODE.search(t.data.body))
    r.check(codes == sorted(set(codes)), "Codes de plans uniques", "Chaque plan a son propre numéro.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
