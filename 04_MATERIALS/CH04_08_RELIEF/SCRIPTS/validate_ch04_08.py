"""
validate_ch04_08.py — Correcteur « Relief » (CH04.08).
Usage : … --python-exit-code 1 --python validate_ch04_08.py -- --exercise relief [--render] [--debug]
PROP_Ground / MAT_Ground — vrai displacement (Cycles) :
  - moteur de rendu Cycles ;
  - nœud Displacement relié à l'entrée Displacement du Material Output ;
  - Height alimentée par une texture procédurale (nœud de type TEX_*) ;
  - Scale du Displacement entre 0,02 et 0,3 m ; Midlevel entre 0 et 1 ;
  - Material > Settings > Displacement = « Displacement Only » ou « Displacement and Bump » (displacement_method) ;
  - maillage subdivisé : modificateur Subdivision Surface adaptatif OU niveaux de rendu ≥ 6.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def upstream_types(sock, seen=None):
    seen = set() if seen is None else seen
    out = set()
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            out.add(n.type)
            for i in n.inputs:
                out |= upstream_types(i, seen)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH04.08 — Relief")
    ob = bpy.data.objects.get("PROP_Ground")
    mat = ob.active_material if ob and ob.data.materials else None
    if not r.check(mat is not None and mat.node_tree is not None, "PROP_Ground avec le matériau MAT_Ground", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.render.engine == "CYCLES", f"Moteur de rendu : {sc.render.engine} (Cycles exigé pour le vrai displacement)", "Render Properties > Render Engine : Cycles.", 3)
    nt = mat.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    ds_link = [l for l in nt.links if l.to_node == out and l.to_socket.name == "Displacement" and l.from_node.type == "DISPLACEMENT"] if out else []
    r.check(bool(ds_link), "Displacement relié à Material Output [Displacement]", "Displacement [Displacement] -> Material Output [Displacement].", 3)
    ds = ds_link[0].from_node if ds_link else next((n for n in nt.nodes if n.type == "DISPLACEMENT"), None)
    tex = {t for t in upstream_types(ds.inputs["Height"]) if t.startswith("TEX_")} if ds else set()
    r.check(bool(tex), f"Height alimentée par une texture ({sorted(tex) or 'aucune'})", "Noise Texture [Fac] -> Height.", 3)
    sc_v = ds.inputs["Scale"].default_value if ds else 0.0
    mid = ds.inputs["Midlevel"].default_value if ds else -1
    r.check(0.02 <= sc_v <= 0.3, f"Displacement Scale {sc_v:.2f} m (0,02–0,3)", "Un relief de terrain : quelques centimètres à 30 cm.", 2)
    r.check(0.0 <= mid <= 1.0, f"Midlevel {mid:.2f} (0–1)", "", 1)
    r.check(mat.displacement_method in ("DISPLACEMENT", "BOTH"), f"Material > Settings > Displacement : {mat.displacement_method} (Displacement Only / Displacement and Bump)", "Par défaut le mode « Bump Only » ne déplace pas la géométrie.", 3)
    sub = next((m for m in ob.modifiers if m.type == "SUBSURF"), None)
    ok_sub = sub is not None and (sub.use_adaptive_subdivision or sub.render_levels >= 6)
    r.check(ok_sub, f"Maillage subdivisé : {'adaptatif' if sub and sub.use_adaptive_subdivision else ('niveaux de rendu ' + str(sub.render_levels)) if sub else 'aucun modificateur'}", "Un plan d'une face ne peut pas se déformer : Subdivision Surface (Adaptive Subdivision ou Render ≥ 6).", 3)
    if debug:
        print("[DEBUG] engine", sc.render.engine, "scale", sc_v, "mid", mid, "method", mat.displacement_method, "tex", sorted(tex), "sub", None if sub is None else (sub.use_adaptive_subdivision, sub.render_levels))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
