"""
build_ch03_10_files.py — « Préparation au rigging » (CH03.10 : pose en A/T, échelle, origine, symétrie, nommage).

  STARTER_FILES/ch03_10_char_starter.blend
      Un mannequin SALE : objet « Mannequin.001 », échelle 100 non appliquée (le maillage est en cm), origine au centre du corps,
      rotation de 4° autour de Z, pas de collection de personnage. À nettoyer.
  COMPLETED_EXAMPLES/ch03_10_char_solution.blend (+ _reference.png : face, profil)
      CHR_Hero_Body : 1,76 m, échelle/rotation/position appliquées, origine entre les pieds au sol, nom conforme,
      données ME_CHR_Hero_Body, collection CHR_Hero, symétrique en X, pose en A (bras à 40° de la verticale), pieds écartés de 36 cm (centre à centre),
      face vers −Y, maillage propre.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : wrong_scale, bad_name, origin_off, arms_down, asymmetric, floating, tpose_ok (VALIDE : pose en T)
Convention : Z vers le haut, personnage face à −Y, pieds sur z = 0, origine en (0, 0, 0) entre les pieds.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_10_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH03_05_REALISTIC", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import build_ch03_05_files as B5  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH03.10 — PERSONNAGE PRÊT POUR LE RIG (Z haut, face à −Y, pieds sur z = 0)
Le mannequin du fichier de départ est volontairement SALE. À faire :
1. Nom : objet CHR_Hero_Body, données ME_CHR_Hero_Body (pas de .001), dans une collection CHR_Hero.
2. Transformations : Object > Apply > All Transforms (échelle, rotation, position) : échelle 1, rotation 0.
3. Rotation de 4° autour de Z : la remettre à 0 AVANT d'appliquer (la face doit regarder −Y).
4. Origine : au sol, entre les pieds, en (0, 0, 0) (Object > Set Origin > Origin to 3D Cursor, curseur à l'origine).
5. Taille réelle : ≈ 1,76 m ; pieds sur z = 0.
6. Pose : A (bras à ≈ 30–55° de la verticale) ou T (≈ 90°) ; pieds écartés de ≈ 20–40 cm (centre à centre) ; symétrie X.
Vérification : SCRIPTS/validate_ch03_10.py -- --exercise rigready
"""


def ellip(name, col, mat, c, r, rot=(0, 0, 0)):
    return L.sphere(name, col, mat, radius=1, location=c, scale=r, rotation=rot)


def limb(name, col, mat, origin, d, start, length, radius, side):
    """Ellipsoïde allongé le long de la direction d (dans le plan XZ) à partir de `origin`."""
    a = math.atan2(d[0], -d[2])          # angle par rapport à la verticale descendante
    c = Vector(origin) + Vector(d) * (start + length / 2)
    return ellip(name, col, mat, tuple(c), (radius, radius * 0.9, length / 2 * 1.25), rot=(0, -a if side > 0 else -a, 0))


def body_parts(col, mat, arm_deg=40.0, shift_arm=0.0, tpose=False):
    P = [ellip("Pelvis", col, mat, (0, 0, 0.98), (0.17, 0.11, 0.10)),
         ellip("Chest", col, mat, (0, 0, 1.22), (0.19, 0.12, 0.20)),
         ellip("Neck", col, mat, (0, 0, 1.50), (0.05, 0.05, 0.07)),
         ellip("Head", col, mat, (0, 0, 1.64), (0.095, 0.11, 0.12))]
    a = math.radians(90.0 if tpose else arm_deg)
    for s, nm in ((1, "L"), (-1, "R")):
        sh = (s * 0.17 + (shift_arm if s > 0 else 0.0), 0.0, 1.38)
        P.append(L.sphere(f"Shoulder_{nm}", col, mat, radius=1, location=(s * 0.14, 0.0, 1.37), scale=(0.085, 0.075, 0.075)))
        d = (s * math.sin(a), 0.0, -math.cos(a))
        # rotation Y : l'axe long (Z local) doit s'aligner sur d
        ang = math.atan2(d[0], d[2])
        def seg(name_, start, length, radius):
            c = Vector(sh) + Vector(d) * (start + length / 2)
            return L.sphere(name_, col, mat, radius=1, location=tuple(c), scale=(radius, radius, length / 2 * 1.2), rotation=(0, -math.atan2(-d[0], -d[2]) * 0 + math.atan2(d[0], -d[2]) * -1 * -1 if False else ang, 0))
        P.append(seg(f"UpperArm_{nm}", 0.0, 0.30, 0.050))
        P.append(seg(f"Forearm_{nm}", 0.30, 0.26, 0.040))
        P.append(seg(f"Hand_{nm}", 0.56, 0.18, 0.036))
        # jambes : légèrement écartées (6°)
        hip = (s * 0.09, 0.0, 0.95)
        la = math.radians(6.0)
        ld = (s * math.sin(la), 0.0, -math.cos(la))
        lang = math.atan2(ld[0], ld[2])
        for nm2, st, ln, rr in (("Thigh", 0.0, 0.45, 0.085), ("Shin", 0.45, 0.43, 0.060)):
            c = Vector(hip) + Vector(ld) * (st + ln / 2)
            P.append(L.sphere(f"{nm2}_{nm}", col, mat, radius=1, location=tuple(c), scale=(rr, rr, ln / 2 * 1.15), rotation=(0, lang, 0)))
        ankle = Vector(hip) + Vector(ld) * 0.88
        P.append(L.sphere(f"Foot_{nm}", col, mat, radius=1, location=(ankle.x, -0.04, 0.04), scale=(0.05, 0.12, 0.04)))
    return P


