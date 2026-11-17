"""
validate_p7.py — Correcteur du projet P7 « Une scène animée » (scène de 15 à 25 s : jeu d'acteur, dialogue, caméras).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p7.py [-- --debug]
Le correcteur lit la scène ÉVALUÉE (images 1 à la dernière) :
  1. Durée : de 360 à 600 images (15 à 25 s) à 24 i/s.
  2. Personnage : RIG_Mannequin (13 bones) et CHR_Mannequin lié par un modificateur Armature.
  3. Montage NLA : aucune action active ; au moins 5 strips sur au moins 2 pistes ; au moins 3 actions différentes ; au moins un strip répété 3 fois ou plus ; au moins 3 fondus d'entrée (Blend In ≥ 4 images) sur des strips qui chevauchent un autre strip.
  4. Jeu d'acteur (lacet évalué du bone head) : une remarque (au moins 40° en 10 images ou moins) et un maintien (12 images consécutives ou plus avec une variation de lacet ≤ 3° à plus de 30° de lacet).
  5. Continuité : aucune cheville ni poignet ne se déplace de plus de 0,40 m d une image à l autre (pas de saut aux raccords des strips).
  6. Caméras : au moins 2 objets caméra animés (action avec clés) et dotés d'une contrainte de visée (Track To, Damped Track, Locked Track) sur un objet ; au moins 2 marqueurs liés à une caméra, à des images différentes, le premier à l'image de début (± 1) ; la caméra de la scène change au raccord.
  7. Dialogue : texte DIALOGUE avec au moins 2 répliques « image N : texte » ; marqueurs line_1, line_2… aux images indiquées, espacés d'au moins 36 images ; à chaque réplique, le lacet de la tête varie d'au moins 25° dans les 14 images qui suivent (le personnage réagit).
  8. Planche renders/p7_contact_sheet.png (dossier du .blend) : ≥ 1 600 px de large, non noire et contrastée.
Testé avec : Blender 5.3.0.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("hips", "head", "shin.L", "shin.R", "fore.L", "fore.R")


def main():
    debug = L.flag("--debug")
    r = L.Report("P7 — Une scène animée")
    sc = bpy.context.scene
    n = sc.frame_end - sc.frame_start + 1
    r.check(360 <= n <= 600 and sc.render.fps == 24, f"Durée : {n} images à {sc.render.fps} i/s = {n / max(sc.render.fps, 1):.1f} s (360–600 images)", "Plage de la scène : 15 à 25 s à 24 i/s.", 4)
    rig, body = bpy.data.objects.get("RIG_Mannequin"), bpy.data.objects.get("CHR_Mannequin")
    if not r.check(rig is not None and body is not None and rig.type == "ARMATURE" and all(x in rig.pose.bones for x in NAMES) and any(m.type == "ARMATURE" and m.object == rig for m in body.modifiers), "RIG_Mannequin et CHR_Mannequin (lié par un modificateur Armature) présents", "Partez du mannequin des chapitres de la phase.", 3):
        return r.finish()
    ad = rig.animation_data
    strips = [(t, s) for t in (ad.nla_tracks if ad else []) for s in t.strips]
    acts = {s.action.name for t, s in strips if s.action}
    over = 0
    for t, s in strips:
        if s.blend_in >= 4 and any(o is not s and o.frame_start < s.frame_start < o.frame_end for t2, o in strips):
            over += 1
    ok = ad is not None and ad.action is None and len(strips) >= 5 and len(ad.nla_tracks) >= 2 and len(acts) >= 3 and max((s.repeat for t, s in strips), default=0) >= 3 and over >= 3
    r.check(ok, f"Montage NLA : {len(strips)} strips sur {len(ad.nla_tracks) if ad else 0} pistes, {len(acts)} actions, répétition max {max((s.repeat for t, s in strips), default=0):.0f}, {over} fondus sur chevauchement ; action active : {ad.action.name if ad and ad.action else 'aucune'}", "Strips sur pistes alternées, Blend In de 6 images sur les raccords, aucune action active.", 8)
    f0, f1 = sc.frame_start, sc.frame_end
    restyaw = math.atan2(rig.data.bones["head"].matrix_local[1][0], rig.data.bones["head"].matrix_local[0][0])
    yaw = np.zeros(f1 + 2)
    jump = 0.0
    prev = None
    cams = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        mw = rig.matrix_world
        m = mw @ rig.pose.bones["head"].matrix
        yaw[f] = (math.degrees(math.atan2(m[1][0], m[0][0]) - restyaw) + 180) % 360 - 180
        pts = np.array([np.array(mw @ rig.pose.bones[x].tail) for x in ("shin.L", "shin.R", "fore.L", "fore.R")])
        if prev is not None:
            jump = max(jump, float(np.linalg.norm(pts - prev, axis=1).max()))
        prev = pts
        cams.append((f, sc.camera.name if sc.camera else None))
    sc.frame_set(f0)
    y = yaw[f0:f1 + 1]
    quick = max(float(np.abs(y[i + 10] - y[i]).max()) if i + 10 < len(y) else 0.0 for i in range(len(y)))
    hold = 0
    i = 0
    while i < len(y):
        j = i
        while j + 1 < len(y) and float(np.ptp(y[i:j + 2])) <= 3.0:
            j += 1
        if j - i + 1 >= 12 and abs(float(y[i:j + 1].mean())) >= 30:
            hold = max(hold, j - i + 1)
        i = j + 1
    r.check(quick >= 40 and hold >= 12, f"Jeu d'acteur : remarque de {quick:.0f}° en 10 images (≥ 40) ; maintien de {hold} images à plus de 30° (≥ 12)", "Reprenez le plan d'acting de CH07.10 : remarque rapide, puis maintien.", 8)
    r.check(jump <= 0.40, f"Continuité : déplacement maximal d'une cheville ou d'un poignet {100 * jump:.0f} cm par image (≤ 40)", "Fondus d'entrée sur les raccords des strips.", 6)
    camobjs = [o for o in bpy.data.objects if o.type == "CAMERA"]
    animated = [o for o in camobjs if o.animation_data and o.animation_data.action]
    tracked = [o for o in camobjs if any(c.type in ("TRACK_TO", "DAMPED_TRACK", "LOCKED_TRACK") and c.target for c in o.constraints)]
    bound = sorted({m.frame: m for m in sc.timeline_markers if m.camera is not None}.items())
    switched = len({c for f, c in cams if c}) >= 2
    r.check(len(animated) >= 2 and len(tracked) >= 2 and len(bound) >= 2 and abs(bound[0][0] - f0) <= 1 and switched, f"Caméras : {len(camobjs)} objets, {len(animated)} animés, {len(tracked)} avec visée ; {len(bound)} marqueurs liés ; la caméra de la scène change : {'oui' if switched else 'non'}", "Deux caméras animées avec Track To et des marqueurs liés (M, puis Bind Camera to Markers).", 8)
    txt = bpy.data.texts.get("DIALOGUE")
    lines = []
    if txt:
        for ln in txt.as_string().splitlines():
            mm = re.match(r"\s*image\s+(\d+)\s*:\s*(.+)", ln)
            if mm:
                lines.append((int(mm.group(1)), mm.group(2)))
    mk = {m.name: m.frame for m in sc.timeline_markers}
    okm = len(lines) >= 2 and all(mk.get(f"line_{i}") == f for i, (f, t) in enumerate(lines, 1)) and all(lines[i + 1][0] - lines[i][0] >= 36 for i in range(len(lines) - 1))
    react = [float(np.ptp(y[max(f - f0, 0):max(f - f0, 0) + 15])) if f - f0 < len(y) else 0.0 for f, t in lines]
    r.check(okm and all(a >= 25 for a in react), f"Dialogue : {len(lines)} répliques, marqueurs line_n {'conformes' if okm else 'non conformes'} ; réaction de la tête {[round(a) for a in react]}° dans les 14 images (≥ 25)", "Texte DIALOGUE « image N : réplique », marqueurs line_n, réaction alignée.", 8)
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p7_contact_sheet.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        ok_img = W >= 1600 and px.mean() > 0.05 and px.std() > 0.03
        msg = f"{W} × {H}, moyenne {px.mean():.2f}, écart-type {px.std():.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche renders/p7_contact_sheet.png : {msg}", "Quatre images de la scène côte à côte, ≥ 1 600 px de large.", 4)
    if debug:
        print("[DEBUG] n", n, "strips", len(strips), "acts", sorted(acts), "over", over, "quick", round(quick, 1), "hold", hold, "jump", round(jump, 3), "cams", len(camobjs), len(animated), len(tracked), bound, "lines", lines, "react", [round(a, 1) for a in react])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
