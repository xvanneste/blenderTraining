"""
build_ch03_05_files.py — « Le buste réaliste » (CH03.05, sculpture réaliste).

  STARTER_FILES/ch03_05_bust_starter.blend
      Studio, 3 caméras (face, 3/4, profil), guide de proportions en Grease Pencil (couronne, racine
      des cheveux, sourcils, base du nez, menton, ligne des yeux) ; aucun buste.
  COMPLETED_EXAMPLES/ch03_05_bust_solution.blend (+ _reference.png : face, 3/4, profil)
      Buste à l'échelle 1 : blocage en ellipsoïdes (crâne, face, mâchoire, pommettes, arcades, nez,
      lèvres, oreilles, cou, trapèzes) → Join → Voxel Remesh (2,5 mm) → orbites creusées par Boolean
      → Voxel Remesh → socle plat (Bisect + Fill) → détails SECONDAIRES (plis naso-géniens, sillon
      labial, poches) et TERTIAIRES (rides du front, pores) écrits par déplacement des sommets,
      + deux globes oculaires EYE_L / EYE_R. Objet SCULPT_Bust, un seul volume fermé.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : fichiers FAUX (pour la contre-épreuve du correcteur)
      smooth  : même buste sans aucun détail secondaire/tertiaire (lisse comme de l'argile)
      eyes_high : yeux placés au tiers supérieur de la tête (proportion fausse)
      lopsided : tête décalée et nez dévié (asymétrie)
      tiny    : buste réaliste réduit à 25 cm (échelle fausse)
      no_tertiary / no_secondary : un seul des deux niveaux de détail est absent
COMPLETED_EXAMPLES/ch03_05_bust_learner.blend : construit comme le TUTORIEL (torse en ellipsoïdes, lissage léger) — VALIDÉ
Les détails fins sont écrits par script (les opérateurs de sculpt font planter Blender en arrière-plan,
cf. CLAUDE.md) : la consigne de l'apprenant utilise, elle, les brosses (Draw Sharp, Crease Sharp, Clay Strips).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_05_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import noise as mnoise  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH03.05 — LE BUSTE RÉALISTE (vues : Num 1 face, Num 3 profil)
1. Proportions (guide GUIDE) : la tête fait ≈ 23 cm du menton à la couronne ; les yeux sont à la
   MOITIÉ de la hauteur ; racine des cheveux, sourcils, base du nez, menton = tiers égaux du visage.
2. Blocage : ellipsoïdes / Voxel Remesh (≈ 2,5 mm), orbites creusées, socle plat (Bisect + Fill).
3. Globes oculaires : deux sphères EYE_L et EYE_R (≈ 2,5 cm) posées dans les orbites.
4. Plans -> transitions : Clay Strips (C) puis Smooth (S) ; arcades, pommettes, plan du nez, mâchoire.
5. Détails secondaires : plis naso-géniens, sillon entre les lèvres, poches sous les yeux (Draw Sharp,
   Crease Sharp). Détails tertiaires : rides du front, pores (brosse fine, Multires ou Voxel plus fin).
Vérification : SCRIPTS/validate_ch03_05.py -- --exercise bust
"""
# nom, centre, demi-dimensions (m) ; visage tourné vers -Y ; tête : menton z=0,27 → couronne z=0,50
PARTS = [
    ("Neck", (0, 0.015, 0.19), (0.057, 0.06, 0.1)),
    ("Sterno_L", (0.032, -0.012, 0.2), (0.019, 0.028, 0.07)),
    ("Sterno_R", (-0.032, -0.012, 0.2), (0.019, 0.028, 0.07)),
    ("Skull", (0, 0.025, 0.395), (0.078, 0.1, 0.1)),
    ("Face", (0, -0.012, 0.335), (0.066, 0.062, 0.085)),
    ("Jaw", (0, -0.014, 0.297), (0.056, 0.058, 0.042)),
    ("Chin", (0, -0.05, 0.288), (0.022, 0.03, 0.024)),
    ("Zygo_L", (0.05, -0.03, 0.368), (0.015, 0.028, 0.013)),
    ("Zygo_R", (-0.05, -0.03, 0.368), (0.015, 0.028, 0.013)),
    ("Brow", (0, -0.052, 0.402), (0.06, 0.022, 0.016)),
    ("NoseBridge", (0, -0.07, 0.374), (0.010, 0.017, 0.03)),
    ("NoseTip", (0, -0.081, 0.341), (0.014, 0.017, 0.014)),
    ("NoseWing_L", (0.016, -0.072, 0.335), (0.010, 0.012, 0.010)),
    ("NoseWing_R", (-0.016, -0.072, 0.335), (0.010, 0.012, 0.010)),
    ("LipUp", (0, -0.067, 0.318), (0.024, 0.011, 0.007)),
    ("LipLow", (0, -0.066, 0.299), (0.020, 0.011, 0.008)),
]
EARS = [  # ajoutées APRÈS le lissage (sinon elles fondent dans le crâne)
    ("Ear_L", (0.075, 0.016, 0.372), (0.010, 0.019, 0.029)),
    ("Ear_R", (-0.075, 0.016, 0.372), (0.010, 0.019, 0.029)),
]
SOCKET_R = 0.0155
EYE_R = 0.0125
EYE_X, EYE_Y, EYE_Z = 0.032, -0.050, 0.385
SOCKET_Y = -0.056
VOXEL = 0.0025


