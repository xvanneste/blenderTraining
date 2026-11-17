"""
build_ch04_11_files.py — « Gestion des couleurs » (CH04.11).

Une planche d'essai PLATE_Test : matériau MAT_Plate avec trois images 64 x 64 — T_Albedo (couleurs), T_Rough (gris, donnée), T_Normal (normales, donnée) — branchées
sur Base Color, Roughness et Normal (via Normal Map) ; un panneau lumineux EMIT_Panel (Emission 4) pour voir le comportement des hautes lumières.
Réglages à poser :
  - T_Albedo : sRGB ; T_Rough et T_Normal : Non-Color ;
  - Scene > Color Management : View Transform AgX (ou un autre transform « tone-mapped » : Filmic, ACES 1.3/2.0, Khronos PBR Neutral), Look None ou AgX-*,
    Exposure ∈ [−1,5 ; +1,5], Gamma 1, Display Device sRGB ;
  - sortie maîtresse : OpenEXR (linéaire scène), pas PNG 8 bits.
  STARTER_FILES/ch04_11_color_starter.blend : tout par défaut « faux » (images sRGB, View Transform Standard, PNG).
  COMPLETED_EXAMPLES/ch04_11_color_solution.blend (+ _reference.png : deux vues, AgX)
  COUNTER_EXAMPLES/ : albedo_noncolor, rough_srgb, standard_view, raw_view, big_exposure, gamma2, png_master
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_11_files.py
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
NOTE = """CH04.11 — GESTION DES COULEURS (PLATE_Test, images T_Albedo / T_Rough / T_Normal, panneau EMIT_Panel)
1. Espace colorimétrique de chaque image : T_Albedo = sRGB (c'est une COULEUR) ; T_Rough et T_Normal = Non-Color (ce sont des DONNÉES).
2. Render Properties > Color Management : View Transform AgX (ou Filmic, ACES 1.3, ACES 2.0, Khronos PBR Neutral) ; Look None ou AgX - … ;
   Exposure entre -1,5 et +1,5 ; Gamma 1 ; Display Device sRGB.
3. Output Properties : format de sortie maître OpenEXR (données linéaires de la scène), pas PNG 8 bits.
Vérification : SCRIPTS/validate_ch04_11.py -- --exercise color
"""


def make_images(albedo_cs, rough_cs, normal_cs):
    imgs = {}
    for name, cs in (("T_Albedo", albedo_cs), ("T_Rough", rough_cs), ("T_Normal", normal_cs)):
        im = bpy.data.images.new(name, 64, 64)
        im.colorspace_settings.name = cs                     # AVANT d'écrire les pixels (voir CH04.07)
        px = np.zeros((64, 64, 4), np.float32)
        px[..., 3] = 1.0
        ys, xs = np.mgrid[0:64, 0:64]
        if name == "T_Albedo":
            chk = ((xs // 16 + ys // 16) % 2).astype(bool)
            px[..., :3] = np.where(chk[..., None], (0.80, 0.25, 0.15), (0.20, 0.45, 0.75))
        elif name == "T_Rough":
            px[..., :3] = (xs / 63.0)[..., None] * 0.7 + 0.15
        else:
            px[..., :3] = (0.5, 0.5, 1.0)
        im.pixels = px.ravel()
        im.pack()
        imgs[name] = im
    return imgs


def build(kind):
    L.reset("SC_COLOR")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.6)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -4.2, 1.3), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.8))
    cam2 = L.camera("CAM_Side", c, (2.6, -3.6, 1.9), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.8))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    wrong = kind == "starter"
    imgs = make_images("Non-Color" if kind == "albedo_noncolor" else "sRGB",
                       "sRGB" if (wrong or kind == "rough_srgb") else "Non-Color",
                       "sRGB" if wrong else "Non-Color")
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    pl = bpy.context.active_object
    pl.name = "PLATE_Test"
    pl.data.transform(__import__("mathutils").Matrix.Diagonal((1.6, 1.0, 1.0, 1.0)))
    pl.rotation_euler = (1.5707963, 0, 0)
    pl.location = (0, 0, 0.8)
    mat = bpy.data.materials.new("MAT_Plate")
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    t1 = nt.nodes.new("ShaderNodeTexImage"); t1.image = imgs["T_Albedo"]; t1.location = (-700, 200)
    t2 = nt.nodes.new("ShaderNodeTexImage"); t2.image = imgs["T_Rough"]; t2.location = (-700, -100)
    t3 = nt.nodes.new("ShaderNodeTexImage"); t3.image = imgs["T_Normal"]; t3.location = (-700, -400)
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.location = (-400, -400)
    for t in (t1, t2, t3):
        t.interpolation = "Closest"
    nt.links.new(t1.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(t2.outputs["Color"], b.inputs["Roughness"])
    nt.links.new(t3.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    pl.data.materials.append(mat)
    # panneau lumineux (hautes lumières)
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(1.15, -0.05, 1.35))
    em = bpy.context.active_object
    em.name = "EMIT_Panel"
    em.rotation_euler = (1.5707963, 0, 0)
    em_m = bpy.data.materials.new("MAT_Emit")
    e = em_m.node_tree.nodes["Principled BSDF"]
    e.inputs["Emission Color"].default_value = (1.0, 0.85, 0.6, 1.0)
    e.inputs["Emission Strength"].default_value = 4.0
    em.data.materials.append(em_m)
    vs = sc.view_settings
    vs.view_transform = "Standard" if kind in ("starter", "standard_view") else ("Raw" if kind == "raw_view" else "AgX")
    vs.look = "None"
    vs.exposure = 4.0 if kind == "big_exposure" else 0.0
    vs.gamma = 2.2 if kind == "gamma2" else 1.0
    sc.display_settings.display_device = "sRGB"
    im_s = sc.render.image_settings
    if kind in ("starter", "png_master"):
        im_s.file_format = "PNG"
        im_s.color_depth = "8"
    else:
        im_s.file_format = "OPEN_EXR"
        im_s.color_depth = "16"
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    sc.render.image_settings.file_format = "PNG"                   # aperçu PNG seulement (le réglage EXR de la scène n'est pas modifié dans le .blend)
    tiles = []
    for cam in ("CAM_Front", "CAM_Side"):
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_11_color_starter.blend"))
    for k in ("albedo_noncolor", "rough_srgb", "standard_view", "raw_view", "big_exposure", "gamma2", "png_master"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_11_color_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_11_color_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_11_color_reference.png"))


if __name__ == "__main__":
    L.run(main)
