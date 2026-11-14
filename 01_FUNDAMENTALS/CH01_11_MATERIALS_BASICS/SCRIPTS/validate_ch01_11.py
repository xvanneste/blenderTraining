"""
validate_ch01_11.py — Correcteur « la maison en couleurs » (CH01.11).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch01_11.py --python-exit-code 1 -- --exercise colors [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def bsdf(mat):
    if mat is None or mat.node_tree is None:
        return None
    return next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)


def face_mat(o, poly):
    slots = o.material_slots
    return slots[poly.material_index].material if poly.material_index < len(slots) else None


def main():
    r = L.Report("CH01.11 — La maison en couleurs")
    h = L.obj("GEO_House")
    if not r.check(h is not None, "GEO_House présent", "", 1):
        return r.finish()
    polys = h.data.polygons
    roof = [p for p in polys if p.normal.z > 0.3 and p.center.z > 2.0]
    door = min((p for p in polys if p.normal.y < -0.9 and p.center.z < 2.0), key=lambda p: p.area)
    walls = [p for p in polys if p not in roof and p != door]
    wb = bsdf(bpy.data.materials.get("MAT_Wall"))
    c = wb.inputs["Base Color"].default_value if wb else (0, 0, 0, 1)
    r.check(wb and min(c[:3]) > 0.6, "MAT_Wall éclairci (blanc cassé)", "Material > Surface > Base Color.", 1)
    r.check(all(face_mat(h, p) and face_mat(h, p).name == "MAT_Wall" for p in walls), "Murs en MAT_Wall", "", 1)
    rm = [face_mat(h, p) for p in roof]
    r.check(roof and all(m and m.name == "MAT_Roof" for m in rm), "Les 2 pans du toit en MAT_Roof",
            "Edit Mode, mode faces, sélectionnez les 2 pans, choisissez l'emplacement MAT_Roof, Assign.", 3)
    rb = bsdf(bpy.data.materials.get("MAT_Roof"))
    rc = rb.inputs["Base Color"].default_value if rb else (0, 0, 0, 1)
    r.check(rb and rc[0] > rc[1] and rc[0] > rc[2] and rb.inputs["Roughness"].default_value >= 0.6,
            "MAT_Roof rouge et rugueux", "Base Color rouge, Roughness ≥ 0,6.", 1)
    dm = face_mat(h, door)
    r.check(dm and dm.name == "MAT_Door", "Face de porte en MAT_Door", "Sélectionnez la seule face de porte, Assign.", 3)
    g = L.obj("GEO_Gutter")
    gb = bsdf(g.active_material) if g else None
    r.check(gb and gb.inputs["Metallic"].default_value >= 0.99 and gb.inputs["Roughness"].default_value <= 0.4,
            "Gouttière métallique (Metallic 1, Roughness ≤ 0,4)", "Metallic = 1 : le métal reflète sa couleur.", 2)
    lt = L.obj("GEO_Lantern")
    lb = bsdf(lt.active_material) if lt else None
    ok = lb and lb.inputs["Emission Strength"].default_value >= 5 and lb.inputs["Emission Color"].default_value[2] < \
        lb.inputs["Emission Color"].default_value[0]
    r.check(ok, "Lanterne émissive jaune (Strength ≥ 5)", "Material > Emission > Color jaune, Strength 5 à 10.", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 8)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
