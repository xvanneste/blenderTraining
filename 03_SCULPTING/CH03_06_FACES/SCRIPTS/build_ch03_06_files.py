"""
build_ch03_06_files.py — « Le visage » (CH03.06 : yeux, nez, bouche, oreilles, expressions de base).

  STARTER_FILES/ch03_06_face_starter.blend
      Le buste réaliste de CH03.05 SANS détails de visage (volume lissé, orbites creusées, globes EYE_L/EYE_R) :
      c'est le point de départ de l'apprenant (SCULPT_Bust : ni paupières, ni narines, ni bouche, ni oreilles creusées).
  COMPLETED_EXAMPLES/ch03_06_face_solution.blend  (+ _reference.png : neutre, sourire, détail yeux)
      Visage neutre : paupières (bourrelets haut/bas + pli), narines, bouche (ligne + commissures), oreilles
      (hélix, conque), plis de CH03.05.
  COMPLETED_EXAMPLES/ch03_06_smile_solution.blend
      Même visage avec un sourire : commissures relevées, plis naso-géniens creusés.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : no_lids, no_nostrils, no_mouth, no_ears, frown (moue), flat_smile (pas de sourire)
Les détails sont écrits par déplacement des sommets (les opérateurs de sculpt plantent en arrière-plan, cf. CLAUDE.md).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_06_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH03_05_REALISTIC", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import build_ch03_05_files as B  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils import noise as mnoise  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH03.06 — LE VISAGE (vues : Num 1 face, Num 3 profil, Num 7 dessous du nez)
Point de départ : buste réaliste (CH03.05) avec orbites et globes, SANS détails de visage.
1. Paupières : un bourrelet autour de chaque globe (la paupière haute recouvre le haut de l'iris), un pli au-dessus.
2. Nez : deux narines sous la pointe (creux), ailes du nez qui s'enroulent.
3. Bouche : une ligne entre les lèvres, des commissures nettes ; sa largeur ≈ distance entre les pupilles.
4. Oreilles : hélix (bord), conque (creux central) ; elles vont de la ligne des sourcils à la base du nez.
5. Expression : un SOURIRE = commissures relevées, plis naso-géniens plus marqués ; l'œil se plisse un peu.
REF_Base (caché) : copie du buste de départ, utilisée par le correcteur : NE LA SUPPRIMEZ PAS.
Brosses (5.3) : Draw Sharp, Crease Sharp, Clay Strips (C), Smooth (S), Inflate/Deflate (I), Pinch/Magnify (P).
Vérification : SCRIPTS/validate_ch03_06.py -- --exercise face   |   --exercise smile
"""
EYE_C = [(B.EYE_X, B.EYE_Z), (-B.EYE_X, B.EYE_Z)]
MOUTH_Z = 0.3085
MOUTH_HALF = 0.030


def bump(P, N, mask, centers, width, amp):
    """Déplacement le long de la normale : gaussienne autour de points 3D (amp > 0 = relief, < 0 = creux)."""
    out = np.zeros(len(P))
    for c in centers:
        d = np.linalg.norm(P - np.array(c), axis=1)
        out += amp * np.exp(-((d / width) ** 2))
    return out * mask


def ring_relief(P, cx, cz, r0, width, amp, upper):
    """Bourrelet circulaire (plan XZ) autour d'un œil ; moitié haute ou basse."""
    rr = np.hypot(P[:, 0] - cx, P[:, 2] - cz)
    half = (P[:, 2] >= cz - 0.001) if upper else (P[:, 2] < cz - 0.001)
    return amp * np.exp(-(((rr - r0) / width) ** 2)) * half


