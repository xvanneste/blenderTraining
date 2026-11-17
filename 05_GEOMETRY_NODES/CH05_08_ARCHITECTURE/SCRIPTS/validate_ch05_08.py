"""
validate_ch05_08.py — Correcteur « Architecture procédurale » (CH05.08).
Usage : … --python-exit-code 1 --python validate_ch05_08.py -- --exercise architecture [--render] [--debug]
GEO_Building / outil GN_Building — le correcteur RÈGLE les paramètres et mesure la géométrie évaluée, pour DEUX réglages :
  A (défaut) : Floors 4, Bays 5, Floor Height 3, Bay Width 2,5, Depth 8 ;   B : Floors 7, Bays 3, Floor Height 3,4, Bay Width 3,2, Depth 10.
  Interface : Floors (Integer), Bays (Integer), Floor Height, Bay Width, Depth (Float) avec descriptions, bornes et défauts cohérents.
  Pour chaque réglage : nombre de fenêtres = Floors × Bays ; corps : largeur = Bays × Bay Width, profondeur = Depth, hauteur = Floors × Floor Height (± 2 cm), posé sur z = 0 ;
  fenêtres sur la façade avant (y = −Depth ÷ 2 ± 5 cm), dans la largeur du corps, espacées de Bay Width en X et de Floor Height en Z (± 2 cm), première rangée à 0,55 × Floor Height (± 5 cm).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

EXPECT = {"Floors": "NodeSocketInt", "Bays": "NodeSocketInt", "Floor Height": "NodeSocketFloat", "Bay Width": "NodeSocketFloat", "Depth": "NodeSocketFloat"}
BOUNDS = {"Floors": (1, 20), "Bays": (1, 30), "Floor Height": (2.0, 6.0), "Bay Width": (1.0, 6.0), "Depth": (3.0, 30.0)}
A = {"Floors": 4, "Bays": 5, "Floor Height": 3.0, "Bay Width": 2.5, "Depth": 8.0}
B = {"Floors": 7, "Bays": 3, "Floor Height": 3.4, "Bay Width": 3.2, "Depth": 10.0}


def measure(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    ev.to_mesh_clear()
    wins = np.array([tuple(i.matrix_world.translation) for i in dg.object_instances if i.is_instance and i.parent is not None and i.parent.original == ob]).reshape(-1, 3)
    return co, wins


def check(r, tag, par, co, wins):
    F, Bb, fh, bw, d = par["Floors"], par["Bays"], par["Floor Height"], par["Bay Width"], par["Depth"]
    r.check(len(wins) == F * Bb, f"{tag} : {len(wins)} fenêtres (Floors × Bays = {F * Bb})", "Grid : Vertices X = Bays, Vertices Y = Floors.", 3)
    ex, ey, ez = (float(np.ptp(co[:, k])) for k in range(3))
    r.check(abs(ex - Bb * bw) <= 0.02 and abs(ey - d) <= 0.02, f"{tag} : corps {ex:.2f} × {ey:.2f} m (attendu {Bb * bw:.2f} × {d:.2f})", "Cube : X = Bays × Bay Width ; Y = Depth.", 3)
    r.check(abs(ez - F * fh) <= 0.02 and abs(float(co[:, 2].min())) <= 0.02, f"{tag} : hauteur {ez:.2f} m (attendu {F * fh:.2f}), posé sur z = {float(co[:, 2].min()):+.2f}", "Cube : Z = Floors × Floor Height ; Transform z = hauteur ÷ 2.", 3)
    if len(wins) == 0:
        r.check(False, f"{tag} : fenêtres sur la façade", "", 3)
        r.check(False, f"{tag} : régularité de la façade", "", 3)
        return
    on_facade = bool((np.abs(wins[:, 1] + d / 2) <= 0.05).all() and (np.abs(wins[:, 0]) <= Bb * bw / 2).all())
    r.check(on_facade, f"{tag} : fenêtres sur la façade avant (y = {-d / 2:.1f} m) et dans la largeur du corps", "Transform de la grille : y = −Depth ÷ 2.", 3)
    ux = np.unique(np.round(wins[:, 0], 3))
    uz = np.unique(np.round(wins[:, 2], 3))
    dx = np.diff(ux)
    dz = np.diff(uz)
    ok = (len(ux) == Bb and len(uz) == F and (len(dx) == 0 or np.abs(dx - bw).max() <= 0.02) and (len(dz) == 0 or np.abs(dz - fh).max() <= 0.02) and abs(float(uz[0]) - 0.55 * fh) <= 0.05)
    r.check(ok, f"{tag} : {len(ux)} colonnes espacées de {float(dx.mean()) if len(dx) else 0:.2f} m (attendu {bw}), {len(uz)} rangées espacées de {float(dz.mean()) if len(dz) else 0:.2f} m (attendu {fh}), première rangée à {float(uz[0]):.2f} m (attendu {0.55 * fh:.2f})", "Size X = (Bays − 1) × Bay Width ; Size Y = (Floors − 1) × Floor Height.", 3)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.08 — Architecture procédurale")
    ob = bpy.data.objects.get("GEO_Building")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Building avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    socks = {i.name: i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name != "Geometry"}
    ok_t = all(n in socks and socks[n].socket_type == t for n, t in EXPECT.items())
    r.check(ok_t, f"Interface : Floors, Bays (Integer), Floor Height, Bay Width, Depth (Float) — trouvées : {sorted(socks)}", "Créer les cinq entrées.", 4)
    if not ok_t:
        return r.finish()
    r.check(all((socks[n].description or "").strip() for n in EXPECT), "Chaque entrée a une description", "", 2)
    bad = [n for n, (lo, hi) in BOUNDS.items() if not (socks[n].min_value >= lo and socks[n].max_value <= hi and socks[n].min_value <= socks[n].default_value <= socks[n].max_value)]
    r.check(not bad, f"Bornes et défauts plausibles ({bad or 'tous OK'})", "", 2)
    r.check(all(abs(socks[n].default_value - v) < 1e-6 for n, v in A.items()), "Valeurs par défaut : 4 étages, 5 travées, 3 m, 2,5 m, 8 m", "", 2)
    for n, v in A.items():
        md.properties.inputs[socks[n].identifier]["value"] = v
    co, wins = measure(ob)
    check(r, "Réglage A", A, co, wins)
    for n, v in B.items():
        md.properties.inputs[socks[n].identifier]["value"] = v
    co, wins = measure(ob)
    check(r, "Réglage B", B, co, wins)
    for n, v in A.items():
        md.properties.inputs[socks[n].identifier]["value"] = v
    if debug:
        print("[DEBUG] B fenêtres", len(wins), "bbox", np.ptp(co, axis=0).round(2))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
