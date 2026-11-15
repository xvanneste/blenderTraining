"""
build_ch18_13_files.py — « La tasse tombe » : storyboard d'action et d'émotion en 12 cases (CH18.13).
C'est aussi le PROJET OBLIGATOIRE n° 1 de la phase 18 (planche de 12 cases).

  STARTER_FILES/ch18_13_action_starter.blend — gabarit 12 cases (4 × 3), calques USER_Drawing / USER_Arrows.
  COMPLETED_EXAMPLES/ch18_13_action_solution.blend (+ _reference.png) — séquence complète, 12 notes
      normées, en-tête ; rythme : plans courts pendant l'action, longs à l'installation et à la fin.
Usage : blender -b --factory-startup --python build_ch18_13_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_board as B  # noqa: E402
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH18.13 — STORYBOARD D'ACTION ET D'ÉMOTION (12 cases) — projet obligatoire n° 1
Racontez une action courte et lisible avec une émotion (exemple : une tasse tombe, quelqu'un la
rattrape). 12 cases, chacune annotée « SQnnn_SHnnnn · valeur · mouvement · durée ».
Exigences : au moins 5 valeurs de plans différentes dont un insert et un gros plan (ou TGP) ;
au moins 6 traits de flèches ; RYTHME : durée moyenne ≤ 2,5 s, au moins un plan ≤ 1 s et un ≥ 3 s ;
durée totale 10 à 40 s ; en-tête « … Page 01 ».
Vérification : SCRIPTS/validate_ch18_13.py -- --exercise action
"""
NOTES = [("PE", "fixe", 3), ("PM", "fixe", 1.5), ("INS", "fixe", 1), ("GP", "fixe", 0.8), ("INS", "fixe", 0.5),
         ("PA", "panoramique droite", 1), ("TGP", "fixe", 0.7), ("INS", "fixe", 1), ("PRP", "fixe", 2),
         ("PM", "fixe", 2), ("GP", "fixe", 1.5), ("PE", "travelling arrière", 4)]


def cup(d, cx, cz, s, rect, tilt=0.0):
    c, sn = math.cos(tilt), math.sin(tilt)
    pts = [(-0.3, 0.35), (-0.25, -0.35), (0.25, -0.35), (0.3, 0.35)]
    rot = lambda p: (cx + s * (p[0] * c - p[1] * sn), cz + s * (p[0] * sn + p[1] * c))
    G.polyline_clipped(d, [rot(p) for p in pts], rect, 0.01, 0)
    G.polyline_clipped(d, [rot((0.3 * math.cos(t), 0.35 + 0.07 * math.sin(t))) for t in [i * 2 * math.pi / 20 for i in range(21)]], rect, 0.01, 0)


def speed_lines(d, x, z0, z1, n, rect, dx=0.12):
    for i in range(n):
        G.polyline_clipped(d, [(x + (i - n / 2) * dx, z0), (x + (i - n / 2) * dx, z1)], rect, 0.005, 0)


def face(d, cx, cz, r, rect, mood):
    G.polyline_clipped(d, B.ellipse_pts(cx, cz, r, r * 1.1), rect, 0.012, 0)
    eye = {"surprise": 0.16, "worry": 0.1, "joy": 0.06, "shame": 0.07}[mood]
    for sx in (-0.35, 0.35):
        G.polyline_clipped(d, B.ellipse_pts(cx + sx * r, cz + 0.15 * r, 0.12 * r, eye * r, 16), rect, 0.01, 0)
        brow = {"surprise": 0.45, "worry": 0.38, "joy": 0.3, "shame": 0.3}[mood]
        tilt = {"surprise": 0.0, "worry": 0.12 * (1 if sx < 0 else -1), "joy": 0.0, "shame": 0.1 * (1 if sx < 0 else -1)}[mood]
        G.polyline_clipped(d, [(cx + (sx - 0.15) * r, cz + (brow - tilt) * r), (cx + (sx + 0.15) * r, cz + (brow + tilt) * r)], rect, 0.01, 0)
    if mood == "surprise":
        G.polyline_clipped(d, B.ellipse_pts(cx, cz - 0.5 * r, 0.12 * r, 0.18 * r, 16), rect, 0.01, 0)
    else:
        curve = {"worry": 0.12, "joy": -0.2, "shame": 0.0}[mood]
        wobble = 0.05 if mood == "shame" else 0.0       # bouche hésitante (gêne)
        G.polyline_clipped(d, [(cx + 0.3 * r * t, cz - 0.5 * r + curve * r * (1 - t * t) + wobble * r * math.sin(t * 9))
                               for t in [i / 8 - 1 for i in range(17)]], rect, 0.01, 0)
        if mood == "shame":                              # rougeur des joues
            for sx in (-0.55, 0.55):
                for k in range(3):
                    G.polyline_clipped(d, [(cx + sx * r - 0.06 * r + k * 0.06 * r, cz - 0.2 * r), (cx + sx * r + k * 0.06 * r, cz - 0.12 * r)], rect, 0.006, 0)


