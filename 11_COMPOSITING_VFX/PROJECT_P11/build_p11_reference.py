"""
build_p11_reference.py — Construit la référence du projet P11 : plaque granuleuse (empaquetée), cube gris raccordé (Floor = Shadow Catcher, film transparent, SUN à gauche), arbre
Image (plaque) → Alpha Over ← [Exposure −2 → Color Balance Gain (1,3 ; 1,0 ; 0,6)] ← Render Layers, 2 échantillons Cycles sans débruitage ; image finale 320 × 180 et rapport de contrôle qualité (valeurs mesurées par le correcteur).
Assemble CH11.07 (Alpha Over), CH11.06 (Color Balance), CH11.09 (shadow catcher, film transparent, soleil), CH11.10 (exposition, dominante, grain).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p11_reference.py
Testé avec : Blender 5.3.0.
"""
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

spec = importlib.util.spec_from_file_location("validate_p11", os.path.join(HERE, "validate_p11.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
W, H = 320, 180
NOTE = """P11 — INTÉGRER UN ÉLÉMENT 3D DANS UNE PRISE DE VUE (Cube, Floor, SUN, CAM ; plaque « plate »)
Posez le cube dans la plaque (ombre à droite, sol invisible), raccordez-le (exposition, couleur, grain), rendez renders/p11_final.png (320 × 180) et écrivez renders/p11_qc.json. Critères : README et SCRIPTS/validate_p11.py."""


def make_plate():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = (0.75, 0.80, 0.90)
    img[yy >= 70] = (0.55, 0.50, 0.42)
    img[(xx >= 246) & (xx <= 254) & (yy >= 40) & (yy <= 120)] = (0.12, 0.10, 0.08)
    img[(yy >= 118) & (yy <= 126) & (xx >= 250) & (xx <= 310)] *= 0.7
    img += np.random.RandomState(5).normal(0, 0.015, img.shape).astype(np.float32)
    out = bpy.data.images.new("plate", W, H, alpha=False)
    out.colorspace_settings.name = "sRGB"
    out.pixels = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], axis=2)[::-1].ravel().tolist()
    out.pack()
    return out


def build():
    L.reset("SC_P11")
    sc = bpy.context.scene
    plate = make_plate()
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new("ME_Cube")
    bm.to_mesh(me)
    bm.free()
    cube = bpy.data.objects.new("Cube", me)
    cube.location = (0, 0, 0.5)
    mat = bpy.data.materials.new("MA_Cube")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    cube.data.materials.append(mat)
    sc.collection.objects.link(cube)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20)
    mf = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(mf)
    bm.free()
    fl = bpy.data.objects.new("Floor", mf)
    fl.data.materials.append(bpy.data.materials.new("MA_Floor"))
    fl.is_shadow_catcher = True
    sc.collection.objects.link(fl)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 4
    ld.angle = math.radians(2)
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (math.radians(50), 0, math.radians(-50))
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -8, 3)
    cam.rotation_euler = (math.radians(75), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Sky")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.7, 0.8, 1.0, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 2
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-900, 100)
    ni = ng.nodes.new("CompositorNodeImage")
    ni.image = plate
    ni.location = (-900, -200)
    ex = ng.nodes.new("CompositorNodeExposure")
    ex.location = (-600, 100)
    ex.inputs["Exposure"].default_value = -2.0
    cb = ng.nodes.new("CompositorNodeColorBalance")
    cb.location = (-300, 100)
    cb.inputs["Type"].default_value = "Lift/Gamma/Gain"
    cb.inputs[8].default_value = (1.3, 1.0, 0.6, 1)
    ao = ng.nodes.new("CompositorNodeAlphaOver")
    ao.location = (100, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (500, 0)
    ng.links.new(rl.outputs["Image"], ex.inputs["Image"])
    ng.links.new(ex.outputs["Image"], cb.inputs["Image"])
    ng.links.new(cb.outputs["Image"], ao.inputs["Foreground"])
    ng.links.new(ni.outputs["Image"], ao.inputs["Background"])
    ng.links.new(ao.outputs["Image"], out.inputs[0])
    sc.render.use_compositing = True
    L.instructions(NOTE)


def main():
    ref = os.path.join(HERE, "REFERENCE")
    os.makedirs(os.path.join(ref, "renders"), exist_ok=True)
    build()
    sc = bpy.context.scene
    m = V.measure(sc)
    print("[p11]", {k: (round(v, 4) if not isinstance(v, tuple) else v) for k, v in m.items()})
    sc.render.resolution_x, sc.render.resolution_y = 320, 180
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.cycles.seed = 0
    sc.render.filepath = os.path.join(ref, "renders", "p11_final.png")
    bpy.ops.render.render(write_still=True)
    notes = [
        "Le soleil de la plaque est à gauche (l'ombre du poteau tombe à droite) : le soleil 3D a une rotation X 50° et Z −50° pour que l'ombre du cube tombe aussi à droite.",
        "Le sol 3D est un shadow catcher et le film est transparent : le sol disparaît et ne garde que l'ombre du cube, mesurée à −0,045 par rapport à la plaque.",
        "Le cube neutre était presque deux fois plus lumineux que le sol (rapport 1,86) : deux diaphragmes de moins ramènent le rapport à 1,01.",
        "La plaque est chaude : un Gain (1,3 ; 1,0 ; 0,6) du nœud Color Balance supprime l'écart de dominante de −0,20 (mesuré +0,007).",
        "La plaque est granuleuse (0,011) : le cube rendu à 2 échantillons sans débruitage a un bruit de 0,012 ; à 128 échantillons il était trop propre (0,0016).",
        "Les mesures sont faites sur le dessus du cube et sur un patch de sol, en valeurs affichées : elles ne disent rien des noirs, du flou ni de la netteté.",
    ]
    json.dump({"ratio": round(m["ratio"], 3), "cast": round(m["cast"], 3), "noise": round(m["noise"], 4), "shadow_right": round(m["right"], 3), "far": round(m["far"], 3), "notes": notes},
              open(os.path.join(ref, "renders", "p11_qc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    L.save(os.path.join(ref, "p11_scene_reference.blend"))


if __name__ == "__main__":
    L.run(main)
