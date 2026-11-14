"""
build_ch01_08_files.py — Le grand rangement (CH01.08 : collections, Outliner, parentage).

  STARTER_FILES/ch01_08_living_room_starter.blend
      Un salon de 17 objets, TOUS dans la Scene Collection (aucune organisation) :
      décor (GEO_Floor, GEO_Wall_*), accessoires (GEO_Sofa, GEO_Table, GEO_Vase,
      GEO_LampBase, GEO_LampShade…), lumières, caméra + cible, repères de travail
      (EMP_Guide_1..3, GEO_Debug_Box) qui ne doivent pas apparaître au rendu.
  COMPLETED_EXAMPLES/ch01_08_living_room_solution.blend
      Collections SET / PROPS / LIGHTS / CAMERAS / HELPERS (HELPERS désactivée au rendu),
      abat-jour parenté au pied de lampe sans avoir bougé.
Usage : blender -b --factory-startup --python build_ch01_08_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.08 — LE GRAND RANGEMENT
Tous les objets sont en vrac dans la Scene Collection. Rangez-les :
  SET (sol, murs) · PROPS (meubles et objets) · LIGHTS · CAMERAS (caméra + sa cible)
  HELPERS (EMP_Guide_*, GEO_Debug_Box) : collection DÉSACTIVÉE AU RENDU (icône appareil photo).
Outils : M (Move to Collection > + New Collection), Outliner (glisser-déposer),
         filtre de l'Outliner > Restriction Toggles pour afficher l'icône appareil photo.
Parentage : GEO_LampShade doit devenir enfant de GEO_LampBase (sélectionner l'abat-jour,
puis le pied en dernier, Ctrl+P > Object). L'abat-jour ne doit pas bouger.
Vérifiez : déplacez le pied, l'abat-jour suit. Puis Ctrl+Z.
"""

LAYOUT = {
    "SET": [("GEO_Floor", "plane", (0, 0, 0), (8, 8, 1)), ("GEO_Wall_Back", "cube", (0, 4, 1.4), (8, 0.1, 2.8)),
            ("GEO_Wall_Left", "cube", (-4, 0, 1.4), (0.1, 8, 2.8))],
    "PROPS": [("GEO_Sofa", "cube", (0, 2.8, 0.4), (2.2, 0.9, 0.8)), ("GEO_Table", "cube", (0, 1.2, 0.22), (1.2, 0.6, 0.44)),
              ("GEO_Vase", "cyl", (0.3, 1.2, 0.6), (0.12, 0.12, 0.32)), ("GEO_Rug", "cube", (0, 1.4, 0.005), (3, 2, 0.01)),
              ("GEO_LampBase", "cyl", (-2.8, 3, 0.75), (0.08, 0.08, 1.5)), ("GEO_LampShade", "cyl", (-2.8, 3, 1.6), (0.3, 0.3, 0.3)),
              ("GEO_Shelf", "cube", (-3.7, 1, 1.0), (0.4, 1.6, 2.0))],
    "HELPERS": [("GEO_Debug_Box", "cube", (2, -2, 0.25), (0.5, 0.5, 0.5))],
}


def add(name, kind, loc, scale, col):
    if kind == "plane":
        o = L.plane(name, col, size=1, location=loc)
    elif kind == "cyl":
        o = L.cylinder(name, col, radius=1, depth=1, location=loc)
    else:
        o = L.cube(name, col, size=1, location=loc)
    o.scale = scale
    return o


def build(solution):
    L.reset("SC_LivingRoom")
    root = bpy.context.scene.collection
    cols = {k: (L.collection(k) if solution else root) for k in ("SET", "PROPS", "LIGHTS", "CAMERAS", "HELPERS")}
    for cname, items in LAYOUT.items():
        for name, kind, loc, sc in items:
            add(name, kind, loc, sc, cols[cname])
    for i, loc in enumerate([(-3, -3, 0.1), (3, -3, 0.1), (0, 3.9, 2.7)]):
        L.empty(f"EMP_Guide_{i + 1}", cols["HELPERS"], loc, "ARROWS", 0.4)
    tgt = L.empty("EMP_CamTarget", cols["CAMERAS"], (0, 2, 0.8))
    L.camera("CAM_Main", cols["CAMERAS"], (3.5, -4.5, 1.7), 35, tgt)
    L.light("LGT_Key", cols["LIGHTS"], "AREA", (-2, -2, 2.6), 300, 1.5, target=tgt)
    L.light("LGT_Window", cols["LIGHTS"], "SUN", (0, 0, 5), 3, rotation=(50, 0, -30))
    L.world((0.3, 0.32, 0.36), 0.6)
    if solution:
        cols["HELPERS"].hide_render = True
        shade, base = bpy.data.objects["GEO_LampShade"], bpy.data.objects["GEO_LampBase"]
        mw = shade.matrix_world.copy()
        shade.parent = base
        shade.matrix_parent_inverse = base.matrix_world.inverted()
        bpy.context.view_layer.update()
        assert (shade.matrix_world.translation - mw.translation).length < 1e-5
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_08_living_room_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_08_living_room_solution.blend"))


if __name__ == "__main__":
    L.run(main)
