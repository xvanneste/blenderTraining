"""
validate_ch06_11.py — Correcteur « Rigging avancé et réutilisation » (CH06.11).
Usage : … --python-exit-code 1 --python validate_ch06_11.py -- --exercise bendy|override [--debug]

--exercise bendy  (GEO_Tube, RIG_Tube, bone spine) :
    spine : Bendy Bones à 6 segments au moins ; use_deform ; modificateur Armature → RIG_Tube ; groupe « spine ».
    Comportement : Curve In X = Curve Out X = 0,3 (puis remis à 0) ; centres des 41 anneaux :
        milieu décalé en X d'au moins 15 cm (arche) ; extrémités à ≤ 1 cm de leur place ; virage maximal entre anneaux consécutifs ≤ 8° (courbe lisse) ; au repos, tube inchangé (≤ 1 mm).
--exercise override  (plan) :
    Bibliothèque : une seule bibliothèque, chemin RELATIF (commence par //), fichier ch06_11_rig_library.blend existant, contenant COL_Rig, RIG_Lib et GEO_Lib.
    Overrides : RIG_Lib et GEO_Lib sont des library overrides (override_library, référence dans cette bibliothèque) ÉDITABLES (pas « système »), ni des liens nus ni des copies locales.
    Posage : RIG_Lib porte une Action avec une courbe de pose.bones["arm"].rotation_euler ; à l'image 1, arm est tourné de 20° au moins ; le bout de GEO_Lib (sommets dont x > 0,55 m au repos) est déplacé de 20 cm au moins en Y.
    Placement : RIG_Lib est à plus d'1 m de l'origine.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

N_RING, N_SEG = 41, 12


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def bendy(r, debug):
    geo, rig = bpy.data.objects.get("GEO_Tube"), bpy.data.objects.get("RIG_Tube")
    if not r.check(geo is not None and rig is not None and "spine" in rig.data.bones, "GEO_Tube, RIG_Tube et le bone spine présents", "Partez du fichier de départ.", 2):
        return
    bone = rig.data.bones["spine"]
    r.check(bone.bbone_segments >= 6, f"Bendy Bones : {bone.bbone_segments} segment(s) (≥ 6)", "Bone properties > Bendy Bones > Segments.", 5)
    r.check(bone.use_deform and any(m.type == "ARMATURE" and m.object == rig for m in geo.modifiers) and "spine" in geo.vertex_groups, "spine déforme ; modificateur Armature → RIG_Tube ; groupe « spine »", "Ne défaites pas le skinning.", 3)
    rest = coords(geo)
    pb = rig.pose.bones["spine"]
    pb.bbone_curveinx = pb.bbone_curveoutx = 0.3
    co = coords(geo)
    pb.bbone_curveinx = pb.bbone_curveoutx = 0.0
    back = coords(geo)
    cen0 = np.array([rest[i * N_SEG:(i + 1) * N_SEG].mean(axis=0) for i in range(N_RING)])
    cen = np.array([co[i * N_SEG:(i + 1) * N_SEG].mean(axis=0) for i in range(N_RING)])
    arch = float(cen[N_RING // 2][0] - cen0[N_RING // 2][0])
    ends = max(float(np.linalg.norm(cen[0] - cen0[0])), float(np.linalg.norm(cen[-1] - cen0[-1])))
    seg = np.diff(cen, axis=0)
    seg = seg / np.linalg.norm(seg, axis=1)[:, None]
    turn = max(math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(seg[i], seg[i + 1])))))) for i in range(len(seg) - 1))
    r.check(arch >= 0.15, f"Courbe à 0,3 : le milieu du tube est décalé de {100 * arch:.1f} cm (≥ 15)", "Il faut des segments ET le modificateur Armature actif.", 5)
    r.check(ends <= 0.01, f"Extrémités fixes (écart {1000 * ends:.1f} mm ≤ 10)", "", 2)
    r.check(turn <= 8.0, f"Courbe lisse : virage maximal {turn:.1f}° entre anneaux (≤ 8)", "Augmentez le nombre de segments.", 4)
    r.check(float(np.abs(back - rest).max()) <= 0.001, "Au repos (courbure 0) le tube est inchangé", "", 2)
    if debug:
        print("[DEBUG] seg", bone.bbone_segments, "arch", round(arch, 3), "ends", round(ends, 4), "turn", round(turn, 2))


def override(r, debug):
    libs = list(bpy.data.libraries)
    one = len(libs) == 1
    r.check(one, f"Une seule bibliothèque liée ({len(libs)})", "File > Link depuis ch06_11_rig_library.blend.", 4)
    lib = libs[0] if libs else None
    okpath = lib is not None and lib.filepath.startswith("//") and os.path.basename(lib.filepath.replace("\\", "/")) == "ch06_11_rig_library.blend" and os.path.exists(bpy.path.abspath(lib.filepath))
    r.check(okpath, f"Chemin de la bibliothèque relatif et valide ({lib.filepath if lib else 'aucune'})", "Cochez Relative Path en liant ; la bibliothèque est dans le dossier voisin.", 4)
    valid = False
    if lib is not None and os.path.exists(bpy.path.abspath(lib.filepath)):
        with bpy.data.libraries.load(bpy.path.abspath(lib.filepath)) as (df, dt):
            valid = "COL_Rig" in df.collections and "RIG_Lib" in df.objects and "GEO_Lib" in df.objects
    r.check(valid, "La bibliothèque contient COL_Rig, RIG_Lib et GEO_Lib", "Ne modifiez pas la bibliothèque.", 2)
    rig, geo = bpy.data.objects.get("RIG_Lib"), bpy.data.objects.get("GEO_Lib")
    if not r.check(rig is not None and geo is not None, "RIG_Lib et GEO_Lib présents dans le plan", "Liez la collection COL_Rig.", 2):
        return

    def is_override(o):
        ol = o.override_library
        return ol is not None and ol.reference is not None and lib is not None and ol.reference.library == lib

    ov = is_override(rig) and is_override(geo)
    r.check(ov, f"RIG_Lib et GEO_Lib sont des overrides de la bibliothèque (rig : lien nu = {rig.library is not None}, copie locale = {rig.library is None and rig.override_library is None})", "Object > Library Override > Make (Selected & Content).", 6)
    r.check(ov and not rig.override_library.is_system_override and not geo.override_library.is_system_override, "Les overrides sont éditables (ni « système »)", "Override fully editable : Make > Selected & Content.", 3)
    act = rig.animation_data.action if rig.animation_data else None
    paths = {f.data_path for f in act.fcurves} if act and hasattr(act, "fcurves") else set()
    if act is not None and not paths:                                  # API actions par couches (5.x)
        try:
            paths = {f.data_path for layer in act.layers for st in layer.strips for cb in st.channelbags for f in cb.fcurves}
        except Exception:
            paths = set()
    r.check('pose.bones["arm"].rotation_euler' in paths, f"Action avec une courbe de rotation du bone arm (courbes : {sorted(paths) or 'aucune'})", "Pose Mode > tourner arm > I (rotation) à l'image 1.", 4)
    bpy.context.scene.frame_set(1)
    ang = 0.0
    tip = 0.0
    if ov:
        ang = abs(math.degrees(rig.pose.bones["arm"].rotation_euler[2]))
        co = coords(geo)
        rest = np.array([v.co[:] for v in geo.data.vertices])
        mask = rest[:, 0] > 0.55                                      # bout du tube choisi sur la forme de REPOS
        tip = float(abs(co[mask][:, 1]).mean()) if mask.any() and len(co) == len(rest) else 0.0
    r.check(ang >= 20.0, f"Image 1 : arm tourné de {ang:.0f}° (≥ 20)", "30° autour de Z.", 3)
    r.check(tip >= 0.20, f"Image 1 : le bout du tube est déplacé de {100 * tip:.0f} cm en Y (≥ 20)", "Le tube doit suivre le rig overridé.", 4)
    r.check(rig.location.length >= 1.0, f"Rig placé dans le plan : {rig.location.length:.2f} m de l'origine (≥ 1)", "Déplacez l'objet RIG_Lib (transform overridable).", 2)
    if debug:
        print("[DEBUG] libs", [(l.filepath) for l in libs], "ov", ov, "paths", paths, "ang", round(ang, 1), "tip", round(tip, 3), "loc", tuple(rig.location))


def main():
    r = L.Report("CH06.11 — Rigging avancé et réutilisation")
    ex = L.arg("--exercise") if hasattr(L, "arg") else None
    if ex is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
        ex = argv[argv.index("--exercise") + 1] if "--exercise" in argv else "bendy"
    debug = L.flag("--debug")
    if ex == "bendy":
        bendy(r, debug)
    else:
        override(r, debug)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
