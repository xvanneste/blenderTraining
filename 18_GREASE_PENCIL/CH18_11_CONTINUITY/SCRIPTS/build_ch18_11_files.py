"""
build_ch18_11_files.py — « Le dialogue découpé » (CH18.11, continuité et dialogue).

  STARTER_FILES/ch18_11_dialogue_starter.blend
      CHR_A (x = −1, regarde +X) et CHR_B (x = +1, regarde −X) se font face ; table et tasse entre
      eux ; aucune caméra de plan, aucun marqueur. Scène de 288 images (12 s à 24 i/s).
  STARTER_FILES/ch18_11_board_starter.blend : planche GP de 6 cases (découpage dessiné).
  COMPLETED_EXAMPLES/ch18_11_dialogue_solution.blend (+ _contact.png) :
      6 caméras SH010–SH060 (master, amorce sur B, amorce sur A, plan serré B, plan serré A, insert),
      toutes du même côté de l'axe ; 6 marqueurs liés aux caméras (Bind Camera to Markers).
  COMPLETED_EXAMPLES/ch18_11_board_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python build_ch18_11_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
A, B = (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)
NOTE = """CH18.11 — LE DIALOGUE DÉCOUPÉ
A (rouge, gauche) et B (bleu, droite) se parlent. Découpez la scène en au moins 6 plans :
1. Créez 6 caméras CAM_SH010 … CAM_SH060 : un plan d'ensemble (master) qui montre A et B,
   une amorce sur B (épaule de A au premier plan), une amorce sur A, un plan serré sur B,
   un plan serré sur A, un insert sur la tasse.
2. RÈGLE DES 180° : toutes les caméras du MÊME CÔTÉ de la ligne A–B (ici y < 0).
3. Continuité des regards : A toujours dans la moitié GAUCHE de l'image, B dans la moitié DROITE.
4. Timeline : ajoutez 6 marqueurs (M) nommés SH010…SH060, espacés d'au moins 24 images ;
   pour chacun, sélectionnez la caméra puis le marqueur : Marker > Bind Camera to Markers (Ctrl+B).
