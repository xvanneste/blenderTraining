"""
validate_ch04_03.py — Correcteur « PBR et Principled BSDF » (CH04.03).
Usage : … --python-exit-code 1 --python validate_ch04_03.py -- --exercise pbr [--render] [--debug]
Quatre sphères SPH_Metal, SPH_Rubber, SPH_Glass, SPH_Wax, chacune avec SON matériau MAT_<Nom> (Principled BSDF) :
  Metal  : Metallic ≥ 0,9 ; luminance de Base Color ≥ 0,5 (un métal reflète clair) ; Roughness 0,05–0,6.
  Rubber : Metallic ≤ 0,05 ; albedo (luminance) 0,02–0,5 ; Roughness ≥ 0,55 ; pas de transmission.
  Glass  : Metallic ≤ 0,05 ; Transmission Weight ≥ 0,9 ; Roughness ≤ 0,1 ; IOR 1,3–1,7.
  Wax    : Metallic ≤ 0,05 ; albedo 0,3–0,9 ; Subsurface Weight ≥ 0,2 avec un rayon coloré (R > B) ; Roughness 0,2–0,8.
  Général : matériaux distincts ; aucun diélectrique « blanc pur » (albedo ≤ 0,9) ; Metallic proche de 0 ou 1 (pas de valeur intermédiaire entre 0,1 et 0,9).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def principled(mat):
    if mat is None or not mat.node_tree:
        return None
    return next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)


def vals(b):
    g = lambda n: b.inputs[n].default_value  # noqa: E731
    return {"base": tuple(g("Base Color"))[:3], "metal": float(g("Metallic")), "rough": float(g("Roughness")), "ior": float(g("IOR")),
            "trans": float(g("Transmission Weight")), "sss": float(g("Subsurface Weight")), "sssr": tuple(g("Subsurface Radius")),
            "coat": float(g("Coat Weight"))}


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.03 — PBR et Principled BSDF")
    mats = {}
    for name in ("Metal", "Rubber", "Glass", "Wax"):
        ob = bpy.data.objects.get("SPH_" + name)
        m = ob.active_material if ob and ob.data.materials else None
        b = principled(m)
        mats[name] = (m, b)
        r.check(b is not None, f"SPH_{name} : matériau avec un Principled BSDF", f"Un matériau MAT_{name} sur SPH_{name}.", 1)
    if any(b is None for _, b in mats.values()):
        return r.finish()
    r.check(len({m.name for m, _ in mats.values()}) == 4, "Quatre matériaux distincts (un par sphère)", "Un matériau par sphère : pas de partage.", 2)
    v = {n: vals(b) for n, (m, b) in mats.items()}
    if debug:
        for n, x in v.items():
            print(f"[DEBUG] {n}: base={tuple(round(c, 3) for c in x['base'])} lum={lum(x['base']):.3f} metal={x['metal']:.2f} rough={x['rough']:.2f} ior={x['ior']:.2f} trans={x['trans']:.2f} sss={x['sss']:.2f} sssr={tuple(round(c, 2) for c in x['sssr'])}")
    M, R, G, W = v["Metal"], v["Rubber"], v["Glass"], v["Wax"]
    r.check(M["metal"] >= 0.9, f"Metal : Metallic {M['metal']:.2f} (≥ 0,9)", "Un métal est entièrement métallique (1).", 3)
    r.check(lum(M["base"]) >= 0.5, f"Metal : Base Color claire (luminance {lum(M['base']):.2f} ≥ 0,5)", "Pour un métal, Base Color = couleur de la réflexion (F0) : jamais sombre (or ≈ 1 / 0,77 / 0,34).", 3)
    r.check(0.05 <= M["rough"] <= 0.6, f"Metal : Roughness {M['rough']:.2f} (0,05–0,6)", "Un métal poli : 0,1–0,4.", 1)
    r.check(R["metal"] <= 0.05, f"Rubber : Metallic {R['metal']:.2f} (≤ 0,05)", "Un caoutchouc n'est pas métallique : 0.", 3)
    r.check(0.02 <= lum(R["base"]) <= 0.5, f"Rubber : albedo {lum(R['base']):.2f} (0,02–0,5)", "Caoutchouc noir : 0,02–0,1 (jamais 0 ni blanc).", 2)
    r.check(R["rough"] >= 0.55 and R["trans"] <= 0.05, f"Rubber : Roughness {R['rough']:.2f} (≥ 0,55), transmission {R['trans']:.2f}", "Matière mate et opaque.", 2)
    r.check(G["trans"] >= 0.9, f"Glass : Transmission Weight {G['trans']:.2f} (≥ 0,9)", "Le verre transmet la lumière : Transmission Weight 1.", 3)
    r.check(G["rough"] <= 0.1 and G["metal"] <= 0.05, f"Glass : Roughness {G['rough']:.2f} (≤ 0,1), Metallic {G['metal']:.2f}", "Verre lisse et non métallique.", 2)
    r.check(1.3 <= G["ior"] <= 1.7, f"Glass : IOR {G['ior']:.2f} (1,3–1,7)", "Verre ≈ 1,45–1,55.", 2)
    r.check(W["metal"] <= 0.05 and 0.3 <= lum(W["base"]) <= 0.9, f"Wax : Metallic {W['metal']:.2f} ; albedo {lum(W['base']):.2f} (0,3–0,9)", "Cire : non métallique, claire mais pas blanche pure.", 2)
    r.check(W["sss"] >= 0.2 and W["sssr"][0] > W["sssr"][2], f"Wax : Subsurface Weight {W['sss']:.2f} (≥ 0,2), rayon R/V/B {tuple(round(c, 2) for c in W['sssr'])} (R > B)", "Le sous-surface diffuse davantage le rouge que le bleu.", 3)
    r.check(0.2 <= W["rough"] <= 0.8, f"Wax : Roughness {W['rough']:.2f} (0,2–0,8)", "", 1)
    diel = [("Rubber", R), ("Wax", W)]
    r.check(all(lum(x["base"]) <= 0.9 for _, x in diel), "Aucun diélectrique blanc pur (albedo ≤ 0,9)", "Le blanc le plus clair de la nature (neige fraîche) ≈ 0,9.", 2)
    inter = [n for n, x in v.items() if 0.1 < x["metal"] < 0.9]
    r.check(not inter, f"Metallic proche de 0 ou de 1 partout (valeurs intermédiaires : {inter or 'aucune'})", "Metallic est presque binaire : 0 ou 1 ; l'intermédiaire ne sert qu'aux transitions (rouille, peinture écaillée).", 2)
    if L.flag("--render"):
        lum_r = L.quick_render(15, 4)
        r.check(lum_r > 0.05, f"Rendu de contrôle non noir ({lum_r:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
