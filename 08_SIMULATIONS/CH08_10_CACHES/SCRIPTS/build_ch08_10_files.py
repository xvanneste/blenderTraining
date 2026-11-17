"""
build_ch08_10_files.py — « Caches et baking » (CH08.10 : cuire une simulation de particules sur disque, la relire dans n'importe quel ordre).

Scène : EMITTER (grille de 0,5 m à z = 0,3 m, 100 particules émises de l'image 1 à 20, durée de vie 80, Normal 2, gravité normale, pas de rendu), images 1–60.
  Solution : cache du système de particules cuit (Bake) de l'image 1 à 60, sur DISQUE (Disk Cache) : le dossier `blendcache_<nom du .blend>` voisin du fichier contient 60 fichiers .bphys ;
             on peut alors sauter d'une image à l'autre (image 60 puis 40) et retrouver exactement les mêmes positions (écart 0, mesuré), alors qu'une simulation non cuite ne le garantit pas.
  Le fichier doit être ENREGISTRÉ avant de cuire (sinon pas de dossier de cache) et son cache est lié à son NOM : renommer le .blend sans copier le dossier perd le cache.
  STARTER_FILES/ch08_10_caches_starter.blend : l'émetteur, rien de cuit. COMPLETED_EXAMPLES/ch08_10_caches_solution.blend + son dossier blendcache_ch08_10_caches_solution
  (+ _reference.png : hauteur moyenne des particules par image : simulation lue dans l'ordre (orange) et relue en sens inverse depuis le cache (bleu) : superposées)
  COUNTER_EXAMPLES/ : no_bake, short_range (scène 1–30 pendant la cuisson : 31 fichiers), memory_only, outdated (Number changé à 150 après la cuisson : is_outdated reste FAUX, mais le cache est ignoré : 150 particules ; chacun avec son dossier de cache s'il y en a un)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch08_10_files.py
Testé avec : Blender 5.3.0.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH08.10 — CACHES ET BAKING (EMITTER)
Cuire la simulation de particules de EMITTER (100 particules, images 1–60) sur disque, puis la relire en sautant d'une image à l'autre.
1. Enregistrez d'abord le fichier (File > Save As) : le cache se range dans un dossier « blendcache_<nom du fichier> » voisin.
2. Images 1–60 dans la scène ; EMITTER > Physics > Particles > Cache : Disk Cache coché ; bouton Bake (la plage cuite d'un système de particules suit la plage de la scène : la plage du cache n'est pas réglable).
3. Ne changez plus aucun réglage de l'émetteur après la cuisson (le cache ne correspondrait plus à la simulation).
Contrôles : cache cuit sur disque ; dossier blendcache avec 60 fichiers .bphys ou plus ; 100 particules vivantes à l'image 40 ; positions identiques en sautant 60 → 40 → 60 → 40.
Vérification : SCRIPTS/validate_ch08_10.py -- --exercise caches
"""


def emitter():
    sc = bpy.context.scene
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=0.25)
    me = bpy.data.meshes.new("ME_EMITTER")
    bm.to_mesh(me)
    bm.free()
    em = bpy.data.objects.new("EMITTER", me)
    sc.collection.objects.link(em)
    em.location = (0, 0, 0.3)
    em.modifiers.new("Particles", "PARTICLE_SYSTEM")
    st = em.particle_systems[0].settings
    st.count = 100
    st.frame_start, st.frame_end = 1, 20
    st.lifetime = 80
    st.emit_from = "FACE"
    st.normal_factor = 2.0
    st.physics_type = "NEWTON"
    st.render_type = "NONE"
    return em


def bake(em, disk, last):
    pc = em.particle_systems[0].point_cache
    pc.use_disk_cache = disk
    sc = bpy.context.scene
    sc.frame_end = last  # la plage cuite d'un système de particules suit la plage de la scène (la plage du cache n'est pas réglable)
    bpy.context.view_layer.objects.active = em
    with bpy.context.temp_override(point_cache=pc):
        bpy.ops.ptcache.bake(bake=True)
    sc.frame_end = 60


def build(kind, path=None):
    """Construit la scène ; si le type exige une cuisson, enregistre d'abord le fichier à `path`."""
    L.reset("SC_CACHES")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 60
    em = emitter()
    if kind in ("solution", "short_range", "memory_only", "outdated"):
        old = os.path.join(os.path.dirname(path), "blendcache_" + os.path.splitext(os.path.basename(path))[0])
        if os.path.isdir(old):
            shutil.rmtree(old)  # cache d'une régénération précédente : repartir de zéro
        L.save(path)
        bake(em, kind != "memory_only", 30 if kind == "short_range" else 60)
        if kind == "outdated":
            em.particle_systems[0].settings.count = 150
    sc.frame_set(1)
    L.instructions(NOTE)
    return em


def mean_z(em):
    ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
    P = np.array([p.location[2] for p in ev.particle_systems[0].particles if p.alive_state == "ALIVE"])
    return float(P.mean()) if len(P) else 0.0


def sketch(path, out_blend):
    em = build("no_bake")
    seq = []
    sc = bpy.context.scene
    for f in range(1, 61):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        seq.append(mean_z(em))
    em = build("solution", out_blend)
    rev = {}
    sc = bpy.context.scene
    for f in range(60, 0, -1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        rev[f] = mean_z(em)
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    zmax = max(max(seq), 0.01)
    img[270, 20:W - 20] = (0.3, 0.3, 0.3)
    for f in range(1, 61):
        x = int(30 + (f - 1) / 59 * 720)
        y = int(270 - seq[f - 1] / zmax * 230)
        y2 = int(270 - rev[f] / zmax * 230)
        img[max(y - 4, 0):y + 5, x - 4:x + 5] = (0.95, 0.6, 0.25)
        img[max(y2 - 2, 0):y2 + 3, x - 2:x + 3] = (0.3, 0.7, 1.0)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print("[cache] écart max lecture inverse / lecture directe :", max(abs(rev[f] - seq[f - 1]) for f in range(1, 61)))


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch08_10_caches_starter.blend"))
    for k in ("no_bake", "short_range", "memory_only", "outdated"):
        p = os.path.join(out, "COUNTER_EXAMPLES", f"ch08_10_caches_{k}.blend")
        build(k, p)
        L.save(p)
    sol = os.path.join(out, "ch08_10_caches_solution.blend")
    sketch(os.path.join(out, "ch08_10_caches_reference.png"), sol)
    L.save(sol)


if __name__ == "__main__":
    L.run(main)
