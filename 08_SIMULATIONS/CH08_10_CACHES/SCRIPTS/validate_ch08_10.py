"""
validate_ch08_10.py — Correcteur « Caches et baking » (CH08.10).
Usage : blender -b <fichier.blend> --python-exit-code 1 --python validate_ch08_10.py -- --exercise caches [--debug]
  (le fichier doit être ouvert depuis son emplacement : le cache disque est lu à côté de lui)
Objet : EMITTER (100 particules, images 1–60).
  Configuration : le cache du système de particules est cuit (is_baked), sur disque (use_disk_cache) ; (la plage cuite suit la plage de la scène : pas de réglage séparé ; is_outdated reste faux même après un réglage modifié : mesuré).
  Dossier : `blendcache_<nom du fichier>` voisin du .blend contient au moins 60 fichiers .bphys.
  Relecture : à l'image 40 il y a 100 particules vivantes ; en sautant 60 → 40 → 60 → 40 les positions à l'image 40 sont identiques (écart ≤ 1e-6 m).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def snapshot(em):
    ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return np.array([p.location[:] for p in ev.particle_systems[0].particles if p.alive_state == "ALIVE"])


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.10 — Caches et baking")
    sc = bpy.context.scene
    em = bpy.data.objects.get("EMITTER")
    if not r.check(em is not None and em.particle_systems, "EMITTER et son système de particules présents", "Partez du fichier de départ.", 2):
        return r.finish()
    pc = em.particle_systems[0].point_cache
    r.check(pc.is_baked, f"Cache cuit : {'oui' if pc.is_baked else 'non'} ({pc.info or '–'})", "Physics > Particles > Cache > Bake.", 7)
    r.check(pc.use_disk_cache, f"Cache sur disque : {'oui' if pc.use_disk_cache else 'non'}", "Cocher Disk Cache avant de cuire.", 5)
    folder = os.path.join(os.path.dirname(bpy.data.filepath), "blendcache_" + os.path.splitext(os.path.basename(bpy.data.filepath))[0]) if bpy.data.filepath else ""
    nfiles = len([f for f in os.listdir(folder) if f.endswith(".bphys")]) if folder and os.path.isdir(folder) else 0
    r.check(nfiles >= 60, f"Fichiers .bphys dans le dossier blendcache voisin : {nfiles} (≥ 60)", "Enregistrer le fichier AVANT de cuire ; ne pas renommer le .blend sans copier le dossier.", 6)
    sc.frame_set(60)
    sc.frame_set(40)
    a = snapshot(em)
    sc.frame_set(60)
    sc.frame_set(40)
    b = snapshot(em)
    sc.frame_set(1)
    same = len(a) == len(b) and len(a) > 0 and float(np.abs(a - b).max()) <= 1e-6
    r.check(len(a) == 100, f"Particules vivantes à l'image 40 : {len(a)} (100)", "100 particules : ne changez plus Number après le Bake.", 6)
    r.check(same, f"Relecture en sautant 60 → 40 → 60 → 40 identique : {'oui' if same else 'non'}", "Un cache cuit se relit dans n'importe quel ordre.", 7)
    if debug:
        print("[DEBUG] baked", pc.is_baked, "disk", pc.use_disk_cache, "range", pc.frame_start, pc.frame_end, "outdated", pc.is_outdated, "files", nfiles, "n", len(a), "same", same)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
