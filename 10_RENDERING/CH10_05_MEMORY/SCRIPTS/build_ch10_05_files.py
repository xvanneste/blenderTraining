"""
build_ch10_05_files.py — « Mémoire et optimisation » (CH10.05 : instances, maillages partagés, niveaux de subdivision, limite de texture).

Scène (200 rochers + une texture lourde) : Rock_000 … Rock_199 posés sur une grille de 20 × 10 (pas de 1,2 m) ; chaque rocher est une icosphère de 0,4 m (subdivisions 2 : 80 triangles) avec un modificateur Subdivision Surface (niveau de rendu 2 : 1 920 triangles évalués) ;
  matériau MA_Rock avec un nœud Image Texture « rock_albedo » généré de 4 096 × 4 096 pixels (64 Mo en mémoire, 8 bits RGBA) ; Floor (plan), SUN, CAM.
  Départ : 200 objets, 200 maillages DIFFÉRENTS (un par rocher), Subdivision Surface au niveau 2, texture de 4 096 pixels sans limite (Simplify désactivé) : 384 000 triangles évalués, 200 maillages, 64 Mo de textures.
  Consigne : rendre la scène légère SANS perdre de rochers (au moins 200 rochers dans le rendu) :
    (1) au plus 5 maillages de rochers différents (partager le maillage : Object > Link/Transfer Data > Link Object Data, ou une instance de collection) ;
    (2) au plus 100 000 triangles évalués (instances de collection : un seul rocher évalué ; ou niveau de Subdivision Surface réduit) ;
    (3) textures : au plus 16 Mo effectifs (Render Properties > Simplify > Render > Texture Limit 1024, ou réduire l'image).
  Solution : un collection source « RockSource » (exclue du calque) contenant un seul rocher (Rock_src) et 200 empties Rock_000…Rock_199 qui l'instancient ; Simplify activé avec Texture Limit 1024 : 1 920 triangles évalués, 1 maillage, 4 Mo de textures effectifs.
  Variante acceptée (non fournie comme fichier) : 200 objets partageant UN maillage, modificateur au niveau 0, Texture Limit 1024 : 16 000 triangles, 1 maillage, 4 Mo.
  STARTER_FILES/ch10_05_memory_starter.blend ; COMPLETED_EXAMPLES/ch10_05_memory_solution.blend (+ _reference.png : le champ de rochers de la solution)
  COUNTER_EXAMPLES/ : unique_meshes (200 maillages, niveau 0, texture limitée), high_poly (un maillage partagé mais niveau 2 : 384 000 triangles), big_texture (instances mais texture 4 096 sans limite), few_rocks (50 rochers seulement)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_05_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH10.05 — MÉMOIRE ET OPTIMISATION (Rock_000…Rock_199, Floor, SUN, CAM)
200 rochers, chacun avec son propre maillage et sa Subdivision Surface, et une texture de 4 096 × 4 096 pixels. Allégez la scène sans perdre de rochers (au moins 200 dans le rendu).
1. Au plus 5 maillages de rochers différents : Object > Link/Transfer Data > Link Object Data (Ctrl+L), ou une instance de collection.
2. Au plus 100 000 triangles évalués : instances de collection (un seul rocher évalué) ou niveau de Subdivision Surface plus bas.
3. Textures : au plus 16 Mo effectifs : Render Properties > Simplify (case de l'en-tête) > Render > Texture Limit 1024 (ou réduire l'image).
Vérification : SCRIPTS/validate_ch10_05.py -- --exercise memory
"""
N = 200


def rock_mesh(name):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.4)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return me


def build(kind):
    L.reset("SC_MEMORY")
    sc = bpy.context.scene
    mat = bpy.data.materials.new("MA_Rock")
    nt = mat.node_tree
    img = bpy.data.images.new("rock_albedo", 4096, 4096)
    img.generated_color = (0.55, 0.45, 0.35, 1)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    shared = rock_mesh("ME_Rock")
    shared.materials.append(mat)
    level = {"starter": 2, "unique_meshes": 0, "high_poly": 2}.get(kind, 2)
    instances = kind in ("solution", "big_texture", "few_rocks")
    n = 50 if kind == "few_rocks" else N
    if instances:
        src = bpy.data.collections.new("RockSource")
        sc.collection.children.link(src)
        r = bpy.data.objects.new("Rock_src", shared)
        md = r.modifiers.new("Subsurf", "SUBSURF")
        md.levels = md.render_levels = 2
        src.objects.link(r)
        sc.view_layers[0].layer_collection.children["RockSource"].exclude = True
    for i in range(n):
        x, y = (i % 20) * 1.2 - 11.4, (i // 20) * 1.2 + 1.0
        if instances:
            e = bpy.data.objects.new(f"Rock_{i:03d}", None)
            e.instance_type, e.instance_collection = "COLLECTION", src
            e.location = (x, y, 0.4)
        else:
            me = rock_mesh(f"ME_Rock_{i:03d}") if kind in ("starter", "unique_meshes") else shared
            if me is not shared:
                me.materials.append(mat)
            e = bpy.data.objects.new(f"Rock_{i:03d}", me)
            e.location = (x, y, 0.4)
            md = e.modifiers.new("Subsurf", "SUBSURF")
            md.levels = md.render_levels = level
        sc.collection.objects.link(e)
    if kind != "starter" and not instances:
        pass
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=16)
    mf = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(mf)
    bm.free()
    fl = bpy.data.objects.new("Floor", mf)
    fl.location = (0, 4, 0)
    sc.collection.objects.link(fl)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 3
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (0.8, 0.2, 0.6)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -12, 6)
    cam.rotation_euler = (math.radians(68), 0, 0)
    sc.camera = cam
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    limited = kind in ("solution", "unique_meshes", "high_poly", "few_rocks")
    sc.render.use_simplify = limited
    sc.cycles.texture_limit_render = "1024" if limited else "OFF"
    sc.frame_set(1)
    L.instructions(NOTE)


def metrics():
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
    mb = 0.0
    used = {n.image for ma in bpy.data.materials if ma.node_tree for n in ma.node_tree.nodes if n.bl_idname == "ShaderNodeTexImage" and n.image}
    lim = int(sc.cycles.texture_limit_render) if sc.render.use_simplify and sc.cycles.texture_limit_render != "OFF" else 0
    for im in used:
        w, h = im.size
        if lim:
            w, h = min(w, lim), min(h, lim)
        mb += w * h * (16 if im.is_float else 4) / 1048576.0
    return {"rocks": count, "meshes": len(meshes), "tris": sum(seen.values()), "texture_mb": mb}


def calibrate():
    for kind in ("starter", "solution", "unique_meshes", "high_poly", "big_texture", "few_rocks"):
        build(kind)
        print("[mem]", kind, {k: round(v, 2) for k, v in metrics().items()})


def sketch(path):
    build("solution")
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 640, 360
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1005.png")
    sc.render.filepath = p
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    bpy.data.images.load(p).save_render(path) if False else None
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(360, 640, 4)
    out = bpy.data.images.new("sk", 640, 360)
    out.pixels = px.ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_05_memory_starter.blend"))
    for k in ("unique_meshes", "high_poly", "big_texture", "few_rocks"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_05_memory_{k}.blend"))
    sketch(os.path.join(out, "ch10_05_memory_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_05_memory_solution.blend"))


if __name__ == "__main__":
    L.run(main)
