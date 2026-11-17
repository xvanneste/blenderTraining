"""
build_ch06_05_files.py — « Rig humanoïde » (CH06.05 : Rigify).

Le personnage est le CHR_Hero_Body du projet P3 (retopologie de 4 681 quads, 1,76 m, pieds au sol, face à −Y).
  Étapes de la solution : (1) Add > Armature > Human ; (2) mise à l'échelle sur la taille du corps (1,76 / 1,98) et application de l'échelle ;
  (3) Rigify > Generate Rig (objet « rig » -> RIG_Hero, ~700 bones) ; (4) lier CHR_Hero_Body à RIG_Hero (Automatic Weights sur les bones DEF-*), normaliser, limiter à 4 influences.
  STARTER_FILES/ch06_05_humanoid_starter.blend : le corps et un méta-rig humain NON ajusté (hauteur 1,98 m), rien de généré.
  COMPLETED_EXAMPLES/ch06_05_humanoid_solution.blend (+ _reference.png : croquis de face et de profil des bones DEF et du corps, puis jambe levée)
  COUNTER_EXAMPLES/ : not_generated, unskinned, wrong_scale, no_modifier, partial_weights, offset, arms_unfitted
Bras : le méta-rig humain a les bras à ≈ 29° sous l'horizontale et trop courts, le mannequin les a à ≈ 51° (A) : la chaîne du bras (upper_arm et descendants)
         est RECALÉE en Edit Mode (rotation autour de l'épaule + mise à longueur jusqu'au bout des doigts) avant la génération ; contre-exemple arms_unfitted.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_05_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "03_SCULPTING", "PROJECT_P3", "REFERENCE", "p3_character_reference.blend")
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH06.05 — RIG HUMANOÏDE avec Rigify (CHR_Hero_Body, 1,76 m)
1. Add > Armature > Human ; mettre le méta-rig à la taille du corps (échelle ≈ 0,89) puis Ctrl+A > Scale.
2. Ajuster les bras du méta-rig au corps en Edit Mode : sélectionner upper_arm.L et ses enfants, pivot sur le 3D Cursor placé à l'épaule, R (tourner) puis S (allonger)
   jusqu'au bout des doigts ; même chose à droite (ou X-Axis Mirror). Sans cela le coude et la main du rig sont hors du bras.
3. Object Data du méta-rig > Rigify > Generate Rig : un objet « rig » apparaît (renommez-le RIG_Hero).
4. Corps : sélectionner CHR_Hero_Body puis RIG_Hero (actif) : Ctrl+P > With Automatic Weights ; Weights > Normalize All ; Limit Total 4.
Le correcteur vérifie : rig généré (≥ 400 bones, noms DEF-/MCH-/ORG-, collections), taille 1,76 ± 0,12 m, pieds au sol, centrage sous le corps, peau liée (modificateur, groupes DEF-*, sommets pesés),
bras alignés (coude et bout de la main à ≤ 5 cm du maillage, des deux côtés), puis DÉPLACE le rig : racine (0,5 m), pied gauche levé de 0,25 m : le bon côté du corps suit, la tête et le pied droit restent.
Vérification : SCRIPTS/validate_ch06_05.py -- --exercise humanoid
"""


def prepare_scene():
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(SRC))
    body = bpy.data.objects["CHR_Hero_Body"]
    for n in ("HIGH_Hero",):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    for o in list(bpy.data.objects):
        if o.type in ("LIGHT", "EMPTY") or o.name.startswith("GEO_"):
            pass
    bpy.ops.preferences.addon_enable(module="rigify")
    return body


def add_meta(fit=True, offset=0.0):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.armature_human_metarig_add()
    meta = bpy.context.active_object
    meta.name = "META_Hero"
    if fit:
        meta.scale = (1.759 / 1.9796,) * 3
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action="DESELECT")
        meta.select_set(True)
        bpy.context.view_layer.objects.active = meta
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    meta.location.x += offset
    return meta


def chain(eb_root):
    out = [eb_root]
    for c in eb_root.children_recursive:
        out.append(c)
    return out


def fit_arms(meta, body):
    """Place les articulations de chaque bras du méta-rig sur l'axe du bras du maillage (axe principal des sommets |x| > 0,25 m) :
    épaule gardée, coude et poignet sur l'axe (coude reculé de 1,5 cm pour donner le sens de pliage à l'IK), main + doigts tournés
    sur l'axe ; longueurs du méta-rig mises à l'échelle jusqu'au bout des doigts du maillage."""
    V = np.array([body.matrix_world @ v.co for v in body.data.vertices])
    bpy.ops.object.select_all(action="DESELECT")
    meta.select_set(True)
    bpy.context.view_layer.objects.active = meta
    bpy.ops.object.mode_set(mode="EDIT")
    ebs = meta.data.edit_bones
    for side, sgn in (("L", 1), ("R", -1)):
        ua, fa, hd = ebs[f"upper_arm.{side}"], ebs[f"forearm.{side}"], ebs[f"hand.{side}"]
        arm = V[sgn * V[:, 0] > 0.25]
        c = arm.mean(0)
        d = np.linalg.svd(arm - c)[2][0]
        if sgn * d[0] < 0:
            d = -d
        h = ua.head.copy()
        hn = np.array(h[:])
        # l'axe passe par le centre des sommets : projeter l'épaule dessus pour l'origine des longueurs
        reach = float(((arm - hn) @ d).max())
        D = Vector(d)
        hand_bones = chain(hd)
        w0 = hd.head.copy()
        tip = max(((bb.tail - w0).length for bb in hand_bones))
        l1, l2 = ua.length, fa.length
        k = reach * 0.97 / (l1 + l2 + tip)
        axis_pt = Vector(c) + D * float((hn - c) @ d)          # point de l'axe au niveau de l'épaule
        e = axis_pt + D * (l1 * k) + Vector((0, 0.015, 0))
        w = axis_pt + D * ((l1 + l2) * k)
        q_arm = (fa.tail - ua.head).normalized().rotation_difference(D)
        z_ua, z_fa = q_arm @ ua.z_axis, q_arm @ fa.z_axis
        q_hand = (hd.tail - hd.head).normalized().rotation_difference(D)
        M = Matrix.Translation(w) @ Matrix.Scale(k, 4) @ q_hand.to_matrix().to_4x4() @ Matrix.Translation(-w0)
        for bb in hand_bones:
            bb.transform(M, scale=True, roll=True)
        ua.tail = e
        fa.head = e
        fa.tail = w
        ua.align_roll(z_ua)
        fa.align_roll(z_fa)
        print(f"[fit_arms] {side} axe {np.degrees(np.arctan2(-d[2], abs(d[0]))):.1f}° sous l'horizontale, échelle {k:.3f}, coude {tuple(round(x, 3) for x in e)}, poignet {tuple(round(x, 3) for x in w)}")
    bpy.ops.object.mode_set(mode="OBJECT")


