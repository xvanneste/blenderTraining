"""
validate_ch04_04.py — Correcteur « Shader Editor et nœuds » (CH04.04).
Usage : … --python-exit-code 1 --python validate_ch04_04.py -- --exercise nodes [--render] [--debug]
SPH_Rust / matériau MAT_RustyMetal (analyse du GRAPHE de nœuds) :
  - Principled BSDF relié à Surface du Material Output ;
  - Base Color alimentée par un Mix (type Color) piloté par une Color Ramp, elle-même alimentée par un Noise Texture ;
  - Metallic piloté (Color Ramp / Noise) et Roughness pilotée (Noise) : pas de valeurs constantes ;
  - le Noise reçoit ses coordonnées d'un Mapping, lui-même alimenté par un Texture Coordinate ;
  - Color Ramp : au moins deux stops de couleurs bien différentes (écart de luminance ≥ 0,5) ;
  - Noise Scale entre 2 et 30 ; couleurs du Mix : une rouille (R − B ≥ 0,2) et un gris de luminance ≥ 0,3 ;
  - aucun nœud orphelin (dont aucune sortie n'est utilisée), 7 à 18 nœuds.
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
    """Ensemble des nœuds en amont d'une entrée (traversée des liens)."""
    seen = set() if seen is None else seen
    for l in sock.links:
        n = l.from_node
        if n.name in seen:
            continue
        seen.add(n.name)
        for i in n.inputs:
            upstream(i, seen)
    return seen


def types(nt, names):
    return {nt.nodes[n].type for n in names}


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.04 — Shader Editor et nœuds")
    ob = bpy.data.objects.get("SPH_Rust")
    mat = ob.active_material if ob and ob.data.materials else None
    if not r.check(mat is not None and mat.node_tree is not None, "SPH_Rust avec un matériau à nœuds", "Partez du fichier de départ (MAT_RustyMetal).", 2):
        return r.finish()
    nt = mat.node_tree
    N = nt.nodes
    outs = [n for n in N if n.type == "OUTPUT_MATERIAL"]
    bsdf = next((n for n in N if n.type == "BSDF_PRINCIPLED"), None)
    linked_out = bool(outs and bsdf and any(l.from_node == bsdf and l.to_node in outs and l.to_socket.name == "Surface" for l in nt.links))
    r.check(linked_out, "Principled BSDF relié à Surface du Material Output", "Tirez BSDF -> Surface.", 3)
    if bsdf is None:
        return r.finish()
    base_up = upstream(bsdf.inputs["Base Color"])
    met_up = upstream(bsdf.inputs["Metallic"])
    rou_up = upstream(bsdf.inputs["Roughness"])
    tb, tm, tr = types(nt, base_up), types(nt, met_up), types(nt, rou_up)
    r.check({"MIX", "VALTORGB", "TEX_NOISE"} <= tb, f"Base Color : Noise → Color Ramp → Mix (types en amont : {sorted(tb)})", "Mix (Color) piloté par une Color Ramp elle-même pilotée par un Noise Texture.", 3)
    r.check("TEX_NOISE" in tm, f"Metallic piloté par la texture (types : {sorted(tm)})", "Reliez la Color Ramp à Metallic (pas de valeur constante).", 3)
    r.check("TEX_NOISE" in tr, f"Roughness pilotée par la texture (types : {sorted(tr)})", "Noise -> Map Range -> Roughness.", 2)
    noises = [n for n in N if n.type == "TEX_NOISE"]
    main_noise = next((n for n in noises if n.name in base_up), None)
    ok_map = False
    if main_noise is not None:
        vt = types(nt, upstream(main_noise.inputs["Vector"]))
        ok_map = {"MAPPING", "TEX_COORD"} <= vt
    r.check(ok_map, "Noise : coordonnées via Texture Coordinate → Mapping", "Texture Coordinate (Object) -> Mapping -> Vector du Noise.", 3)
    ramp = next((n for n in N if n.type == "VALTORGB" and n.name in base_up), None)
    cols = [lum(e.color) for e in ramp.color_ramp.elements] if ramp else [0]
    spread = max(cols) - min(cols)
    r.check(ramp is not None and len(ramp.color_ramp.elements) >= 2 and spread >= 0.5, f"Color Ramp : écart de luminance des stops {spread:.2f} (≥ 0,5)", "Un stop clair, un stop sombre : le masque doit passer de 0 à 1.", 2)
    sc_ok = main_noise is not None and 2.0 <= main_noise.inputs["Scale"].default_value <= 30.0
    r.check(sc_ok, f"Noise Scale {main_noise.inputs['Scale'].default_value if main_noise else float('nan'):.1f} (2–30)", "Trop petit : uniforme ; trop grand : sel et poivre.", 2)
    mix = next((n for n in N if n.type == "MIX" and n.name in base_up), None)
    cols_ok = False
    if mix is not None:
        a = next(i for i in mix.inputs if i.identifier == "A_Color").default_value
        b = next(i for i in mix.inputs if i.identifier == "B_Color").default_value
        rust = [c for c in (a, b) if c[0] - c[2] >= 0.2]
        grey = [c for c in (a, b) if abs(c[0] - c[2]) < 0.2 and lum(c) >= 0.3]
        cols_ok = bool(rust) and bool(grey)
    r.check(cols_ok, "Mix : une couleur rouille (R − B ≥ 0,2) et un gris clair (luminance ≥ 0,3)", "A et B du Mix : rouille et acier.", 2)
    orph = [n.name for n in N if n.type not in ("OUTPUT_MATERIAL", "FRAME") and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "Supprimez (X) ou reliez les nœuds dont aucune sortie n'est utilisée.", 2)
    n_nodes = len([n for n in N if n.type != "FRAME"])
    r.check(7 <= n_nodes <= 18, f"{n_nodes} nœuds (7–18)", "Un graphe lisible reste court.", 1)
    if debug:
        print("[DEBUG] amont base", sorted(tb), "metallic", sorted(tm), "roughness", sorted(tr), "orphelins", orph, "spread", round(spread, 2))
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
