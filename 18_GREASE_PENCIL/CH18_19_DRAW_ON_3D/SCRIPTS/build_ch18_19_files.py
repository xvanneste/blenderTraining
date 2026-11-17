"""
build_ch18_19_files.py — « Personnage 2D dans un décor 3D » (CH18.19, phase 18 module F).

  STARTER_FILES/ch18_19_hybrid_starter.blend
      Décor 3D (collection SET : sol, mur du fond, mur gauche, deux caisses, étagère), caméra
      CAM_Shot (35 mm), soleil, EEVEE ; objets GP vides GP_Character (calque USER_Char) et GP_Decal
      (calque USER_Decal) ; passe Z DÉSACTIVÉE (à activer) ; aucune Line Art.
  COMPLETED_EXAMPLES/ch18_19_hybrid_solution.blend (+ _reference.png)
      GP_LineArt : objet GP avec modificateur Line Art (source : collection SET) ; personnage 2D
      dessiné DEBOUT dans le décor (plan X-Z à y = 1,0, pieds au sol), en partie caché par la caisse
      avant ; affiche et fenêtre dessinées SUR le mur du fond (placement Surface) ; passe Z activée.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_19_files.py
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
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
CY = 1.0                     # profondeur du personnage
WALL_Y = 4.0                 # face avant du mur du fond (y = 4)
NOTE = """CH18.19 — UN PERSONNAGE 2D DANS UN DÉCOR 3D (vue caméra : Num 0)
1. Contours du décor : Add > Grease Pencil > Collection Line Art (collection active : SET), ou un objet
   GP + modificateur Line Art (Source Type : Collection, SET). Le trait suit la caméra.
2. Personnage : GP_Character, calque USER_Char, mode Draw. Drawing Plane : Front (X-Z) ; placez le
   curseur 3D au sol, derrière la caisse avant (≈ x 0,9, y 1,0) ; Stroke Placement : 3D Cursor.
   Dessinez-le DEBOUT, pieds au sol, à taille humaine (1,2 à 2,2 m), en partie caché par la caisse.
3. Sur le mur : GP_Decal, calque USER_Decal, Stroke Placement : Surface ; dessinez une affiche ou une
   fenêtre SUR le mur du fond (au moins 3 traits).
4. View Layer Properties > Passes > Data > Z : COCHÉ (sinon, au rendu final, le GP passe devant les
   objets 3D qui devraient le cacher).