def generate(meta):
    bpy.ops.object.select_all(action="DESELECT")
    meta.select_set(True)
    bpy.context.view_layer.objects.active = meta
    bpy.ops.object.mode_set(mode="OBJECT")
    r = bpy.ops.pose.rigify_generate()
    print("[rigify]", r, [o.name for o in bpy.data.objects if o.type == "ARMATURE"])
    rig = bpy.data.objects.get("rig") or next(o for o in bpy.data.objects if o.type == "ARMATURE" and o != meta)
    rig.name = "RIG_Hero"
    rig.data.name = "ARM_RIG_Hero"
    return rig


def skin(body, rig):
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    r = bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    assert "FINISHED" in r, r
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
    bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=4)
    bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)


def build(kind):
    body = prepare_scene()
    meta = add_meta(fit=(kind not in ("starter", "wrong_scale")))
    if kind not in ("starter", "wrong_scale", "arms_unfitted"):
        fit_arms(meta, body)
    if kind == "starter":
        L.instructions(NOTE)
        return body, meta, None
    rig = generate(meta)
    if kind == "offset":                                   # rig décalé de 50 cm en X par rapport au corps (la génération ignore la position du méta-rig)
        rig.location.x = 0.5
    if kind == "not_generated":
        bpy.data.objects.remove(rig, do_unlink=True)
        rig = None
    elif kind != "unskinned":
        skin(body, rig)
        if kind == "no_modifier":
            for m in list(body.modifiers):
                body.modifiers.remove(m)
        elif kind == "partial_weights":
            idx = [v.index for v in body.data.vertices if v.co.z < 0.5]
            for g in body.vertex_groups:
                g.remove(idx)
    L.instructions(NOTE)
    return body, meta, rig


def sketch(body, rig, path):
    """Croquis de face (x, z) : sommets du corps, bones DEF-*, puis pied gauche levé de 0,25 m."""
    S_W, S_H = 360, 560
    tiles = []
    for lift in (0.0, 0.25):
        img = np.zeros((S_H, S_W, 3), np.float32)
        img[...] = 0.08
        if lift:
            pb = rig.pose.bones["foot_ik.L"]
            pb.location = pb.bone.matrix_local.to_3x3().inverted() @ __import__("mathutils").Vector((0, 0, lift))
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        ev_b = body.evaluated_get(dg)
        me = ev_b.to_mesh()
        V = np.array([v.co[:] for v in me.vertices])
        ev_b.to_mesh_clear()
        for p in V[::2]:
            x, y = int(S_W / 2 + p[0] * 150), int(S_H - 20 - p[2] * 290)
            if 0 <= x < S_W and 0 <= y < S_H:
                img[y, x] = (0.4, 0.4, 0.45)
        evr = rig.evaluated_get(dg)
        for b in evr.pose.bones:
            if not b.name.startswith("DEF-"):
                continue
            h, t = evr.matrix_world @ b.head, evr.matrix_world @ b.tail
            x0, y0 = int(S_W / 2 + h.x * 150), int(S_H - 20 - h.z * 290)
            x1, y1 = int(S_W / 2 + t.x * 150), int(S_H - 20 - t.z * 290)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < S_W and 0 <= y < S_H:
                    img[y, x] = (0.95, 0.6, 0.15) if b.name.endswith(".L") else ((0.3, 0.7, 1.0) if b.name.endswith(".R") else (0.9, 0.9, 0.3))
        tiles.append(img)
    sheet = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([sheet, np.ones(sheet.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", sheet.shape[1], S_H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    rig.pose.bones["foot_ik.L"].location = (0, 0, 0)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_05_humanoid_starter.blend"))
    for k in ("not_generated", "unskinned", "wrong_scale", "no_modifier", "partial_weights", "offset", "arms_unfitted"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_05_humanoid_{k}.blend"))
    body, meta, rig = build("solution")
    L.save(os.path.join(out, "ch06_05_humanoid_solution.blend"))
    sketch(body, rig, os.path.join(out, "ch06_05_humanoid_reference.png"))


if __name__ == "__main__":
    L.run(main)