Vérification : SCRIPTS/validate_ch18_11.py -- --exercise dialogue
"""
NOTE_BOARD = """CH18.11 — DÉCOUPAGE DESSINÉ (GP_Practice, calque USER_Board)
Dessinez les 6 plans de votre découpage dans les 6 cases (A à gauche, B à droite, toujours),
avec une flèche de regard dans chaque case. Vérification : -- --exercise board
"""
SHOTS = [  # nom, position caméra, point visé, focale, image du marqueur
    ("CAM_SH010", (0.0, -6.5, 1.6), (0.0, 0.0, 1.1), 35, 1),
    ("CAM_SH020", (-1.75, -0.95, 1.65), (0.7, 0.0, 1.5), 50, 49),
    ("CAM_SH030", (1.75, -0.95, 1.65), (-0.7, 0.0, 1.5), 50, 97),
    ("CAM_SH040", (-0.2, -1.9, 1.6), (0.72, 0.0, 1.55), 50, 145),
    ("CAM_SH050", (0.2, -1.9, 1.6), (-0.72, 0.0, 1.55), 50, 193),
    ("CAM_SH060", (0.0, -0.55, 0.92), (0.0, -0.3, 0.8), 50, 241),
]


def scene(sol):
    L.reset("SC_Dialogue")
    set_c, chr_c, cam_c, lgt_c = (L.collection(n) for n in ("SET", "CHARACTERS", "CAMERAS", "LIGHTS"))
    L.plane("GEO_Floor", set_c, L.material("MAT_Floor", (0.35, 0.33, 0.3), 0.8), size=60)
    L.cube("GEO_Wall", set_c, L.material("MAT_Wall", (0.62, 0.6, 0.55), 0.9), size=1, location=(0, 4, 3), scale=(30, 0.2, 6))
    a = S.mannequin_mesh("CHR_A", chr_c, A, L.material("MAT_A", (0.75, 0.3, 0.2), 0.6))
    b = S.mannequin_mesh("CHR_B", chr_c, B, L.material("MAT_B", (0.2, 0.4, 0.75), 0.6))
    a.rotation_euler.z = math.radians(90)      # regarde +X (vers B)
    b.rotation_euler.z = math.radians(-90)     # regarde −X (vers A)
    wood = L.material("MAT_Wood", (0.45, 0.28, 0.14), 0.6)
    L.cube("GEO_Table", set_c, wood, size=1, location=(0, -0.3, 0.375), scale=(0.7, 0.5, 0.75))
    L.cylinder("PROP_Cup", set_c, L.material("MAT_Cup", (0.9, 0.9, 0.85), 0.3), radius=0.045, depth=0.1, location=(0, -0.3, 0.8))
    L.light("LGT_Sun", lgt_c, "SUN", (0, -4, 6), 3.5, rotation=(50, 0, 25))
    L.world((0.5, 0.55, 0.62), 0.8, "WO_Studio")
    sc = L.render_defaults("BLENDER_EEVEE", 25)
    sc.frame_start, sc.frame_end = 1, 288
    sc.render.fps = 24
    if sol:
        for name, loc, tgt, lens, frame in SHOTS:
            c = L.camera(name, cam_c, loc, lens, make_active=False)
            S.look_at(c, tgt)
            m = sc.timeline_markers.new(name.replace("CAM_", ""), frame=frame)
            m.camera = c
        sc.camera = L.obj("CAM_SH010")
    L.instructions(NOTE)
    return sc


def board(sol):
    L.reset("SC_Board")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Board",))
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    ob.data.layers["GUIDE"].lock = False
    cells = []
    for r in range(2):
        for c in range(3):
            x0, z1 = -5.6 + c * 3.8, 2.9 - r * 3.0
            cells.append((x0, z1 - 3.4 * 9 / 16, x0 + 3.4, z1))
            G.rect(drw["GUIDE"], *cells[-1], 0.008, blue)
    ob.data.layers["GUIDE"].lock = True
    if sol:
        d = drw["USER_Board"]
        ink = 0

        def ellipse_pts(cx, cz, rx, rz, n=20):
            return [(cx + rx * math.cos(t), cz + rz * math.sin(t)) for t in [k * 2 * math.pi / n for k in range(n + 1)]]

        def person(x, z, h, look, rect):
            G.polyline_clipped(d, ellipse_pts(x, z + h * 0.9, h * 0.09, h * 0.1), rect, 0.01, ink)
            G.polyline_clipped(d, [(x - h * 0.17, z), (x - h * 0.14, z + h * 0.72), (x + h * 0.14, z + h * 0.72), (x + h * 0.17, z)], rect, 0.01, ink)
            G.polyline_clipped(d, [(x + look * h * 0.12, z + h * 0.9), (x + look * h * 0.4, z + h * 0.9)], rect, 0.006, ink)
            tip = (x + look * h * 0.4, z + h * 0.9)
            G.polyline_clipped(d, [(tip[0] - look * 0.06, tip[1] + 0.04), tip, (tip[0] - look * 0.06, tip[1] - 0.04)], rect, 0.006, ink)
        for i, (x0, z0, x1, z1) in enumerate(cells):
            w, h = x1 - x0, z1 - z0
            if i == 0:                                  # master : A à gauche, B à droite
                person(x0 + w * 0.3, z0 + 0.15, h * 0.6, 1, (x0, z0, x1, z1))
                person(x0 + w * 0.7, z0 + 0.15, h * 0.6, -1, (x0, z0, x1, z1))
                G.line(d, (x0 + 0.1, z0 + 0.1), (x1 - 0.1, z0 + 0.1), 0.005, ink)
            elif i in (1, 3):                           # sur B (à droite), amorce de A pour i = 1
                person(x0 + w * 0.65, z0 - h * 0.35, h * 1.2, -1, (x0, z0, x1, z1))
                if i == 1:
                    G.polyline(d, [(x0, z0 + h * 0.2), (x0 + w * 0.18, z0 + h * 0.55), (x0 + w * 0.25, z0)], 0.03, ink)
            elif i in (2, 4):                           # sur A (à gauche), amorce de B pour i = 2
                person(x0 + w * 0.35, z0 - h * 0.35, h * 1.2, 1, (x0, z0, x1, z1))
                if i == 2:
                    G.polyline(d, [(x1, z0 + h * 0.2), (x1 - w * 0.18, z0 + h * 0.55), (x1 - w * 0.25, z0)], 0.03, ink)
            else:                                       # insert : tasse
                cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
                G.polyline(d, [(cx - 0.3, cz + 0.35), (cx - 0.25, cz - 0.45), (cx + 0.25, cz - 0.45), (cx + 0.3, cz + 0.35)], 0.012, ink)
                G.ellipse(d, (cx, cz + 0.35), 0.3, 0.07, 0.012, ink)
    L.instructions(NOTE_BOARD)


def contact(sc, out):
    tiles = []
    for name, _loc, _tgt, _lens, frame in SHOTS:
        sc.frame_set(frame)                  # les marqueurs liés choisissent la caméra active
        sc.camera = bpy.data.objects[name]
        p = os.path.join(bpy.app.tempdir, name + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tiles.append(p)
    W = sc.render.resolution_x * sc.render.resolution_percentage // 100
    H = sc.render.resolution_y * sc.render.resolution_percentage // 100
    img = bpy.data.images.new("contact", W * 3, H * 2)
    px = [0.1] * (W * 3 * H * 2 * 4)
    for i, t in enumerate(tiles):
        src = list(bpy.data.images.load(t).pixels)
        ox, oy = (i % 3) * W, (1 - i // 3) * H
        for row in range(H):
            px[((oy + row) * W * 3 + ox) * 4:((oy + row) * W * 3 + ox) * 4 + W * 4] = src[row * W * 4:(row + 1) * W * 4]
    img.pixels = px
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    scene(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_11_dialogue_starter.blend"))
    sc = scene(True)
    L.save(os.path.join(out, "ch18_11_dialogue_solution.blend"))
    contact(sc, os.path.join(out, "ch18_11_dialogue_contact.png"))
    board(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_11_board_starter.blend"))
    board(True)
    L.save(os.path.join(out, "ch18_11_board_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(out, "ch18_11_board_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
