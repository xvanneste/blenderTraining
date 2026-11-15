"""
validate_ch03_04.py — Correcteur « Le buste stylisé » (CH03.04).
Usage : … --python validate_ch03_04.py --python-exit-code 1 -- --exercise bust [--render]
SCULPT_Bust : un seul volume fermé ; socle plat ; buste 0,3–0,9 m ; cou repéré (largeur minimale) ;
stylisation : tête ≥ 45 % de la hauteur OU contraste tête/épaules ≥ 25 % ; nez en relief sur le profil
(saillie ≥ 2 cm par rapport au profil voisin), cou marqué ; symétrie X (surface miroir à moins de 1 cm).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402


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


def main():
    r = L.Report("CH03.04 — Le buste stylisé")
    ob = bpy.data.objects.get("SCULPT_Bust")
    if not r.check(ob is not None and ob.type == "MESH", "Objet SCULPT_Bust (maillage)", "Convertissez/renommez votre buste.", 2):
        return r.finish()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(ob.matrix_world)
    bm.verts.ensure_lookup_table()
    nc = components(bm)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nc == 1 and nm == 0, f"Un seul volume fermé ({nc} morceau(x), {nm} arête(s) ouvertes)",
            "Chevauchements + Voxel Remesh (CH03.03), socle rebouché.", 3)
    r.check(3000 <= len(bm.faces) <= 1_500_000, f"{len(bm.faces)} faces (3 000 – 1 500 000)", "", 1)
    P = np.array([v.co[:] for v in bm.verts])
    z0, z1 = P[:, 2].min(), P[:, 2].max()
    Hb = z1 - z0
    r.check(0.3 <= Hb <= 0.9, f"Hauteur du buste {Hb:.2f} m (0,3–0,9)", "Échelle réelle d'un buste.", 1)
    base_area = sum(f.calc_area() for f in bm.faces if f.normal.z < -0.95 and abs(f.calc_center_median().z - z0) < 0.003)
    r.check(base_area >= 0.008, f"Socle plat ({base_area * 1e4:.0f} cm² de face horizontale en bas)",
            "Mesh > Bisect (Clear Inner, Fill) ou Boolean.", 2)
    # profil de largeur : cou = largeur minimale entre 25 % et 75 % de la hauteur
    zs = np.linspace(z0 + 0.25 * Hb, z0 + 0.75 * Hb, 40)
    widths = []
    for z in zs:
        sl = P[np.abs(P[:, 2] - z) < Hb / 40]
        widths.append(sl[:, 0].max() - sl[:, 0].min() if len(sl) >= 8 else np.inf)   # tranche trop pauvre : ignorée
    neck_z = zs[int(np.argmin(widths))]
    neck_w = min(widths)
    head = P[P[:, 2] > neck_z]
    body = P[P[:, 2] < neck_z]
    hw0 = head[:, 0].max() - head[:, 0].min() if len(head) else 0
    sw0 = body[:, 0].max() - body[:, 0].min() if len(body) else 0
    r.check(hw0 >= 1.3 * neck_w and sw0 >= 1.3 * neck_w,
            f"Cou marqué (largeur {neck_w * 100:.1f} cm ; tête {hw0 * 100:.1f}, épaules {sw0 * 100:.1f})",
            "Un buste = tête + cou + épaules : le cou doit être nettement plus étroit.", 2)
    head_ratio = (z1 - neck_z) / Hb
    hw = head[:, 0].max() - head[:, 0].min()
    sw = body[:, 0].max() - body[:, 0].min()
    contrast = max(hw, sw) / max(min(hw, sw), 1e-6)
    r.check(head_ratio >= 0.45 or contrast >= 1.25,
            f"Stylisation : tête {100 * head_ratio:.0f} % de la hauteur, contraste tête/épaules ×{contrast:.2f}",
            "Exagérez : grosse tête (≥ 45 %) ou fort contraste de largeur (≥ 25 %).", 3)
    # nez : saillie du profil central (|x| petit) par rapport aux hauteurs voisines
    front = head[np.abs(head[:, 0]) < 0.012]
    hh = z1 - neck_z
    best = 0.0
    if len(front):
        zz = np.linspace(neck_z + 0.15 * hh, z1 - 0.15 * hh, 30)
        prof = []
        for z in zz:
            sl = front[np.abs(front[:, 2] - z) < hh / 60]
            prof.append(sl[:, 1].min() if len(sl) else np.nan)
        prof = np.array(prof)
        k = max(2, int(0.15 * len(zz) / 0.7))
        for i in range(k, len(zz) - k):
            if np.isnan(prof[i]) or np.isnan(prof[i - k]) or np.isnan(prof[i + k]):
                continue
            best = max(best, (prof[i - k] + prof[i + k]) / 2 - prof[i])
    r.check(best >= 0.02, f"Nez en relief sur le profil (saillie {best * 100:.1f} cm, ≥ 2)", "Ajoutez/accentuez le nez (Clay Strips, Inflate).", 2)
    # symétrie : distance du point miroir à la surface
    samp = P[:: max(1, len(P) // 1500)]
    dists = []
    for p in samp:
        ok, loc, _n, _i = ob.closest_point_on_mesh(ob.matrix_world.inverted() @ Vector((-p[0], p[1], p[2])))
        if ok:
            dists.append(((ob.matrix_world @ loc) - Vector((-p[0], p[1], p[2]))).length)
    sym = np.mean(np.array(dists) <= 0.01) if dists else 0
    r.check(sym >= 0.95, f"Symétrie X ({100 * sym:.0f} % des points à moins de 1 cm de leur miroir)", "Mirror X (Sculpt) ou Symmetrize.", 2)
    bm.free()
    ev.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
