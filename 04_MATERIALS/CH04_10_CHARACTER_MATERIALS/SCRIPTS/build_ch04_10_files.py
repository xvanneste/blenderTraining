"""
build_ch04_10_files.py — « Matériaux de personnages » (CH04.10).

Quatre sphères d'essai : SPH_Skin (peau), SPH_Eye (œil), SPH_Hair (cheveux), SPH_Cloth (tissu), matériaux MAT_<Nom>. Rendu Cycles.
  MAT_Skin  : Base Color chair (0,65 ; 0,42 ; 0,34) ; Subsurface Weight 1, Radius (1 ; 0,2 ; 0,1), Scale 0,05 ; Roughness 0,45 ; pores : Noise fin -> Bump -> Normal
  MAT_Eye   : Gradient [Linear, Mapping] -> Color Ramp (sclère claire / iris brun, interpolation constante) -> Base Color ; Roughness 0,2 ; Coat Weight 1, Coat Roughness 0,02 (cornée humide)
  MAT_Hair  : Principled Hair BSDF (Chiang, couleur (0,12 ; 0,06 ; 0,03), Roughness 0,3) -> Surface
  MAT_Cloth : Base Color bleu (0,15 ; 0,25 ; 0,55), Roughness 0,8, Sheen Weight 0,5 ; trame : Wave (bandes fines) -> Bump -> Normal
  STARTER_FILES/ch04_10_character_starter.blend : quatre matériaux Principled par défaut.
  COMPLETED_EXAMPLES/ch04_10_character_solution.blend (+ _reference.png)
  COUNTER_EXAMPLES/ : skin_opaque, skin_uniform_radius, eye_dry, hair_principled, cloth_no_sheen
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_10_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NAMES = ("Skin", "Eye", "Hair", "Cloth")
NOTE = """CH04.10 — MATÉRIAUX DE PERSONNAGES (SPH_Skin / Eye / Hair / Cloth, matériaux MAT_<Nom>, moteur Cycles)
1. Peau : Base Color chair (R > V > B, luminance 0,3–0,8) ; Subsurface Weight ≥ 0,5 avec un Subsurface Radius R > V > B (R ≥ 3 × B) et Scale 0,01–0,2 ; Roughness 0,3–0,65 ;
   Bump alimenté par une texture fine relié à Normal (pores).
2. Œil : Base Color pilotée par un dégradé (Gradient Texture) et une Color Ramp (sclère claire / iris sombre, écart de luminance ≥ 0,3) ; Roughness ≤ 0,4 ;
   Coat Weight ≥ 0,8 avec Coat Roughness ≤ 0,1 (la cornée humide brille).
3. Cheveux : nœud Principled Hair BSDF relié à Surface ; couleur de luminance ≤ 0,4 (ou mélanine) ; Roughness 0,2–0,5.
4. Tissu : Sheen Weight ≥ 0,3 ; Roughness ≥ 0,6 ; Metallic 0 ; trame : texture -> Bump -> Normal.
Vérification : SCRIPTS/validate_ch04_10.py -- --exercise character
"""


def principled(mat):
    return mat.node_tree.nodes["Principled BSDF"]


def mk_skin(mat, opaque=False, uniform=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Base Color"].default_value = (0.65, 0.42, 0.34, 1)
    b.inputs["Roughness"].default_value = 0.45
    b.inputs["Subsurface Weight"].default_value = 0.0 if opaque else 1.0
    b.inputs["Subsurface Radius"].default_value = (1.0, 1.0, 1.0) if uniform else (1.0, 0.2, 0.1)
    b.inputs["Subsurface Scale"].default_value = 0.05
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-800, -300)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.location = (-550, -300)
    nz.inputs["Scale"].default_value = 250.0
    nz.inputs["Detail"].default_value = 3.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.location = (-250, -300)
    bp.inputs["Strength"].default_value = 0.15
    bp.inputs["Distance"].default_value = 0.005
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def mk_eye(mat, dry=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Roughness"].default_value = 0.2
    b.inputs["Coat Weight"].default_value = 0.0 if dry else 1.0
    b.inputs["Coat Roughness"].default_value = 0.02
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1000, 0)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-800, 0)
    mp.inputs["Rotation"].default_value = (0.0, 0.0, math.pi / 2)
    gr = nt.nodes.new("ShaderNodeTexGradient"); gr.location = (-600, 0)
    gr.gradient_type = "LINEAR"
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.location = (-350, 0)
    cr.color_ramp.interpolation = "CONSTANT"
    cr.color_ramp.elements[0].position = 0.0
    cr.color_ramp.elements[0].color = (0.85, 0.82, 0.78, 1)      # sclère
    cr.color_ramp.elements[1].position = 0.42
    cr.color_ramp.elements[1].color = (0.22, 0.10, 0.04, 1)      # iris
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
    nt.links.new(gr.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])


def mk_hair(mat, use_principled=False):
    nt = mat.node_tree
    out = nt.nodes["Material Output"]
    b = principled(mat)
    if use_principled:
        b.inputs["Base Color"].default_value = (0.12, 0.06, 0.03, 1)
        b.inputs["Roughness"].default_value = 0.3
        return
    nt.nodes.remove(b)
    h = nt.nodes.new("ShaderNodeBsdfHairPrincipled")
    h.location = (-100, 0)
    h.model = "CHIANG"
    h.parametrization = "COLOR"
    h.inputs["Color"].default_value = (0.12, 0.06, 0.03, 1)
    h.inputs["Roughness"].default_value = 0.3
    nt.links.new(h.outputs["BSDF"], out.inputs["Surface"])


def mk_cloth(mat, no_sheen=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Base Color"].default_value = (0.15, 0.25, 0.55, 1)
    b.inputs["Roughness"].default_value = 0.8
    b.inputs["Sheen Weight"].default_value = 0.0 if no_sheen else 0.5
    b.inputs["Sheen Roughness"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-800, -300)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.location = (-550, -300)
    wv.wave_type = "BANDS"
    wv.inputs["Scale"].default_value = 120.0
    wv.inputs["Distortion"].default_value = 0.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.location = (-250, -300)
    bp.inputs["Strength"].default_value = 0.4
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def build(kind):
    L.reset("SC_CHARACTER")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -7.2, 1.6), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.55))
    cam2 = L.camera("CAM_High", c, (3.0, -6.0, 3.4), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.45))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    mats = {n: bpy.data.materials.new("MAT_" + n) for n in NAMES}
    for i, n in enumerate(NAMES):
        ob = L.sphere("SPH_" + n, L.collection("OBJETS"), None, radius=0.5, location=((i - 1.5) * 1.15, 0, 0.5), segments=64, ring_count=32)
        ob.data.materials.append(mats[n])
        if n == "Eye":
            ob.rotation_euler = (0, 0, math.radians(4.6))          # l'œil regarde vers la caméra de face
    if kind != "starter":
        mk_skin(mats["Skin"], opaque=(kind == "skin_opaque"), uniform=(kind == "skin_uniform_radius"))
        mk_eye(mats["Eye"], dry=(kind == "eye_dry"))
        mk_hair(mats["Hair"], use_principled=(kind == "hair_principled"))
        mk_cloth(mats["Cloth"], no_sheen=(kind == "cloth_no_sheen"))
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 96
        sc.cycles.use_denoising = True
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_10_character_starter.blend"))
    for k in ("skin_opaque", "skin_uniform_radius", "eye_dry", "hair_principled", "cloth_no_sheen"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_10_character_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_10_character_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_10_character_reference.png"))


if __name__ == "__main__":
    L.run(main)
