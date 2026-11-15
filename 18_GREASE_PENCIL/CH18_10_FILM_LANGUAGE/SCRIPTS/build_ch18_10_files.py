"""
build_ch18_10_files.py — « Les valeurs de plans » (CH18.10, langage cinématographique).

  STARTER_FILES/ch18_10_shots_starter.blend
      Plateau : CHR_A (x = −1) et CHR_B (x = +1), 1,75 m, face à face ; table et tasse PROP_Cup
      devant A ; une caméra d'exemple CAM_00_Exemple. À créer : 12 caméras (8 valeurs, 2 angles,
      champ/contrechamp).
  STARTER_FILES/ch18_10_board_starter.blend
      Planche GP : 8 cadres 16:9 (calque GUIDE) à remplir sur USER_Shots.
  COMPLETED_EXAMPLES/ch18_10_shots_solution.blend (+ ch18_10_shots_contact.png : planche-contact
      des 12 caméras) ; ch18_10_board_solution.blend (+ _reference.png).
Usage : blender -b --factory-startup --python build_ch18_10_files.py --python-exit-code 1
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
NOTE_SHOTS = """CH18.10 — LES VALEURS DE PLANS (caméras)
Personnage étudié : CHR_A (x = −1). Créez ces caméras (Add > Camera, F2), objectif libre :
CAM_01_PE  plan d'ensemble : A entier, ≤ 30 % de la hauteur d'image
CAM_02_PM  plan moyen (en pied) : A entier, 55–95 % de la hauteur
CAM_03_PA  plan américain : bas de l'image entre genou et mi-cuisse
CAM_04_PRT plan rapproché taille : bas de l'image à la taille
CAM_05_PRP plan rapproché poitrine : bas de l'image à la poitrine
CAM_06_GP  gros plan : le visage, coupé sous le menton
CAM_07_TGP très gros plan : une partie du visage (yeux)
CAM_08_INS insert : la tasse PROP_Cup remplit le cadre
CAM_09_PLONGEE  caméra au-dessus des yeux, qui regarde vers le bas, A dans le cadre
CAM_10_CONTREPLONGEE  caméra basse, qui regarde vers le haut, A dans le cadre
CAM_11_CHAMP (vers B) et CAM_12_CONTRECHAMP (vers A) : DU MÊME CÔTÉ de l'axe A–B (règle des 180°).
Astuce : sélectionnez la caméra, View > Cameras > Set Active Object as Camera (Ctrl+Num 0), puis
N > View > View Lock > Lock : Camera to View, pour cadrer en naviguant.
Vérification : SCRIPTS/validate_ch18_10.py -- --exercise shots
"""
NOTE_BOARD = """CH18.10 — PLANCHE DES 8 VALEURS (GP_Practice, Draw Mode, Num 0)
Dans les 8 cadres (de gauche à droite, haut puis bas) dessinez le même personnage en :
PE, PM, PA, PRT, PRP, GP, TGP, Insert. Coupez le personnage par le bord du cadre au bon endroit.
Calque USER_Shots. Vérification : SCRIPTS/validate_ch18_10.py -- --exercise board
"""


def scene_shots(sol):
    L.reset("SC_Shots")
    set_c, chr_c, cam_c, lgt_c = (L.collection(n) for n in ("SET", "CHARACTERS", "CAMERAS", "LIGHTS"))
    L.plane("GEO_Floor", set_c, L.material("MAT_Floor", (0.35, 0.33, 0.3), 0.8), size=60)
    L.cube("GEO_Wall", set_c, L.material("MAT_Wall", (0.6, 0.62, 0.66), 0.9), size=1, location=(0, 6, 3), scale=(40, 0.2, 6))
    S.mannequin_mesh("CHR_A", chr_c, A, L.material("MAT_A", (0.75, 0.3, 0.2), 0.6))
    S.mannequin_mesh("CHR_B", chr_c, B, L.material("MAT_B", (0.2, 0.4, 0.75), 0.6))
    wood = L.material("MAT_Wood", (0.45, 0.28, 0.14), 0.6)
    L.cube("GEO_Table", set_c, wood, size=1, location=(-1.0, -0.65, 0.375), scale=(0.6, 0.45, 0.75))
    L.cylinder("PROP_Cup", set_c, L.material("MAT_Cup", (0.9, 0.9, 0.85), 0.3), radius=0.045, depth=0.1,
               location=(-0.85, -0.7, 0.8))
    L.light("LGT_Sun", lgt_c, "SUN", (0, -4, 6), 3.5, rotation=(50, 0, 25))
    L.world((0.5, 0.55, 0.62), 0.8, "WO_Studio")
    ex = L.camera("CAM_00_Exemple", cam_c, (0, -7, 1.6), 35, make_active=True)
    S.look_at(ex, (0, 0, 1.0))
    sc = L.render_defaults("BLENDER_EEVEE", 25)
    if sol:
        k = 2 * math.tan(math.atan(10.125 / 50))          # 50 mm, capteur 36 mm, image 16:9
        frames = [("CAM_01_PE", 8.0, 1.6), ("CAM_02_PM", 2.2, 0.9), ("CAM_03_PA", 1.25, 1.325),
                  ("CAM_04_PRT", 0.95, 1.475), ("CAM_05_PRP", 0.65, 1.625), ("CAM_06_GP", 0.38, 1.66),
                  ("CAM_07_TGP", 0.13, 1.635)]
        for name, h, zc in frames:
            d = h / k
            c = L.camera(name, cam_c, (A[0], -d, zc), 50, make_active=False)
            S.look_at(c, (A[0], 0, zc))
        cup = L.obj("PROP_Cup").location
        c = L.camera("CAM_08_INS", cam_c, (cup.x, cup.y - 0.22 / k, cup.z + 0.04), 50, make_active=False)
        S.look_at(c, (cup.x, cup.y, cup.z))
        c = L.camera("CAM_09_PLONGEE", cam_c, (A[0], -3.2, 3.6), 50, make_active=False)
        S.look_at(c, (A[0], 0, 1.0))
        c = L.camera("CAM_10_CONTREPLONGEE", cam_c, (A[0], -2.4, 0.35), 50, make_active=False)
        S.look_at(c, (A[0], 0, 1.45))
        c = L.camera("CAM_11_CHAMP", cam_c, (-1.7, -0.75, 1.62), 50, make_active=False)
        S.look_at(c, (B[0], 0, 1.5))
        c = L.camera("CAM_12_CONTRECHAMP", cam_c, (1.7, -0.75, 1.62), 50, make_active=False)
        S.look_at(c, (A[0], 0, 1.5))
    L.instructions(NOTE_SHOTS)
    return sc


# --- planche GP -------------------------------------------------------------------------------

FRAME_W = 2.6


def frames():
    out = []
    for r in range(2):
        for c in range(4):
            x0 = -5.6 + c * 2.85
            z1 = 2.9 - r * 2.4
            out.append((x0, z1 - FRAME_W * 9 / 16, x0 + FRAME_W, z1))
    return out


def figure(scale, x, z_feet):
    """Polylignes d'un personnage stylisé (1,75 unité × scale), pieds en (x, z_feet)."""
    s = scale

    def ell(cz, rx, rz, n=24):
        return [(x + rx * s * math.cos(t), z_feet + (cz + rz * math.sin(t)) * s) for t in [i * 2 * math.pi / n for i in range(n + 1)]]
    lines = [ell(1.635, 0.115, 0.125), ell(1.25, 0.2, 0.27), ell(0.98, 0.17, 0.13)]
    for sgn in (-1, 1):
        lines.append([(x + 0.1 * sgn * s, z_feet + 0.9 * s), (x + 0.1 * sgn * s, z_feet)])
        lines.append([(x + 0.22 * sgn * s, z_feet + 1.43 * s), (x + 0.3 * sgn * s, z_feet + 0.82 * s)])
    eyes = [[(x + (sg * 0.045 - 0.02) * s, z_feet + 1.64 * s), (x + (sg * 0.045 + 0.02) * s, z_feet + 1.64 * s)] for sg in (-1, 1)]
    mouth = [[(x - 0.035 * s, z_feet + 1.565 * s), (x + 0.035 * s, z_feet + 1.565 * s)]]
    return lines + eyes + mouth


