"""
validate_ch03_10.py — Correcteur « Personnage prêt pour le rig » (CH03.10).
Usage : … --python-exit-code 1 --python validate_ch03_10.py -- --exercise rigready [--render] [--debug]
Convention : Z haut, personnage face à −Y, pieds sur z = 0, origine en (0, 0, 0) entre les pieds.
Nommage : objet `CHR_<Nom>_Body`, données `ME_CHR_<Nom>_Body`, collection `CHR_<Nom>`, aucun suffixe .001.
Transformations appliquées (échelle 1, rotation 0, position 0). Volume fermé. Taille 1,55–1,95 m, pieds au sol (±1 cm).
Origine entre les pieds ; avant = −Y (les orteils dépassent vers −Y). Symétrie X (≥ 97 % à 5 mm). Pose A (bras à 30–55° de la
verticale) ou T (80–100°), bras symétriques. Pieds écartés de 18–45 cm. Maillage propre (pas de sommets isolés, pas de doublons).
Testé avec : Blender 5.3.0.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

SYM_MIN = 0.97


def components(bm):
    seen, n = set(), 0
    for v in bm.verts:
        if v.index in seen:
            continue
        n += 1
        st = [v]
        seen.add(v.index)
        while st:
            x = st.pop()
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    st.append(o)
    return n


def arm_angle(P, side):
    sel = P[(P[:, 0] * side > 0.30) & (P[:, 2] > 0.5)]
    if len(sel) < 30:
        return None
    c = sel - sel.mean(0)
    _u, _s, vt = np.linalg.svd(c, full_matrices=False)
    d = vt[0]
    return math.degrees(math.atan2(abs(d[0]), abs(d[2])))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH03.10 — Personnage prêt pour le rig")
    cands = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.name.startswith("GEO_")]
    named = [o for o in cands if re.fullmatch(r"CHR_[A-Za-z0-9]+_Body", o.name)]
    ob = named[0] if named else (cands[0] if cands else None)
    if not r.check(ob is not None, "Un objet maillage de personnage", "Le personnage doit être dans la scène.", 2):
        return r.finish()
    # nommage
    nm = ob.name
    ok_name = bool(re.fullmatch(r"CHR_[A-Za-z0-9]+_Body", nm))
    r.check(ok_name, f"Nom d'objet « {nm} » conforme à CHR_<Nom>_Body", "Renommez (F2) : CHR_Hero_Body (pas de .001, pas d'espace).", 3)
    r.check(ok_name and ob.data.name == "ME_" + nm, f"Données « {ob.data.name} » = ME_{nm}", "Renommez aussi les données du maillage (Object Data > nom).", 1)
    owner = ok_name and any(c.name == "CHR_" + nm.split("_")[1] and ob.name in c.objects for c in bpy.data.collections)
    r.check(owner, "Objet dans une collection CHR_<Nom> (ex. CHR_Hero)", "Créez la collection et déplacez-y l'objet (M).", 1)
    # transformations
    sc_ok = all(abs(v - 1.0) < 1e-4 for v in ob.scale)
    rot_ok = all(abs(v) < 1e-4 for v in ob.rotation_euler)
    loc_ok = all(abs(v) < 1e-4 for v in ob.location)
    r.check(sc_ok and rot_ok and loc_ok,
            f"Transformations appliquées : échelle {tuple(round(v, 3) for v in ob.scale)}, rotation {tuple(round(math.degrees(v), 1) for v in ob.rotation_euler)}°, position {tuple(round(v, 3) for v in ob.location)}",
            "Object > Apply > All Transforms ; l'origine doit être en (0, 0, 0) (Set Origin > Origin to 3D Cursor, curseur à l'origine).", 4)
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(ob.matrix_world)
    bm.verts.ensure_lookup_table()
    nc = components(bm)
    nm_e = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nc == 1 and nm_e == 0, f"Un seul volume fermé ({nc} morceau(x), {nm_e} arête(s) ouvertes)", "Voxel Remesh / Fill ; un seul maillage pour le corps.", 2)
    P = np.array([v.co[:] for v in bm.verts])
    H = P[:, 2].max() - P[:, 2].min()
    r.check(1.55 <= H <= 1.95, f"Taille {H:.2f} m (1,55–1,95)", "Échelle réelle : ≈ 1,76 m (maillage en cm ? appliquez l'échelle).", 2)
    r.check(abs(P[:, 2].min()) <= 0.01, f"Pieds au sol (z min = {P[:, 2].min() * 100:.1f} cm ; ±1)", "Les pieds sur z = 0.", 2)
    feet = P[P[:, 2] < P[:, 2].min() + 0.06]
    fx = float(feet[:, 0].mean()) if len(feet) else 0.0
    r.check(abs(fx) <= 0.02 and feet[:, 1].min() - 0.02 <= 0.0 <= feet[:, 1].max() + 0.02,
            f"Origine entre les pieds (centre des pieds x = {fx * 100:.1f} cm, y de {feet[:, 1].min() * 100:.0f} à {feet[:, 1].max() * 100:.0f} cm)",
            "Centrez le personnage entre les pieds, origine au sol.", 2)
    front = abs(feet[:, 1].min()) > abs(feet[:, 1].max()) + 0.04 if len(feet) else False
    r.check(front, "Face vers −Y (les orteils dépassent vers −Y)", "Pivotez le personnage (rotation Z) pour qu'il regarde −Y, puis appliquez.", 3)
    # symétrie
    inv = ob.matrix_world.inverted()
    samp = P[:: max(1, len(P) // 1500)]
    dists = []
    for p in samp:
        ok, loc, _n, _i = ob.closest_point_on_mesh(inv @ Vector((-p[0], p[1], p[2])))
        if ok:
            dists.append(((ob.matrix_world @ loc) - Vector((-p[0], p[1], p[2]))).length)
    sym = float(np.mean(np.array(dists) <= 0.005)) if dists else 0.0
    r.check(sym >= SYM_MIN, f"Symétrie X : {100 * sym:.0f} % des points à moins de 5 mm de leur miroir (≥ {100 * SYM_MIN:.0f})", "Symmetrize ou Mirror ; un personnage à rigger doit être symétrique.", 3)
    # pose
    aL, aR = arm_angle(P, 1), arm_angle(P, -1)
    if aL is None or aR is None:
        pose = None
    else:
        pose = "A" if 30 <= (aL + aR) / 2 <= 55 else ("T" if 80 <= (aL + aR) / 2 <= 100 else None)
    r.check(pose is not None and abs(aL - aR) <= 6,
            f"Pose {'en ' + pose if pose else 'non conforme'} : bras à {0 if aL is None else aL:.0f}° / {0 if aR is None else aR:.0f}° de la verticale (A : 30–55, T : 80–100)",
            "Écartez les bras : pose en A (≈ 40°) ou en T (90°) ; bras le long du corps = épaules impossibles à rigger.", 3)
    cl = P[P[:, 2] < 0.08]
    cxl = cl[cl[:, 0] > 0][:, 0].mean() if (cl[:, 0] > 0).any() else 0.0
    cxr = cl[cl[:, 0] < 0][:, 0].mean() if (cl[:, 0] < 0).any() else 0.0
    gap = cxl - cxr
    r.check(0.18 <= gap <= 0.45, f"Pieds écartés de {gap * 100:.0f} cm (18–45)", "Jambes légèrement écartées : le rig des hanches en dépend.", 1)
    # propreté
    loose = sum(1 for v in bm.verts if not v.link_edges)
    kd = KDTree(len(bm.verts))
    for i, v in enumerate(bm.verts):
        kd.insert(v.co, i)
    kd.balance()
    dup = 0
    step = max(1, len(bm.verts) // 3000)
    for i in range(0, len(bm.verts), step):
        if len(kd.find_range(bm.verts[i].co, 1e-5)) > 1:
            dup += 1
    r.check(loose == 0 and dup <= 3, f"Maillage propre : {loose} sommet(s) isolé(s), {dup} doublon(s) détecté(s)", "Select > Select All by Trait > Loose Geometry ; Mesh > Clean Up > Merge by Distance.", 2)
    if debug:
        print(f"[DEBUG] H={H:.3f} zmin={P[:, 2].min():.4f} feet_x={fx:.4f} sym={sym:.3f} arms={aL}/{aR} gap={gap:.3f} pose={pose}")
    bm.free()
    ev.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
