"""
build_ch18_16_files.py — « La balle rebondissante 2D » (CH18.16, phase 18 module E).

  STARTER_FILES/ch18_16_bounce_starter.blend
      Feuille 16:9 (caméra ortho CAM_Sheet), calque GUIDE verrouillé (sol, départ, zone d'arrivée),
      calque USER_Ball vide, 24 i/s, images 1–64, onion skinning réglé (2 clés avant / 2 après).
  COMPLETED_EXAMPLES/ch18_16_keys_solution.blend
      Étape 1 — les POSES CLÉS seulement : départ au sommet, 4 contacts (écrasés), 3 sommets
      (hauteurs 4 → 2,4 → 1,44 → 0,86 m) ; type de clé Keyframe (contacts) et Extreme (sommets).
  COMPLETED_EXAMPLES/ch18_16_bounce_solution.blend (+ _reference.png : superposition de toutes les images)
      Étape 2 — animation complète « en deux » (un dessin toutes les 2 images) : intervalles serrés
      près des sommets, espacés près du sol, étirement avant/après contact, écrasement au contact,
      type Breakdown pour les intervalles ; maintien final.
Physique : chute libre (g constant), restitution 0,6 de la hauteur à chaque rebond.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_16_files.py
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

CH = L.chapter_dir(__file__)
GROUND, R = -2.6, 0.35
X0, X1 = -5.2, 4.6
H0, DECAY, N_CONTACTS = 4.0, 0.6, 4
FALL0 = 12                      # images de la première chute
END = 64
NOTE = """CH18.16 — LA BALLE REBONDISSANTE (GP_Practice, calque USER_Ball, 24 i/s, images 1–64)
Étape 1 — POSES CLÉS (exercice « keys ») : dessinez seulement les extrêmes : départ en haut à gauche
(image 1), les CONTACTS au sol (balle écrasée) et les SOMMETS de chaque rebond, de plus en plus bas
(≈ 60 % de la hauteur précédente), en avançant vers la droite. Dope Sheet (mode Grease Pencil) :
contacts = type Keyframe, sommets = type Extreme (R).
Étape 2 — INTERVALLES (exercice « bounce ») : complétez « en deux » (un dessin toutes les 2 images) ;
intervalles RAPPROCHÉS près des sommets (ralenti), ÉCARTÉS près du sol (vitesse) ; balle étirée juste
avant et juste après le contact, écrasée au contact, ronde au sommet ; volume constant.
Intervalles : type Breakdown (R). Onion skinning : Viewport Overlays > Onion Skin.
Insérer un dessin : Draw > Animation > Insert Blank Keyframe (Active Layer) (Shift+I).
Vérification : SCRIPTS/validate_ch18_16.py -- --exercise keys | bounce
"""


def plan():
    """Liste des dessins (image, x, z_centre, rx, rz, type) de l'animation complète."""
    g = 2 * H0 / FALL0 ** 2                     # m / image²
    heights = [H0 * DECAY ** i for i in range(N_CONTACTS)]
    # images de contact
    contacts, t = [], 1 + FALL0
    contacts.append(t)
    for h in heights[1:]:
        t += 2 * math.sqrt(2 * h / g)
        contacts.append(t)
    contacts = [round(c) for c in contacts]
    span = contacts[-1] - 1
    vx = (X1 - X0) / span

    def height_at(f):
        if f <= contacts[0]:
            return H0 * (1 - ((f - 1) / (contacts[0] - 1)) ** 2)
        for i in range(1, len(contacts)):
            a, b = contacts[i - 1], contacts[i]
            if a <= f <= b:
                u = (f - a) / (b - a)
                return heights[i] * 4 * u * (1 - u)
        return 0.0

    frames = set(range(1, contacts[0], 2))
    for i in range(1, len(contacts)):
        a, b = contacts[i - 1], contacts[i]
        frames |= set(range(a, b, 2))
    frames |= set(contacts)
    frames = sorted(frames)
    apex = [1] + [round((contacts[i - 1] + contacts[i]) / 2) for i in range(1, len(contacts))]
    for a in apex:                               # un dessin exactement au sommet
        if a not in frames:
            frames = sorted(set(frames) | {a})
    out = []
    for f in frames:
        x = X0 + vx * (f - 1)
        h = height_at(f)
        kind = "BREAKDOWN"
        rx = rz = R
        near = min(abs(f - c) for c in contacts)
        energy = max(heights[min(i, len(heights) - 1)] for i in range(len(contacts)) if abs(f - contacts[i]) == near) / H0
        if f in contacts:
            k = 0.32 * math.sqrt(energy)
            rx, rz = R * (1 + k), R / (1 + k)
            kind = "KEYFRAME"
        elif near <= 2 and h < 1.6:
            k = 0.22 * math.sqrt(energy)
            rx, rz = R / (1 + k), R * (1 + k)
        if f in apex:
            kind = "EXTREME"
        out.append((f, x, GROUND + rz + h, rx, rz, kind))
    hold = contacts[-1]
    return out, contacts, apex, hold