def add_face_features(ob, lids=True, nostrils=True, mouth=True, ears=True, smile=0.0):
    """Détails de visage + détails de CH03.05 (plis, grain), par déplacement des sommets le long des normales.
    smile > 0 : commissures relevées de `smile` mètres ; smile < 0 : moue (commissures abaissées)."""
    me = ob.data
    n = len(me.vertices)
    P = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("co", P)
    P = P.reshape(n, 3).astype(np.float64)
    N = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("normal", N)
    N = N.reshape(n, 3).astype(np.float64)
    front = (N[:, 1] < -0.15) & (P[:, 1] < -0.02) & (P[:, 2] > 0.26)
    disp = np.zeros(n)
    k = 1.5                                                              # sourire : plis naso-géniens plus marqués (×1,5)
    for s in (1, -1):
        disp -= B.groove(P, [(s * 0.024, 0.333), (s * 0.033, 0.320), (s * 0.040, 0.302), (s * 0.044, 0.286)], 0.0042, 0.0016 * (k if smile > 0 else 1.0)) * front
        disp -= B.groove(P, [(s * 0.020, 0.372), (s * 0.040, 0.368)], 0.005, 0.0009) * front
        disp -= B.groove(P, [(s * 0.010, 0.4465), (s * 0.045, 0.447)], 0.0022, 0.0008) * front
        disp -= B.groove(P, [(s * 0.010, 0.4565), (s * 0.045, 0.457)], 0.0022, 0.0007) * front
    disp -= B.groove(P, [(-0.012, 0.2825), (0.012, 0.2825)], 0.0030, 0.0014) * front
    if lids:
        for cx, cz in EYE_C:
            disp += ring_relief(P, cx, cz, 0.0148, 0.0030, 0.0026, True) * front        # paupière haute
            disp += ring_relief(P, cx, cz, 0.0140, 0.0028, 0.0016, False) * front       # paupière basse
            rr = np.hypot(P[:, 0] - cx, P[:, 2] - cz)
            disp -= 0.0020 * np.exp(-(((rr - 0.0235) / 0.0030) ** 2)) * (P[:, 2] >= cz) * front   # pli palpébral
    if nostrils:
        under = (N[:, 2] < -0.2) & (np.abs(P[:, 0]) < 0.03) & (P[:, 2] > 0.30) & (P[:, 2] < 0.345) & (P[:, 1] < -0.05)
        for sx in (1, -1):
            disp -= bump(P, N, under, [(sx * 0.0085, -0.078, 0.3265)], 0.0055, 0.0055)
    if mouth:
        xs = np.linspace(-MOUTH_HALF, MOUTH_HALF, 13)
        line = [(x, MOUTH_Z + smile * (abs(x) / MOUTH_HALF) ** 2) for x in xs]
        disp -= B.groove(P, line, 0.0022, 0.0045) * front
        for sx in (1, -1):                                                                  # commissures : petits creux
            disp -= B.groove(P, [(sx * MOUTH_HALF, MOUTH_Z + smile), (sx * (MOUTH_HALF + 0.004), MOUTH_Z + smile)], 0.0030, 0.0045) * front
    if ears:
        for sx in (1, -1):
            side = (P[:, 0] * sx > 0.066) & (P[:, 2] > 0.32) & (P[:, 2] < 0.43)
            cy, cz = 0.016, 0.372
            u = (P[:, 1] - cy) / 0.019
            v = (P[:, 2] - cz) / 0.027
            rn = np.hypot(u, v)
            disp -= 0.0028 * np.exp(-(((rn - 0.62) / 0.16) ** 2)) * side                      # sillon de l'hélix
            disp -= 0.0036 * np.exp(-((rn / 0.30) ** 2)) * side                               # conque
    weight = np.clip((0.01 - P[:, 1]) / 0.02, 0, 1) * np.clip((0.083 - np.abs(P[:, 0])) / 0.02, 0, 1) * np.clip((P[:, 2] - 0.265) / 0.02, 0, 1)
    for i in np.nonzero(weight > 0)[0]:
        disp[i] += weight[i] * 0.00028 * mnoise.noise(Vector((P[i, 0] * 420, P[i, 1] * 420, P[i, 2] * 420)))
    # le déplacement d'oreille / narine suit la normale locale ; les normales des oreilles regardent vers ±X
    me.vertices.foreach_set("co", (P + N * disp[:, None]).ravel().astype(np.float32))
    me.update()


def build(kind):
    """kind : starter | neutral | smile | no_lids | no_nostrils | no_mouth | no_ears | frown | flat_smile"""
    L.reset("SC_Face")
    sc = B.studio_views()
    L.instructions(NOTE)
    ob = B.build_volume("solution")
    # copie cachée du buste de départ : le correcteur mesure ce que l'apprenant a creusé / relevé par rapport à elle
    ref = bpy.data.objects.new("REF_Base", ob.data.copy())
    L.collection("REFERENCE").objects.link(ref)
    ref.matrix_world = ob.matrix_world.copy()          # même transformation que le buste (identité depuis la correction de CH03.05)
    ref.hide_viewport = True
    ref.hide_render = True
    if kind != "starter":
        sm = {"smile": 0.010, "frown": -0.010}.get(kind, 0.0)
        add_face_features(ob, lids=kind != "no_lids", nostrils=kind != "no_nostrils", mouth=kind != "no_mouth",
                          ears=kind != "no_ears", smile=sm)
    B.eyes(L.collection("SCULPT"), "solution")
    return sc


def views(sc, out, cams=(("CAM_Front", None), ("CAM_34", None), ("CAM_Side", None))):
    tiles = []
    sc.render.resolution_x, sc.render.resolution_y = 600, 600
    for cam, _ in cams:
        c = bpy.data.objects[cam]
        sc.camera = c
        c.location = {"CAM_Front": (0, -0.62, 0.36), "CAM_34": (0.43, -0.45, 0.38), "CAM_Side": (0.62, 0, 0.36)}[cam]
        c.rotation_euler = (Vector((0, 0, 0.36)) - Vector(c.location)).to_track_quat("-Z", "Y").to_euler()
        c.data.lens = 85
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("face", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_06_face_starter.blend"))
    for kind in ("no_lids", "no_nostrils", "no_mouth", "no_ears", "frown", "flat_smile"):
        build("neutral" if kind == "flat_smile" else kind)       # flat_smile = visage neutre présenté à l'exercice smile
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_06_face_{kind}.blend"))
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] solutions neutre et sourire sculptées à la brosse (Blender 5.2 via MCP) conservées : non régénérées")
        return
    sc = build("smile")       # repli scripté
    L.save(os.path.join(out, "ch03_06_smile_solution.blend"))
    views(sc, os.path.join(out, "ch03_06_smile_reference.png"))
    sc = build("neutral")
    L.save(os.path.join(out, "ch03_06_face_solution.blend"))
    views(sc, os.path.join(out, "ch03_06_face_reference.png"))


if __name__ == "__main__":
    L.run(main)
