"""
validate_ch11_02.py — Correcteur « Compositing multipasse » (CH11.02).
Usage : … --python-exit-code 1 --python validate_ch11_02.py -- --exercise multipass [--debug]
Objets : Ball, KEY (60 W, light group key), FILL (60 W, light group fill), CAM. Le correcteur lit l'arbre de compositing et rend (Cycles CPU, 128 × 72, 32 échantillons, sans débruitage, compositing de l'élève) :
  structure : Render Layers avec les prises « Combined_key » ET « Combined_fill » reliées ; arbre relié à Group Output ; aucun nœud orphelin ; compositing de rendu activé ;
  relighting : luminance LINÉAIRE du flanc gauche (rangées 32–39, colonnes 36–45) / flanc droit (colonnes 82–91) de 3 à 5,5 (départ 1,17 ; solution 4,28 ; ±3 diaphragmes 27,8 ; inversé 0,32) ;
  le flanc de FILL ne s'éteint pas : luminance linéaire du flanc droit ≥ 0,01 (KEY seul : 0,003).
Les lampes (60 W) ne doivent pas être modifiées.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.02 — Compositing multipasse")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Ball", "KEY", "FILL", "CAM")), "Ball, KEY, FILL et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(abs(O["KEY"].data.energy - 60) < 1e-3 and abs(O["FILL"].data.energy - 60) < 1e-3, "Lampes inchangées : KEY et FILL à 60 W", "Relightez dans le compositeur, pas dans la scène.", 3)
    ng = sc.compositing_node_group
    if not r.check(ng is not None, "Arbre de compositing présent", "Compositing : arbre fourni par le fichier de départ.", 3):
        return r.finish()
    rl = next((n for n in ng.nodes if n.bl_idname == "CompositorNodeRLayers"), None)
    outs = [n for n in ng.nodes if n.bl_idname == "NodeGroupOutput"]
    used = {s.name: any(l.from_socket == s for l in ng.links) for s in rl.outputs} if rl else {}
    r.check(rl is not None and used.get("Combined_key") and used.get("Combined_fill"), f"Prises de light groups utilisées : Combined_key {'oui' if used.get('Combined_key') else 'non'}, Combined_fill {'oui' if used.get('Combined_fill') else 'non'}", "Utilisez les deux prises Combined_key et Combined_fill de Render Layers.", 8)
    reach, todo = set(), list(outs)
    while todo:
        n = todo.pop()
        if n in reach:
            continue
        reach.add(n)
        todo += [l.from_node for l in ng.links if l.to_node == n]
    orphans = [n.name for n in ng.nodes if n not in reach]
    r.check(not orphans and bool(outs) and any(l.to_node == outs[0] for l in ng.links), "Arbre relié à la sortie, aucun nœud orphelin" if not orphans else f"Nœuds orphelins : {', '.join(orphans)}", "Chaque nœud doit mener à Group Output.", 4)
    r.check(sc.render.use_compositing, f"Compositing de rendu : {'activé' if sc.render.use_compositing else 'désactivé'}", "Output > Post Processing > Pipeline : Compositing.", 3)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.cycles.seed = 0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1102_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    lin = np.where(y <= 0.04045, y / 12.92, ((y + 0.055) / 1.055) ** 2.4)
    left, right = float(lin[32:40, 36:46].mean()), float(lin[32:40, 82:92].mean())
    ratio = left / max(right, 1e-6)
    r.check(3.0 <= ratio <= 5.5, f"Relighting : flanc KEY / flanc FILL = {ratio:.2f} (3–5,5)", "Exposure +1 sur Combined_key et −1 sur Combined_fill : rapport 4.", 10)
    r.check(right >= 0.01, f"Le flanc de FILL ne s'éteint pas : {right:.3f} (≥ 0,01)", "Ne coupez pas la lumière de remplissage : gardez-la à quelques diaphragmes sous la KEY.", 5)
    if debug:
        print("[DEBUG] left", round(left, 4), "right", round(right, 4), "ratio", round(ratio, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
