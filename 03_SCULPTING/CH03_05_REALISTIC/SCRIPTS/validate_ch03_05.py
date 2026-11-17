"""
validate_ch03_05.py — Correcteur « Le buste réaliste » (CH03.05).
Usage : … --python-exit-code 1 --python validate_ch03_05.py -- --exercise bust [--render] [--debug]
SCULPT_Bust : un seul volume fermé, socle plat, échelle réelle (0,38–0,70 m) ; cou marqué ; deux globes
EYE_L / EYE_R symétriques ; PROPORTIONS mesurées sur le maillage (hauteur de tête, rapport largeur/hauteur,
yeux à mi-hauteur, écart des yeux, nez en saillie à la bonne hauteur) ; symétrie ; détails SECONDAIRES
(plis, sillons : sommets en creux ≥ 0,5 mm sous la surface lissée) et TERTIAIRES (grain de peau : médiane de l'écart fin).
Les seuils ont été calibrés sur la solution ET sur des fichiers faux (voir COUNTER_EXAMPLES).
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


def profile_front(P, z, half=0.012, tol=0.003):
    """y minimal (point le plus en avant) de la tranche z, sur la bande centrale |x| < half."""
    sl = P[(np.abs(P[:, 0]) < half) & (np.abs(P[:, 2] - z) < tol)]
    return sl[:, 1].min() if len(sl) else np.nan


def smoothed(P, E, iterations):
    """Surface lissée (Taubin λ/μ) : sert de référence « sans détail » à l'échelle ≈ sqrt(iterations) × arête."""
    n = len(P)
    a, b = E[:, 0], E[:, 1]
    deg = np.bincount(np.concatenate([a, b]), minlength=n).astype(float)
    deg[deg == 0] = 1
    Q = P.copy()
    for _ in range(iterations):
        for f in (0.5, -0.53):
            acc = np.zeros_like(Q)
            np.add.at(acc, a, Q[b])
            np.add.at(acc, b, Q[a])
            Q += f * (acc / deg[:, None] - Q)
    return Q


