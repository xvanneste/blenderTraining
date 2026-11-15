"""
build_ch18_18_files.py — « Le plan animé de 5 s : acting, effet, caméra » (CH18.18, module E).

  STARTER_FILES/ch18_18_shot_starter.blend
      Feuille 16:9, calque SET (table, ampoule suspendue) verrouillé, calques USER_Char et USER_FX
      vides, 120 images (5 s à 24 i/s), caméra CAM_Sheet fixe ; texte SCENARIO (« L'ampoule »).
  COMPLETED_EXAMPLES/ch18_18_shot_solution.blend (+ _contact.png)
      USER_Char : personnage en buste — attente (tenue, clignement 24), regard vers l'ampoule (36),
      anticipation (44), sursaut écrasé/étiré (49–51), surprise tenue (53–79), retour (81–89),
      soulagement tenu (91–120). USER_FX : éclair (48–50, en un), fumée qui grossit et monte (52–70,
      en deux), clé vide en 72 (l'effet disparaît). Caméra : tremblement amorti 48–58.
Usage : blender -b --factory-startup --python build_ch18_18_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
END, POP = 120, 48
BULB = (2.6, 1.6)
HEAD = (-2.2, -0.2)
NOTE = """CH18.18 — LE PLAN ANIMÉ DE 5 S (GP_Practice, 120 images à 24 i/s)
Scénario (texte SCENARIO) : un personnage attend ; l'ampoule grésille et ÉCLATE à l'image 48 ; il
sursaute, reste figé de surprise, puis se détend, soulagé.
1. USER_Char : jeu d'acteur — poses tenues pour être lues (≥ 3 tenues de 6 images ou plus), parties
   rapides en un/deux, réaction 1 à 6 images APRÈS l'éclatement (anticipation, sursaut écrasé/étiré).
2. USER_FX : l'effet — éclair en un (2–3 dessins), puis fumée qui grossit/monte en deux ; terminez par
   une clé VIDE (Insert Blank Keyframe) : l'effet disparaît.
3. Caméra CAM_Sheet : tremblement au moment de l'éclatement (clés de Location X/Z alternées et
   amorties sur ~10 images, I sur le champ), retour exact à la position de départ.
