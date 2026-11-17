"""
validate_p8.py — Correcteur du projet P8 « Une séquence d'action » (10 s : destruction + tissu + particules + vent).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p8.py [-- --debug]
Le correcteur lit la scène ÉVALUÉE (images 1 à la dernière, avancées une à une) :
  1. Durée : de 216 à 300 images à 24 i/s (9 à 12,5 s).
  2. Destruction : monde de corps rigides (au moins 20 sous-étapes) ; Ground PASSIVE ; au moins 20 briques Brick_* ACTIVE ; Wreck_Ball ACTIVE de 20 kg ou plus ;
     au moins 30 contraintes Fixed entre deux briques, au moins 90 % cassables (seuil de 0,3 à 3).
  3. Tissu : objet Flag avec un modificateur Cloth dont le groupe d'épinglage (vertex_group_mass) existe et contient au moins 10 sommets.
  4. Particules : objet Dust avec un système de particules d'au moins 100 particules.
  5. Vent : objet FORCE_Wind, champ Wind de force 20 ou plus, axe Z local orienté vers +X (composante x ≥ 0,9).
  6. Simulation : de 8 à 30 liaisons cassées sur 38 (même mesure que CH08.07) ; aucune brique sous le sol (z ≥ 0,05) ; le haut du drapeau reste épinglé (≤ 5 mm) ;
     le bas du drapeau est poussé d'au moins 0,15 m dans le sens +X (le vent agit sur le tissu) ; à l'image 120, au moins 100 particules vivantes dont le x moyen est de 1,5 à 15 m (le vent agit sur la poussière sans la pulvériser).
  7. Planche renders/p8_contact_sheet.png (dossier du .blend) : ≥ 1 600 px de large, non noire et contrastée.
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("P8 — Une séquence d'action (simulations)")
    sc = bpy.context.scene
    n = sc.frame_end - sc.frame_start + 1
    r.check(216 <= n <= 300 and sc.render.fps == 24 and sc.frame_start == 1, f"Durée : {n} images à {sc.render.fps} i/s = {n / max(sc.render.fps, 1):.1f} s (216–300 images, début à 1)", "Images 1–240 à 24 i/s.", 4)
    ground, ball = bpy.data.objects.get("Ground"), bpy.data.objects.get("Wreck_Ball")
    bricks = [o for o in bpy.data.objects if o.name.startswith("Brick_") and o.rigid_body is not None]
    w = sc.rigidbody_world
    names = {b.name for b in bricks}
    cons = [o.rigid_body_constraint for o in bpy.data.objects if o.rigid_body_constraint and o.rigid_body_constraint.type == "FIXED" and o.rigid_body_constraint.object1
            and o.rigid_body_constraint.object2 and o.rigid_body_constraint.object1.name in names and o.rigid_body_constraint.object2.name in names]
    brk = sum(1 for c in cons if c.use_breaking and 0.3 <= c.breaking_threshold <= 3)
    ok = (w is not None and w.substeps_per_frame >= 20 and ground is not None and ground.rigid_body is not None and ground.rigid_body.type == "PASSIVE"
          and len(bricks) >= 20 and all(b.rigid_body.type == "ACTIVE" for b in bricks) and ball is not None and ball.rigid_body is not None and ball.rigid_body.type == "ACTIVE" and ball.rigid_body.mass >= 20)
    r.check(ok, f"Destruction : monde {'oui' if w else 'non'} ({w.substeps_per_frame if w else '–'} sous-étapes ≥ 20), sol Passive, {len(bricks)} briques Active (≥ 20), boulet ≥ 20 kg", "Reprenez CH08.07 : sol, briques, boulet, monde.", 7)
    r.check(len(cons) >= 30 and brk >= 0.9 * max(len(cons), 1), f"Contraintes : {len(cons)} Fixed entre briques (≥ 30), {brk} cassables avec seuil 0,3–3 (≥ 90 %)", "Connect puis Breaking, Threshold 1.", 7)
    flag = bpy.data.objects.get("Flag")
    cm = next((m for m in flag.modifiers if m.type == "CLOTH"), None) if flag else None
    pin = cm.settings.vertex_group_mass if cm else ""
    npin = 0
    if flag and pin and pin in flag.vertex_groups:
        gi = flag.vertex_groups[pin].index
        npin = sum(1 for v in flag.data.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups))
    r.check(cm is not None and npin >= 10, f"Tissu : Flag avec Cloth, groupe d'épinglage « {pin} » de {npin} sommets (≥ 10)", "Cloth > Shape > Pin Group.", 6)
    dust = bpy.data.objects.get("Dust")
    ps = dust.particle_systems[0] if dust and dust.particle_systems else None
    r.check(ps is not None and ps.settings.count >= 100, f"Particules : Dust avec {ps.settings.count if ps else 0} particules (≥ 100)", "Reprenez CH08.04.", 5)
    wd = bpy.data.objects.get("FORCE_Wind")
    fw = wd.field if wd and wd.field and wd.field.type == "WIND" else None
    zx = wd.matrix_world.to_3x3().col[2].normalized().x if wd else 0.0
    r.check(fw is not None and fw.strength >= 20 and zx >= 0.9, f"Vent : {'champ Wind' if fw else 'absent'}, force {fw.strength if fw else 0:.0f} (≥ 20), direction x = {zx:.2f} (≥ 0,9)", "Reprenez CH08.09 (rotation Y +90°).", 6)
    if not (flag and cm and ps and bricks and w):
        return r.finish()
    rest = {b.name: b.matrix_world.translation.copy() for b in bricks}
    idx = {}
    for b in bricks:
        parts = b.name.split("_")
        if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            idx[(int(parts[1]), int(parts[2]))] = b.name
    pairs = [(idx[(i, k)], idx[(i + di, k + dk)]) for (i, k) in idx for di, dk in ((1, 0), (0, 1)) if (i + di, k + dk) in idx]
    sc.frame_set(1)
    m0 = np.array([v.co[:] for v in flag.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices])
    dust_alive, dust_x, mid = 0, 0.0, None
    for f in range(1, sc.frame_end + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f == 120:
            ev = dust.evaluated_get(bpy.context.evaluated_depsgraph_get())
            P = np.array([p.location[:] for p in ev.particle_systems[0].particles if p.alive_state == "ALIVE"])
            dust_alive = len(P)
            dust_x = float(P[:, 0].mean()) if len(P) else 0.0
    end = {b.name: b.matrix_world.translation.copy() for b in bricks}
    fl = np.array([v.co[:] for v in flag.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices])
    sc.frame_set(1)
    broken = sum(1 for a, b in pairs if abs((end[a] - end[b]).length - (rest[a] - rest[b]).length) > 0.1)
    zmin = min(p.z for p in end.values())
    top, low = m0[:, 2] > m0[:, 2].max() - 0.01, m0[:, 2] < m0[:, 2].min() + 0.01
    topmove = float(np.abs(fl[top] - m0[top]).max())
    dx = float((fl[low][:, 0] - m0[low][:, 0]).mean())
    r.check(8 <= broken <= 30 and zmin >= 0.05, f"Destruction simulée : {broken} liaisons cassées sur {len(pairs)} (8–30) ; z minimal d'une brique {zmin:.2f} m (≥ 0,05)", "Seuil 1 ; sol Passive ; boulet comme CH08.07.", 8)
    r.check(topmove <= 0.005, f"Drapeau : le haut bouge de {1000 * topmove:.1f} mm (≤ 5 : épinglé)", "Pin Group : les sommets du haut.", 6)
    r.check(dx >= 0.15, f"Drapeau : le bas est poussé de {dx:.2f} m vers +X (≥ 0,15)", "Le vent agit sur le tissu (poids de champ 1, force assez haute).", 7)
    r.check(dust_alive >= 100 and 1.5 <= dust_x <= 15, f"Poussière à l'image 120 : {dust_alive} particules, x moyen {dust_x:.1f} m (≥ 100 ; 1,5–15)", "Field Weights de la poussière : un vent atténué (0,01).", 7)
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p8_contact_sheet.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        ok_img = W >= 1600 and px.mean() > 0.05 and px.std() > 0.03
        msg = f"{W} × {H}, moyenne {px.mean():.2f}, écart-type {px.std():.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche renders/p8_contact_sheet.png : {msg}", "Quatre images de la séquence côte à côte, ≥ 1 600 px de large.", 4)
    if debug:
        print("[DEBUG] n", n, "bricks", len(bricks), "cons", len(cons), "brk", brk, "npin", npin, "broken", broken, "zmin", round(zmin, 2), "top", round(topmove, 4), "dx", round(dx, 3), "dust", dust_alive, round(dust_x, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
