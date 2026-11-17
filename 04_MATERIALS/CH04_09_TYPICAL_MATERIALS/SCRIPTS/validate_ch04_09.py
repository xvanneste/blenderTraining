"""
validate_ch04_09.py — Correcteur « Matériaux types » (CH04.09).
Usage : … --python-exit-code 1 --python validate_ch04_09.py -- --exercise materials [--render] [--debug]
Cinq sphères SPH_Wood / Stone / Plastic / Glass / Steel et matériaux MAT_<Nom> (Principled BSDF) :
  Wood    : Base Color pilotée par une texture Wave via Color Ramp ; Metallic ≤ 0,05 ; Roughness 0,3–0,7.
  Stone   : Base Color pilotée par une texture (Voronoi / Noise) ; un Bump alimenté par une texture relié à Normal ; Roughness ≥ 0,6.
  Plastic : Metallic ≤ 0,05 ; Base Color saturé (max − min ≥ 0,3) ; Roughness 0,15–0,5 ; Coat Weight ≥ 0,3.
  Glass   : Transmission Weight ≥ 0,9 ; Roughness ≤ 0,1 ; IOR 1,4–1,6.
  Steel   : Metallic ≥ 0,9 ; Base Color de luminance ≥ 0,5 ; Anisotropic ≥ 0,4 ; Roughness pilotée par un Noise.
  Tous : marqués comme assets (asset_data) avec une description non vide ; cinq matériaux distincts.
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
    r = L.Report("CH04.09 — Matériaux types")
    M, B = {}, {}
    for n in ("Wood", "Stone", "Plastic", "Glass", "Steel"):
        ob = bpy.data.objects.get("SPH_" + n)
        m = ob.active_material if ob and ob.data.materials else None
        b = next((x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None) if m and m.node_tree else None
        M[n], B[n] = m, b
        r.check(b is not None, f"SPH_{n} : matériau avec un Principled BSDF", f"MAT_{n} sur SPH_{n}.", 1)
    if any(b is None for b in B.values()):
        return r.finish()
    r.check(len({m.name for m in M.values()}) == 5, "Cinq matériaux distincts", "Un matériau par sphère.", 1)
    g = lambda n, k: B[n].inputs[k].default_value  # noqa: E731
    T = {n: {k: upstream(B[n].inputs[k]) for k in ("Base Color", "Roughness", "Normal")} for n in B}
    # Bois
    r.check({"TEX_WAVE", "VALTORGB"} <= T["Wood"]["Base Color"], f"Wood : Base Color pilotée par Wave + Color Ramp ({sorted(T['Wood']['Base Color'])})", "Wave Texture [Fac] -> Color Ramp -> Base Color.", 3)
    r.check(g("Wood", "Metallic") <= 0.05 and 0.3 <= g("Wood", "Roughness") <= 0.7, f"Wood : Metallic {g('Wood', 'Metallic'):.2f}, Roughness {g('Wood', 'Roughness'):.2f} (0,3–0,7)", "Le bois n'est pas métallique et reste mi-mat.", 2)
    # Pierre
    st = {t for t in T["Stone"]["Base Color"] if t in ("TEX_VORONOI", "TEX_NOISE")}
    r.check(bool(st), f"Stone : Base Color pilotée par une texture ({sorted(st) or 'aucune'})", "Voronoi ou Noise -> Base Color.", 3)
    bump = any(t == "BUMP" for t in T["Stone"]["Normal"]) and any(t.startswith("TEX_") for t in T["Stone"]["Normal"])
    r.check(bump, "Stone : Normal alimentée par Bump et une texture", "Texture -> Bump [Height] -> Normal.", 3)
    r.check(g("Stone", "Roughness") >= 0.6, f"Stone : Roughness {g('Stone', 'Roughness'):.2f} (≥ 0,6)", "Une pierre brute est mate.", 1)
    # Plastique
    c = g("Plastic", "Base Color")
    r.check(g("Plastic", "Metallic") <= 0.05 and max(c[:3]) - min(c[:3]) >= 0.3, f"Plastic : Metallic {g('Plastic', 'Metallic'):.2f}, saturation {max(c[:3]) - min(c[:3]):.2f} (≥ 0,3)", "Un plastique coloré franc, non métallique.", 2)
    r.check(0.15 <= g("Plastic", "Roughness") <= 0.5, f"Plastic : Roughness {g('Plastic', 'Roughness'):.2f} (0,15–0,5)", "Brillant mais pas miroir.", 2)
    r.check(g("Plastic", "Coat Weight") >= 0.3, f"Plastic : Coat Weight {g('Plastic', 'Coat Weight'):.2f} (≥ 0,3)", "Vernis : Coat.", 1)
    # Verre
    r.check(g("Glass", "Transmission Weight") >= 0.9 and g("Glass", "Roughness") <= 0.1, f"Glass : Transmission {g('Glass', 'Transmission Weight'):.2f}, Roughness {g('Glass', 'Roughness'):.2f}", "Transmission 1, Roughness ≤ 0,1.", 2)
    r.check(1.4 <= g("Glass", "IOR") <= 1.6, f"Glass : IOR {g('Glass', 'IOR'):.2f} (1,4–1,6)", "", 1)
    # Acier
    r.check(g("Steel", "Metallic") >= 0.9 and lum(g("Steel", "Base Color")) >= 0.5, f"Steel : Metallic {g('Steel', 'Metallic'):.2f}, luminance {lum(g('Steel', 'Base Color')):.2f} (≥ 0,5)", "Métal clair.", 2)
    r.check(g("Steel", "Anisotropic") >= 0.4, f"Steel : Anisotropic {g('Steel', 'Anisotropic'):.2f} (≥ 0,4)", "Brossé : anisotropie.", 3)
    r.check("TEX_NOISE" in T["Steel"]["Roughness"], f"Steel : Roughness pilotée par un Noise ({sorted(T['Steel']['Roughness'])})", "Noise étiré -> Map Range -> Roughness.", 2)
    # Assets
    bad = [n for n, m in M.items() if m.asset_data is None or not (m.asset_data.description or "").strip()]
    r.check(not bad, f"Matériaux marqués asset avec description (manquants : {bad or 'aucun'})", "Clic droit sur le matériau > Mark as Asset, puis une description.", 3)
    if debug:
        for n in T:
            print("[DEBUG]", n, {k: sorted(v) for k, v in T[n].items()})
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