def studio_views():
    L.studio(subject_height=0.55)
    c = L.collection("CAMERAS")
    front = L.camera("CAM_Front", c, (0, -1.45, 0.27), 75, make_active=True)
    S.look_at(front, (0, 0, 0.27))
    side = L.camera("CAM_Side", c, (1.45, 0, 0.27), 75, make_active=False)
    S.look_at(side, (0, 0, 0.27))
    tq = L.camera("CAM_34", c, (0.95, -1.15, 0.36), 75, make_active=False)
    S.look_at(tq, (0, 0, 0.27))
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.camera = front
    return sc


def guide_board():
    """Guide de proportions (Grease Pencil) : repères horizontaux et ovale de tête, à côté du buste."""
    ob = G.new_object("GP_Guide", L.collection("GUIDE"))
    ob.location = (-0.18, 0.0, 0)          # bcma_gp écrit déjà les points en (x, 0, z) : pas de rotation
    ink = G.material(ob, "MAT_GP_Ink", (0.05, 0.05, 0.08))
    red = G.material(ob, "MAT_GP_Eye", (0.8, 0.1, 0.1))
    d = G.layer(ob, "GUIDE")
    ob.data.layers["GUIDE"].use_lights = False
    G.ellipse(d, (0.0, 0.385), 0.075, 0.115, 0.0015, ink)
    for z, mat in ((0.50, ink), (0.47, ink), (0.404, ink), (0.337, ink), (0.27, ink), (0.385, red)):
        G.polyline(d, [(-0.085, z), (0.085, z)], 0.0015, mat)
    return ob


def head_geometry_variant(parts, variant):
    out = []
    for n, c, r in parts:
        c = list(c)
        if variant == "lopsided":
            c[0] += 0.02 if n in ("Skull", "Face", "Jaw", "Brow", "Chin", "Zygo_L", "Zygo_R") else 0.0
            if n.startswith("Nose"):
                c[0] += 0.03
        out.append((n, tuple(c), r))
    return out


