"""
validate_ch04_10.py — Correcteur « Matériaux de personnages » (CH04.10).
Usage : … --python-exit-code 1 --python validate_ch04_10.py -- --exercise character [--render] [--debug]
SPH_Skin / SPH_Eye / SPH_Hair / SPH_Cloth, matériaux MAT_<Nom> :
  Skin  : Base Color chair (R > V > B, luminance 0,3–0,8) ; Subsurface Weight ≥ 0,5 ; Subsurface Radius R > V > B avec R ≥ 3 × B ; Scale 0,01–0,2 ;
          Roughness 0,3–0,65 ; Normal alimentée par un Bump et une texture (pores).
  Eye   : Base Color pilotée par Gradient + Color Ramp (écart de luminance des stops ≥ 0,3) ; Roughness ≤ 0,4 ; Coat Weight ≥ 0,8 ; Coat Roughness ≤ 0,1.
  Hair  : nœud Principled Hair BSDF relié à Surface ; couleur de luminance ≤ 0,4 (modèle Couleur) ; Roughness 0,2–0,5.
  Cloth : Metallic ≤ 0,05 ; Roughness ≥ 0,6 ; Sheen Weight ≥ 0,3 ; Normal alimentée par un Bump et une texture (trame).
  Rendu Cycles ; quatre matériaux distincts.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def upstream(sock, seen=None):
    seen = set() if seen is None else seen
    out = set()
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            out.add(n.type)
            for i in n.inputs:
                out |= upstream(i, seen)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.10 — Matériaux de personnages")
    M = {}
    for n in ("Skin", "Eye", "Hair", "Cloth"):
        ob = bpy.data.objects.get("SPH_" + n)
        m = ob.active_material if ob and ob.data.materials else None
        M[n] = m
        r.check(m is not None and m.node_tree is not None, f"SPH_{n} : matériau à nœuds", f"MAT_{n} sur SPH_{n}.", 1)
    if any(m is None or m.node_tree is None for m in M.values()):
        return r.finish()
    r.check(len({m.name for m in M.values()}) == 4, "Quatre matériaux distincts", "", 1)
    r.check(bpy.context.scene.render.engine == "CYCLES", f"Moteur : {bpy.context.scene.render.engine} (Cycles)", "Cheveux et sous-surface : Cycles.", 1)
    P = {n: next((x for x in M[n].node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None) for n in ("Skin", "Eye", "Cloth")}
    gv = lambda n, k: P[n].inputs[k].default_value  # noqa: E731
    # Peau
    if P["Skin"] is None:
        r.check(False, "Skin : Principled BSDF présent", "", 3)
    else:
        c = gv("Skin", "Base Color")
        r.check(c[0] > c[1] > c[2] and 0.3 <= lum(c) <= 0.8, f"Skin : Base Color chair (R > V > B), luminance {lum(c):.2f} (0,3–0,8)", "Teinte chair, ni blanche ni sombre.", 2)
        sw = gv("Skin", "Subsurface Weight")
        rad = tuple(gv("Skin", "Subsurface Radius"))
        sc_ = gv("Skin", "Subsurface Scale")
        r.check(sw >= 0.5, f"Skin : Subsurface Weight {sw:.2f} (≥ 0,5)", "La peau diffuse la lumière en profondeur.", 3)
        r.check(rad[0] > rad[1] > rad[2] and rad[0] >= 3 * rad[2], f"Skin : Subsurface Radius {tuple(round(v, 2) for v in rad)} (R > V > B, R ≥ 3 × B)", "Le rouge pénètre plus loin que le bleu : (1 ; 0,2 ; 0,1).", 3)
        r.check(0.01 <= sc_ <= 0.2, f"Skin : Subsurface Scale {sc_:.3f} (0,01–0,2)", "Échelle en mètres du rayon.", 1)
        r.check(0.3 <= gv("Skin", "Roughness") <= 0.65, f"Skin : Roughness {gv('Skin', 'Roughness'):.2f} (0,3–0,65)", "", 1)
        nu = upstream(P["Skin"].inputs["Normal"])
        r.check("BUMP" in nu and any(t.startswith("TEX_") for t in nu), f"Skin : Normal alimentée par Bump + texture ({sorted(nu)})", "Noise fin -> Bump -> Normal (pores).", 2)
    # Oeil
    if P["Eye"] is None:
        r.check(False, "Eye : Principled BSDF présent", "", 3)
    else:
        eu = upstream(P["Eye"].inputs["Base Color"])
        ramp = next((x for x in M["Eye"].node_tree.nodes if x.type == "VALTORGB"), None)
        spread = (max(lum(e.color) for e in ramp.color_ramp.elements) - min(lum(e.color) for e in ramp.color_ramp.elements)) if ramp else 0
        r.check("TEX_GRADIENT" in eu and "VALTORGB" in eu and spread >= 0.3, f"Eye : Base Color par Gradient + Color Ramp (écart de luminance {spread:.2f} ≥ 0,3)", "Sclère claire / iris sombre.", 3)
        r.check(gv("Eye", "Roughness") <= 0.4, f"Eye : Roughness {gv('Eye', 'Roughness'):.2f} (≤ 0,4)", "", 1)
        r.check(gv("Eye", "Coat Weight") >= 0.8 and gv("Eye", "Coat Roughness") <= 0.1, f"Eye : Coat Weight {gv('Eye', 'Coat Weight'):.2f}, Coat Roughness {gv('Eye', 'Coat Roughness'):.2f}", "La cornée humide : vernis net.", 3)
    # Cheveux
    nt = M["Hair"].node_tree
    out = next((x for x in nt.nodes if x.type == "OUTPUT_MATERIAL"), None)
    hair = next((l.from_node for l in nt.links if out is not None and l.to_node == out and l.to_socket.name == "Surface" and l.from_node.type == "BSDF_HAIR_PRINCIPLED"), None)
    r.check(hair is not None, "Hair : Principled Hair BSDF relié à Surface", "Add > Shader > Principled Hair BSDF.", 3)
    if hair is not None:
        col = hair.inputs["Color"].default_value
        ok_col = hair.parametrization != "COLOR" or lum(col) <= 0.4
        r.check(ok_col, f"Hair : couleur de luminance {lum(col):.2f} (≤ 0,4)", "Cheveux sombres à moyens.", 2)
        r.check(0.2 <= hair.inputs["Roughness"].default_value <= 0.5, f"Hair : Roughness {hair.inputs['Roughness'].default_value:.2f} (0,2–0,5)", "", 1)
    # Tissu
    if P["Cloth"] is None:
        r.check(False, "Cloth : Principled BSDF présent", "", 3)
    else:
        r.check(gv("Cloth", "Metallic") <= 0.05 and gv("Cloth", "Roughness") >= 0.6, f"Cloth : Metallic {gv('Cloth', 'Metallic'):.2f}, Roughness {gv('Cloth', 'Roughness'):.2f} (≥ 0,6)", "", 2)
        r.check(gv("Cloth", "Sheen Weight") >= 0.3, f"Cloth : Sheen Weight {gv('Cloth', 'Sheen Weight'):.2f} (≥ 0,3)", "Les fibres diffusent un liseré clair en bordure : Sheen.", 3)
        nu = upstream(P["Cloth"].inputs["Normal"])
        r.check("BUMP" in nu and any(t.startswith("TEX_") for t in nu), f"Cloth : trame par Bump + texture ({sorted(nu)})", "Wave -> Bump -> Normal.", 2)
    if debug:
        print("[DEBUG] ok")
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
