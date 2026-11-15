"""
validate_ch03_03.py — Correcteur « Choisir sa résolution » (CH03.03).
Usage : … --python validate_ch03_03.py --python-exit-code 1 -- --exercise remesh|multires|decide [--render]
  remesh   : un seul objet SCULPT_Body (plus de MASS_*), UN seul morceau, fermé (aucune arête non
             manifold), ≥ 99 % de quads, densité régulière (arête moyenne 0,5–3 cm), taille 1,6–1,9 m.
  multires : SCULPT_HeadBase garde une base légère (≤ 2 000 faces) et porte un Multiresolution de
             ≥ 4 niveaux, Sculpt = niveau max, Render = niveau max, Viewport ≤ Sculpt, non appliqué.
  decide   : texte DECISIONS : la bonne méthode (VOXEL, DYNTOPO, MULTIRES) pour les 5 situations.
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

ANSWERS = {1: "VOXEL", 2: "DYNTOPO", 3: "MULTIRES", 4: "VOXEL", 5: "MULTIRES"}
WHY = {1: "boules jointes → un volume unique et régulier", 2: "densité locale ajoutée là où l'on sculpte",
       3: "base légère conservée, détail sur des niveaux", 4: "redistribution uniforme de la densité",
       5: "seul Multires conserve la topologie de base (donc les UV)"}


def components(bm):
    seen, n = set(), 0
    for v in bm.verts:
        if v.index in seen:
            continue
        n += 1
        stack = [v]
        seen.add(v.index)
        while stack:
            x = stack.pop()
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
    return n


def remesh(r):
    masses = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.startswith("MASS_")]
    ob = bpy.data.objects.get("SCULPT_Body")
    if not r.check(ob is not None and ob.type == "MESH", "Objet SCULPT_Body présent (masses jointes)",
                   "Sélection de toutes les masses, Ctrl+J, F2 : SCULPT_Body.", 2):
        return
    r.check(not masses, f"Plus aucune masse séparée ({len(masses)} restante(s))", "Joignez TOUTES les masses.", 1)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.verts.ensure_lookup_table()
    nc = components(bm)
    r.check(nc == 1, f"Un seul morceau ({nc} composante(s))",
            "Des masses ne se chevauchent pas : ajoutez cou, abdomen, épaules qui pénètrent leurs voisins, puis refaites le remesh.", 3)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nm == 0, f"Volume fermé ({nm} arête(s) non manifold)", "Voxel Remesh produit un volume fermé.", 2)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4) / max(len(bm.faces), 1)
    r.check(quads >= 0.99, f"{100 * quads:.1f} % de quads (≥ 99)", "Le maillage n'a pas été remeshé (Voxel).", 2)
    mw = ob.matrix_world
    lens = [((mw @ e.verts[0].co) - (mw @ e.verts[1].co)).length for e in bm.edges]
    mean = sum(lens) / len(lens)
    r.check(0.005 <= mean <= 0.03 and 8000 <= len(bm.faces) <= 600000,
            f"Densité : arête moyenne {mean * 100:.2f} cm, {len(bm.faces)} faces", "Voxel Size entre 0,005 et 0,03 m (0,012 conseillé).", 2)
    zs = [(mw @ v.co).z for v in bm.verts]
    r.check(1.6 <= max(zs) <= 1.9 and abs(min(zs)) <= 0.03, f"Taille conservée ({max(zs):.2f} m, pieds à {min(zs):.3f})", "", 1)
    bm.free()


def multires(r):
    ob = bpy.data.objects.get("SCULPT_HeadBase")
    if not r.check(ob is not None and ob.type == "MESH", "Objet SCULPT_HeadBase présent", "Repartez du starter.", 1):
        return
    base = len(ob.data.polygons)
    r.check(base <= 2000, f"Base légère conservée ({base} faces, ≤ 2 000)", "N'appliquez pas le Multires.", 2)
    mr = next((m for m in ob.modifiers if m.type == "MULTIRES"), None)
    if not r.check(mr is not None, "Modificateur Multiresolution présent", "Add Modifier > Generate > Multiresolution.", 2):
        return
    r.check(mr.total_levels >= 4, f"{mr.total_levels} niveaux de subdivision (≥ 4)", "Bouton Subdivide.", 2)
    r.check(mr.sculpt_levels == mr.total_levels and mr.render_levels == mr.total_levels,
            f"Sculpt {mr.sculpt_levels} et Render {mr.render_levels} au niveau max ({mr.total_levels})", "", 2)
    r.check(mr.levels <= mr.sculpt_levels and mr.levels < mr.total_levels,
            f"Viewport {mr.levels} plus bas que Sculpt (fluidité)", "Levels Viewport plus bas que Sculpt.", 1)


def decide(r):
    t = bpy.data.texts.get("DECISIONS")
    got = {}
    for line in (t.as_string().splitlines() if t else []):
        m = re.match(r"\s*(\d)\s*[:=.)-]\s*([A-Za-z]+)", line)
        if m and not line.strip().startswith("#"):
            got[int(m.group(1))] = m.group(2).upper()
    ok = [k for k, v in ANSWERS.items() if got.get(k) == v]
    bad = [f"{k} : {got.get(k, '—')} (attendu {v} : {WHY[k]})" for k, v in ANSWERS.items() if got.get(k) != v]
    r.check(len(ok) == 5, f"Méthodes choisies : {len(ok)}/5 justes", " ; ".join(bad[:3]), 5)


def main():
    ex = L.opt("--exercise", "remesh")
    r = L.Report(f"CH03.03 — Résolution ({ex})")
    {"remesh": remesh, "multires": multires, "decide": decide}[ex](r)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
