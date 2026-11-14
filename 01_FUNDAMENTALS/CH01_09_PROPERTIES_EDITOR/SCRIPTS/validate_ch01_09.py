"""
validate_ch01_09.py — Correcteur de la chasse aux propriétés (CH01.09).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch01_09.py --python-exit-code 1 -- --exercise hunt
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH01.09 — La chasse aux propriétés")
    sc = bpy.context.scene
    rd = sc.render
    r.check(rd.engine == "BLENDER_EEVEE" and sc.eevee.taa_render_samples == 32, "1. EEVEE, 32 échantillons",
            "Render > Render Engine ; Sampling > Render > Samples.", 1)
    r.check((rd.resolution_x, rd.resolution_y, rd.resolution_percentage) == (1280, 720, 100),
            f"2. Résolution {rd.resolution_x}×{rd.resolution_y} {rd.resolution_percentage} %", "Output > Format.", 1)
    r.check(rd.fps == 25 and rd.fps_base == 1.0 and (sc.frame_start, sc.frame_end) == (1, 120),
            "2. 25 fps, images 1 à 120", "Output > Format > Frame Rate ; Frame Range.", 1)
    r.check(sc.camera is not None and sc.camera.name == "CAM_Shot", "3. Caméra active = CAM_Shot", "Scene > Camera.", 1)
    r.check(sc.unit_settings.length_unit == "CENTIMETERS", "3. Unités de longueur en centimètres", "Scene > Units > Length.", 1)
    bg = next((n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND"), None) if sc.world else None
    c = bg.inputs["Color"].default_value if bg else (1, 1, 1, 1)
    r.check(bg and c[2] > c[0] and c[2] > c[1] and max(c[:3]) < 0.2, "4. Monde bleu nuit", "World > Surface > Color.", 1)
    g = L.obj("GEO_Guide")
    r.check(g and g.display_type == "WIRE" and g.hide_render, "5. GEO_Guide en fil de fer et non rendu",
            "Object > Viewport Display > Display As ; Object > Visibility > Renders.", 1)
    h = L.obj("GEO_Hero")
    r.check(h and h.show_name, "6. Nom de GEO_Hero affiché", "Object > Viewport Display > Name.", 1)
    cam = L.obj("CAM_Shot")
    r.check(cam and abs(cam.data.lens - 35) < 0.01, "7. Focale 35 mm", "Object Data (caméra) > Lens > Focal Length.", 1)
    k = L.obj("LGT_Key")
    r.check(k and abs(k.data.energy - 250) < 0.5 and k.data.color[0] > k.data.color[1] > k.data.color[2],
            "8. LGT_Key : 250 W, couleur chaude", "Object Data (lumière) > Power, Color.", 1)
    m = bpy.data.materials.get("MAT_Hero")
    bsdf = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m else None
    bc = bsdf.inputs["Base Color"].default_value if bsdf else (1, 1, 1, 1)
    r.check(bsdf and bc[0] >= 0.6 and bc[1] <= 0.2 and bc[2] <= 0.2, "9. MAT_Hero rouge", "Material > Surface > Base Color.", 1)
    r.check(sc.get("shot") == "sq010_sh0010", "10. Propriété personnalisée scene['shot']",
            "Scene > Custom Properties > New, type String.", 1)
    gold = bpy.data.materials.get("MAT_Library_Gold")
    used = g is not None and any(ms.material == gold for ms in g.material_slots) if gold else False
    r.check(gold is not None and gold.use_fake_user and not used, "11. MAT_Library_Gold protégé (Fake User) et retiré de GEO_Guide",
            "Outliner (Blender File) > Materials > bouclier, ou Material > bouclier dans l'en-tête du matériau.", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
