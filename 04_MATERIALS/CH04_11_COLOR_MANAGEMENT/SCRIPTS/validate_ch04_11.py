"""
validate_ch04_11.py — Correcteur « Gestion des couleurs » (CH04.11).
Usage : … --python-exit-code 1 --python validate_ch04_11.py -- --exercise color [--render] [--debug]
PLATE_Test / MAT_Plate / images T_Albedo, T_Rough, T_Normal :
  - T_Albedo (couleur) en sRGB ; T_Rough et T_Normal (données) en Non-Color ;
  - les trois images sont réellement branchées (Base Color, Roughness, Normal Map -> Normal) ;
  - View Transform parmi AgX, Filmic, ACES 1.3, ACES 2.0, Khronos PBR Neutral (pas Standard, Raw, False Color, Filmic Log) ;
  - Look : None ou « AgX - … » ; Exposure ∈ [−1,5 ; +1,5] ; Gamma = 1 ; Display Device sRGB ; espace du séquenceur sRGB ;
  - sortie maître : OpenEXR.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

TONEMAPPED = ("AgX", "Filmic", "ACES 1.3", "ACES 2.0", "Khronos PBR Neutral")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.11 — Gestion des couleurs")
    ob = bpy.data.objects.get("PLATE_Test")
    mat = ob.active_material if ob and ob.data.materials else None
    imgs = {n: bpy.data.images.get(n) for n in ("T_Albedo", "T_Rough", "T_Normal")}
    if not r.check(mat is not None and all(imgs.values()), "PLATE_Test, MAT_Plate et les trois images présentes", "Partez du fichier de départ.", 2):
        return r.finish()
    nt = mat.node_tree
    b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)

    def wired(img, sock, via_normalmap=False):
        for l in nt.links:
            if l.from_node.type == "TEX_IMAGE" and l.from_node.image == img:
                if not via_normalmap and l.to_node == b and l.to_socket.name == sock:
                    return True
                if via_normalmap and l.to_node.type == "NORMAL_MAP" and any(k.from_node.type == "NORMAL_MAP" and k.to_node == b and k.to_socket.name == "Normal" for k in nt.links):
                    return True
        return False
    r.check(b is not None and wired(imgs["T_Albedo"], "Base Color") and wired(imgs["T_Rough"], "Roughness") and wired(imgs["T_Normal"], "Normal", True), "Images branchées : Albedo → Base Color, Rough → Roughness, Normal → Normal Map → Normal", "Ne débranchez pas les images.", 2)
    cs = {n: im.colorspace_settings.name for n, im in imgs.items()}
    r.check(cs["T_Albedo"] == "sRGB", f"T_Albedo : {cs['T_Albedo']} (sRGB exigé : c'est une couleur)", "Image Texture : Color Space sRGB pour une couleur.", 3)
    r.check(cs["T_Rough"] == "Non-Color", f"T_Rough : {cs['T_Rough']} (Non-Color exigé : c'est une donnée)", "Roughness est un nombre : Non-Color.", 3)
    r.check(cs["T_Normal"] == "Non-Color", f"T_Normal : {cs['T_Normal']} (Non-Color exigé)", "Une normal map est un vecteur : Non-Color.", 3)
    sc = bpy.context.scene
    vs = sc.view_settings
    r.check(vs.view_transform in TONEMAPPED, f"View Transform : {vs.view_transform} (parmi {', '.join(TONEMAPPED)})", "Standard clippe les hautes lumières ; Raw est une donnée brute ; choisissez AgX.", 3)
    r.check(vs.look == "None" or vs.look.startswith("AgX - "), f"Look : {vs.look}", "None ou un look AgX.", 1)
    r.check(-1.5 <= vs.exposure <= 1.5, f"Exposure {vs.exposure:+.2f} (−1,5 à +1,5)", "Réglez la lumière dans la scène, pas par une exposition extrême.", 2)
    r.check(abs(vs.gamma - 1.0) < 1e-6, f"Gamma {vs.gamma:.2f} (1 exigé)", "Gamma ≠ 1 double la correction de la vue : image délavée.", 2)
    r.check(sc.display_settings.display_device == "sRGB", f"Display Device : {sc.display_settings.display_device} (sRGB)", "", 1)
    r.check(sc.sequencer_colorspace_settings.name == "sRGB", f"Espace du séquenceur : {sc.sequencer_colorspace_settings.name}", "", 1)
    ff = sc.render.image_settings.file_format
    r.check(ff == "OPEN_EXR", f"Sortie maître : {ff} (OPEN_EXR exigé : linéaire scène, flottant)", "PNG 8 bits perd la dynamique : réservé à la livraison finale.", 2)
    if debug:
        print("[DEBUG]", cs, vs.view_transform, vs.look, vs.exposure, vs.gamma, ff)
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
