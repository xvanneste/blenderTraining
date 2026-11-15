"""
validate_ch18_08.py — Correcteur CH18.08 (calques, masques, modificateurs non destructifs).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch18_08.py --python-exit-code 1 -- --exercise layers [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402

LINE_STROKES = 18   # traits du personnage fourni (mannequin « reach » de bcma_gp)


def main():
    r = L.Report("CH18.08 — Calques, masques, modificateurs")
    ob = L.obj("GP_Practice")
    if not r.check(ob is not None and ob.type == "GREASEPENCIL", "Objet GP_Practice présent", "Ne renommez pas l'objet.", 1):
        return r.finish()
    lay = {l.name: l for l in ob.data.layers}
    need = ("BG", "CLOUDS", "FX_LIGHT", "MASK_WINDOW", "SHADE", "LINE")
    r.check(all(n in lay for n in need), "Les 6 calques fournis sont présents", "Ne supprimez ni ne renommez les calques.", 1)
    n_line = sum(len(f.drawing.strokes) for f in lay["LINE"].frames) if "LINE" in lay else 0
    r.check(n_line == LINE_STROKES, f"Dessin LINE intact ({n_line} traits, attendu {LINE_STROKES})",
            "Ne pas appliquer les modificateurs (Apply) : le travail doit rester non destructif.", 2)
    mods = {}
    for m in ob.modifiers:
        mods.setdefault(m.type, []).append(m)
    for t, label, layer_name in (("GREASE_PENCIL_THICKNESS", "Thickness", "LINE"),
                                 ("GREASE_PENCIL_NOISE", "Noise", "LINE"),
                                 ("GREASE_PENCIL_TINT", "Tint", "BG"),
                                 ("GREASE_PENCIL_BUILD", "Build", "LINE")):
        ms = mods.get(t, [])
        if r.check(ms, f"Modificateur {label} présent", f"Add Modifier > {label}.", 2):
            r.check(any(m.tree_node_filter == layer_name for m in ms), f"{label} limité au calque {layer_name}",
                    f"Panneau Influence du modificateur > Layer : {layer_name}.", 1)
            r.check(all(m.show_render for m in ms), f"{label} actif au rendu", "Icône appareil photo du modificateur.", 1)
    if "FX_LIGHT" in lay:
        fl = lay["FX_LIGHT"]
        r.check(fl.use_masks and any(mk.name == "MASK_WINDOW" for mk in fl.mask_layers),
                "FX_LIGHT masqué par MASK_WINDOW", "Calque FX_LIGHT actif > panneau Masks (cocher) > + > MASK_WINDOW.", 3)
    if "MASK_WINDOW" in lay:
        mw = lay["MASK_WINDOW"]
        r.check(not mw.hide and mw.opacity < 0.05, f"MASK_WINDOW invisible mais actif (œil ouvert, opacité {mw.opacity:.2f})",
                "Opacity du calque MASK_WINDOW = 0 ; ne fermez pas son œil (un masque caché n'agit plus en 5.3).", 2)
    if "SHADE" in lay:
        r.check(lay["SHADE"].blend_mode == "MULTIPLY", f"SHADE en Multiply ({lay['SHADE'].blend_mode})",
                "Calque SHADE > Blend Mode : Multiply.", 2)
        r.check(lay["SHADE"].opacity < 0.95, f"SHADE semi-transparent (opacité {lay['SHADE'].opacity:.2f})",
                "Opacity ≈ 0.6.", 1)
    if "CLOUDS" in lay:
        t = lay["CLOUDS"].translation
        r.check(abs(t[0]) > 0.5, f"CLOUDS déplacé par la transformation du calque (X = {t[0]:.2f})",
                "Panneau Layers > Transform (calque CLOUDS actif) > Translation X = 2.", 2)
        r.check(abs(ob.location.x) < 1e-4 and abs(ob.location.z) < 1e-4, "Objet GP_Practice non déplacé",
                "Déplacez le calque, pas l'objet.", 1)
    r.check(len(ob.shader_effects) >= 1, f"Effet (Shader FX) ajouté ({len(ob.shader_effects)})",
            "Properties > onglet Effects > Add Effect > Shadow (facultatif).", 1, mandatory=False)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.1, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
