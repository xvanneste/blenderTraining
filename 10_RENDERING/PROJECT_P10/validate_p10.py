"""
validate_p10.py — Correcteur du projet P10 « Une scène optimisée, rendue en EXR multicouche, avec rapport de temps ».
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p10.py [-- --debug]
Le fichier contient une scène de 200 accessoires (Prop_000…Prop_199 : rochers ou instances de collection), Floor, SUN (lampe, light group « sun »), CAM. Le correcteur contrôle :
  1. Géométrie : au moins 200 accessoires dans le rendu ; au plus 5 maillages différents ; au plus 150 000 triangles évalués (objets sources comptés une fois) ; textures de matériaux : au plus 16 Mo effectifs (limite de texture de Simplify prise en compte).
  2. Cycles : moteur Cycles, échantillons de 4 à 64, débruitage activé, échantillonnage adaptatif activé (seuil ≤ 0,05).
  3. Qualité mesurée : rendu de 160 × 90 avec les réglages de l'élève (graine 0) comparé à une référence de 256 échantillons sans débruitage : EQM de la luminance ≤ 0,025 (référence 0,011 ; 4 échantillons bruts 0,040).
  4. EXR renders/p10_master.exr (dossier du .blend) : multicouche ; canaux Combined (32 bits flottants), Depth.Z, Normal.X, Object Index.X, CryptoObject00.r, Combined_sun.R ; aucun codec à perte (B44, B44A, DWAA, DWAB) dans les en-têtes.
  5. Rapport renders/p10_report.json : « before » et « after » avec triangles, meshes, texture_mb, seconds_per_frame ; « after » cohérent avec la scène (triangles et Mo à 5 % près, maillages exacts) ;
     gain déclaré : after.seconds_per_frame ≤ 0,8 × before.seconds_per_frame (valeurs saisies par l'élève : non vérifiables, seule la cohérence est contrôlée) ; « notes » : au moins 5 phrases de plus de 20 caractères.
Testé avec : Blender 5.3.0.
"""
import json
import os
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

LOSSY = {6, 7, 8, 9}  # B44, B44A, DWAA, DWAB


def exr_info(path):
    d = open(path, "rb").read()
    types, comps, pos = {}, set(), 0
    while True:
        i = d.find(b"channels\x00chlist\x00", pos)
        if i < 0:
            break
        size = struct.unpack("<i", d[i + 16:i + 20])[0]
        blob, j = d[i + 20:i + 20 + size], 0
        while j < len(blob) and blob[j] != 0:
            k = blob.index(b"\x00", j)
            types[blob[j:k].decode()] = struct.unpack("<i", blob[k + 1:k + 5])[0]
            j = k + 1 + 16
        pos = i + 20 + size
    q = 0
    while True:
        c = d.find(b"compression\x00compression\x00", q)
        if c < 0:
            break
        comps.add(d[c + 30 + 4] if False else d[c + len(b"compression\x00compression\x00") + 4])
        q = c + 30
    return types, comps


def scene_metrics():
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    seen, count, meshes = {}, 0, set()
    for inst in dg.object_instances:
        o = inst.object
        if o.type != "MESH" or not o.name.startswith("Prop"):
            continue
        count += 1
        meshes.add(o.original.data.name)
        if o.original.name not in seen:
            m = o.to_mesh()
            m.calc_loop_triangles()
            seen[o.original.name] = len(m.loop_triangles)
            o.to_mesh_clear()
    mb = 0.0
    used = {n.image for ma in bpy.data.materials if ma.node_tree for n in ma.node_tree.nodes if n.bl_idname == "ShaderNodeTexImage" and n.image}
    lim = int(sc.cycles.texture_limit_render) if sc.render.use_simplify and sc.cycles.texture_limit_render != "OFF" else 0
    for im in used:
        w, h = im.size
        if lim:
            w, h = min(w, lim), min(h, lim)
        mb += w * h * (16 if im.is_float else 4) / 1048576.0
    return {"props": count, "meshes": len(meshes), "triangles": sum(seen.values()), "texture_mb": mb}


