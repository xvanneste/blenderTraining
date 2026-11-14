"""
bcma_naming_check.py — Contrôle des conventions BCMA dans un .blend (réutilisable partout).

Vérifie :
  - objets : préfixe de type (GEO_, CAM_, LGT_, EMP_, CRV_, RIG_, GP_, TXT_, GN_, FX_) et
    absence de noms par défaut (« .001 », « Cube », « Material »…)
  - collections : MAJUSCULES (sauf la collection de scène)
  - matériaux : préfixe MAT_ et pas de « .001 »
  - images : chemins relatifs (//), fichiers existants
  - nom du fichier : minuscules, sans espace, suffixe _vNNN

Usage autonome :
  blender -b <fichier.blend> --python SCRIPTS/bcma_naming_check.py
Utilisation depuis un correcteur : import bcma_naming_check as N ; N.check(report)
Testé avec : Blender 5.3.0.
"""
import os
import re

import bpy

PREFIX = {"MESH": ("GEO_", "GN_", "FX_"), "CAMERA": ("CAM_",), "LIGHT": ("LGT_",),
          "EMPTY": ("EMP_",), "CURVE": ("CRV_",), "ARMATURE": ("RIG_",),
          "GREASEPENCIL": ("GP_",), "FONT": ("TXT_",), "LIGHT_PROBE": ("LPB_",),
          "SPEAKER": ("SPK_",)}
DEFAULT_NAMES = re.compile(r"(^(Cube|Plane|Sphere|Cylinder|Cone|Torus|Suzanne|Camera|Light|"
                           r"Empty|Material|Collection|Text|BézierCurve|Icosphere)\b)|(\.\d{3}$)")


def problems():
    out = []
    for o in bpy.data.objects:
        exp = PREFIX.get(o.type)
        if exp and not o.name.startswith(exp):
            out.append(("objet", o.name, f"préfixe attendu {' ou '.join(exp)}"))
        if DEFAULT_NAMES.search(o.name.split("_", 1)[-1]):
            out.append(("objet", o.name, "nom par défaut ou suffixe .001"))
    for c in bpy.data.collections:
        if c.name != c.name.upper():
            out.append(("collection", c.name, "MAJUSCULES attendues"))
    for m in bpy.data.materials:
        if m.users == 0:
            continue
        if not m.name.startswith("MAT_") or re.search(r"\.\d{3}$", m.name):
            out.append(("matériau", m.name, "préfixe MAT_ sans .001"))
    for im in bpy.data.images:
        if im.source != "FILE" or not im.filepath:
            continue
        if not im.filepath.startswith("//"):
            out.append(("image", im.name, f"chemin absolu : {im.filepath}"))
        if not os.path.exists(bpy.path.abspath(im.filepath)):
            out.append(("image", im.name, "fichier introuvable"))
    fname = os.path.basename(bpy.data.filepath)
    if fname and (fname != fname.lower() or " " in fname or not re.search(r"_v\d{3}\.blend$|solution\.blend$|starter\.blend$", fname)):
        out.append(("fichier", fname, "minuscules, sans espace, suffixe _vNNN"))
    return out


def check(report, points=4):
    pb = problems()
    by_kind = {}
    for k, n, why in pb:
        by_kind.setdefault(k, []).append(f"{n} ({why})")
    plural = {"objet": "objets", "collection": "collections", "matériau": "matériaux", "image": "images"}
    for kind in ("objet", "collection", "matériau", "image"):
        items = by_kind.get(kind, [])
        report.check(not items, f"Conventions {plural[kind]} : {len(items)} problème(s)",
                     "; ".join(items[:5]) + (" …" if len(items) > 5 else ""), points)
    return pb


if __name__ == "__main__":
    pb = problems()
    print("\n====== BCMA — CONTRÔLE DES CONVENTIONS ======")
    for k, n, why in pb:
        print(f" ✘ {k:10s} {n:30s} {why}")
    print(f" {len(pb)} problème(s)\n=============================================\n")
