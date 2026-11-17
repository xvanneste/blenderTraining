"""
build_p10_reference.py — Construit la référence du projet P10 : un champ de 200 accessoires (rochers) en Cycles, d'abord ALOURDI (« avant » : 200 maillages, Subdivision Surface niveau 2, texture 4 096², sans limite),
puis OPTIMISÉ (« après » : instances de collection, texture limitée à 1 024, 32 échantillons + OpenImageDenoise + échantillonnage adaptatif), rendu en EXR multicouche 32 bits (renders/p10_master.exr) avec passes
(Depth, Normal, Object Index, Cryptomatte Object) et un light group « sun ; un rapport de temps (renders/p10_report.json : mesures de l'« avant » et de l'« après », temps par image à 160 × 90) ; un aperçu PNG.
Assemble CH10.02 (Cycles), CH10.03 (débruitage), CH10.04 (passes, light group), CH10.05 (instances, textures), CH10.06 (EXR).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p10_reference.py
Testé avec : Blender 5.3.0.
"""
import importlib.util
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

spec = importlib.util.spec_from_file_location("validate_p10", os.path.join(HERE, "validate_p10.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

NOTE = """P10 — UNE SCÈNE OPTIMISÉE, RENDUE EN EXR MULTICOUCHE (Prop_000…Prop_199, Floor, SUN, CAM)
Allégez la scène (instances, texture limitée), réglez Cycles (échantillons, débruitage, adaptatif), rendez renders/p10_master.exr (multicouche, 32 bits, passes Z, Normal, Object Index, Cryptomatte Object, light group sun) et écrivez renders/p10_report.json. Critères : README et SCRIPTS/validate_p10.py."""
N = 200


def rock_mesh(name):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.4)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return me


def build(optimized):
    L.reset("SC_P10")
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
    if optimized:
        src = bpy.data.collections.new("PropSource")
        sc.collection.children.link(src)
        r = bpy.data.objects.new("Prop_src", shared)
        md = r.modifiers.new("Subsurf", "SUBSURF")
        md.levels = md.render_levels = 2
        r.pass_index = 1
        src.objects.link(r)
        sc.view_layers[0].layer_collection.children["PropSource"].exclude = True
    for i in range(N):
        x, y = (i % 20) * 1.2 - 11.4, (i // 20) * 1.2 + 1.0
        if optimized:
            e = bpy.data.objects.new(f"Prop_{i:03d}", None)
            e.instance_type, e.instance_collection = "COLLECTION", src
        else:
            me = rock_mesh(f"ME_Rock_{i:03d}")
            me.materials.append(mat)
            e = bpy.data.objects.new(f"Prop_{i:03d}", me)
            md = e.modifiers.new("Subsurf", "SUBSURF")
            md.levels = md.render_levels = 2
            e.pass_index = 1
        e.location = (x, y, 0.4)
        sc.collection.objects.link(e)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=16)
    mf = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(mf)
    bm.free()
    fl = bpy.data.objects.new("Floor", mf)
    fl.location = (0, 4, 0)
    fl.pass_index = 2
    sc.collection.objects.link(fl)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 3
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (0.8, 0.2, 0.6)
    wo = bpy.data.worlds.new("WO_Sky")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.5, 0.6, 0.8, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -12, 6)
    cam.rotation_euler = (math.radians(68), 0, 0)
    sc.camera = cam
    cy = sc.cycles
    sc.render.engine = "CYCLES"
    cy.device = "CPU"
    cy.seed = 0
    cy.samples = 32
    cy.use_denoising = True
    cy.denoiser = "OPENIMAGEDENOISE"
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.02
    sc.render.use_simplify = optimized
    cy.texture_limit_render = "1024" if optimized else "OFF"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    vl = sc.view_layers[0]
    vl.use_pass_z = vl.use_pass_normal = vl.use_pass_object_index = vl.use_pass_cryptomatte_object = True
    vl.lightgroups.add(name="sun")
    lo.lightgroup = "sun"
    L.instructions(NOTE)


def time_frame():
    sc = bpy.context.scene
    ims = sc.render.image_settings
    keep = (ims.media_type, ims.file_format)
    ims.media_type, ims.file_format = "IMAGE", "PNG"
    sc.render.filepath = os.path.join(os.environ.get("TEMP", "."), "bcma_p10_time.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t
    ims.media_type, ims.file_format = keep
    return dt


def main():
    ref = os.path.join(HERE, "REFERENCE")
    os.makedirs(os.path.join(ref, "renders"), exist_ok=True)
    build(False)
    time_frame()  # chauffe
    bm = V.scene_metrics()
    tb = time_frame()
    before = {"triangles": bm["triangles"], "meshes": bm["meshes"], "texture_mb": round(bm["texture_mb"], 2), "seconds_per_frame": round(tb, 2)}
    print("[p10] before", before)
    build(True)
    time_frame()
    am = V.scene_metrics()
    ta = time_frame()
    after = {"triangles": am["triangles"], "meshes": am["meshes"], "texture_mb": round(am["texture_mb"], 2), "seconds_per_frame": round(ta, 2)}
    print("[p10] after", after, "EQM", round(V.quality(bpy.context.scene), 4))
    sc = bpy.context.scene
    ims = sc.render.image_settings
    ims.media_type = "MULTI_LAYER_IMAGE"
    ims.color_depth, ims.exr_codec = "32", "ZIP"
    sc.render.filepath = os.path.join(ref, "renders", "p10_master.exr")
    bpy.ops.render.render(write_still=True)
    ims.media_type, ims.file_format = "IMAGE", "PNG"
    sc.render.resolution_x, sc.render.resolution_y = 640, 360
    sc.render.filepath = os.path.join(ref, "renders", "p10_preview.png")
    bpy.ops.render.render(write_still=True)
    sc.render.resolution_x, sc.render.resolution_y = 160, 90
    ims.media_type = "MULTI_LAYER_IMAGE"
    ims.color_depth, ims.exr_codec = "32", "ZIP"
    notes = [
        "Le départ évalue 384 000 triangles (200 maillages de 1 920 triangles) : le poids vient de la Subdivision Surface appliquée à chaque objet.",
        "Les instances de collection évaluent la source une seule fois : 1 920 triangles et un seul maillage pour 200 accessoires.",
        "La texture de 4 096 pixels pèse 64 Mo ; la limite de texture de Simplify à 1 024 la ramène à 4 Mo effectifs.",
        "Avec 32 échantillons et OpenImageDenoise, l'image reste proche d'une référence de 256 échantillons (EQM mesurée par le correcteur).",
        "Les temps par image sont mesurés à 160 × 90 sur la machine de développement : ils changent avec la machine et ne se comparent qu'entre eux.",
        "Le rendu final en EXR multicouche conserve les passes pour le compositing : profondeur, normales, index d'objet, Cryptomatte et light group sun.",
    ]
    json.dump({"before": before, "after": after, "notes": notes}, open(os.path.join(ref, "renders", "p10_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    L.save(os.path.join(ref, "p10_scene_reference.blend"))


if __name__ == "__main__":
    L.run(main)
