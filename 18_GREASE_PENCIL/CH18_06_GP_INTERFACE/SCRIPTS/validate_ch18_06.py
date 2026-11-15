"""
validate_ch18_06.py — Correcteur CH18.06 (objets Grease Pencil organisés dans une scène 3D).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch18_06.py --python-exit-code 1 -- --exercise organize [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402


def world_points(ob):
    pts = []
    for lay in ob.data.layers:
        for fr in lay.frames:
            for s in fr.drawing.strokes:
                for p in s.points:
                    pts.append(ob.matrix_world @ lay.matrix_local @ p.position)
    return pts


def n_strokes(ob, lname):
    lay = next((l for l in ob.data.layers if l.name == lname), None)
    return sum(len(fr.drawing.strokes) for fr in lay.frames) if lay else 0


def main():
    r = L.Report("CH18.06 — Objets Grease Pencil dans la scène")
    sc = bpy.context.scene
    cam, house = L.obj("CAM_Shot"), L.obj("GEO_House")
    if not r.check(cam is not None and house is not None, "Caméra CAM_Shot et maison GEO_House conservées",
                   "Ne supprimez pas les éléments du décor fourni.", 1):
        return r.finish()
    col = bpy.data.collections.get("DRAWINGS")
    r.check(col is not None and col.name in sc.collection.children, "Collection DRAWINGS dans la scène",
            "Outliner : clic droit > New Collection, renommez-la DRAWINGS.", 1)
    cpos = cam.matrix_world.translation
    d_house = (house.matrix_world.translation - cpos).length
    for name, where in (("GP_Character", "front"), ("GP_Background", "back")):
        ob = L.obj(name)
        if not r.check(ob is not None and ob.type == "GREASEPENCIL", f"Objet Grease Pencil {name}",
                       "Add > Grease Pencil > Blank, puis F2 pour renommer.", 2):
            continue
        r.check(col is not None and ob.name in col.objects, f"{name} rangé dans DRAWINGS", "M > DRAWINGS.", 1)
        pts = world_points(ob)
        if not r.check(len(pts) >= 20, f"{name} : {len(pts)} points dessinés (≥ 20)", "Dessinez en Draw Mode (Ctrl+Tab).", 2):
            continue
        dist = sum((p - cpos).length for p in pts) / len(pts)
        if where == "front":
            r.check(dist < d_house - 0.5, f"{name} devant la maison ({dist:.1f} m < {d_house:.1f} m de la caméra)",
                    "Placez l'objet entre la caméra et la maison (G puis Y), ou Stroke Placement > 3D Cursor.", 2)
        else:
            r.check(dist > d_house + 0.5, f"{name} derrière la maison ({dist:.1f} m > {d_house:.1f} m de la caméra)",
                    "Éloignez l'objet de la caméra, derrière la maison (G puis Y).", 2)
        inside = 0
        for p in pts:
            v = world_to_camera_view(sc, cam, p)
            if 0 <= v.x <= 1 and 0 <= v.y <= 1 and v.z > 0:
                inside += 1
        r.check(inside / len(pts) >= 0.6, f"{name} visible dans CAM_Shot ({100 * inside / len(pts):.0f} % des points)",
                "Vérifiez en vue caméra (Num 0) que le dessin est dans le cadre.", 1)
    r.check(bpy.context.view_layer.use_pass_z, "Passe Z activée (occlusion correcte du GP au rendu final)",
            "Properties > View Layer > Passes > Data > Z.", 2)
    ch = L.obj("GP_Character")
    if ch is not None and ch.type == "GREASEPENCIL":
        names = [l.name for l in ch.data.layers]
        r.check(all(n in names for n in ("LINE", "COLOR", "SKETCH")), f"Calques LINE, COLOR, SKETCH ({', '.join(names)})",
                "Properties > Object Data > Layers : bouton + puis double-clic pour renommer.", 2)
        grp = next((g for g in ch.data.layer_groups if g.name == "CHAR"), None)
        inside = [l.name for l in ch.data.layers if l.parent_group is not None and l.parent_group.name == "CHAR"]
        r.check(grp is not None and "LINE" in inside and "COLOR" in inside, "Groupe de calques CHAR contenant LINE et COLOR",
                "Icône dossier (Add New Layer Group), renommez CHAR, glissez-y LINE et COLOR.", 2)
        sk = next((l for l in ch.data.layers if l.name == "SKETCH"), None)
        r.check(sk is not None and sk.lock, "Calque SKETCH verrouillé", "Cliquez le cadenas du calque SKETCH.", 1)
        r.check(n_strokes(ch, "LINE") >= 6, f"LINE : {n_strokes(ch, 'LINE')} traits (≥ 6)", "Dessinez le personnage sur LINE.", 2)
    bg = L.obj("GP_Background")
    if bg is not None and bg.type == "GREASEPENCIL":
        tot = sum(len(fr.drawing.strokes) for l in bg.data.layers for fr in l.frames)
        r.check(tot >= 6, f"GP_Background : {tot} traits (≥ 6)", "Dessinez collines ou nuages.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