def build_body(name="Mannequin", arm_deg=40.0, shift_arm=0.0, tpose=False):
    col = L.collection("SCULPT")
    skin = L.material("MAT_Skin", (0.7, 0.55, 0.48), 0.6)
    parts = body_parts(col, skin, arm_deg, shift_arm, tpose)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = Matrix()
    ob.data.remesh_voxel_size = 0.010
    bpy.ops.object.voxel_remesh()
    B5.taubin(ob, 10)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0.0), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(ob.data)
    bm.free()
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.name, ob.data.name = name, "ME_" + name
    return ob


def studio():
    L.studio(subject_height=1.8)
    c = L.collection("CAMERAS")
    front = L.camera("CAM_Front", c, (0, -4.2, 0.95), 50, make_active=True)
    side = L.camera("CAM_Side", c, (4.2, 0, 0.95), 50, make_active=False)
    from bcma_shots import look_at
    look_at(front, (0, 0, 0.9))
    look_at(side, (0, 0, 0.9))
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.camera = front
    return sc


def dirty(ob):
    """Starter : maillage en cm (×100), origine au centre, échelle 0,01 non appliquée, rotation 4° autour de Z, nom .001."""
    ob.data.transform(Matrix.Scale(100.0, 4))
    me = ob.data
    c = np.mean([v.co[:] for v in me.vertices], axis=0)
    me.transform(Matrix.Translation(-Vector(c)))
    ob.location = (0.0, 0.0, c[2] / 100.0)
    ob.location.x, ob.location.y = c[0] / 100.0, c[1] / 100.0
    ob.scale = (0.01, 0.01, 0.01)
    ob.rotation_euler.z = math.radians(4.0)
    ob.name, me.name = "Mannequin.001", "Mannequin.001"


def clean(ob, name="CHR_Hero_Body", pose_ok=True):
    ob.name, ob.data.name = name, "ME_" + name
    col = bpy.data.collections.new("CHR_Hero")
    bpy.context.scene.collection.children.link(col)
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    col.objects.link(ob)
    return ob


def views(out):
    sc = bpy.context.scene
    tiles = []
    sc.render.resolution_x, sc.render.resolution_y = 450, 600
    for cam in ("CAM_Front", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def save(path):
    L.instructions(NOTE)
    L.save(path)


def scene(builder_kwargs=None, post=None, cleaned=True, name="CHR_Hero_Body"):
    L.reset("SC_Rig")
    sc = studio()
    ob = build_body("Mannequin", **(builder_kwargs or {}))
    if cleaned:
        clean(ob, name)
    if post:
        post(ob)
    return sc, ob


def apply_xform(ob):
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    sc, ob = scene(cleaned=False)
    dirty(ob)
    save(os.path.join(CH, "STARTER_FILES", "ch03_10_char_starter.blend"))
    # contre-exemples
    def wrong_scale(o):
        o.data.transform(Matrix.Scale(100.0, 4))
        o.scale = (0.01, 0.01, 0.01)
    def origin_off(o):
        o.data.transform(Matrix.Translation(Vector((0, 0, -0.9))))
        o.location = (0, 0, 0.9)
    def floating(o):
        o.location = (0, 0, 0.3)
        apply_xform(o)
    cases = {
        "wrong_scale": dict(post=wrong_scale),
        "bad_name": dict(name="Cube.001"),
        "origin_off": dict(post=origin_off),
        "arms_down": dict(builder_kwargs={"arm_deg": 4.0}),
        "asymmetric": dict(builder_kwargs={"shift_arm": 0.10}),
        "floating": dict(post=floating),
        "tpose_ok": dict(builder_kwargs={"tpose": True}),
    }
    for k, kw in cases.items():
        scene(**kw)
        save(os.path.join(out, "COUNTER_EXAMPLES", f"ch03_10_char_{k}.blend"))
    sc, ob = scene()
    save(os.path.join(out, "ch03_10_char_solution.blend"))
    views(os.path.join(out, "ch03_10_char_reference.png"))


if __name__ == "__main__":
    L.run(main)
