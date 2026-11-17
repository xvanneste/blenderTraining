"""
validate_ch04_05.py — Correcteur « Textures procédurales » (CH04.05).
Usage : … --python-exit-code 1 --python validate_ch04_05.py -- --exercise procedural [--render] [--debug]
PROP_Wall / matériau MAT_Brick, entièrement procédural :
  - une Brick Texture dont Color alimente Base Color, sans aucune image dans le matériau ;
  - Vector de la Brick alimenté par un Texture Coordinate ;
  - Scale 3–12 ; Mortar Size 0,005–0,1 ; décalage des rangées (Offset) 0,3–0,7 ;
  - Color1 et Color2 différentes (distance ≥ 0,08) ; Mortar plus clair que les briques (écart de luminance ≥ 0,15) ;
  - Bump relié à Normal, avec Height alimentée par la Brick (Fac) ; Strength 0,2–1,5 ;
  - Roughness ≥ 0,6 (constante ou pilotée) ; aucun nœud orphelin.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def upstream(sock, seen=None):
    seen = set() if seen is None else seen
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            for i in n.inputs:
                upstream(i, seen)
    return seen


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.05 — Textures procédurales")
    ob = bpy.data.objects.get("PROP_Wall")
    mat = ob.active_material if ob and ob.data.materials else None
    if not r.check(mat is not None and mat.node_tree is not None, "PROP_Wall avec un matériau à nœuds", "Partez du fichier de départ (MAT_Brick).", 2):
        return r.finish()
    nt = mat.node_tree
    N = nt.nodes
    b = next((n for n in N if n.type == "BSDF_PRINCIPLED"), None)
    if b is None:
        return r.finish()
    bu = {N[k].type for k in upstream(b.inputs["Base Color"])}
    brick = next((n for n in N if n.type == "TEX_BRICK" and any(l.from_node == n and l.to_node == b and l.to_socket.name == "Base Color" for l in nt.links)), None)
    r.check(brick is not None, "Brick Texture [Color] reliée à Base Color", "Brick Texture : sortie Color -> Base Color.", 3)
    r.check(not any(n.type == "TEX_IMAGE" for n in N), "Matériau procédural : aucune image", "Pas de nœud Image Texture ici.", 1)
    if brick is None:
        return r.finish()
    vt = {N[k].type for k in upstream(brick.inputs["Vector"])}
    r.check("TEX_COORD" in vt, "Brick : coordonnées fournies par Texture Coordinate", "Texture Coordinate [Object] -> Vector.", 2)
    sc = brick.inputs["Scale"].default_value
    r.check(3 <= sc <= 12, f"Brick Scale {sc:.1f} (3–12)", "Trop grand : briques minuscules ; trop petit : une seule brique.", 2)
    ms = brick.inputs["Mortar Size"].default_value
    r.check(0.005 <= ms <= 0.1, f"Mortar Size {ms:.3f} (0,005–0,1)", "Joint fin mais visible.", 2)
    r.check(0.3 <= brick.offset <= 0.7, f"Offset des rangées {brick.offset:.2f} (0,3–0,7)", "Briques décalées d'une demi-brique d'une rangée à l'autre (appareil courant) ; 0 = joints alignés.", 2)
    c1, c2, cm = (list(brick.inputs[k].default_value)[:3] for k in ("Color1", "Color2", "Mortar"))
    d = math.dist(c1, c2)
    r.check(d >= 0.08, f"Color1 / Color2 : distance {d:.2f} (≥ 0,08)", "Des briques toutes identiques font un motif artificiel.", 2)
    dl = lum(cm) - max(lum(c1), lum(c2))
    r.check(dl >= 0.15, f"Mortar plus clair que les briques (écart de luminance {dl:.2f} ≥ 0,15)", "Joint de mortier clair.", 2)
    bump = next((n for n in N if n.type == "BUMP" and any(l.from_node == n and l.to_node == b and l.to_socket.name == "Normal" for l in nt.links)), None)
    r.check(bump is not None, "Bump relié à Normal du Principled", "Bump [Normal] -> Normal.", 3)
    drv = bump is not None and brick.name in upstream(bump.inputs["Height"])
    r.check(drv, "Bump : Height alimentée par la Brick (Fac)", "Reliez Brick [Fac] à Bump [Height].", 3)
    if drv:
        height_link = bump.inputs["Height"].links[0]
        if height_link.from_node == brick and height_link.from_socket == brick.outputs["Fac"]:
            r.check(bump.invert, "Sens du relief : joints en creux", "Le masque vaut 1 sur les joints. Activez Invert sur Bump.", 2)
    st = bump.inputs["Strength"].default_value if bump else 0
    r.check(bump is not None and 0.2 <= st <= 1.5, f"Bump Strength {st:.2f} (0,2–1,5)", "", 1)
    rough = b.inputs["Roughness"].default_value if not b.inputs["Roughness"].links else 1.0
    r.check(rough >= 0.6, f"Roughness {rough:.2f} (≥ 0,6)", "Une brique est mate.", 1)
    orph = [n.name for n in N if n.type not in ("OUTPUT_MATERIAL", "FRAME") and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "Supprimez ou reliez.", 2)
    if debug:
        print("[DEBUG] scale", sc, "mortar", ms, "offset", brick.offset, "dist", round(d, 3), "dl", round(dl, 3))
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