def lum_render(sc, tag):
    p = os.path.join(tempfile.gettempdir(), f"bcma_p10_{tag}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3]
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def quality(sc):
    cy = sc.cycles
    ims = sc.render.image_settings
    keep = (ims.media_type, ims.file_format, sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage, cy.samples, cy.use_denoising, cy.seed)
    ims.media_type = "IMAGE"
    ims.file_format = "PNG"
    ims.color_mode = "RGB"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    cy.seed = 0
    y = lum_render(sc, "student")
    cy.samples, cy.use_denoising = 256, False
    ref = lum_render(sc, "ref")
    ims.media_type, ims.file_format = keep[0], keep[1]
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage, cy.samples, cy.use_denoising, cy.seed = keep[2:]
    return float(np.sqrt(((y - ref) ** 2).mean()))


def main():
    debug = L.flag("--debug")
    r = L.Report("P10 — Une scène optimisée, rendue en EXR multicouche")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Floor", "SUN", "CAM")), "Floor, SUN et CAM présents", "Partez de la scène fournie.", 2):
        return r.finish()
    sc = bpy.context.scene
    m = scene_metrics()
    r.check(m["props"] >= 200, f"Accessoires dans le rendu : {m['props']} (≥ 200)", "Ne supprimez pas d'accessoires : partagez ou instanciez-les.", 6)
    r.check(m["meshes"] <= 5 and m["triangles"] <= 150000, f"Géométrie : {m['meshes']} maillage(s) (≤ 5), {m['triangles']} triangles évalués (≤ 150 000)", "Instances de collection ou maillage partagé ; niveau de Subdivision Surface plus bas.", 10)
    r.check(m["texture_mb"] <= 16.0, f"Textures : {m['texture_mb']:.1f} Mo effectifs (≤ 16) ; Simplify {'activé' if sc.render.use_simplify else 'désactivé'}, limite {sc.cycles.texture_limit_render}", "Simplify > Texture Limit 1024, ou réduire l'image.", 8)
    cy = sc.cycles
    ok = sc.render.engine == "CYCLES" and 4 <= cy.samples <= 64 and cy.use_denoising and cy.use_adaptive_sampling and cy.adaptive_threshold <= 0.05
    r.check(ok, f"Cycles : moteur {sc.render.engine}, {cy.samples} échantillons (4–64), débruitage {'activé' if cy.use_denoising else 'désactivé'}, adaptatif {'activé' if cy.use_adaptive_sampling else 'désactivé'} seuil {cy.adaptive_threshold:.3f} (≤ 0,05)", "Cycles, 4 à 64 échantillons, débruitage et échantillonnage adaptatif actifs.", 8)
    if sc.render.engine == "CYCLES":
        cy.device = "CPU"
        e = quality(sc)
        r.check(e <= 0.025, f"Qualité : EQM {e:.4f} contre une référence de 256 échantillons (≤ 0,025)", "Plus d'échantillons, un seuil plus bas, ou un débruitage mieux réglé.", 10)
    here = os.path.dirname(bpy.data.filepath)
    exr = os.path.join(here, "renders", "p10_master.exr")
    if os.path.exists(exr):
        types, comps = exr_info(exr)
        need = ["ViewLayer.Depth.Z", "ViewLayer.Normal.X", "ViewLayer.Object Index.X", "ViewLayer.CryptoObject00.r", "ViewLayer.Combined_sun.R"]
        miss = [c for c in need if c not in types]
        r.check(types.get("ViewLayer.Combined.R") == 2 and not miss and not (comps & LOSSY), f"EXR : Combined {'32 bits' if types.get('ViewLayer.Combined.R') == 2 else '16 bits ou absent'}, canaux manquants : {miss or 'aucun'}, codecs {sorted(comps)} (aucun à perte)", "EXR multicouche, 32 bits, ZIP/PIZ ; passes Z, Normal, Object Index, Cryptomatte Object ; light group sun.", 12)
    else:
        r.check(False, "EXR renders/p10_master.exr", "Rendez l'EXR multicouche dans renders/ à côté du .blend.", 12)
    rep = os.path.join(here, "renders", "p10_report.json")
    if os.path.exists(rep):
        try:
            d = json.load(open(rep, encoding="utf-8"))
            b, a = d["before"], d["after"]
            cons = abs(a["triangles"] - m["triangles"]) <= 0.05 * max(m["triangles"], 1) and a["meshes"] == m["meshes"] and abs(a["texture_mb"] - m["texture_mb"]) <= 0.05 * max(m["texture_mb"], 0.1)
            gain = a["seconds_per_frame"] > 0 and b["seconds_per_frame"] > 0 and a["seconds_per_frame"] <= 0.8 * b["seconds_per_frame"]
            notes = [n for n in d.get("notes", []) if isinstance(n, str) and len(n) > 20]
            r.check(cons, f"Rapport cohérent avec la scène : triangles {a['triangles']} (mesuré {m['triangles']}), maillages {a['meshes']} ({m['meshes']}), textures {a['texture_mb']} Mo ({m['texture_mb']:.1f})", "Le bloc « after » doit décrire la scène livrée (à 5 % près).", 6)
            r.check(gain, f"Gain déclaré : {b['seconds_per_frame']} s → {a['seconds_per_frame']} s par image (≤ 0,8 ×) ; valeurs saisies, non vérifiables", "Mesurez le temps avant et après et reportez-les.", 4)
            r.check(len(notes) >= 5, f"Notes : {len(notes)} phrase(s) de plus de 20 caractères (≥ 5)", "Au moins 5 observations (ce qui a coûté, ce qui a aidé, ce qui reste).", 4)
        except Exception as ex:  # noqa: BLE001
            r.check(False, f"Rapport illisible ({type(ex).__name__})", "JSON avec before, after, notes.", 14)
    else:
        r.check(False, "Rapport renders/p10_report.json", "Écrivez le rapport de temps.", 14)
    if debug:
        print("[DEBUG]", m)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