def detail_measures(P, N, E, mask):
    """Renvoie (creux, grain) :
    creux = % de sommets du visage situés ≥ 0,5 mm SOUS la surface lissée (k = 8) : plis et sillons (secondaire) ;
    grain = médiane (µm) de l'écart à la surface très peu lissée (k = 1) : grain de peau généralisé (tertiaire).
    La médiane ignore les rares plis ; le comptage de creux ignore le grain (trop peu profond)."""
    if not mask.any():
        return 0.0, 0.0
    d8 = 1000.0 * np.einsum("ij,ij->i", smoothed(P, E, 8) - P, N)[mask]
    d1 = 1000.0 * np.einsum("ij,ij->i", smoothed(P, E, 1) - P, N)[mask]
    return 100.0 * float(np.mean(d8 >= 0.5)), 1000.0 * float(np.median(np.abs(d1)))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH03.05 — Le buste réaliste")
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
    closed = nc == 1 and nm == 0
    r.check(closed, f"Un seul volume fermé ({nc} morceau(x), {nm} arête(s) ouvertes)", "Voxel Remesh (CH03.03), socle rebouché.", 3)
    r.check(20_000 <= len(bm.faces) <= 1_500_000, f"{len(bm.faces)} faces (20 000 – 1 500 000)",
            "Assez de géométrie pour des détails fins (Voxel ≈ 2–3 mm ou Multires).", 1)
    P = np.array([v.co[:] for v in bm.verts])
    N = np.array([v.normal[:] for v in bm.verts])
    E = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
    z0, z1 = P[:, 2].min(), P[:, 2].max()
    Hb = z1 - z0
    r.check(0.38 <= Hb <= 0.70, f"Hauteur du buste {Hb * 100:.0f} cm (38–70 : échelle réelle)", "Un buste réaliste est à l'échelle 1.", 2)
    base_area = sum(f.calc_area() for f in bm.faces if f.normal.z < -0.95 and abs(f.calc_center_median().z - z0) < 0.003)
    r.check(base_area >= 0.02, f"Socle plat ({base_area * 1e4:.0f} cm², ≥ 200)", "Mesh > Bisect (Clear Inner, Fill) ou Boolean.", 1)

    # cou : largeur minimale dans la partie centrale
    zs = np.linspace(z0 + 0.3 * Hb, z0 + 0.65 * Hb, 40)
    widths = []
    for z in zs:
        sl = P[np.abs(P[:, 2] - z) < Hb / 50]
        widths.append(sl[:, 0].max() - sl[:, 0].min() if len(sl) >= 8 else np.inf)
    neck_z = zs[int(np.argmin(widths))]
    neck_w = min(widths)
    head = P[P[:, 2] > neck_z]
    # profil de référence du cou : médiane du point le plus en avant, 3 à 6,5 cm SOUS la section la plus étroite
    ref = [profile_front(P, z, 0.02, 0.004) for z in np.arange(neck_z - 0.065, neck_z - 0.03, 0.005)]
    ref = [v for v in ref if not np.isnan(v)]
    neck_front = float(np.median(ref)) if ref else np.nan

    # yeux
    eyes = [bpy.data.objects.get("EYE_L"), bpy.data.objects.get("EYE_R")]

    def world_center(o):          # centre de la boîte englobante en coordonnées monde (l'origine peut être ailleurs)
        pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
        return sum(pts, Vector()) / 8
    have_eyes = all(e is not None for e in eyes)
    r.check(have_eyes, "Globes oculaires EYE_L et EYE_R présents", "Deux sphères nommées EYE_L et EYE_R (≈ 2,5 cm) dans les orbites.", 2)
    eye_z = None
    if have_eyes:
        a, b = (world_center(e) for e in eyes)
        eye_z = (a.z + b.z) / 2
        rad = [max(e.dimensions) / 2 for e in eyes]
        r.check(all(0.009 <= x <= 0.016 for x in rad), f"Globes de {2000 * np.mean(rad):.0f} mm de diamètre (18–32)", "Un œil humain ≈ 24 mm.", 1)
        r.check(abs(abs(a.x) - abs(b.x)) < 0.003 and abs(a.z - b.z) < 0.003 and a.x * b.x < 0,
                f"Yeux symétriques (écart latéral {abs(abs(a.x) - abs(b.x)) * 1000:.1f} mm, hauteur {abs(a.z - b.z) * 1000:.1f} mm)",
                "Placez les deux yeux à la même hauteur, de part et d'autre de x = 0.", 1)

    # chin / hauteur de tête
    chin_z = None
    if eye_z is not None and not np.isnan(neck_front):
        thr = neck_front - 0.02
        z, hits = neck_z - 0.03, 0
        while z < eye_z:
            f = profile_front(P, z)
            hits = hits + 1 if (not np.isnan(f) and f < thr) else 0
            if hits >= 3:                       # 3 tranches de suite : c'est la face inférieure du menton
                chin_z = z - 2 * 0.002
                break
            z += 0.002
    crown = z1
    head_h = (crown - chin_z) if chin_z is not None else 0
    r.check(0.19 <= head_h <= 0.27, f"Hauteur de tête menton→couronne {head_h * 100:.1f} cm (19–27)",
            "Une tête adulte ≈ 23 cm ; le buste doit être à l'échelle réelle.", 2)
    if head_h > 0:
        hw_sl = P[np.abs(P[:, 2] - (crown - 0.06)) < 0.004]
        head_w = hw_sl[:, 0].max() - hw_sl[:, 0].min() if len(hw_sl) else 0
        ratio = head_w / head_h
        r.check(0.55 <= ratio <= 0.80, f"Rapport largeur/hauteur de la tête {ratio:.2f} (0,55–0,80)", "Crâne trop étroit ou trop large.", 2)
        if eye_z is not None:
            eye_pos = (eye_z - chin_z) / head_h
            r.check(0.42 <= eye_pos <= 0.58, f"Yeux à {100 * eye_pos:.0f} % de la hauteur de tête (42–58 : mi-hauteur)",
                    "Règle d'or : la ligne des yeux coupe la tête à la moitié (pas au tiers supérieur).", 3)
            if have_eyes:
                spacing = abs(a.x - b.x)
                r.check(0.35 <= spacing / max(head_w, 1e-6) <= 0.55,
                        f"Écart des yeux {spacing * 100:.1f} cm = {100 * spacing / head_w:.0f} % de la largeur de tête (35–55)",
                        "Entre les deux yeux : à peu près la largeur d'un œil.", 1)
        # nez : pointe la plus en avant entre menton et yeux ; saillie par rapport à la joue
        zz = np.arange(chin_z + 0.02, (eye_z if eye_z else crown) + 0.01, 0.002)
        fr = np.array([profile_front(P, z) for z in zz]) if len(zz) else np.array([np.nan])
        if np.all(np.isnan(fr)):
            fr = np.array([0.0])
            zz = np.array([chin_z])
        tip_i = int(np.nanargmin(fr))
        tip_z, tip_y = zz[tip_i], fr[tip_i]
        cheek = P[(np.abs(P[:, 0]) > 0.035) & (np.abs(P[:, 0]) < 0.06) & (np.abs(P[:, 2] - tip_z) < 0.004)]
        cheek_y = cheek[:, 1].min() if len(cheek) else np.nan
        prot = cheek_y - tip_y
        tip_pos = (tip_z - chin_z) / head_h
        r.check(0.18 <= tip_pos <= 0.42, f"Pointe du nez à {100 * tip_pos:.0f} % de la hauteur de tête depuis le menton (18–42)",
                "Base du nez ≈ au premier tiers du visage en partant du menton.", 2)
        r.check(0.018 <= prot <= 0.05, f"Nez en saillie de {prot * 100:.1f} cm par rapport à la joue (1,8–5)",
                "Trop plat : Clay Strips/Inflate ; trop long : Smooth/Grab.", 2)
    else:
        prot = tip_pos = 0

    # symétrie
    samp = P[:: max(1, len(P) // 1500)]
    inv = ob.matrix_world.inverted()
    dists = []
    for p in samp:
        ok, loc, _n, _i = ob.closest_point_on_mesh(inv @ Vector((-p[0], p[1], p[2])))
        if ok:
            dists.append(((ob.matrix_world @ loc) - Vector((-p[0], p[1], p[2]))).length)
    sym = float(np.mean(np.array(dists) <= 0.005)) if dists else 0
    r.check(sym >= 0.90, f"Symétrie X ({100 * sym:.0f} % des points à moins de 5 mm de leur miroir)",
            "Mirror X en Sculpt Mode ; un visage réel est légèrement asymétrique, pas décalé.", 2)

    if debug:
        print(f"[DEBUG] neck_z={neck_z:.3f} neck_front={neck_front:.3f} chin_z={chin_z} eye_z={eye_z}")
    # détails secondaire / tertiaire sur la zone du visage
    if chin_z is not None:
        face = (P[:, 1] < -0.02) & (np.abs(P[:, 0]) < 0.075) & (P[:, 2] > chin_z) & (P[:, 2] < crown - 0.02) & (N[:, 1] < -0.15)
        sec, ter = detail_measures(P, N, E, face)
        if debug:
            print(f"[DEBUG] creux={sec:.3f} %  grain={ter:.1f} um  verts_face={int(face.sum())}")
        r.check(sec >= SEC_MIN, f"Détails secondaires (plis, sillons) : {sec:.2f} % de sommets en creux ≥ 0,5 mm (≥ {SEC_MIN})",
                "Plis naso-géniens, sillon entre les lèvres, poches sous les yeux : Draw Sharp / Crease.", 3)
        r.check(ter >= TER_MIN, f"Détails tertiaires (rides fines, pores) : grain médian {ter:.1f} µm (≥ {TER_MIN})",
                "Brosse fine ou Multires niveau 4+ ; surface trop lisse = argile, pas une peau.", 3)
    bm.free()
    ev.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


SEC_MIN = 0.03   # % — calibré : solution ≈ 0,10 ; sans plis 0,00
TER_MIN = 10.0   # µm — calibré (voir tests de calibrage en CH03.05)

if __name__ == "__main__":
    L.run(main)
