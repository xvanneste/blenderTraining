"""
build_ch04_04_files.py — « Shader Editor et nœuds » (CH04.04).

Une sphère SPH_Rust et un matériau MAT_RustyMetal à construire avec des nœuds : métal gris usé + rouille pilotés par un bruit.
Graphe attendu (solution) :
  Texture Coordinate (Object) -> Mapping -> Noise Texture -> Color Ramp -> Mix (facteur) : A = rouille, B = acier gris -> Base Color
  Color Ramp (1 = acier, 0 = rouille) -> Metallic (le métal apparaît là où il n'y a pas de rouille) ; Noise -> Map Range -> Roughness ; Principled BSDF -> Material Output.
  STARTER_FILES/ch04_04_nodes_starter.blend : Principled BSDF par défaut seul, relié à la sortie.
  COMPLETED_EXAMPLES/ch04_04_nodes_solution.blend (+ _reference.png : deux vues)
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : orphan, const_metal, no_mapping, no_output, flat_ramp, huge_scale
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_04_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH04.04 — SHADER EDITOR ET NŒUDS (SPH_Rust, matériau MAT_RustyMetal)
Construisez le graphe suivant dans le Shader Editor :
1. Texture Coordinate (sortie Object) -> Mapping -> Noise Texture (Scale entre 2 et 30).
2. Noise Texture (Fac) -> Color Ramp (deux stops : blanc = acier, noir = rouille) -> facteur d'un Mix (type Color).
3. Mix : A = rouille (rouge-brun), B = acier gris clair ; Result -> Base Color du Principled BSDF.
4. Color Ramp -> Metallic ; Noise Texture -> Map Range -> Roughness.
5. Principled BSDF -> Surface du Material Output. Aucun nœud orphelin (dont aucune sortie n'est utilisée), 7 à 18 nœuds.
Vérification : SCRIPTS/validate_ch04_04.py -- --exercise nodes
"""
STEEL = (0.50, 0.52, 0.55, 1.0)
RUST = (0.45, 0.15, 0.05, 1.0)


def inp(node, ident):
    return next(i for i in node.inputs if i.identifier == ident)


def out(node, ident):
    return next(o for o in node.outputs if o.identifier == ident)


def build_nodes(mat, kind):
    nt = mat.node_tree
    nt.nodes.clear()
    N = nt.nodes
    lk = nt.links.new
    o = N.new("ShaderNodeOutputMaterial"); o.location = (900, 0)
    b = N.new("ShaderNodeBsdfPrincipled"); b.location = (600, 0)
    tc = N.new("ShaderNodeTexCoord"); tc.location = (-700, 0)
    mp = N.new("ShaderNodeMapping"); mp.location = (-500, 0)
    nz = N.new("ShaderNodeTexNoise"); nz.location = (-300, 0)
    nz.inputs["Scale"].default_value = 6.0
    nz.inputs["Detail"].default_value = 8.0
    nz.inputs["Roughness"].default_value = 0.6
    cr = N.new("ShaderNodeValToRGB"); cr.location = (-100, 120)
    cr.color_ramp.elements[0].position = 0.45
    cr.color_ramp.elements[0].color = (1, 1, 1, 1)
    cr.color_ramp.elements[1].position = 0.62
    cr.color_ramp.elements[1].color = (0, 0, 0, 1)
    mx = N.new("ShaderNodeMix"); mx.location = (200, 150)
    mx.data_type = "RGBA"
    inp(mx, "A_Color").default_value = RUST
    inp(mx, "B_Color").default_value = STEEL
    mr = N.new("ShaderNodeMapRange"); mr.location = (200, -150)
    mr.inputs["From Min"].default_value = 0.3
    mr.inputs["From Max"].default_value = 0.7
    mr.inputs["To Min"].default_value = 0.25
    mr.inputs["To Max"].default_value = 0.85
    lk(b.outputs["BSDF"], o.inputs["Surface"])
    lk(tc.outputs["Object"], mp.inputs["Vector"])
    lk(mp.outputs["Vector"], nz.inputs["Vector"])
    lk(nz.outputs["Fac"], cr.inputs["Fac"])
    lk(cr.outputs["Color"], inp(mx, "Factor_Float"))
    lk(out(mx, "Result_Color"), b.inputs["Base Color"])
    lk(cr.outputs["Color"], b.inputs["Metallic"])
    lk(nz.outputs["Fac"], mr.inputs["Value"])
    lk(mr.outputs["Result"], b.inputs["Roughness"])
    # --- variantes fausses ---
    if kind == "orphan":
        x = N.new("ShaderNodeTexNoise"); x.location = (-300, -350)
    elif kind == "const_metal":
        for l in list(nt.links):
            if l.to_socket == b.inputs["Metallic"]:
                nt.links.remove(l)
        b.inputs["Metallic"].default_value = 1.0
    elif kind == "no_mapping":
        N.remove(mp)
        lk(tc.outputs["Object"], nz.inputs["Vector"])
    elif kind == "no_output":
        for l in list(nt.links):
            if l.to_node == o:
                nt.links.remove(l)
    elif kind == "flat_ramp":
        cr.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)
        cr.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1)
    elif kind == "huge_scale":
        nz.inputs["Scale"].default_value = 400.0


def build(kind):
    L.reset("SC_NODES")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -5.2, 1.2), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.5))
    cam2 = L.camera("CAM_High", c, (3.2, -4.4, 3.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.5))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    mat = bpy.data.materials.new("MAT_RustyMetal")
    ob = L.sphere("SPH_Rust", L.collection("OBJETS"), None, radius=0.7, location=(0, 0, 0.7), segments=64, ring_count=32)
    ob.data.materials.append(mat)
    if kind == "starter":
        nt = mat.node_tree
        assert any(n.type == "BSDF_PRINCIPLED" for n in nt.nodes)
    else:
        build_nodes(mat, kind)
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for cam in ("CAM_Front", "CAM_High"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out_path
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out_dir = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_04_nodes_starter.blend"))
    for k in ("orphan", "const_metal", "no_mapping", "no_output", "flat_ramp", "huge_scale"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_04_nodes_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_04_nodes_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_04_nodes_reference.png"))


if __name__ == "__main__":
    L.run(main)