Vérification : SCRIPTS/validate_ch18_19.py -- --exercise hybrid
"""


def set_scene():
    sc = L.reset("SC_Hybrid")
    s = L.collection("SET")
    floor = L.material("MAT_Floor", (0.55, 0.5, 0.45), 0.8)
    wall = L.material("MAT_Wall", (0.75, 0.72, 0.66), 0.9)
    wood = L.material("MAT_Crate", (0.55, 0.38, 0.2), 0.7)
    L.plane("GEO_Floor", s, floor, size=12, location=(0, 1, 0))
    L.cube("GEO_WallBack", s, wall, size=1, location=(0, WALL_Y + 0.1, 2), scale=(12, 0.2, 4))
    L.cube("GEO_WallLeft", s, wall, size=1, location=(-4.1, 1, 2), scale=(0.2, 6, 4))
    L.cube("GEO_CrateFront", s, wood, size=1, location=(0.75, -0.1, 0.45), scale=(0.9, 0.9, 0.9))
    L.cube("GEO_CrateBack", s, wood, size=1, location=(-2.2, 2.6, 0.5), scale=(1.0, 1.0, 1.0))
    L.cube("GEO_Shelf", s, wood, size=1, location=(2.6, 3.6, 1.2), scale=(1.6, 0.5, 0.08))
    cams = L.collection("CAMERAS")
    cam = L.camera("CAM_Shot", cams, (0.3, -7.5, 1.5), 35, make_active=True)
    S.look_at(cam, (0.3, 1.5, 1.1))
    L.light("LGT_Sun", L.collection("LIGHTS"), "SUN", (2, -3, 6), 3.0, rotation=(50, 0, 30))
    L.world((0.55, 0.6, 0.68), 0.6, "WO_Room")
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    bpy.context.view_layer.use_pass_z = False
    return sc


def gp_object(name, layer):
    ob = G.new_object(name, L.collection("DRAWING"))
    G.material(ob, "MAT_GP_Ink", (0.02, 0.02, 0.03))
    G.layer(ob, layer)
    ob.data.layers[layer].use_lights = False
    return ob


def character(ob):
    d = G.layer(ob, "USER_Char")
    skin = G.material(ob, "MAT_GP_Coat", (0.05, 0.05, 0.08), fill=(0.85, 0.35, 0.2))
    x, h = 0.95, 1.75

    def P(px, pz):
        return (px, CY, pz)

    G.polyline(d, [P(x + 0.11 * math.cos(t), h - 0.13 + 0.13 * math.sin(t)) for t in [i * 2 * math.pi / 24 for i in range(25)]], 0.01, 0, cyclic=True)
    G.polyline(d, [P(x - 0.2, 0.85), P(x - 0.22, 1.45), P(x + 0.22, 1.45), P(x + 0.2, 0.85)], 0.01, skin, cyclic=True)   # manteau
    for sx in (-0.1, 0.1):
        G.polyline(d, [P(x + sx, 0.85), P(x + sx * 1.3, 0.45), P(x + sx * 1.2, 0.03)], 0.012, 0)   # jambes
        G.line(d, P(x + sx * 1.2, 0.03), P(x + sx * 1.2 + 0.12, 0.0), 0.012, 0)                  # pieds
    G.polyline(d, [P(x - 0.22, 1.42), P(x - 0.42, 1.1), P(x - 0.35, 0.82)], 0.012, 0)              # bras
    G.polyline(d, [P(x + 0.22, 1.42), P(x + 0.45, 1.2), P(x + 0.55, 1.45)], 0.012, 0)
    G.line(d, P(x + 0.03, h - 0.1), P(x + 0.07, h - 0.1), 0.012, 0)                                  # œil (regard à droite)
    G.line(d, P(x - 0.04, h - 0.2), P(x + 0.06, h - 0.19), 0.01, 0)                                  # bouche


def decal(ob):
    d = G.layer(ob, "USER_Decal")
    red = G.material(ob, "MAT_GP_Poster", (0.1, 0.05, 0.05), fill=(0.8, 0.2, 0.15))
    y = WALL_Y - 0.005                                                  # posé sur la face avant du mur

    def P(px, pz):
        return (px, y, pz)

    G.polyline(d, [P(-1.6, 1.4), P(-0.6, 1.4), P(-0.6, 2.8), P(-1.6, 2.8)], 0.012, red, cyclic=True)        # affiche
    G.polyline(d, [P(-1.1 + 0.3 * math.cos(t), 2.3 + 0.3 * math.sin(t)) for t in [i * 2 * math.pi / 20 for i in range(21)]], 0.01, 0)
    G.line(d, P(-1.45, 1.7), P(-0.75, 1.7), 0.01, 0)
    G.polyline(d, [P(1.2, 1.6), P(2.4, 1.6), P(2.4, 2.8), P(1.2, 2.8)], 0.012, 0, cyclic=True)              # fenêtre peinte
    G.line(d, P(1.8, 1.6), P(1.8, 2.8), 0.01, 0)
    G.line(d, P(1.2, 2.2), P(2.4, 2.2), 0.01, 0)


def lineart():
    ob = G.new_object("GP_LineArt", L.collection("DRAWING"))
    ink = G.material(ob, "MAT_GP_LineArt", (0.02, 0.02, 0.03))
    G.layer(ob, "Lines")
    ob.data.layers["Lines"].use_lights = False
    m = ob.modifiers.new("Line Art", "LINEART")
    m.source_type = "COLLECTION"
    m.source_collection = bpy.data.collections["SET"]
    m.target_layer = "Lines"
    m.target_material = bpy.data.materials["MAT_GP_LineArt"]
    m.radius = 0.02                       # en mètres : 4 mm serait invisible à 8 m
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    n = sum(len(fr.drawing.strokes) for lay in ev.data.layers for fr in lay.frames)
    print(f"[BCMA] Line Art : {n} traits générés")
    return ob


def build(sol):
    sc = set_scene()
    ch = gp_object("GP_Character", "USER_Char")
    dc = gp_object("GP_Decal", "USER_Decal")
    if sol:
        character(ch)
        decal(dc)
        lineart()
        bpy.context.view_layer.use_pass_z = True
    L.instructions(NOTE)
    return sc


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_19_hybrid_starter.blend"))
    sc = build(True)
    L.save(os.path.join(out, "ch18_19_hybrid_solution.blend"))
    sc.render.resolution_percentage = 50
    sc.render.filepath = os.path.join(out, "ch18_19_hybrid_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
