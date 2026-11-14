"""
validate_ch01_08.py — Correcteur du grand rangement (CH01.08).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch01_08.py --python-exit-code 1 -- --exercise organize [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

EXPECT = {
    "SET": ["GEO_Floor", "GEO_Wall_Back", "GEO_Wall_Left"],
    "PROPS": ["GEO_Sofa", "GEO_Table", "GEO_Vase", "GEO_Rug", "GEO_LampBase", "GEO_LampShade", "GEO_Shelf"],
    "LIGHTS": ["LGT_Key", "LGT_Window"],
    "CAMERAS": ["CAM_Main", "EMP_CamTarget"],
    "HELPERS": ["EMP_Guide_1", "EMP_Guide_2", "EMP_Guide_3", "GEO_Debug_Box"],
}


def main():
    r = L.Report("CH01.08 — Le grand rangement")
    sc = bpy.context.scene
    for cname, names in EXPECT.items():
        col = bpy.data.collections.get(cname)
        if not r.check(col is not None and col.name in sc.collection.children, f"Collection {cname} dans la scène",
                       "M > + New Collection, ou clic droit dans l'Outliner > New Collection.", 1):
            continue
        missing = [n for n in names if n not in col.objects]
        r.check(not missing, f"{cname} contient les bons objets" + (f" (manque : {', '.join(missing)})" if missing else ""),
                "Sélectionnez les objets, M, choisissez la collection.", 2)
    loose = [o.name for o in sc.collection.objects]
    r.check(not loose, f"Plus aucun objet en vrac dans la Scene Collection ({len(loose)})", "M sur les objets restants.", 2)
    hel = bpy.data.collections.get("HELPERS")
    r.check(hel is not None and hel.hide_render, "HELPERS désactivée au rendu",
            "Outliner > filtre (entonnoir) > icône appareil photo, puis cliquez-la sur HELPERS.", 3)
    r.check(hel is not None and not hel.hide_viewport and all(not o.hide_get() for o in hel.objects if o.name in sc.objects),
            "HELPERS toujours visible dans le viewport (pour travailler)", "Ne masquez la collection qu'au rendu.", 1, mandatory=False)
    shade, base = L.obj("GEO_LampShade"), L.obj("GEO_LampBase")
    r.check(shade and base and shade.parent == base, "Abat-jour enfant du pied de lampe",
            "Abat-jour, puis pied en dernier (actif), Ctrl+P > Object.", 3)
    if shade:
        r.check((shade.matrix_world.translation - Vector((-2.8, 3, 1.6))).length < 0.005, "Abat-jour resté en place",
                "Le parentage ne doit pas déplacer l'enfant : Ctrl+P > Object (ou Object (Keep Transform)).", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