def draw_solution(d, ar, red, rects):
    for i, (x0, z0, x1, z1) in enumerate(rects):
        w, h = x1 - x0, z1 - z0
        r = (x0, z0, x1, z1)
        cx, cz = x0 + w / 2, z0 + h / 2
        if i == 0:      # PE : A assis à la table, B entre
            G.polyline_clipped(d, [(x0, z0 + 0.12), (x1, z0 + 0.12)], r, 0.006, 0)
            G.polyline_clipped(d, [(cx - 0.3, z0 + 0.42), (cx + 0.3, z0 + 0.42)], r, 0.008, 0)
            B.person(d, cx - 0.45, z0 + 0.12, h * 0.42, r, 1)
            B.person(d, x0 + w * 0.88, z0 + 0.12, h * 0.42, r, -1)
            cup(d, cx + 0.05, z0 + 0.5, 0.12, r)
        elif i == 1:    # PM : B heurte la table
            B.person(d, cx + 0.2, z0 + 0.05, h * 0.9, r, -1, arms=[-60, 200])
            G.polyline_clipped(d, [(x0, z0 + h * 0.35), (cx - 0.1, z0 + h * 0.35)], r, 0.01, 0)
            G.arrow(ar, (cx + 0.75, z0 + h * 0.5), (cx + 0.15, z0 + h * 0.4), 0.01, red, 0.1)
        elif i == 2:    # INS : la tasse glisse vers le bord
            G.polyline_clipped(d, [(x0, cz - 0.3), (cx + 0.5, cz - 0.3), (cx + 0.5, z0)], r, 0.012, 0)
            cup(d, cx + 0.2, cz + 0.05, 0.5, r, 0.15)
            G.arrow(ar, (cx - 0.6, cz - 0.1), (cx - 0.1, cz - 0.1), 0.01, red, 0.1)
        elif i == 3:    # GP : A surpris
            face(d, cx, cz, h * 0.38, r, "surprise")
        elif i == 4:    # INS : la tasse tombe (lignes de vitesse)
            cup(d, cx, cz - 0.05, 0.45, r, 0.6)
            speed_lines(d, cx, cz + 0.3, z1, 5, r)
            G.arrow(ar, (cx + 0.6, z1 - 0.1), (cx + 0.6, cz - 0.3), 0.01, red, 0.1)
        elif i == 5:    # PA : A plonge (corps en diagonale)
            G.polyline_clipped(d, [(x0 + 0.2, z0 + 0.1), (cx + 0.3, cz + 0.2)], r, 0.03, 0)
            G.polyline_clipped(d, B.ellipse_pts(cx + 0.45, cz + 0.32, 0.12, 0.13), r, 0.012, 0)
            G.polyline_clipped(d, [(cx + 0.2, cz + 0.15), (x1 - 0.1, cz - 0.2)], r, 0.015, 0)
            G.arrow(ar, (x0 + 0.3, cz + 0.4), (cx + 0.1, cz + 0.55), 0.01, red, 0.1)
            B.dashed_arrow(ar, (x0 + 0.3, z1 + 0.1), (x1 - 0.3, z1 + 0.1), red, 6, 0.008)
        elif i == 6:    # TGP : les yeux inquiets de B
            for sx in (-0.45, 0.45):
                G.polyline_clipped(d, B.ellipse_pts(cx + sx, cz, 0.25, 0.14, 20), r, 0.012, 0)
                G.polyline_clipped(d, B.ellipse_pts(cx + sx, cz - 0.02, 0.07, 0.07, 12), r, 0.012, 0)
                G.polyline_clipped(d, [(cx + sx - 0.25, cz + 0.22 + (0.08 if sx < 0 else 0)), (cx + sx + 0.25, cz + 0.22 + (0 if sx < 0 else 0.08))], r, 0.012, 0)
        elif i == 7:    # INS : la main rattrape la tasse juste au-dessus du sol
            G.polyline_clipped(d, [(x0, z0 + 0.15), (x1, z0 + 0.15)], r, 0.008, 0)
            cup(d, cx, z0 + 0.6, 0.4, r)
            G.polyline_clipped(d, [(x0, cz - 0.05), (cx - 0.25, z0 + 0.45), (cx + 0.25, z0 + 0.4), (cx + 0.3, z0 + 0.65)], r, 0.012, 0)
            G.arrow(ar, (cx + 0.6, z0 + 0.35), (cx + 0.6, z0 + 0.75), 0.01, red, 0.08)
        elif i == 8:    # PRP : A soulagé (épaules + visage souriant)
            G.polyline_clipped(d, [(cx - h * 0.55, z0), (cx - h * 0.45, z0 + h * 0.45), (cx + h * 0.45, z0 + h * 0.45), (cx + h * 0.55, z0)], r, 0.012, 0)
            face(d, cx, z0 + h * 0.68, h * 0.2, r, "joy")
        elif i == 9:    # PM : A montre la tasse, B rit
            B.person(d, cx - 0.45, z0 + 0.05, h * 0.85, r, 1, arms=[60])
            B.person(d, cx + 0.45, z0 + 0.05, h * 0.85, r, -1)
            cup(d, cx - 0.05, z0 + h * 0.85, 0.15, r)
        elif i == 10:   # GP : B gêné
            face(d, cx, cz, h * 0.38, r, "shame")
        else:           # PE : travelling arrière, ils s'assoient
            G.polyline_clipped(d, [(x0, z0 + 0.12), (x1, z0 + 0.12)], r, 0.006, 0)
            B.person(d, cx - 0.25, z0 + 0.12, h * 0.3, r, 1)
            B.person(d, cx + 0.25, z0 + 0.12, h * 0.3, r, -1)
            for ex, ez in ((cx - 0.15, cz + 0.1), (cx + 0.15, cz + 0.1), (cx - 0.15, cz - 0.15), (cx + 0.15, cz - 0.15)):
                B.dashed_arrow(ar, (ex, ez), (ex + (ex - cx) * 3, ez + (ez - cz) * 2.5), red, 3, 0.008)


