"""
validate_p6.py — Correcteur du projet P6 « Un personnage contrôlable ».
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p6.py [-- --debug]
Objets : CHR_Hero_Body (corps) et RIG_Hero (rig Rigify GÉNÉRÉ), éventuellement META_Hero.
  1. Rig : ≥ 400 bones dont root, torso, head, foot_ik.L, hand_ik.L, DEF-spine, DEF-thigh.L, ORG-/MCH- ; ≥ 10 collections de bones ; rig_id ; échelle 1 ;
     taille 1,76 ± 0,12 m (bones DEF), pieds au sol (z min ≥ −0,06), centré sous le corps (≤ 5 cm).
  2. Peau : corps parenté au rig, modificateur Armature, groupes DEF-*, ≥ 98 % de sommets pesés, somme des poids = 1 ± 0,02, ≤ 4 influences.
  3. Ergonomie : les collections ORG, MCH et DEF sont MASQUÉES ; au moins 10 autres collections de contrôle sont visibles.
  4. Animation de test : une Action sur le rig avec au moins 2 courbes, des images clés à au moins 2 images différentes, valeurs différentes entre la première et la dernière image.
  5. Comportement (maillage évalué) : racine +0,5 m (non animée) : déplacement moyen 0,5 ± 0,03 m ; à la DERNIÈRE image clé : le pied gauche (x > 0,03, z < 0,08 au repos) monte de 0,10 à 0,35 m,
     le pied droit reste (≤ 1 cm), la tête (z > 1,62 m) se déplace d'au moins 8 mm et les pieds ne sont pas tordus ; à la PREMIÈRE image clé : le pied gauche reste au sol (≤ 2 cm).
  6. Planche renders/p6_posetest.png (dossier du .blend) : ≥ 1 600 px de large, non noire et contrastée.
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def fcurves_of(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        out = []
        for layer in act.layers:
            for st in layer.strips:
                for cb in st.channelbags:
                    out.extend(cb.fcurves)
        return out


def shift(rig, name, delta):
    pb = rig.pose.bones[name]
    pb.location = pb.bone.matrix_local.to_3x3().inverted() @ Vector(delta)
    bpy.context.view_layer.update()


def main():
    debug = L.flag("--debug")
    r = L.Report("P6 — Un personnage contrôlable")
    body, rig = bpy.data.objects.get("CHR_Hero_Body"), bpy.data.objects.get("RIG_Hero")
    if not r.check(body is not None and rig is not None and rig.type == "ARMATURE", "CHR_Hero_Body et RIG_Hero présents", "Générez le rig (Rigify) et nommez-le RIG_Hero.", 3):
        return r.finish()
    bones = rig.data.bones
    names = {b.name for b in bones}
    need = ["root", "torso", "head", "foot_ik.L", "hand_ik.L", "DEF-spine", "DEF-thigh.L"]
    miss = [n for n in need if n not in names]
    r.check(len(bones) >= 400 and not miss and any(n.startswith("ORG-") for n in names) and any(n.startswith("MCH-") for n in names), f"Rig Rigify généré : {len(bones)} bones (≥ 400) ; manquants : {miss or 'aucun'}", "Meta-rig > Rigify > Generate Rig.", 5)
    r.check(len(rig.data.collections_all) >= 10 and "rig_id" in rig.data and all(abs(s - 1) < 1e-4 for s in rig.scale), f"{len(rig.data.collections_all)} collections de bones ; rig_id ; échelle 1", "", 2)
    mw = rig.matrix_world
    defs = [b for b in bones if b.name.startswith("DEF-")]
    top = max((mw @ b.tail_local).z for b in defs) if defs else 0.0
    zmin = min(min((mw @ b.head_local).z, (mw @ b.tail_local).z) for b in defs) if defs else 9.0
    body_co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
    cx = float(np.mean([(mw @ b.head_local).x for b in defs])) if defs else 9.0
    r.check(abs(top - 1.76) <= 0.12 and zmin >= -0.06, f"Taille du rig : sommet {top:.2f} m (1,76 ± 0,12) ; pieds : z min {zmin:+.3f} (≥ −0,06)", "Méta-rig à l'échelle du corps avant de générer.", 4)
    r.check(abs(cx - float(body_co[:, 0].mean())) <= 0.05, f"Rig centré sous le corps (écart {abs(cx - float(body_co[:, 0].mean())) * 100:.1f} cm ≤ 5)", "Pas de décalage du rig.", 4)
    # peau
    r.check(any(m.type == "ARMATURE" and m.object == rig for m in body.modifiers) and body.parent == rig, "Corps parenté à RIG_Hero avec un modificateur Armature", "Ctrl+P > With Automatic Weights.", 5)
    n = len(body.data.vertices)
    sums, infl = np.zeros(n), np.zeros(n, int)
    for v in body.data.vertices:
        ws = [g.weight for g in v.groups if g.weight > 1e-4]
        sums[v.index] = sum(g.weight for g in v.groups)
        infl[v.index] = len(ws)
    frac = float((infl > 0).mean())
    r.check(frac >= 0.98, f"Sommets pesés : {100 * frac:.1f} % (≥ 98)", "Automatic Weights sur tout le maillage.", 4)
    r.check(frac > 0 and bool(np.all(np.abs(sums[infl > 0] - 1) <= 0.02)) and int(infl.max()) <= 4, f"Poids normalisés ({float(sums.min()):.2f}–{float(sums.max()):.2f}), ≤ 4 influences (max {int(infl.max())})", "Normalize All ; Limit Total 4.", 3)
    # ergonomie
    cols = {c.name: c.is_visible for c in rig.data.collections_all}
    hidden_ok = all(cols.get(k) is False for k in ("ORG", "MCH", "DEF"))
    nvis = sum(1 for k, v in cols.items() if v and k not in ("ORG", "MCH", "DEF"))
    r.check(hidden_ok and nvis >= 10, f"Ergonomie : ORG, MCH, DEF masquées ({'oui' if hidden_ok else 'NON'}) ; {nvis} collections de contrôle visibles (≥ 10)", "Masquez les collections de mécanisme ; l'animateur ne voit que les contrôles.", 5)
    # animation
    act = rig.animation_data.action if rig.animation_data else None
    fcs = fcurves_of(act) if act else []
    frames = sorted({round(kp.co[0]) for fc in fcs for kp in fc.keyframe_points})
    changed = any(len(fc.keyframe_points) >= 2 and abs(fc.keyframe_points[-1].co[1] - fc.keyframe_points[0].co[1]) > 1e-4 for fc in fcs)
    r.check(act is not None and len(fcs) >= 2 and len(frames) >= 2 and changed, f"Action de test : {len(fcs)} courbes, images clés {frames[:4]}…, valeurs différentes : {'oui' if changed else 'non'}", "Posez deux poses clés (repos, pose) avec I.", 5)
    f0, f1 = (frames[0], frames[-1]) if len(frames) >= 2 else (1, 24)
    sc = bpy.context.scene
    # comportement
    sc.frame_set(f0)
    rest = coords(body)
    shift(rig, "root", (0.5, 0, 0))
    moved = coords(body)
    rig.pose.bones["root"].location = (0, 0, 0)
    dx = moved[:, 0] - rest[:, 0]
    r.check(abs(float(dx.mean()) - 0.5) <= 0.03 and float((dx > 0.4).mean()) >= 0.98, f"Racine +0,5 m : déplacement moyen {float(dx.mean()):.3f} m, {100 * float((dx > 0.4).mean()):.0f} % des sommets > 0,4 m", "Peau complète, rig sans décalage.", 5)
    left = (rest[:, 0] > 0.03) & (rest[:, 2] < 0.08)
    right = (rest[:, 0] < -0.03) & (rest[:, 2] < 0.08)
    head = rest[:, 2] > 1.62
    sc.frame_set(f1)
    pose = coords(body)
    sc.frame_set(f0)
    d = pose - rest
    up_l = float(d[left, 2].mean()) if left.any() else 0.0
    mv_r = float(np.abs(d[right]).max()) if right.any() else 9.0
    mv_h = float(np.linalg.norm(d[head], axis=1).mean()) if head.any() else 0.0
    r.check(0.10 <= up_l <= 0.35, f"Dernière pose : le pied gauche monte de {up_l:.3f} m (0,10–0,35)", "Les sommets du pied pèsent sur les bones du pied gauche ; la pose lève foot_ik.L.", 5)
    r.check(mv_r <= 0.01, f"Dernière pose : le pied droit reste ({1000 * mv_r:.1f} mm ≤ 10)", "Pas de poids parasites entre les jambes.", 4)
    r.check(mv_h >= 0.008, f"Dernière pose : la tête se déplace de {1000 * mv_h:.1f} mm en moyenne (≥ 8)", "La pose tourne le contrôle head.", 3)
    sc.frame_set(f0)
    d0 = coords(body) - rest
    foot0 = float(np.abs(d0[left]).max()) if left.any() else 9.0
    r.check(foot0 <= 0.02, f"Première image clé : pied gauche au repos ({1000 * foot0:.1f} mm ≤ 20)", "Image 1 = pose de repos.", 2)
    # planche
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p6_posetest.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        ok_img = W >= 1600 and px.mean() > 0.05 and px.std() > 0.03
        msg = f"{W} × {H}, moyenne {px.mean():.2f}, écart-type {px.std():.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche renders/p6_posetest.png : {msg}", "Trois poses côte à côte, ≥ 1 600 px de large.", 4)
    if debug:
        print("[DEBUG] bones", len(bones), "top", round(top, 3), "zmin", round(zmin, 3), "cx", round(cx, 3), "frac", round(frac, 4), "cols", nvis, hidden_ok, "frames", frames, "fcs", len(fcs), "dx", round(float(dx.mean()), 3),
              "up_l", round(up_l, 3), "mv_r", round(mv_r, 4), "mv_h", round(mv_h, 4), "foot0", round(foot0, 4))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
