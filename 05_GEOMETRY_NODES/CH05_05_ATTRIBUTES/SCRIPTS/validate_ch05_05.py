"""
validate_ch05_05.py — Correcteur « Attributs » (CH05.05).
Usage : … --python-exit-code 1 --python validate_ch05_05.py -- --exercise attributes [--render] [--debug]
GEO_Terrain / arbre GN_Terrain / matériau MAT_Height :
  Arbre   : un Store Named Attribute (Float, Point) nommé « height », Value alimentée par un champ ; Set Material ; Group Output alimenté ; aucun nœud orphelin.
  Évalué  : l'attribut « height » existe sur les POINTS de la géométrie évaluée (type flottant) ; écart-type ≥ 0,05 ; il vaut la coordonnée z des sommets (écart moyen ≤ 1 mm) ;
            10 000 sommets (≥ 2 500).
  Shader  : MAT_Height : Base Color alimentée par un nœud Attribute (type Geometry) dont le nom est « height » (le même que celui de l'arbre), via une Color Ramp.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def upstream(sock, seen=None):
    seen = set() if seen is None else seen
    out = []
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            out.append(n)
            for i in n.inputs:
                out += upstream(i, seen)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.05 — Attributs")
    ob = bpy.data.objects.get("GEO_Terrain")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Terrain avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    N = md.node_group.nodes
    st = next((n for n in N if n.bl_idname == "GeometryNodeStoreNamedAttribute"), None)
    name = st.inputs["Name"].default_value if st else ""
    r.check(st is not None, "Store Named Attribute présent", "Après Set Position.", 3)
    r.check(st is not None and st.data_type == "FLOAT" and st.domain == "POINT", f"Type et domaine : {st.data_type if st else '-'} / {st.domain if st else '-'} (FLOAT / POINT)", "Data Type Float, Domain Point.", 3)
    val = next((i for i in st.inputs if i.name == "Value" and i.enabled), None) if st else None
    r.check(val is not None and val.is_linked, "Value alimentée par un champ", "Position → Separate XYZ [Z] → Value.", 3)
    r.check(name == "height", f"Nom de l'attribut : « {name} » (« height » exigé)", "Le shader cherche « height ».", 3)
    r.check(any(n.bl_idname == "GeometryNodeSetMaterial" for n in N), "Set Material présent", "", 1)
    out = next((n for n in N if n.bl_idname == "NodeGroupOutput"), None)
    r.check(out is not None and out.inputs[0].is_linked, "Group Output alimenté", "", 2)
    orph = [n.name for n in N if n.bl_idname != "NodeGroupOutput" and n.type != "FRAME" and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "", 2)
    # évalué
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    at = me.attributes.get("height")
    nv = len(me.vertices)
    ok_attr = at is not None and at.domain == "POINT" and at.data_type == "FLOAT"
    std, dz = 0.0, 9.0
    if ok_attr:
        h = np.empty(nv, np.float32)
        at.data.foreach_get("value", h)
        co = np.empty(nv * 3, np.float32)
        me.vertices.foreach_get("co", co)
        z = co.reshape(-1, 3)[:, 2]
        std = float(h.std())
        dz = float(np.abs(h - z).mean())
    ev.to_mesh_clear()
    r.check(ok_attr, f"Attribut « height » sur les points de la géométrie évaluée ({'présent' if at else 'absent'}{'' if at is None else ', ' + at.domain + ' / ' + at.data_type})", "Store Named Attribute : nom, Point, Float.", 4)
    r.check(nv >= 2500, f"{nv} sommets (≥ 2 500)", "Grid 100 × 100.", 2)
    r.check(std >= 0.05, f"L'attribut varie : écart-type {std:.3f} (≥ 0,05)", "Value = Position Z, pas une constante.", 3)
    r.check(ok_attr and dz <= 0.001, f"L'attribut vaut z (écart moyen {dz * 1000:.2f} mm ≤ 1 mm)", "Stocker la hauteur APRÈS Set Position.", 2)
    # shader
    mat = bpy.data.materials.get("MAT_Height")
    ok_sh, sh_name = False, ""
    if mat and mat.node_tree:
        b = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        ups = upstream(b.inputs["Base Color"]) if b else []
        att = [n for n in ups if n.type == "ATTRIBUTE" and n.attribute_type == "GEOMETRY"]
        sh_name = att[0].attribute_name if att else ""
        ok_sh = bool(att) and any(n.type == "VALTORGB" for n in ups)
    r.check(ok_sh, f"MAT_Height : Attribute (Geometry) → … → Color Ramp → Base Color (nom lu : « {sh_name} »)", "Attribute, Map Range, Color Ramp.", 4)
    r.check(ok_sh and sh_name == name, "Le nom lu par le shader est celui stocké par l'arbre", "« height » des deux côtés.", 3)
    if debug:
        print("[DEBUG] name", name, "attr", None if at is None else (at.domain, at.data_type), "std", round(std, 3), "dz", round(dz, 5), "shader", sh_name, "nv", nv)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
