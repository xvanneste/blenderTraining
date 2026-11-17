"""
build_ch11_05_files.py — « Glare et effets » (CH11.05 : halo de lumière (Glare), distorsion d'objectif (Lens Distortion)).

Scène (Cycles CPU, 160 × 90, 4 échantillons, sans débruitage, monde noir) : Lamp (disque émissif de 0,4 m de rayon, force 30, à (0, 6, 0), tourné vers la caméra), Line (barre émissive horizontale de 14 m × 3 cm à (0, 6, 1,2), force 1), CAM à l'origine (35 mm).
  Au rendu la lampe est un disque net (rayon ≈ 11 pixels), la barre est droite à la rangée 13.
  Consigne (compositeur) : Render Layers → Glare → Lens Distortion → Group Output :
    1. Glare : un halo doux autour de la lampe : luminance moyenne d'un anneau (rayon 20–30 pixels du centre de la lampe, rangées ≥ 25) de 0,002 à 0,1 ; champ lointain (rayon 40–60, rangées ≥ 25) ≤ 0,1 ; cœur de la lampe (rayon < 5) ≥ 0,95 ;
       (mesuré, anneau 20–30 : sans glare 0,0003 ; Fog Glow 0,0066 (0,0037 sans distorsion) ; Bloom 0,88 ; Ghosts 1,0 ; le Fog Glow par défaut est subtil).
    2. Lens Distortion : prise Distortion entre 0,15 et 0,4 : la barre se courbe : (moyenne des rangées de la barre aux colonnes 10 et 150) − (rangée au centre, colonne 80) de +4 à +12 pixels (mesuré : 0,3 → +7 ; 0,1 → +2 ; sans : 0 ; 0,6 → la barre sort de l'image).
  Départ : Render Layers (Image) → Group Output. Solution : Glare « Fog Glow » (réglages par défaut) → Lens Distortion (Distortion 0,3) → Group Output.
  STARTER_FILES/ch11_05_glare_starter.blend ; COMPLETED_EXAMPLES/ch11_05_glare_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : no_glare, bloom_strong (Bloom : anneau 0,88), ghosts (Ghosts : champ lointain 0,72), no_distortion, over_distortion (0,6)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_05_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.05 — GLARE ET EFFETS (Lamp, Line, CAM)
Le rendu montre une lampe nette et une barre droite. Dans le compositeur : Render Layers → Glare → Lens Distortion → Group Output.
1. Glare : un halo doux (type Fog Glow) : anneau (rayon 20–30 pixels) autour de la lampe entre 0,002 et 0,1, champ lointain ≤ 0,1, cœur ≥ 0,95. Bloom, Streaks et Ghosts sont trop forts ici.
2. Lens Distortion : prise Distortion entre 0,15 et 0,4 : la barre se courbe de 4 à 12 pixels (0,3 → 7 pixels). Pas de nœud orphelin ; compositing activé.
La création de grain de pellicule n'est pas évaluée ici (pas de nœud de grain dédié dans la liste 5.3 des nœuds du compositeur).
Vérification : SCRIPTS/validate_ch11_05.py -- --exercise glare
"""


def emissive(name, mesh_op, strength):
    mesh_op()
    o = bpy.context.object
    o.name = name
    m = bpy.data.materials.new("MA_" + name)
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Strength"].default_value = strength
    oo = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], oo.inputs[0])
    o.data.materials.append(m)
    return o


def build(kind):
    L.reset("SC_GLARE")
    sc = bpy.context.scene
    emissive("Lamp", lambda: bpy.ops.mesh.primitive_circle_add(vertices=48, radius=0.4, fill_type="NGON", location=(0, 6, 0), rotation=(math.radians(90), 0, 0)), 30)
    ln = emissive("Line", lambda: bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 6, 1.2)), 1)
    ln.scale = (14, 0.01, 0.03)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 4
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-800, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (600, 0)
    prev = rl.outputs["Image"]
    if kind != "starter":
        gtype = {"bloom_strong": "Bloom", "ghosts": "Ghosts"}.get(kind, "Fog Glow")
        if kind != "no_glare":
            g = ng.nodes.new("CompositorNodeGlare")
            g.location = (-400, 0)
            g.inputs["Type"].default_value = gtype
            ng.links.new(prev, g.inputs["Image"])
            prev = g.outputs["Image"]
        if kind != "no_distortion":
            d = ng.nodes.new("CompositorNodeLensdist")
            d.location = (0, 0)
            d.inputs["Distortion"].default_value = 0.6 if kind == "over_distortion" else 0.3
            ng.links.new(prev, d.inputs["Image"])
            prev = d.outputs["Image"]
    ng.links.new(prev, out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1105.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(px=None):
    px = render() if px is None else px
    y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    yy, xx = np.mgrid[0:90, 0:160]
    r = np.hypot(xx - 80, yy - 45)
    low = yy >= 25
    ring = float(y[(r > 15) & (r < 25) & low].mean())
    far = float(y[(r > 40) & (r < 60) & low].mean())
    ring2 = float(y[(r > 20) & (r < 30) & low].mean())
    ring3 = float(y[(r > 24) & (r < 34) & low].mean())
    core = float(y[r < 5].mean())

    def row(c):
        col = y[:27, c]
        return int(np.argmax(col)) if col.max() > 0.2 else -1
    edge = (row(10) + row(150)) / 2.0
    center = row(80)
    return {"ring": ring, "ring2": ring2, "ring3": ring3, "far": far, "core": core, "curv": (edge - center) if edge >= 0 and center >= 0 else 99.0}


def calibrate():
    for kind in ("starter", "solution", "no_glare", "bloom_strong", "ghosts", "no_distortion", "over_distortion"):
        build(kind)
        print("[glare]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(np.repeat(np.repeat(np.clip(render(), 0, 1), 2, axis=0), 2, axis=1))
    img = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_05_glare_starter.blend"))
    for k in ("no_glare", "bloom_strong", "ghosts", "no_distortion", "over_distortion"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_05_glare_{k}.blend"))
    sketch(os.path.join(out, "ch11_05_glare_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_05_glare_solution.blend"))


if __name__ == "__main__":
    L.run(main)