def torso(col, mat):
    """Buste : sections en super-ellipses (épaules larges -> pente du trapèze -> cou), fermé aux deux bouts."""
    bm = bmesh.new()
    rings = []
    zs = np.linspace(-0.01, 0.17, 19)
    for z in zs:
        t = min(max((z - 0.07) / 0.10, 0.0), 1.0)
        w = 0.19 - 0.145 * t ** 1.2
        d = 0.105 - 0.062 * t
        ring = []
        for k in range(56):
            a = 2 * math.pi * k / 56
            c, s_ = math.cos(a), math.sin(a)
            x = w * math.copysign(abs(c) ** (2 / 2.6), c)
            y = 0.012 + d * math.copysign(abs(s_) ** (2 / 2.6), s_)
            ring.append(bm.verts.new((x, y, z)))
        rings.append(ring)
    for r0, r1 in zip(rings[:-1], rings[1:]):
        for k in range(56):
            bm.faces.new((r0[k], r0[(k + 1) % 56], r1[(k + 1) % 56], r1[k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new("ME_BLOCK_Torso")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("BLOCK_Torso", me)
    col.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


def taubin(ob, iterations, lam=0.5, mu=-0.53):
    """Lissage de Taubin (lambda/mu) : fond les raccords entre blocs sans faire rétrécir le volume.
    C'est l'équivalent scripté du pinceau Smooth : on arrondit les TRANSITIONS, pas les grandes masses."""
    me = ob.data
    n = len(me.vertices)
    P = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("co", P)
    P = P.reshape(n, 3).astype(np.float64)
    E = np.empty(len(me.edges) * 2, dtype=np.int32)
    me.edges.foreach_get("vertices", E)
    a, b = E[0::2], E[1::2]
    deg = np.bincount(np.concatenate([a, b]), minlength=n).astype(np.float64)
    deg[deg == 0] = 1
    for _ in range(iterations):
        for f in (lam, mu):
            acc = np.zeros_like(P)
            np.add.at(acc, a, P[b])
            np.add.at(acc, b, P[a])
            P += f * (acc / deg[:, None] - P)
    me.vertices.foreach_set("co", P.ravel().astype(np.float32))
    me.update()


def build_volume(variant):
    col = L.collection("SCULPT")
    clay = L.material("MAT_Clay", (0.72, 0.58, 0.5), 0.6)
    parts = [L.sphere("BLOCK_" + n, col, clay, radius=1, location=c, scale=r)
             for n, c, r in head_geometry_variant(PARTS, variant)]
    if variant == "learner":      # construction du TUTORIEL : poitrine + deux pentes en ellipsoïdes (pas de loft)
        for n, c, r in (("Chest", (0, 0.0, 0.06), (0.19, 0.1, 0.12)), ("Slope_L", (0.1, 0.012, 0.13), (0.085, 0.07, 0.035)),
                        ("Slope_R", (-0.1, 0.012, 0.13), (0.085, 0.07, 0.035))):
            parts.append(L.sphere("BLOCK_" + n, col, clay, radius=1, location=c, scale=r))
    else:
        parts.append(torso(col, clay))
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_Bust", "ME_SCULPT_Bust"
    ob.data.transform(ob.matrix_world)          # le Join garde l'origine du 1er bloc : on la remet à (0,0,0)
    ob.matrix_world = type(ob.matrix_world)()
    ob.data.remesh_voxel_size = VOXEL
    bpy.ops.object.voxel_remesh()
    taubin(ob, 12 if variant == "learner" else 45)    # fondre les blocs : transitions (l'apprenant le fait à la brosse Smooth)
    ears = [L.sphere("BLOCK_" + n, col, clay, radius=1, location=(c[0] + (0.02 if variant == "lopsided" else 0.0),) + c[1:], scale=r)
            for n, c, r in EARS]
    bpy.ops.object.select_all(action="DESELECT")
    for o in ears + [ob]:
        o.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.data.remesh_voxel_size = VOXEL
    bpy.ops.object.voxel_remesh()
    taubin(ob, 4)
    ez = EYE_Z + (0.07 if variant == "eyes_high" else 0.0)
    for i, sx in enumerate((EYE_X, -EYE_X)):
        backup = ob.data.copy()
        for attempt, jitter in enumerate((0.0, 0.00031, 0.00073)):      # garde-fou : résultat vide -> on retente
            cutter = L.sphere(f"CUT_Socket_{i}", col, None, radius=SOCKET_R, location=(sx + jitter, SOCKET_Y + jitter, ez + jitter))
            m = ob.modifiers.new(f"Socket_{i}", "BOOLEAN")
            m.operation, m.object, m.solver = "DIFFERENCE", cutter, "MANIFOLD"   # EXACT renvoie un maillage vide ici (mesuré)
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.modifier_apply(modifier=m.name)
            bpy.data.objects.remove(cutter, do_unlink=True)
            if len(ob.data.vertices) > 1000:
                break
            ob.data = backup.copy()                                    # résultat vide : on restaure et on retente
        else:
            raise RuntimeError("Boolean des orbites : résultat vide après 3 essais")
        bpy.data.meshes.remove(backup)
    bpy.ops.object.voxel_remesh()
    taubin(ob, 6)                                      # adoucir les bords des orbites
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.005), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.transform(Matrix.Translation((0, 0, -0.005)))      # base à z = 0 : on déplace les SOMMETS (transform_apply échoue sans sélection)
    ob.location = (0, 0, 0)
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.data.use_mirror_x = True
    return ob


def groove(P, poly, width, depth):
    """Profondeur (≥ 0) d'un sillon : gaussienne de la distance (plan XZ) à une polyligne."""
    d = np.full(len(P), 1e9)
    q = P[:, [0, 2]]
    for a, b in zip(poly[:-1], poly[1:]):
        a, b = np.array(a), np.array(b)
        ab = b - a
        t = np.clip(((q - a) @ ab) / (ab @ ab), 0, 1)
        proj = a + t[:, None] * ab
        d = np.minimum(d, np.linalg.norm(q - proj, axis=1))
    return depth * np.exp(-((d / width) ** 2))


def add_skin_detail(ob, secondary=True, tertiary=True):
    """Détails secondaires + tertiaires par déplacement des sommets le long des normales."""
    me = ob.data
    n = len(me.vertices)
    P = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("co", P)
    P = P.reshape(n, 3).astype(np.float64)
    N = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("normal", N)
    N = N.reshape(n, 3).astype(np.float64)
    front = (N[:, 1] < -0.15) & (P[:, 1] < -0.02) & (P[:, 2] > 0.26)
    depth = np.zeros(n)
    for s in (1, -1):
        depth += groove(P, [(s * 0.024, 0.333), (s * 0.033, 0.320), (s * 0.040, 0.302), (s * 0.044, 0.286)], 0.0042, 0.0016)   # naso-génien
        depth += groove(P, [(s * 0.020, 0.372), (s * 0.040, 0.368)], 0.005, 0.0009)                                          # poches sous les yeux
        depth += groove(P, [(s * 0.010, 0.4465), (s * 0.045, 0.447)], 0.0022, 0.0008)                                       # ride du front
        depth += groove(P, [(s * 0.010, 0.4565), (s * 0.045, 0.457)], 0.0022, 0.0007)
    depth += groove(P, [(-0.021, 0.3085), (0.021, 0.3085)], 0.0013, 0.0026)                                                  # sillon labial
    depth += groove(P, [(-0.012, 0.2825), (0.012, 0.2825)], 0.0030, 0.0014)                                                  # pli mento-labial
    disp = -depth * front if secondary else np.zeros(n)
    # pores / grain de peau : bruit fin (tertiaire)
    # poids du grain : plein sur le visage, nul au-delà (atténuation progressive : pas de limite visible)
    wy = np.clip((0.01 - P[:, 1]) / 0.02, 0, 1)
    wx = np.clip((0.083 - np.abs(P[:, 0])) / 0.02, 0, 1)
    wz = np.clip((P[:, 2] - 0.265) / 0.02, 0, 1)
    weight = wy * wx * wz
    for i in (np.nonzero(weight > 0)[0] if tertiary else []):
        v = Vector((P[i, 0] * 420, P[i, 1] * 420, P[i, 2] * 420))
        disp[i] += weight[i] * 0.00028 * mnoise.noise(v)
    P2 = P + N * disp[:, None]
    me.vertices.foreach_set("co", P2.ravel().astype(np.float32))
    me.update()
    print(f"[BCMA] détails : {int((np.abs(disp) > 1e-4).sum())} sommets déplacés, max {np.abs(disp).max() * 1000:.2f} mm")


def eyes(ob_col, variant):
    white = L.material("MAT_EyeWhite", (0.92, 0.9, 0.86), 0.15)
    iris = L.material("MAT_Iris", (0.12, 0.16, 0.22), 0.1)
    ez = EYE_Z + (0.07 if variant == "eyes_high" else 0.0)
    out = []
    for name, sx in (("EYE_L", EYE_X), ("EYE_R", -EYE_X)):
        e = L.sphere(name, ob_col, white, radius=EYE_R, location=(sx, EYE_Y, ez))
        e.data.name = "ME_" + name
        ir = L.sphere(name + "_Iris", ob_col, iris, radius=0.0058, location=(sx, EYE_Y - 0.0105, ez))
        ir.scale.y = 0.5
        ir.parent = e
        ir.matrix_parent_inverse = e.matrix_world.inverted()
        out.append(e)
    return out


def bust(variant):
    ob = build_volume(variant)
    if variant != "smooth":
        add_skin_detail(ob, secondary=variant != "no_secondary", tertiary=variant != "no_tertiary")
    eyes(L.collection("SCULPT"), variant)
    if variant == "tiny":
        for o in bpy.data.objects:
            if o.name.startswith(("SCULPT_Bust", "EYE_")) and o.parent is None:
                o.scale = (0.5, 0.5, 0.5)
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action="DESELECT")
        for o in bpy.data.objects:
            if o.name.startswith(("SCULPT_Bust", "EYE_")) and o.parent is None:
                o.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_Bust"]
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
    print(f"[BCMA] SCULPT_Bust ({variant}) : {len(ob.data.vertices)} sommets, {len(ob.data.polygons)} faces")
    return ob


def build(sol, variant="solution"):
    L.reset("SC_RealBust")
    sc = studio_views()
    guide_board()
    if sol:
        bust(variant)
    L.instructions(NOTE)
    return sc


def views(sc, out):
    tiles = []
    sc.render.resolution_x, sc.render.resolution_y = 720, 900
    for cam in ("CAM_Front", "CAM_34", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("bust", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_05_bust_starter.blend"))
    for variant in ("smooth", "no_tertiary", "no_secondary", "eyes_high", "lopsided", "tiny"):
        build(True, variant)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_05_bust_{variant}.blend"))
    build(True, "learner")      # construit comme le TUTORIEL : doit être VALIDÉ (le correcteur n'est pas collé à la solution)
    L.save(os.path.join(out, "ch03_05_bust_learner.blend"))
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] solution avec détails sculptés à la brosse (Blender 5.2 via MCP) conservée : non régénérée")
        return
    sc = build(True)          # repli scripté (détails écrits par déplacement de sommets)
    L.save(os.path.join(out, "ch03_05_bust_solution.blend"))
    for o in bpy.data.objects:
        if o.name == "GP_Guide":
            o.hide_render = True
    views(sc, os.path.join(out, "ch03_05_bust_reference.png"))


if __name__ == "__main__":
    L.run(main)
