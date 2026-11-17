"""
build_ch11_06_files.py — « Color grading » (CH11.06 : étalonnage avec Color Balance : tons froids dans les ombres, chauds dans les hautes lumières, exposition préservée).

Scène (Cycles CPU, 160 × 90, 1 échantillon, caméra orthographique) : Chart (plan émissif de 2 × 1,125 m qui remplit le cadre) : une rampe de gris linéaire de 0 (gauche) à 1 (droite) ; CAM orthographique (échelle 2). Image affichée en Standard.
  Consigne (compositeur) : Render Layers → Color Balance → Group Output : un étalonnage « ombres froides, hautes lumières chaudes » SANS changer l'exposition :
    1. ombres (colonnes 4–31) : bleu − rouge ≥ 0,05 (froid) ; 2. hautes lumières (colonnes 128–155) : rouge − bleu ≥ 0,03 (chaud) ;
    3. la luminance moyenne de l'image reste à ± 0,08 de celle du rendu non étalonné (mesuré par le correcteur avec le compositing désactivé) ;
    4. aucun nœud orphelin, compositing activé.
  Color Balance 5.3 : Type « Lift/Gamma/Gain » ; les prises sont dédoublées (facteur + couleur) : la COULEUR de Lift (prise 4), de Gamma (prise 6) et de Gain (prise 8) ; le facteur Lift est la prise 3.
  Départ : Render Layers (Image) → Group Output. Solution : Color Balance (Lift/Gamma/Gain) : Lift (0,96 ; 1,0 ; 1,04), Gain (1,08 ; 1,0 ; 0,92).
  STARTER_FILES/ch11_06_grading_starter.blend ; COMPLETED_EXAMPLES/ch11_06_grading_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : all_warm (Lift et Gain chauds), all_cool (Lift et Gain froids), swapped (ombres chaudes, hautes lumières froides), too_bright (solution + Gamma 2,0 : tons moyens trop clairs), no_grade (Color Balance neutre)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.06 — COLOR GRADING (Chart, CAM)
Une rampe de gris de 0 (gauche) à 1 (droite). Étalonnez en « ombres froides, hautes lumières chaudes » sans changer l'exposition.
Compositeur : Render Layers → Color Balance (Type Lift/Gamma/Gain) → Group Output. Couleurs de Lift (ombres), Gamma (tons moyens), Gain (hautes lumières).
Cible : ombres (colonnes 4–31) : bleu − rouge ≥ 0,05 ; hautes lumières (colonnes 128–155) : rouge − bleu ≥ 0,03 ; luminance moyenne à ± 0,08 de l'image non étalonnée ; pas de nœud orphelin ; compositing activé.
Vérification : SCRIPTS/validate_ch11_06.py -- --exercise grading
"""

SETS = {  # (Lift RGB, Gamma RGB, Gain RGB)
    "starter": None,
    "solution": ((0.96, 1.0, 1.04), (1.0, 1.0, 1.0), (1.08, 1.0, 0.92)),
    "all_warm": ((1.04, 1.0, 0.96), (1.0, 1.0, 1.0), (1.08, 1.0, 0.92)),
    "all_cool": ((0.96, 1.0, 1.04), (1.0, 1.0, 1.0), (0.92, 1.0, 1.08)),
    "swapped": ((1.04, 1.0, 0.96), (1.0, 1.0, 1.0), (0.92, 1.0, 1.08)),
    "too_bright": ((0.96, 1.0, 1.04), (2.0, 2.0, 2.0), (1.08, 1.0, 0.92)),
    "no_grade": ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
}


def build(kind):
    L.reset("SC_GRADE")
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 5, 0), rotation=(1.5707963, 0, 0))
    ch = bpy.context.object
    ch.name = "Chart"
    ch.scale = (2.0, 1.125, 1.0)
    m = bpy.data.materials.new("MA_Chart")
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    gr = nt.nodes.new("ShaderNodeTexGradient")
    gr.gradient_type = "LINEAR"
    em = nt.nodes.new("ShaderNodeEmission")
    oo = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tc.outputs["Generated"], gr.inputs["Vector"])
    nt.links.new(gr.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], oo.inputs[0])
    ch.data.materials.append(m)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (1.5707963, 0, 0)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 2.0
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-600, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (400, 0)
    prev = rl.outputs["Image"]
    s = SETS[kind]
    if s is not None:
        cb = ng.nodes.new("CompositorNodeColorBalance")
        cb.location = (-200, 0)
        cb.inputs["Type"].default_value = "Lift/Gamma/Gain"
        cb.inputs[4].default_value = (*s[0], 1)
        cb.inputs[6].default_value = (*s[1], 1)
        cb.inputs[8].default_value = (*s[2], 1)
        ng.links.new(prev, cb.inputs["Image"])
        prev = cb.outputs["Image"]
    ng.links.new(prev, out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)


def render(compositing=True):
    sc = bpy.context.scene
    keep = sc.render.use_compositing
    sc.render.use_compositing = compositing
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1106.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    sc.render.use_compositing = keep
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(px=None, ref=None):
    px = render() if px is None else px
    ref = render(False) if ref is None else ref
    y = lambda a: float((a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722).mean())
    sh, hl = px[:, 4:32].reshape(-1, 3).mean(axis=0), px[:, 128:156].reshape(-1, 3).mean(axis=0)
    return {"shadow_cool": float(sh[2] - sh[0]), "high_warm": float(hl[0] - hl[2]), "dY": y(px) - y(ref), "mean": y(px)}


def calibrate():
    for kind in SETS:
        build(kind)
        print("[grade]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(np.repeat(np.repeat(render(), 3, axis=0), 3, axis=1))
    img = np.concatenate(tiles, axis=0)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_06_grading_starter.blend"))
    for k in ("all_warm", "all_cool", "swapped", "too_bright", "no_grade"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_06_grading_{k}.blend"))
    sketch(os.path.join(out, "ch11_06_grading_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_06_grading_solution.blend"))


if __name__ == "__main__":
    L.run(main)
