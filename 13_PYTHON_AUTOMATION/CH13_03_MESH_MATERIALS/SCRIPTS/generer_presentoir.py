"""Exemple CH13.03. Dans Blender, ouvrir ce texte dans Scripting et lancer Run Script."""
import bmesh
import bpy


def creer_bloc(collection, nom, x, y, hauteur):
    demi = 0.44
    sommets = [(-demi, -demi, 0), (demi, -demi, 0), (demi, demi, 0), (-demi, demi, 0)]
    sommets += [(vx, vy, hauteur) for vx, vy, _ in sommets]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = bpy.data.meshes.new(nom)
    mesh.from_pydata(sommets, [], faces)
    mesh.update()

    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
    finally:
        bm.free()
    mesh.update()

    bloc = bpy.data.objects.new(nom, mesh)
    collection.objects.link(bloc)
    bloc.location = (x, y, 0)

    bevel = bloc.modifiers.new("Reflets sur les arêtes", "BEVEL")
    bevel.width = 0.045
    bevel.segments = 3
    return bloc


def creer_materiau(nom, rgb):
    mat = bpy.data.materials.new(nom)
    mat.diffuse_color = (*rgb, 1)
    arbre = mat.node_tree
    shader = next(node for node in arbre.nodes if node.type == "BSDF_PRINCIPLED")
    shader.inputs["Base Color"].default_value = mat.diffuse_color

    bruit = arbre.nodes.new("ShaderNodeTexNoise")
    bruit.location = (-650, 20)
    bruit.inputs["Scale"].default_value = 5.0

    plage = arbre.nodes.new("ShaderNodeMapRange")
    plage.location = (-340, 20)
    plage.inputs["To Min"].default_value = 0.25
    plage.inputs["To Max"].default_value = 0.65
    arbre.links.new(bruit.outputs["Fac"], plage.inputs["Value"])
    arbre.links.new(plage.outputs["Result"], shader.inputs["Roughness"])
    return mat


def generer():
    nom = "COL_Presentoir"
    if bpy.data.collections.get(nom):
        raise RuntimeError("COL_Presentoir existe déjà. Reprenez depuis une copie du starter.")

    collection = bpy.data.collections.new(nom)
    bpy.context.scene.collection.children.link(collection)
    bleu = creer_materiau("MAT_Ceramique_Bleue", (0.025, 0.25, 0.44))
    ocre = creer_materiau("MAT_Ceramique_Ocre", (0.78, 0.24, 0.05))
    hauteurs = ((0.36, 0.54, 0.72), (0.54, 0.72, 0.90))
    for rang, ligne in enumerate(hauteurs):
        for colonne, hauteur in enumerate(ligne):
            nom_bloc = f"GEO_Bloc_{rang + 1}_{colonne + 1}"
            bloc = creer_bloc(collection, nom_bloc, (colonne - 1) * 1.12, rang * 1.12, hauteur)
            bloc.data.materials.append(ocre if (rang, colonne) == (1, 2) else bleu)


generer()
