"""
build_ch18_12_files.py — « La planche normée » (CH18.12, cadrage et découpage technique).

  STARTER_FILES/ch18_12_board_starter.blend
      Gabarit GP : 6 cases 16:9 (3 × 2) avec bandeau de notes sous chaque case, calques
      USER_Drawing (dessin) et USER_Arrows (flèches de mouvement), aucun texte.
      Les rectangles des cases sont mémorisés dans la scène (propriété « bcma_panels »).
  COMPLETED_EXAMPLES/ch18_12_board_solution.blend (+ _reference.png)
      Séquence « La tasse » en 6 plans : dessins coupés par les cases, flèches (travelling,
      panoramique, déplacement), 6 annotations normées (objets texte) et un en-tête de page.
Usage : blender -b --factory-startup --python build_ch18_12_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH18.12 — LA PLANCHE NORMÉE (GP_Practice, Num 0)
1. USER_Drawing : dessinez un plan dans chacune des 6 cases (coupé par le bord de la case).
2. USER_Arrows : au moins 3 flèches de mouvement (caméra : travelling, panoramique… ;
   personnage : déplacement). Convention : flèche pleine = personnage, flèche en tirets = caméra.
3. Annotations : Add > Text (Object Mode), Tab pour éditer, une note par case, dans le bandeau
   sous la case, au format :  SQ010_SH0010 · PM · fixe · 3 s
   (code du plan · valeur · mouvement · durée). Renommez-les TXT_SH0010…
4. En-tête : un texte TXT_Header en haut de page : « Projet — SQ010 — Page 01 ».
Vérification : SCRIPTS/validate_ch18_12.py -- --exercise board
"""
NOTES = ["SQ010_SH0010 · PE · fixe · 3 s", "SQ010_SH0020 · PM · travelling avant · 4 s",
         "SQ010_SH0030 · PRP · panoramique droite · 2,5 s", "SQ010_SH0040 · INS · fixe · 1,5 s",
         "SQ010_SH0050 · GP · fixe · 2 s", "SQ010_SH0060 · PE · grue montante · 5 s"]


def text(name, body, loc, size=0.14, mat=None, col=None):
    cu = bpy.data.curves.new(name.replace("TXT_", "FNT_"), "FONT")
    cu.body = body
    cu.size = size
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    ob.rotation_euler = (math.radians(90), 0, 0)        # face à la caméra de la feuille (axe −Y)
    (col or bpy.context.scene.collection).objects.link(ob)
    if mat:
        cu.materials.append(mat)
    return ob


def ell(cx, cz, rx, rz, n=24):
    return [(cx + rx * math.cos(t), cz + rz * math.sin(t)) for t in [i * 2 * math.pi / n for i in range(n + 1)]]


def person(d, x, zf, h, rect, look=1):
    """Silhouette simple (tête, corps, jambes) coupée par la case ; pieds en (x, zf), hauteur h."""
    for poly in (ell(x, zf + h * 0.92, h * 0.07, h * 0.08),
                 [(x - h * 0.12, zf + h * 0.45), (x - h * 0.1, zf + h * 0.82), (x + h * 0.1, zf + h * 0.82), (x + h * 0.12, zf + h * 0.45), (x - h * 0.12, zf + h * 0.45)],
                 [(x - h * 0.06, zf + h * 0.45), (x - h * 0.08, zf)], [(x + h * 0.06, zf + h * 0.45), (x + h * 0.08, zf)],
                 [(x + look * h * 0.02, zf + h * 0.93), (x + look * h * 0.06, zf + h * 0.93)]):
        G.polyline_clipped(d, poly, rect, 0.01, 0)


