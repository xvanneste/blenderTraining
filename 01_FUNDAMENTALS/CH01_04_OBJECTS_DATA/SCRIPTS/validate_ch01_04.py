"""
validate_ch01_04.py — Correcteur de la ferme (CH01.04).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch01_04.py --python-exit-code 1 -- --exercise farm
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH01.04 — La ferme")
    posts = sorted([o for o in bpy.context.scene.objects if o.name.startswith("GEO_Post_")], key=lambda o: o.name)
    r.check(len(posts) >= 8, f"8 piquets ({len(posts)})",
            "Alt+D puis X 1 Entrée ; Shift+R répète la dernière action.", 2)
    shared = [o for o in posts if o.name != "GEO_Post_08"]
    meshes = {o.data.name for o in shared}
    r.check(len(shared) >= 7 and len(meshes) == 1,
            f"Piquets 01–07 partagent un seul maillage ({len(meshes)} maillage(s))",
            "Utilisez Alt+D (duplication liée), pas Shift+D.", 3)
    p8 = L.obj("GEO_Post_08")
    ok8 = p8 is not None and p8.data.users == 1 and (not shared or p8.data != shared[0].data)
    r.check(ok8, "GEO_Post_08 a ses propres données",
            "Object Data : cliquez le nombre d'utilisateurs à côté du nom (Make Single User).", 2)
    if p8 is not None:
        top = max(v.co.z for v in p8.data.vertices)
        r.check(0.6 < top < 1.0, f"GEO_Post_08 cassé (hauteur {top:.2f} m, attendu ~0,8)",
                "Edit Mode, sélectionnez les 4 sommets du haut, G Z -0.4 Entrée.", 2)
        if shared:
            ref = max(v.co.z for v in shared[0].data.vertices)
            r.check(abs(ref - 1.2) < 0.01, "Les autres piquets ne sont pas cassés",
                    "Si tous sont cassés, Make Single User n'a pas été fait AVANT l'édition.", 2)
    table = L.obj("GEO_Table")
    legs_left = [o for o in bpy.context.scene.objects if o.name.startswith("GEO_TableLeg")]
    r.check(table is not None and len(table.data.vertices) == 40 and not legs_left,
            "Table jointe en un seul objet GEO_Table (40 sommets, plus de pieds séparés)",
            "Sélectionnez les 5 morceaux, plateau actif en dernier, Ctrl+J, puis F2 pour renommer.", 3)
    ra, rb = L.obj("GEO_Rock_A"), L.obj("GEO_Rock_B")
    ok = bool(ra and rb) and ra.data != rb.data and len(ra.data.vertices) == len(rb.data.vertices) == 42
    r.check(ok, "Rochers séparés en GEO_Rock_A et GEO_Rock_B",
            "Edit Mode, A, P > By Loose Parts, puis renommez les deux objets.", 3)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
