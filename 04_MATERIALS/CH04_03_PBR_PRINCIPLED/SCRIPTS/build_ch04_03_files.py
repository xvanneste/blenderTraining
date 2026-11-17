"""
build_ch04_03_files.py — « PBR et Principled BSDF » (CH04.03).

Quatre sphères : SPH_Metal (or poli), SPH_Rubber (caoutchouc noir), SPH_Glass (verre), SPH_Wax (cire translucide : subsurface).
  STARTER_FILES/ch04_03_pbr_starter.blend : quatre matériaux Principled BSDF aux valeurs PAR DÉFAUT (gris 0,8, rugosité 0,5).
  COMPLETED_EXAMPLES/ch04_03_pbr_solution.blend (+ _reference.png : deux vues)
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : metal_dark, mixed_metal, glass_opaque, white_wax, shared_material
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_03_files.py
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
NOTE = """CH04.03 — PBR ET PRINCIPLED BSDF (quatre sphères, quatre matériaux MAT_Metal / MAT_Rubber / MAT_Glass / MAT_Wax)
Réglez chaque Principled BSDF pour qu'il soit physiquement plausible :
1. MAT_Metal  : Metallic 1 ; Base Color = la couleur de la réflexion (or ≈ 1,0 / 0,77 / 0,34) ; Roughness 0,1–0,5.
2. MAT_Rubber : Metallic 0 ; Base Color sombre (albedo 0,02–0,1) ; Roughness ≥ 0,6.
3. MAT_Glass  : Metallic 0 ; Transmission Weight 1 ; Roughness ≤ 0,1 ; IOR 1,5.
4. MAT_Wax    : Metallic 0 ; Base Color clair (albedo 0,5–0,85) ; Subsurface Weight ≥ 0,2 ; Subsurface Radius R > V > B.
Règle d'or : un diélectrique n'est jamais « blanc pur » ni « noir pur » (albedo entre 0,02 et 0,9) ; Metallic vaut 0 ou 1, presque jamais entre les deux.
Vérification : SCRIPTS/validate_ch04_03.py -- --exercise pbr
"""
SPEC = {   # nom : (couleur, métal, rugosité, transmission, ior, sss poids, sss rayon, coat)
    "Metal":  ((1.00, 0.77, 0.34), 1.0, 0.25, 0.0, 1.45, 0.0, (1.0, 0.2, 0.1), 0.0),
    "Rubber": ((0.05, 0.05, 0.05), 0.0, 0.75, 0.0, 1.52, 0.0, (1.0, 0.2, 0.1), 0.0),
    "Glass":  ((1.00, 1.00, 1.00), 0.0, 0.02, 1.0, 1.50, 0.0, (1.0, 0.2, 0.1), 0.0),
    "Wax":    ((0.85, 0.70, 0.48), 0.0, 0.45, 0.0, 1.45, 0.6, (1.0, 0.5, 0.25), 0.2),
}


def set_mat(mat, color, metal, rough, trans, ior, sss, radius, coat):
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = trans
    b.inputs["IOR"].default_value = ior
    b.inputs["Subsurface Weight"].default_value = sss
    b.inputs["Subsurface Radius"].default_value = radius
    b.inputs["Subsurface Scale"].default_value = 0.05
    b.inputs["Coat Weight"].default_value = coat


def build(kind):
    L.reset("SC_PBR")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)                       # environnement clair : sans lui, un métal n'a rien à refléter
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -6.9, 1.9), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.55))
    cam2 = L.camera("CAM_High", c, (3.0, -5.6, 3.6), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.45))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    mats = {}
    for name in SPEC:
        m = bpy.data.materials.new("MAT_" + name)           # un Principled BSDF par défaut (gris 0,8) : ne pas toucher à use_nodes (obsolète)
        mats[name] = m
    for i, name in enumerate(SPEC):
        x = (i - 1.5) * 1.15
        ob = L.sphere("SPH_" + name, L.collection("OBJETS"), None, radius=0.5, location=(x, 0, 0.5), segments=64, ring_count=32)
        ob.data.materials.append(mats[name])
    if kind != "starter":
        for name, vals in SPEC.items():
            set_mat(mats[name], *vals)
    if kind == "metal_dark":
        set_mat(mats["Metal"], (0.05, 0.05, 0.05), 1.0, 0.25, 0.0, 1.45, 0.0, (1, 0.2, 0.1), 0.0)
    elif kind == "mixed_metal":
        set_mat(mats["Rubber"], (0.05, 0.05, 0.05), 0.5, 0.75, 0.0, 1.52, 0.0, (1, 0.2, 0.1), 0.0)
    elif kind == "glass_opaque":
        set_mat(mats["Glass"], (1, 1, 1), 0.0, 0.02, 0.0, 1.5, 0.0, (1, 0.2, 0.1), 0.0)
    elif kind == "white_wax":
        set_mat(mats["Wax"], (1.0, 1.0, 1.0), 0.0, 0.45, 0.0, 1.45, 0.6, (1.0, 0.5, 0.25), 0.2)
    elif kind == "shared_material":
        for o in bpy.data.objects:
            if o.name.startswith("SPH_"):
                o.data.materials.clear()
                o.data.materials.append(mats["Metal"])
    L.instructions(NOTE)
    return sc


def views(sc, out):
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
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_03_pbr_starter.blend"))
    for k in ("metal_dark", "mixed_metal", "glass_opaque", "white_wax", "shared_material"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch04_03_pbr_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out, "ch04_03_pbr_solution.blend"))
    views(sc, os.path.join(out, "ch04_03_pbr_reference.png"))


if __name__ == "__main__":
    L.run(main)