def scene(stage):
    L.reset("SC_Bounce")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Ball",))
    guide = G.material(ob, "MAT_GP_Guide", (0.35, 0.45, 0.7))
    gl = ob.data.layers["GUIDE"]
    gl.lock = False
    d = drw["GUIDE"]
    G.line(d, (-5.9, GROUND), (5.9, GROUND), 0.012, guide)
    G.circle(d, (X0, GROUND + 2 * R + H0 - R), R, 0.005, guide)                      # position de départ
    G.line(d, (X1 - 0.6, GROUND - 0.15), (X1 + 0.6, GROUND - 0.15), 0.02, guide)      # zone d'arrivée
    gl.lock = True
    sc = bpy.context.scene
    sc.render.fps, sc.frame_start, sc.frame_end = 24, 1, END
    sc["bcma_ground"], sc["bcma_ball_r"] = GROUND, R
    gp = ob.data
    gp.onion_mode = "RELATIVE"
    gp.ghost_before_range = gp.ghost_after_range = 2
    gp.onion_keyframe_type = "ALL"
    ball = G.material(ob, "MAT_GP_Ball", (0.12, 0.04, 0.03), fill=(0.85, 0.22, 0.15))
    lay = ob.data.layers["USER_Ball"]
    if stage:
        drawings, contacts, apex, hold = plan()
        for f, x, z, rx, rz, kind in drawings:
            if stage == "keys" and kind == "BREAKDOWN":
                continue
            dr = G.layer(ob, "USER_Ball", frame=f)
            G.ellipse(dr, (x, z), rx, rz, 0.012, ball, n=40, fill_mat=None)
            G.line(dr, (x - rx * 0.5, z + rz * 0.35), (x - rx * 0.15, z + rz * 0.6), 0.008, ball)  # reflet : lit la rotation
            fr = next(fr for fr in lay.frames if fr.frame_number == f)
            fr.keyframe_type = kind
        print(f"[BCMA] {stage} : {len(lay.frames)} dessins, contacts {contacts}, sommets {apex}")
    else:
        # le calque vide garde sa clé image 1 (vide) ; on la supprime pour un départ propre
        pass
    L.instructions(NOTE)
    return sc, ob


def overlay_reference(sc, ob, out):
    """Image de contrôle : toutes les images de la balle superposées (comme un onion skin total)."""
    lay = ob.data.layers["USER_Ball"]
    trail = G.layer(ob, "TRAIL", frame=1)
    mat = G.material(ob, "MAT_GP_Trail", (0.6, 0.2, 0.15))
    for fr in lay.frames:
        for s in fr.drawing.strokes:
            G.polyline(trail, [(p.position.x, p.position.z) for p in s.points], 0.006, mat, cyclic=s.cyclic, fill=False)
    ob.data.layers["TRAIL"].use_lights = False
    sc.frame_set(1)
    sc.render.resolution_percentage = 60
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    scene(None)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_16_bounce_starter.blend"))
    scene("keys")
    L.save(os.path.join(out, "ch18_16_keys_solution.blend"))
    sc, ob = scene("bounce")
    L.save(os.path.join(out, "ch18_16_bounce_solution.blend"))
    overlay_reference(sc, ob, os.path.join(out, "ch18_16_bounce_reference.png"))


if __name__ == "__main__":
    L.run(main)
