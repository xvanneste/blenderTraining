"""
build_ch04_09_files.py — « Matériaux types » (CH04.09).

Une étagère de cinq sphères et cinq matériaux de bibliothèque, tous marqués comme ASSETS (Asset Browser) :
  MAT_Wood    : Texture Coordinate [Object] -> Mapping (étiré) -> Wave Texture [Fac] -> Color Ramp -> Base Color ; Roughness 0,45
  MAT_Stone   : Voronoi [Distance] -> Color Ramp -> Base Color ; Noise -> Bump -> Normal ; Roughness 0,85
  MAT_Plastic : Base Color rouge saturé, Roughness 0,3, Coat Weight 0,5
  MAT_Glass   : Transmission 1, Roughness 0,02, IOR 1,5
  MAT_Steel   : acier brossé : Metallic 1, Anisotropic 0,6, Roughness pilotée par un Noise étiré (Mapping)
  STARTER_FILES/ch04_09_materials_starter.blend : cinq matériaux Principled par défaut, non marqués asset.
  COMPLETED_EXAMPLES/ch04_09_materials_solution.blend (+ _reference.png)
  COUNTER_EXAMPLES/ : wood_flat, stone_no_bump, steel_isotropic, not_marked, plastic_matte
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_09_files.py
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
NAMES = ("Wood", "Stone", "Plastic", "Glass", "Steel")
NOTE = """CH04.09 — MATÉRIAUX TYPES (cinq sphères SPH_Wood / Stone / Plastic / Glass / Steel, matériaux MAT_<Nom>)
Construisez une mini-bibliothèque :
1. Bois : Wave Texture (bandes) pilotant une Color Ramp brune vers Base Color ; Metallic 0 ; Roughness 0,3–0,7.
2. Pierre : Voronoi ou Noise pilotant Base Color ; un Bump alimenté par une texture relié à Normal ; Roughness ≥ 0,6.
3. Plastique : Metallic 0 ; Base Color saturé (écart max-min ≥ 0,3) ; Roughness 0,15–0,5 ; Coat Weight ≥ 0,3.
4. Verre : Transmission Weight ≥ 0,9 ; Roughness ≤ 0,1 ; IOR 1,4–1,6.
5. Acier brossé : Metallic ≥ 0,9 ; Base Color claire ; Anisotropic ≥ 0,4 ; Roughness pilotée par un Noise (rayures).
6. Marquez CHAQUE matériau comme asset (clic droit > Mark as Asset) avec une description non vide.
Vérification : SCRIPTS/validate_ch04_09.py -- --exercise materials
"""


def inp(n, k):
    return n.inputs[k]


def principled(mat):
    return mat.node_tree.nodes["Principled BSDF"]


def ramp(nt, loc, stops):
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.location = loc
    r.color_ramp.elements[0].position = stops[0][0]
    r.color_ramp.elements[0].color = stops[0][1]
    r.color_ramp.elements[1].position = stops[1][0]
    r.color_ramp.elements[1].color = stops[1][1]
    return r


def mk_wood(mat, flat=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Roughness"].default_value = 0.45
    b.inputs["Base Color"].default_value = (0.30, 0.17, 0.08, 1)
    if flat:
        return
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1000, 0)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-800, 0)
    mp.inputs["Scale"].default_value = (1.0, 1.0, 0.15)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.location = (-600, 0)
    wv.wave_type = "BANDS"
    wv.inputs["Scale"].default_value = 6.0
    wv.inputs["Distortion"].default_value = 4.0
    wv.inputs["Detail"].default_value = 3.0
    cr = ramp(nt, (-350, 0), ((0.2, (0.20, 0.09, 0.04, 1)), (0.8, (0.50, 0.30, 0.15, 1))))
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])


def mk_stone(mat, no_bump=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Roughness"].default_value = 0.85
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1000, 0)
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.location = (-700, 100)
    vr.inputs["Scale"].default_value = 4.0
    cr = ramp(nt, (-400, 100), ((0.1, (0.18, 0.17, 0.16, 1)), (0.7, (0.55, 0.53, 0.50, 1))))
    nt.links.new(tc.outputs["Object"], vr.inputs["Vector"])
    nt.links.new(vr.outputs["Distance"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    if not no_bump:
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.location = (-700, -250)
        nz.inputs["Scale"].default_value = 18.0
        nz.inputs["Detail"].default_value = 8.0
        bp = nt.nodes.new("ShaderNodeBump"); bp.location = (-300, -250)
        bp.inputs["Strength"].default_value = 0.6
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def mk_plastic(mat, matte=False):
    b = principled(mat)
    b.inputs["Base Color"].default_value = (0.80, 0.05, 0.04, 1)
    b.inputs["Roughness"].default_value = 0.9 if matte else 0.3
    b.inputs["Coat Weight"].default_value = 0.5


def mk_glass(mat):
    b = principled(mat)
    b.inputs["Base Color"].default_value = (1, 1, 1, 1)
    b.inputs["Roughness"].default_value = 0.02
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.5


def mk_steel(mat, isotropic=False):
    nt = mat.node_tree
    b = principled(mat)
    b.inputs["Base Color"].default_value = (0.75, 0.76, 0.78, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Anisotropic"].default_value = 0.0 if isotropic else 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-900, -300)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-700, -300)
    mp.inputs["Scale"].default_value = (1.0, 60.0, 1.0)             # rayures étirées
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.location = (-500, -300)
    nz.inputs["Scale"].default_value = 8.0
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.location = (-250, -300)
    mr.inputs["To Min"].default_value = 0.2
    mr.inputs["To Max"].default_value = 0.45
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])


DESC = {"Wood": "Bois à veines (Wave + Color Ramp)", "Stone": "Pierre grise (Voronoi + bump)", "Plastic": "Plastique rouge brillant avec vernis",
        "Glass": "Verre clair (transmission, IOR 1,5)", "Steel": "Acier brossé anisotrope"}


def mark(mat, name):
    mat.asset_mark()
    mat.asset_data.description = DESC[name]
    mat.asset_data.tags.new("BCMA")


def build(kind):
    L.reset("SC_MATERIALS")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -8.6, 2.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.55))
    cam2 = L.camera("CAM_High", c, (3.5, -7.0, 4.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.45))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    mats = {n: bpy.data.materials.new("MAT_" + n) for n in NAMES}
    for i, n in enumerate(NAMES):
        ob = L.sphere("SPH_" + n, L.collection("OBJETS"), None, radius=0.5, location=((i - 2) * 1.15, 0, 0.5), segments=64, ring_count=32)
        ob.data.materials.append(mats[n])
    if kind != "starter":
        mk_wood(mats["Wood"], flat=(kind == "wood_flat"))
        mk_stone(mats["Stone"], no_bump=(kind == "stone_no_bump"))
        mk_plastic(mats["Plastic"], matte=(kind == "plastic_matte"))
        mk_glass(mats["Glass"])
        mk_steel(mats["Steel"], isotropic=(kind == "steel_isotropic"))
        for n in NAMES:
            if kind == "not_marked" and n == "Stone":
                continue
            mark(mats[n], n)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_09_materials_starter.blend"))
    for k in ("wood_flat", "stone_no_bump", "steel_isotropic", "not_marked", "plastic_matte"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_09_materials_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_09_materials_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_09_materials_reference.png"))


if __name__ == "__main__":
    L.run(main)