def clip(poly, rect):
    """Découpe une polyligne par un rectangle (échantillonnage fin) → morceaux intérieurs."""
    x0, z0, x1, z1 = rect
    pts = []
    for a, b in zip(poly, poly[1:]):
        for i in range(12):
            t = i / 12
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    pts.append(poly[-1])
    out, cur = [], []
    for p in pts:
        if x0 <= p[0] <= x1 and z0 <= p[1] <= z1:
            cur.append(p)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [c for c in out if len(c) >= 2]


def board(sol):
    L.reset("SC_Board")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Shots",))
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    ob.data.layers["GUIDE"].lock = False
    for f in frames():
        G.rect(drw["GUIDE"], *f, 0.008, blue)
    ob.data.layers["GUIDE"].lock = True
    if sol:
        # (taille du personnage en hauteur de cadre, hauteur de coupe en bas du cadre)
        fh = FRAME_W * 9 / 16
        specs = [(0.25, None), (0.8, None), (fh / 1.25, 0.7), (fh / 0.95, 1.0), (fh / 0.65, 1.3), (fh / 0.38, 1.47), (fh / 0.13, 1.57)]
        for (x0, z0, x1, z1), (k, cut) in zip(frames()[:7], specs):
            cx = (x0 + x1) / 2
            if cut is None:
                scale = k * fh / 1.75
                zf = z0 + (fh - 1.75 * scale) / 2 if k > 0.5 else z0 + 0.08
            else:
                scale = k
                zf = z0 - cut * scale
            for poly in figure(scale, cx, zf):
                for piece in clip(poly, (x0, z0, x1, z1)):
                    G.polyline(drw["USER_Shots"], piece, 0.008, 0)
        x0, z0, x1, z1 = frames()[7]          # insert : une tasse et une main
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        G.polyline(drw["USER_Shots"], [(cx - 0.35, cz + 0.45), (cx - 0.3, cz - 0.5), (cx + 0.3, cz - 0.5), (cx + 0.35, cz + 0.45)], 0.012, 0)
        G.ellipse(drw["USER_Shots"], (cx, cz + 0.45), 0.35, 0.08, 0.012, 0)
        G.ellipse(drw["USER_Shots"], (cx + 0.5, cz), 0.15, 0.22, 0.012, 0)
        G.polyline(drw["USER_Shots"], [(x0, cz - 0.1), (cx - 0.38, cz - 0.05), (cx - 0.36, cz + 0.2), (x0, cz + 0.25)], 0.01, 0)
    L.instructions(NOTE_BOARD)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    scene_shots(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_10_shots_starter.blend"))
    sc = scene_shots(True)
    p = L.save(os.path.join(out, "ch18_10_shots_solution.blend"))
    # planche-contact : une image par caméra, assemblée dans une grille 4 × 3
    tiles = []
    for c in sorted(o.name for o in bpy.data.objects if o.type == "CAMERA" and o.name[4:6].isdigit() and o.name != "CAM_00_Exemple"):
        sc.camera = bpy.data.objects[c]
        path = os.path.join(bpy.app.tempdir, c + ".png")
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        tiles.append(path)
    W, H = sc.render.resolution_x * sc.render.resolution_percentage // 100, sc.render.resolution_y * sc.render.resolution_percentage // 100
    sheet = bpy.data.images.new("contact", W * 4, H * 3)
    px = [0.1] * (W * 4 * H * 3 * 4)
    for i, t in enumerate(tiles):
        im = bpy.data.images.load(t)
        src = list(im.pixels)
        ox, oy = (i % 4) * W, (2 - i // 4) * H
        for row in range(H):
            a = (row * W) * 4
            b = ((oy + row) * W * 4 + ox) * 4
            px[b:b + W * 4] = src[a:a + W * 4]
    sheet.pixels = px
    sheet.filepath_raw = os.path.join(out, "ch18_10_shots_contact.png")
    sheet.file_format = "PNG"
    sheet.save()
    board(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_10_board_starter.blend"))
    board(True)
    p = L.save(os.path.join(out, "ch18_10_board_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(out, "ch18_10_board_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