def dashed(d, a, b, mat, n=7):
    for i in range(n):
        t0, t1 = i / n, (i + 0.55) / n
        G.line(d, (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 0.012, mat)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (1, -1):
        G.line(d, b, (b[0] - 0.15 * math.cos(ang + s * 0.5), b[1] - 0.15 * math.sin(ang + s * 0.5)), 0.012, mat)


def build(sol):
    L.reset("SC_Board")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Drawing", "USER_Arrows"))
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    red = G.material(ob, "MAT_GP_Arrow", (0.8, 0.15, 0.1))
    ob.data.layers["GUIDE"].lock = False
    rects = G.storyboard_page(drw["GUIDE"], cols=3, rows=2, panel_w=3.2, gap=0.5, note_h=0.6,
                              origin=(-5.3, 2.6), radius=0.008, mat=blue)
    G.line(drw["GUIDE"], (-5.6, 2.8), (5.6, 2.8), 0.004, blue)          # ligne d'en-tête
    ob.data.layers["GUIDE"].lock = True
    sc = bpy.context.scene
    sc["bcma_panels"] = json.dumps(rects)
    sc["bcma_note_h"] = 0.6
    if sol:
        ink = L.material("MAT_Text", (0.03, 0.03, 0.04), 0.9)
        tcol = L.collection("NOTES")
        d, ar = drw["USER_Drawing"], drw["USER_Arrows"]
        for i, (x0, z0, x1, z1) in enumerate(rects):
            w, h = x1 - x0, z1 - z0
            r = (x0, z0, x1, z1)
            if i == 0:                                   # PE : A et B petits, table
                person(d, x0 + w * 0.35, z0 + 0.2, h * 0.35, r, 1)
                person(d, x0 + w * 0.65, z0 + 0.2, h * 0.35, r, -1)
                G.polyline_clipped(d, [(x0, z0 + 0.2), (x1, z0 + 0.2)], r, 0.006, 0)
            elif i == 1:                                 # PM + travelling avant (caméra)
                person(d, x0 + w * 0.5, z0 + 0.1, h * 0.85, r, 1)
                for cx, cz in ((x0 + 0.2, z1 - 0.2), (x1 - 0.2, z1 - 0.2), (x0 + 0.2, z0 + 0.2), (x1 - 0.2, z0 + 0.2)):
                    dashed(ar, (cx, cz), (cx + (0.4 if cx < x0 + w / 2 else -0.4), cz + (-0.25 if cz > z0 + h / 2 else 0.25)), red, 3)
            elif i == 2:                                 # PRP + panoramique droite (caméra, au-dessus de la case)
                person(d, x0 + w * 0.6, z0 - h * 0.9, h * 1.75, r, -1)
                dashed(ar, (x0 + 0.3, z1 + 0.15), (x1 - 0.3, z1 + 0.15), red)
            elif i == 3:                                 # insert : main et tasse
                cx, cz = x0 + w / 2, z0 + h / 2
                G.polyline_clipped(d, [(cx - 0.35, cz + 0.45), (cx - 0.3, cz - 0.55), (cx + 0.3, cz - 0.55), (cx + 0.35, cz + 0.45)], r, 0.012, 0)
                G.polyline_clipped(d, ell(cx, cz + 0.45, 0.35, 0.08), r, 0.012, 0)
                G.polyline_clipped(d, [(x0, cz - 0.1), (cx - 0.4, cz - 0.05), (cx - 0.38, cz + 0.2), (x0, cz + 0.25)], r, 0.01, 0)
            elif i == 4:                                 # GP de B + flèche de regard
                person(d, x0 + w * 0.55, z0 - h * 2.6, h * 3.6, r, -1)
            else:                                        # PE final, B part vers la droite (flèche pleine = personnage)
                person(d, x0 + w * 0.45, z0 + 0.2, h * 0.35, r, 1)
                G.arrow(ar, (x0 + w * 0.52, z0 + 0.45), (x0 + w * 0.85, z0 + 0.45), 0.012, red, 0.12)
                G.arrow(ar, (x1 + 0.15, z0 + 0.2), (x1 + 0.15, z1 - 0.2), 0.008, red, 0.1)   # grue montante
            text(f"TXT_SH{(i + 1) * 10:04d}", NOTES[i], (x0 + 0.05, 0.0, z0 - 0.42), 0.14, ink, tcol)
        text("TXT_Header", "Projet La tasse — SQ010 — Page 01", (-5.3, 0.0, 2.9), 0.2, ink, tcol)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_12_board_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_12_board_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_12_board_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