def build(sol):
    L.reset("SC_Action")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 7.2, ("GUIDE",), ("USER_Drawing", "USER_Arrows"))
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    red = G.material(ob, "MAT_GP_Arrow", (0.8, 0.15, 0.1))
    ob.data.layers["GUIDE"].lock = False
    rects = B.page(ob, drw["GUIDE"], blue, 4, 3, 2.5, 0.3, 0.45, (-5.45, 3.0), header_z=3.15)
    ob.data.layers["GUIDE"].lock = True
    if sol:
        ink = L.material("MAT_Text", (0.03, 0.03, 0.04), 0.9)
        tcol = L.collection("NOTES")
        draw_solution(drw["USER_Drawing"], drw["USER_Arrows"], red, rects)
        for i, ((x0, z0, x1, z1), (val, mv, dur)) in enumerate(zip(rects, NOTES)):
            body = f"SQ020_SH{(i + 1) * 10:04d} · {val} · {mv} · {str(dur).replace('.', ',')} s"
            B.text(f"TXT_SH{(i + 1) * 10:04d}", body, (x0 + 0.03, 0.0, z0 - 0.3), 0.1, ink, tcol)
        B.text("TXT_Header", "La tasse tombe — SQ020 — Page 01", (-5.45, 0.0, 3.25), 0.17, ink, tcol)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_13_action_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_13_action_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 70
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_13_action_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