4. (Conseillé) PROP_Bulb : clé vide à l'image 48 — le verre de l'ampoule a disparu.
Vérification : SCRIPTS/validate_ch18_18.py -- --exercise shot
"""
SCENARIO = """L'AMPOULE — 5 s
0,0–1,5 s  Un personnage attend, immobile (il cligne des yeux).
1,5–2,0 s  Il lève les yeux vers l'ampoule qui grésille ; il plisse les yeux (anticipation).
2,0 s      L'ampoule éclate : éclair, la caméra tremble.
2,0–3,3 s  Sursaut (écrasé puis étiré), puis surprise figée, bouche ouverte ; la fumée monte.
3,4–5,0 s  Il se détend, sourire soulagé.
"""

# poses du personnage : image -> (humeur, écrasement, regard x, regard z)
CHAR = [(1, "neutral", 1.0, 0.0, 0.0), (24, "blink", 1.0, 0.0, 0.0), (26, "neutral", 1.0, 0.0, 0.0),
        (36, "look", 1.0, 0.6, 0.5), (40, "look", 1.0, 0.7, 0.6), (44, "squint", 0.94, 0.7, 0.6),
        (49, "surprise", 0.8, 0.5, 0.4), (51, "surprise", 1.18, 0.6, 0.5), (53, "surprise", 1.06, 0.6, 0.5),
        (55, "surprise", 1.04, 0.6, 0.5), (79, "surprise", 1.03, 0.4, 0.3), (81, "neutral", 1.0, 0.2, 0.1),
        (85, "neutral", 0.97, 0.1, 0.0), (89, "relief", 0.99, 0.0, 0.0), (91, "relief", 1.0, 0.0, 0.0)]
SHAKE = [(POP - 1, 0, 0), (POP, 0.18, -0.12), (POP + 1, -0.15, 0.1), (POP + 2, 0.12, 0.08),
         (POP + 4, -0.08, -0.06), (POP + 6, 0.05, 0.03), (POP + 8, -0.02, -0.01), (POP + 10, 0, 0)]


def face(d, mood, s, gx, gz, ink, red):
    cx, cz = HEAD
    rx, rz = 1.0 / math.sqrt(s), 1.1 * s
    cz += (rz - 1.1)                                   # la base de la tête reste en place
    G.ellipse(d, (cx, cz), rx, rz, 0.03, ink, n=48)
    G.polyline(d, [(cx - 0.6, cz - rz + 0.05), (cx - 1.5, -3.2)], 0.03, ink)          # épaules
    G.polyline(d, [(cx + 0.6, cz - rz + 0.05), (cx + 1.5, -3.2)], 0.03, ink)
    ey = cz + 0.25 * s
    big = mood == "surprise"
    for ex in (-0.38, 0.38):
        x = cx + ex / math.sqrt(s)
        if mood == "blink":
            G.line(d, (x - 0.15, ey), (x + 0.15, ey), 0.025, ink)
            continue
        h = 0.07 if mood == "squint" else (0.24 if big else 0.16)
        G.ellipse(d, (x, ey), 0.15 if not big else 0.2, h, 0.022, ink, n=24)
        if mood != "squint":
            G.circle(d, (x + 0.1 * gx, ey + 0.08 * gz), 0.05, 0.03, ink, n=12)                # pupille
        by = ey + (0.42 if big else (0.22 if mood == "squint" else 0.3))
        tilt = -0.08 if mood == "squint" else (-0.06 if big else 0.0)   # < 0 : intérieur relevé
        G.line(d, (x - 0.18, by + (tilt if ex < 0 else -tilt)), (x + 0.18, by - (tilt if ex < 0 else -tilt)), 0.025, ink)
    my = cz - 0.45 * s
    if big:
        G.ellipse(d, (cx, my - 0.05), 0.16, 0.24, 0.025, ink, n=24)
    elif mood == "relief":
        G.polyline(d, [(cx - 0.35, my + 0.08), (cx - 0.15, my - 0.06), (cx + 0.15, my - 0.06), (cx + 0.35, my + 0.08)], 0.025, ink)
        for ex in (-0.6, 0.6):
            G.line(d, (cx + ex - 0.08, my + 0.15), (cx + ex + 0.08, my + 0.12), 0.015, red)       # joues
    elif mood == "squint":
        G.line(d, (cx - 0.2, my), (cx + 0.22, my - 0.05), 0.025, ink)
    else:
        G.line(d, (cx - 0.25, my), (cx + 0.25, my), 0.025, ink)


def fx_flash(d, k, yellow, ink):
    bx, bz = BULB
    for i in range(12):
        a = 2 * math.pi * i / 12 + 0.2 * k
        r0, r1 = 0.4 + 0.2 * k, 0.9 + 0.6 * k
        G.line(d, (bx + r0 * math.cos(a), bz + r0 * math.sin(a)), (bx + r1 * math.cos(a), bz + r1 * math.sin(a)), 0.03, yellow)
    G.circle(d, (bx, bz), 0.35 + 0.15 * k, 0.03, yellow, n=24)
    for j in range(5):                                # éclats de verre
        a = 1.3 * j + k
        G.line(d, (bx + (0.5 + 0.3 * k) * math.cos(a), bz + (0.5 + 0.3 * k) * math.sin(a)),
               (bx + (0.62 + 0.3 * k) * math.cos(a + 0.2), bz + (0.62 + 0.3 * k) * math.sin(a + 0.2)), 0.02, ink)


def fx_smoke(d, k, grey):
    bx, bz = BULB
    for j, (ox, oz) in enumerate(((0, 0), (0.35, 0.25), (-0.3, 0.3), (0.1, 0.55))):
        r = 0.18 + 0.07 * k + 0.03 * j
        G.circle(d, (bx + ox * (1 + 0.15 * k) + 0.04 * k, bz + 0.2 + oz * (1 + 0.1 * k) + 0.11 * k), r, 0.02, grey, n=20)


def scene(sol):
    L.reset("SC_Shot")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("SET",), ("USER_Char", "USER_FX"))
    ink = 0
    line = G.material(ob, "MAT_GP_Set", (0.35, 0.35, 0.4))
    yellow = G.material(ob, "MAT_GP_Flash", (0.95, 0.7, 0.05))
    grey = G.material(ob, "MAT_GP_Smoke", (0.5, 0.5, 0.55))
    red = G.material(ob, "MAT_GP_Blush", (0.85, 0.3, 0.3))
    sl = ob.data.layers["SET"]
    sl.lock = False
    s = drw["SET"]
    G.line(s, (-5.9, -2.6), (5.9, -2.6), 0.02, line)                               # table
    G.line(s, (BULB[0], 3.4), (BULB[0], BULB[1] + 0.45), 0.015, line)              # fil
    G.rect(s, BULB[0] - 0.12, BULB[1] + 0.3, BULB[0] + 0.12, BULB[1] + 0.48, 0.015, line)
    sl.lock = True
    G.circle(G.layer(ob, "PROP_Bulb", frame=1), BULB, 0.3, 0.015, line, n=24)       # verre de l'ampoule
    ob.data.layers["PROP_Bulb"].use_lights = False
    sl.opacity = 1.0
    sc = bpy.context.scene
    sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, END
    L.instructions(SCENARIO, "SCENARIO")
    if sol:
        for f, mood, sq, gx, gz in CHAR:
            face(G.layer(ob, "USER_Char", frame=f), mood, sq, gx, gz, ink, red)
        for k, f in enumerate((POP, POP + 1, POP + 2)):
            fx_flash(G.layer(ob, "USER_FX", frame=f), k, yellow, ink)
        for k, f in enumerate(range(POP + 4, POP + 23, 2)):
            fx_smoke(G.layer(ob, "USER_FX", frame=f), k, grey)
        G.layer(ob, "USER_FX", frame=POP + 24)                                     # clé vide : fin de l'effet
        G.layer(ob, "PROP_Bulb", frame=POP)                                        # clé vide : l'ampoule a éclaté
        # le calque FX vide en image 1 (créé par sheet) reste vide jusqu'à l'éclatement
        for f, x, z in SHAKE:
            cam.location.x, cam.location.z = x, z
            cam.keyframe_insert("location", frame=f)
        cam.location = (0, -10, 0)
    L.instructions(NOTE)
    return sc


def contact(sc, frames, out):
    sc.render.resolution_percentage = 25
    W, H = sc.render.resolution_x // 4, sc.render.resolution_y // 4
    sheet = np.zeros((2 * H, 4 * W, 4), dtype=np.float32)
    for i, f in enumerate(frames):
        sc.frame_set(f)
        p = os.path.join(bpy.app.tempdir, f"shot_{f}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        sheet[(1 - i // 4) * H:(2 - i // 4) * H, (i % 4) * W:(i % 4 + 1) * W] = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
    img = bpy.data.images.new("shot_contact", 4 * W, 2 * H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    scene(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_18_shot_starter.blend"))
    sc = scene(True)
    L.save(os.path.join(out, "ch18_18_shot_solution.blend"))
    contact(sc, [10, 38, 44, 48, 50, 58, 66, 100], os.path.join(out, "ch18_18_shot_contact.png"))


if __name__ == "__main__":
    L.run(main)
