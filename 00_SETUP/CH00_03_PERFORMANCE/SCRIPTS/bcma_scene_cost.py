"""
bcma_scene_cost.py — Estime le « coût » d'une scène (CH00.03, réutilisé dans tout le cursus).

Pour chaque objet maillage : faces de base, niveaux de Subdivision viewport/rendu
(en tenant compte de Render > Simplify), faces estimées au rendu, et partage des données.
Affiche un résumé et les 10 objets les plus coûteux.

Usage :
  blender -b <fichier.blend> --python bcma_scene_cost.py
  (dans Blender : Scripting > Run Script ; résultat dans la console système)
Fonction réutilisable : scene_cost(scene) -> dict

Note : l'estimation multiplie les faces par 4 à chaque niveau de Subdivision (règle exacte
pour des quads, approchée pour des triangles/n-gons). Les autres modificateurs sont
évalués tels quels en viewport.
Testé avec : Blender 5.3.0.
"""
import bpy


def subsurf_levels(obj, scene):
    lv, lr = 0, 0
    for m in obj.modifiers:
        if m.type in {"SUBSURF", "MULTIRES"}:
            v = m.levels if m.type == "SUBSURF" else m.levels
            r = m.render_levels
            if m.show_viewport:
                lv += v
            if m.show_render:
                lr += r
    if scene.render.use_simplify:
        lv = min(lv, scene.render.simplify_subdivision)
        lr = min(lr, scene.render.simplify_subdivision_render)
    return lv, lr


def scene_cost(scene=None):
    scene = scene or bpy.context.scene
    rows, meshes = [], {}
    for o in scene.objects:
        if o.type != "MESH" or o.hide_render:
            continue
        base = len(o.data.polygons)
        lv, lr = subsurf_levels(o, scene)
        rows.append((o.name, base, lv, lr, base * 4 ** lr, o.data.name))
        meshes.setdefault(o.data.name, 0)
        meshes[o.data.name] += 1
    total = sum(r[4] for r in rows)
    return {"objects": len(rows), "unique_meshes": len(meshes), "render_faces_est": total,
            "rows": sorted(rows, key=lambda r: -r[4]), "simplify": scene.render.use_simplify}


def main():
    c = scene_cost()
    print("\n========== BCMA — COÛT DE LA SCÈNE ==========")
    print(f" Objets maillage rendus   : {c['objects']}")
    print(f" Maillages distincts      : {c['unique_meshes']}")
    print(f" Faces estimées au rendu  : {c['render_faces_est']:,}".replace(",", " "))
    print(f" Simplify                 : {'actif' if c['simplify'] else 'inactif'}")
    print(" Top 10 :")
    for name, base, lv, lr, est, me in c["rows"][:10]:
        print(f"   {name:24s} base {base:6d}  subdiv {lv}/{lr}  → {est:>12,} faces  (mesh {me})".replace(",", " "))
    print("=============================================\n")
    return c


if __name__ == "__main__":
    main()
