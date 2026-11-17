"""
validate_ch03_06.py — Correcteur « Le visage » (CH03.06).
Usage : … --python-exit-code 1 --python validate_ch03_06.py -- --exercise face|smile [--render] [--debug]
Base : SCULPT_Bust fermé, EYE_L/EYE_R symétriques, tête 19–27 cm, yeux à mi-hauteur.
face  : paupières (bourrelet autour des deux yeux), narines (deux creux sous le nez), bouche (ligne entre les
        lèvres, largeur ≈ écart des pupilles), oreilles (hélix/conque creusés des deux côtés).
smile : tout `face` + commissures de la bouche relevées d'au moins 4 mm par rapport au centre.
Les creux/reliefs sont mesurés par rapport à REF_Base (copie cachée du buste de départ) : seuils calibrés sur la solution ET sur
des fichiers faux (COUNTER_EXAMPLES). Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH03_05_REALISTIC", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
import validate_ch03_05 as V  # noqa: E402
from mathutils import Vector  # noqa: E402

LID_MIN = 0.10       # fraction de l'anneau relevée ≥ 0,8 mm   (calibré : solution 0,36 ; sans paupières 0,00)
NOSTRIL_MIN = 10     # sommets ≥ 1,5 mm sous la référence, par côté (calibré : solution 18–19 ; sans narines 0)
MOUTH_MIN = 5        # sommets de la ligne ≥ 2,8 mm au centre (calibré : solution 8 ; sans bouche 0)
EAR_MIN = 60         # sommets ≥ 1,2 mm sous la référence, par oreille (calibré : solution ≈ 172 ; sans oreilles 0)
SMILE_MIN = 0.004    # m : relèvement des commissures


def world_center(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return sum(pts, Vector()) / 8


def main():
    debug = L.flag("--debug")
    exercise = L.opt("--exercise", "face")
    r = L.Report(f"CH03.06 — Le visage ({exercise})")
    ob = bpy.data.objects.get("SCULPT_Bust")
    if not r.check(ob is not None and ob.type == "MESH", "Objet SCULPT_Bust (maillage)", "Partez du fichier de départ.", 2):
        return r.finish()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(ob.matrix_world)
    bm.verts.ensure_lookup_table()
    nc = V.components(bm)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nc == 1 and nm == 0, f"Un seul volume fermé ({nc} morceau(x), {nm} arête(s) ouvertes)", "Voxel Remesh, socle rebouché.", 3)
    P = np.array([v.co[:] for v in bm.verts])
    N = np.array([v.normal[:] for v in bm.verts])
    E = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
    z0, z1 = P[:, 2].min(), P[:, 2].max()
    Hb = z1 - z0
    eyes = [bpy.data.objects.get("EYE_L"), bpy.data.objects.get("EYE_R")]
    if not r.check(all(e is not None for e in eyes), "Globes EYE_L et EYE_R présents", "Deux sphères nommées EYE_L et EYE_R.", 2):
        return r.finish()
    a, b = (world_center(e) for e in eyes)
    eye_z = (a.z + b.z) / 2
    r.check(abs(abs(a.x) - abs(b.x)) < 0.003 and abs(a.z - b.z) < 0.003 and a.x * b.x < 0, "Yeux symétriques", "Même hauteur, x opposés.", 1)
    # repères : cou, menton, pointe du nez (même logique que CH03.05)
    zs = np.linspace(z0 + 0.3 * Hb, z0 + 0.65 * Hb, 40)
    widths = []
    for z in zs:
        sl = P[np.abs(P[:, 2] - z) < Hb / 50]
        widths.append(sl[:, 0].max() - sl[:, 0].min() if len(sl) >= 8 else np.inf)
    neck_z = zs[int(np.argmin(widths))]
    ref = [V.profile_front(P, z, 0.02, 0.004) for z in np.arange(neck_z - 0.065, neck_z - 0.03, 0.005)]
    ref = [v for v in ref if not np.isnan(v)]
    neck_front = float(np.median(ref)) if ref else np.nan
    chin_z, z, hits = None, neck_z - 0.03, 0
    while z < eye_z and not np.isnan(neck_front):
        f = V.profile_front(P, z)
        hits = hits + 1 if (not np.isnan(f) and f < neck_front - 0.02) else 0
        if hits >= 3:
            chin_z = z - 0.004
            break
        z += 0.002
    if not r.check(chin_z is not None, "Menton repéré sur le profil", "Un menton en saillie sous la bouche.", 2):
        return r.finish()
    head_h = z1 - chin_z
    r.check(0.19 <= head_h <= 0.27, f"Hauteur de tête {head_h * 100:.1f} cm (19–27)", "Échelle réelle (CH03.05).", 1)
    eye_pos = (eye_z - chin_z) / head_h
    r.check(0.42 <= eye_pos <= 0.58, f"Yeux à {100 * eye_pos:.0f} % de la hauteur de tête (42–58)", "Yeux à mi-hauteur.", 2)
    zz = np.arange(chin_z + 0.02, eye_z + 0.01, 0.002)
    fr = np.array([V.profile_front(P, z) for z in zz])
    tip_z = zz[int(np.nanargmin(fr))] if not np.all(np.isnan(fr)) else eye_z - 0.04
    spacing = abs(a.x - b.x)

    # écart signé (mm) de chaque sommet par rapport à REF_Base : > 0 = relevé, < 0 = creusé
    ref = bpy.data.objects.get("REF_Base")
    if not r.check(ref is not None and ref.type == "MESH", "REF_Base (copie cachée du buste de départ) présent",
                   "Ne supprimez pas REF_Base : le correcteur s'en sert pour mesurer ce que vous avez sculpté.", 2):
        return r.finish()
    from mathutils.bvhtree import BVHTree
    mb = ref.matrix_basis          # REF_Base est caché : sa matrix_world n'est pas évaluée à l'ouverture
    rv = [mb @ v.co for v in ref.data.vertices]
    bvh = BVHTree.FromPolygons(rv, [tuple(p.vertices) for p in ref.data.polygons])
    s = np.zeros(len(P))
    for i, co in enumerate(P):
        loc, nor, _idx, _d = bvh.find_nearest(Vector(co))
        s[i] = 1000.0 * (Vector(co) - loc).dot(nor) if loc is not None else 0.0
    frontal = (N[:, 1] < -0.1) & (P[:, 1] < -0.04)

    # paupières : relief en anneau autour de chaque œil
    fr_lid = []
    for e in (a, b):
        rr = np.hypot(P[:, 0] - e.x, P[:, 2] - e.z)
        ann = frontal & (rr > 0.012) & (rr < 0.020)
        fr_lid.append(float(np.mean(s[ann] >= 0.8)) if ann.any() else 0.0)
    lid = min(fr_lid)
    # narines : creux sous la pointe du nez, de chaque côté
    under = (N[:, 2] < -0.2) & (P[:, 1] < -0.05) & (P[:, 2] > tip_z - 0.020) & (P[:, 2] < tip_z + 0.003) & (np.abs(P[:, 0]) < 0.020)
    nos = [int(np.sum(under & (P[:, 0] * sg > 0.002) & (s <= -1.5))) for sg in (1, -1)]
    # bouche : la ligne entre les lèvres est un creux CONTINU qui part du centre ; on la suit vers chaque commissure
    band = frontal & (P[:, 2] > chin_z + 0.02) & (P[:, 2] < tip_z - 0.012) & (np.abs(P[:, 0]) < 0.05)
    hit = band & (s <= -2.8)
    cen = hit & (np.abs(P[:, 0]) < 0.008)
    mouth_n = int(cen.sum())
    mouth_w, lift = 0.0, None
    if mouth_n >= 3:
        zc = float(P[cen, 2].mean())
        ends = []
        for sg in (1, -1):
            x, zprev = 0.0, zc
            while x < 0.030:                      # on suit la ligne jusqu'à ±3 cm (au-delà : plis naso-géniens)
                sel = hit & (np.abs(P[:, 0] * sg - (x + 0.004)) < 0.002) & (np.abs(P[:, 2] - zprev) < 0.006)
                if not sel.any():
                    break
                x += 0.004
                zprev = float(P[sel, 2].mean())
            ends.append((x, zprev))
        mouth_w = ends[0][0] + ends[1][0]
        lift = (ends[0][1] + ends[1][1]) / 2 - zc
    # oreilles : creux de chaque côté, à hauteur des yeux
    ears = []
    for sg in (1, -1):
        sel = (P[:, 0] * sg > 0.066) & (P[:, 2] > eye_z - 0.05) & (P[:, 2] < eye_z + 0.045)
        ears.append(int(np.sum(sel & (s <= -1.2))))
    if debug:
        print(f"[DEBUG] lid={fr_lid} nostrils={nos} mouth_n={mouth_n} mouth_w={mouth_w:.4f} spacing={spacing:.4f} ears={ears} lift={lift}")
    r.check(lid >= LID_MIN, f"Paupières : relief autour des deux yeux ({100 * lid:.0f} % de l'anneau ; ≥ {100 * LID_MIN:.0f})",
            "Un bourrelet autour de chaque globe : la paupière haute recouvre le haut de l'iris (Clay Strips, Pinch).", 3)
    r.check(min(nos) >= NOSTRIL_MIN, f"Narines : creux sous le nez ({nos[0]} / {nos[1]} sommets ; ≥ {NOSTRIL_MIN} de chaque côté)",
            "Deux creux sous la pointe du nez, de part et d'autre de la cloison (Draw Sharp inversé, Inflate).", 3)
    r.check(mouth_n >= MOUTH_MIN and 0.5 <= mouth_w / max(spacing, 1e-6) <= 1.3,
            f"Bouche : ligne entre les lèvres ({mouth_n} sommets), largeur {mouth_w * 100:.1f} cm = {100 * mouth_w / spacing:.0f} % de l'écart des yeux (50–130)",
            "Creusez la ligne des lèvres ; la bouche est large comme l'écart des pupilles environ.", 3)
    r.check(min(ears) >= EAR_MIN, f"Oreilles : hélix et conque creusés ({ears[0]} / {ears[1]} sommets ; ≥ {EAR_MIN})",
            "Une oreille n'est pas une pastille : bord (hélix) et creux (conque).", 2)
    if exercise == "smile":
        r.check(lift is not None and lift >= SMILE_MIN,
                f"Sourire : commissures relevées de {0 if lift is None else lift * 1000:.1f} mm (≥ {SMILE_MIN * 1000:.0f})",
                "Relevez les coins de la bouche, creusez les plis naso-géniens.", 3)
    bm.free()
    ev.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
