"""
build_ch18_08_files.py — Scène « calques, masques, modificateurs, transformations » (CH18.08).

  STARTER_FILES/ch18_08_layers_starter.blend
      GP_Practice déjà dessiné, 6 calques : BG (mur et fenêtre), FX_LIGHT (rayons de soleil sur
      toute la feuille), MASK_WINDOW (vitres remplies), SHADE (ombre au sol), LINE (personnage),
      CLOUDS (nuages, mal placés). Aucun modificateur, aucun masque.
  COMPLETED_EXAMPLES/ch18_08_layers_solution.blend (+ _reference.png, rendu image 60)
      Thickness + Noise sur LINE, Tint sur BG, Build sur LINE ; FX_LIGHT masqué par MASK_WINDOW ;
      SHADE en Multiply ; CLOUDS décalé par la transformation du calque ; effet Shadow.
Usage : blender -b --factory-startup --python build_ch18_08_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH18.08 — CALQUES, MODIFICATEURS, TRANSFORMATIONS (GP_Practice, Num 0)
Le dessin est fourni. NE L'APPLIQUEZ PAS : tout doit rester non destructif.
1. Modificateurs (Properties > Modifiers > Add Modifier) sur GP_Practice :
   - Deform > Thickness (Influence > Layer : LINE) : trait du personnage plus épais ;
   - Deform > Noise (Layer : LINE) : léger tremblement ;
   - Color > Tint (Layer : BG) : teinte chaude du décor ;
   - Generate > Build (Layer : LINE) : le personnage se dessine de l'image 1 à 48.
2. Masque : sélectionnez le calque FX_LIGHT, cochez Masks, + > MASK_WINDOW : les rayons ne
   doivent apparaître qu'à travers la fenêtre. Puis MASK_WINDOW : Opacity = 0 (NE PAS fermer son
   œil : en 5.3, un calque masque caché ne masque plus rien).
3. Calque SHADE : Blend Mode = Multiply, Opacity 0.6.
4. Calque CLOUDS : panneau Layers > Transform, Translation X = 2 (nuages déplacés sans toucher aux
   traits ni à l'objet).
5. (Facultatif) Effects > Add Effect > Shadow.
Vérification : SCRIPTS/validate_ch18_08.py -- --exercise layers --render
"""
WIN = (-3.6, -0.6, -0.6, 2.4)


def draw(ob, drw):
    ink = 0
    wall = G.material(ob, "MAT_GP_Wall", (0.02, 0.02, 0.02), fill=(0.78, 0.74, 0.68))
    sky = G.material(ob, "MAT_GP_Sky", (0.02, 0.02, 0.02), fill=(0.55, 0.75, 0.95))
    light = G.material(ob, "MAT_GP_Light", (1.0, 0.85, 0.3))
    shade = G.material(ob, "MAT_GP_Shade", (0.02, 0.02, 0.02), fill=(0.35, 0.3, 0.5))
    cloud = G.material(ob, "MAT_GP_Cloud", (0.3, 0.3, 0.35), fill=(1.0, 1.0, 1.0))
    # BG : mur, sol, fenêtre (cadre + vitres bleues)
    d = drw["BG"]
    G.polyline(d, [(-6, -3.375), (6, -3.375), (6, 3.375), (-6, 3.375)], 0.005, wall, cyclic=True, fill=True)
    G.polyline(d, [(-6, -1.6), (6, -1.6)], 0.012, ink)
    x0, z0, x1, z1 = WIN
    G.polyline(d, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], 0.005, sky, cyclic=True, fill=True)
    G.rect(d, x0, z0, x1, z1, 0.03, ink)
    G.line(d, ((x0 + x1) / 2, z0), ((x0 + x1) / 2, z1), 0.02, ink)
    G.line(d, (x0, (z0 + z1) / 2), (x1, (z0 + z1) / 2), 0.02, ink)
    # CLOUDS : nuages dans la fenêtre... mais mal placés (à gauche de la fenêtre)
    d = drw["CLOUDS"]
    for cx, cz in ((-5.2, 1.6), (-4.6, 1.9), (-4.0, 1.6)):
        G.circle(d, (cx, cz), 0.4, 0.01, cloud, 24, fill_mat=None)
        d.strokes[len(d.strokes) - 1].material_index = cloud
    # FX_LIGHT : rayons sur toute la feuille (à limiter par le masque)
    d = drw["FX_LIGHT"]
    for k in range(40):
        x = -6.5 + k * 0.33
        G.polyline(d, [(x, 3.4), (x + 2.2, -3.4)], 0.05, light, opacity=0.45)
    # MASK_WINDOW : forme des vitres
    d = drw["MASK_WINDOW"]
    G.polyline(d, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], 0.005, sky, cyclic=True, fill=True)
    # SHADE : ombre au sol sous le personnage
    d = drw["SHADE"]
    G.polyline(d, [(2.0 + 1.3 * math.cos(t), -2.6 + 0.25 * math.sin(t)) for t in [i * 2 * math.pi / 32 for i in range(32)]],
               0.005, shade, cyclic=True, fill=True, hide_stroke=True)
    # LINE : personnage
    G.mannequin(drw["LINE"], 2.0, -2.6, 3.6, "reach", 0.01, ink)


def solve(ob):
    gp = ob.data
    lay = {l.name: l for l in gp.layers}
    m = ob.modifiers.new("Thickness", "GREASE_PENCIL_THICKNESS")
    m.tree_node_filter = "LINE"
    m.use_uniform_thickness = False
    m.thickness_factor = 2.5
    m = ob.modifiers.new("Noise", "GREASE_PENCIL_NOISE")
    m.tree_node_filter = "LINE"
    m.factor = 0.3
    m = ob.modifiers.new("Tint", "GREASE_PENCIL_TINT")
    m.tree_node_filter = "BG"
    m.color = (1.0, 0.6, 0.25)
    m.factor = 0.2
    m = ob.modifiers.new("Build", "GREASE_PENCIL_BUILD")
    m.tree_node_filter = "LINE"
    m.length = 48
    lay["FX_LIGHT"].use_masks = True
    lay["FX_LIGHT"].mask_layers.add(lay["MASK_WINDOW"])
    lay["MASK_WINDOW"].opacity = 0.0   # invisible mais actif (un calque masque CACHÉ n'agit plus, 5.3)
    lay["SHADE"].blend_mode = "MULTIPLY"
    lay["SHADE"].opacity = 0.6
    lay["CLOUDS"].translation = (2.0, 0.0, 0.0)
    fx = ob.shader_effects.new("Shadow", "FX_SHADOW")
    fx.offset = (8, -8)
    fx.shadow_color = (0, 0, 0, 0.35)


def build(sol):
    L.reset("SC_Layers")
    names = ("BG", "CLOUDS", "FX_LIGHT", "MASK_WINDOW", "SHADE", "LINE")   # du bas vers le haut
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, (), names)
    draw(ob, drw)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, 72
    if sol:
        solve(ob)
    L.instructions(NOTE)
    return sc


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_08_layers_starter.blend"))
    sc = build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_08_layers_solution.blend"))
    sc.render.resolution_percentage = 60
    for f, tag in ((60, "reference"), (20, "build_frame20")):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(os.path.dirname(p), f"ch18_08_layers_{tag}.png")
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
