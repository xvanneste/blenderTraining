"""
validate_ch10_05.py — Correcteur « Mémoire et optimisation » (CH10.05).
Usage : … --python-exit-code 1 --python validate_ch10_05.py -- --exercise memory [--debug]
Objets : Rock_* (objets de nom commençant par « Rock » : rochers ou empties d'instance de collection), Floor, SUN, CAM. Le correcteur évalue le graphe de dépendances et mesure :
  rochers dans le rendu : nombre d'instances d'objets maillage dont le nom commence par « Rock » (instances de collection comprises) ≥ 200 ;
  maillages : nombre de datablocks Mesh différents utilisés par ces objets ≤ 5 (départ : 200) ;
  triangles évalués : somme sur les objets distincts (modificateurs appliqués ; une instance de collection n'évalue la source qu'une fois) ≤ 100 000 (départ : 384 000) ;
  textures : images référencées par un nœud Image Texture d'un matériau, taille effective (limite de texture de Simplify prise en compte : use_simplify et texture_limit_render) en Mo, 8 bits = 4 octets/pixel, flottant = 16 ≤ 16 Mo (départ : 64 Mo).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.05 — Mémoire et optimisation")
    if not r.check(all(bpy.data.objects.get(n) for n in ("Floor", "SUN", "CAM")), "Floor, SUN et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    seen, count, meshes = {}, 0, set()
    for inst in dg.object_instances:
        o = inst.object
        if o.type != "MESH" or not o.name.startswith("Rock"):
            continue
        count += 1
        meshes.add(o.original.data.name)
        key = o.original.name
        if key not in seen:
            m = o.to_mesh()
            m.calc_loop_triangles()
            seen[key] = len(m.loop_triangles)
            o.to_mesh_clear()
    tris = sum(seen.values())
    mb = 0.0
    used = {n.image for ma in bpy.data.materials if ma.node_tree for n in ma.node_tree.nodes if n.bl_idname == "ShaderNodeTexImage" and n.image}
    lim = int(sc.cycles.texture_limit_render) if sc.render.use_simplify and sc.cycles.texture_limit_render != "OFF" else 0
    for im in used:
        w, h = im.size
        if lim:
            w, h = min(w, lim), min(h, lim)
        mb += w * h * (16 if im.is_float else 4) / 1048576.0
    r.check(count >= 200, f"Rochers dans le rendu : {count} (≥ 200)", "Ne supprimez pas de rochers : partagez ou instanciez-les.", 8)
    r.check(len(meshes) <= 5, f"Maillages de rochers différents : {len(meshes)} (≤ 5)", "Object > Link/Transfer Data > Link Object Data, ou instance de collection.", 8)
    r.check(tris <= 100000, f"Triangles évalués : {tris} (≤ 100 000)", "Instances de collection ou niveau de Subdivision Surface plus bas.", 8)
    r.check(mb <= 16.0, f"Textures : {mb:.1f} Mo effectifs (≤ 16) ; Simplify {'activé' if sc.render.use_simplify else 'désactivé'}, limite {sc.cycles.texture_limit_render}", "Render Properties > Simplify > Render > Texture Limit 1024, ou réduire l'image.", 8)
    if debug:
        print("[DEBUG] rocks", count, "meshes", len(meshes), "tris", tris, "texture_mb", round(mb, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
