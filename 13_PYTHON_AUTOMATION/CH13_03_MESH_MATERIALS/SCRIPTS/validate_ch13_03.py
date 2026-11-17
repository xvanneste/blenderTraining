"""Contrôle la géométrie évaluée et le graphe de matériaux de la scène livrée."""
import sys
from pathlib import Path

import bmesh
import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "SCRIPTS"))
import bcma_lib as L


def est_volume(mesh):
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        return len(bm.faces) == 6 and all(edge.is_manifold for edge in bm.edges) and bm.calc_volume(signed=True) > 0
    finally:
        bm.free()


def entree_liee(node, input_name, node_type, output_name):
    links = node.inputs[input_name].links
    if len(links) == 1 and links[0].from_node.type == node_type and links[0].from_socket.identifier == output_name:
        return links[0].from_node
    return None


def graphe_valide(mat):
    if not mat or not mat.node_tree:
        return False
    output = next((node for node in mat.node_tree.nodes
                   if node.type == "OUTPUT_MATERIAL" and node.is_active_output), None)
    shader = output and entree_liee(output, "Surface", "BSDF_PRINCIPLED", "BSDF")
    plage = shader and entree_liee(shader, "Roughness", "MAP_RANGE", "Result")
    bruit = plage and entree_liee(plage, "Value", "TEX_NOISE", "Fac")
    return bool(bruit and plage.inputs["To Min"].default_value < plage.inputs["To Max"].default_value)


def main():
    report = L.Report("CH13.03 — Présentoir généré")
    scene = bpy.context.scene
    collection = scene.collection.children.get("COL_Presentoir")
    report.check(collection and len(collection.objects) == 6, "Six objets dans COL_Presentoir",
                 "Liez chaque objet à la collection, puis comptez les deux rangées de trois.", points=2)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for row in range(2):
        for col in range(3):
            name = f"GEO_Bloc_{row + 1}_{col + 1}"
            obj = collection and collection.objects.get(name)
            mesh = obj.data if obj and obj.type == "MESH" else None
            expected = ((col - 1) * 1.12, row * 1.12, 0)
            report.check(mesh and max(abs(a - b) for a, b in zip(obj.location, expected)) < 0.01,
                         f"{name} à sa position", "Vérifiez l’origine de grille et l’espacement de 1,12 m.")
            height = 0.36 + 0.18 * (row + col)
            report.check(mesh and len(mesh.vertices) == 8 and est_volume(mesh)
                         and all(abs(a - b) < 0.01 for a, b in zip(obj.dimensions, (.88, .88, height))),
                         f"{name} fermé, orienté et à la bonne taille", "Contrôlez les faces, les normales et la hauteur.")
            bevel = next((mod for mod in obj.modifiers if mod.type == "BEVEL"), None) if mesh else None
            report.check(bevel and abs(bevel.width - .045) < .001 and bevel.segments == 3
                         and len(obj.evaluated_get(depsgraph).data.polygons) > len(mesh.polygons),
                         f"{name} biseauté", "Vérifiez le modificateur actif dans le viewport et ses trois segments.")
            material = mesh.materials[0] if mesh and mesh.materials else None
            expected_mat = "MAT_Ceramique_Ocre" if (row, col) == (1, 2) else "MAT_Ceramique_Bleue"
            report.check(material and material.name == expected_mat, f"{name} reçoit {expected_mat}")

    for name in ("MAT_Ceramique_Bleue", "MAT_Ceramique_Ocre"):
        report.check(graphe_valide(bpy.data.materials.get(name)), f"{name} · graphe actif",
                     "Reliez Fac → Value puis Result → Roughness du Principled qui alimente la sortie.", points=2)
    return report.finish()


if __name__ == "__main__":
    L.run(main)
