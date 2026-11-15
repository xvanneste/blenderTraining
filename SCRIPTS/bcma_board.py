"""
bcma_board.py — Planches de storyboard : construction et lecture (phase 18, modules C–D).

Construction (scripts build) :
  page(ob, guide_drawing, mat, cols, rows, panel_w, gap, note_h, origin) → rectangles des cases,
      mémorisés dans la scène (propriétés « bcma_panels », « bcma_note_h ») ;
  text(name, body, loc, size, mat, col) → objet texte face à la caméra de feuille (−Y) ;
  person(drawing, x, z_feet, h, rect, look) → silhouette simple coupée par la case ;
  dashed_arrow(drawing, a, b, mat) → flèche en tirets (mouvement de caméra).
Lecture (correcteurs) :
  read(scene) → dict : rects, strokes par case, flèches, notes (code, valeur, mouvement, durée,
      case), en-tête. Norme des notes : « SQnnn_SHnnnn · valeur · mouvement · durée ».
Testé avec : Blender 5.3.0.
"""
import json
import math
import re

import bpy

import bcma_gp as G

CODE = re.compile(r"SQ\d{3}_SH\d{4}")
VALUE = re.compile(r"\b(PE|PM|PA|PRT|PRP|GP|TGP|INS)\b")
MOVE = re.compile(r"(fixe|pano|travelling|zoom|grue|steadicam|épaule|tilt|dolly)", re.I)
DUR = re.compile(r"(\d+(?:[.,]\d+)?)\s?s\b")


# --- construction ------------------------------------------------------------------------------

def page(ob, drawing, mat, cols, rows, panel_w, gap, note_h, origin, header_z=None):
    rects = G.storyboard_page(drawing, cols=cols, rows=rows, panel_w=panel_w, gap=gap, note_h=note_h,
                              origin=origin, radius=0.008, mat=mat)
    if header_z is not None:
        x0 = origin[0]
        x1 = origin[0] + cols * panel_w + (cols - 1) * gap
        G.line(drawing, (x0, header_z), (x1, header_z), 0.004, mat)
    sc = bpy.context.scene
    sc["bcma_panels"] = json.dumps(rects)
    sc["bcma_note_h"] = note_h
    return rects


def text(name, body, loc, size=0.12, mat=None, col=None):
    cu = bpy.data.curves.new(name.replace("TXT_", "FNT_"), "FONT")
    cu.body = body
    cu.size = size
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    ob.rotation_euler = (math.radians(90), 0, 0)
    (col or bpy.context.scene.collection).objects.link(ob)
    if mat:
        cu.materials.append(mat)
    return ob


def ellipse_pts(cx, cz, rx, rz, n=24):
    return [(cx + rx * math.cos(t), cz + rz * math.sin(t)) for t in [i * 2 * math.pi / n for i in range(n + 1)]]


def person(d, x, zf, h, rect, look=1, mat=0, arms=None):
    """Silhouette : tête, torse, jambes, regard (petit trait), bras optionnels (liste d'angles en degrés)."""
    polys = [ellipse_pts(x, zf + h * 0.92, h * 0.07, h * 0.08),
             [(x - h * 0.12, zf + h * 0.45), (x - h * 0.1, zf + h * 0.82), (x + h * 0.1, zf + h * 0.82),
              (x + h * 0.12, zf + h * 0.45), (x - h * 0.12, zf + h * 0.45)],
             [(x - h * 0.06, zf + h * 0.45), (x - h * 0.08, zf)], [(x + h * 0.06, zf + h * 0.45), (x + h * 0.08, zf)],
             [(x + look * h * 0.02, zf + h * 0.93), (x + look * h * 0.06, zf + h * 0.93)]]
    for i, ang in enumerate(arms or []):
        sx = x + (h * 0.1 if i == 0 else -h * 0.1)
        a = math.radians(ang)
        polys.append([(sx, zf + h * 0.78), (sx + h * 0.35 * math.cos(a), zf + h * 0.78 + h * 0.35 * math.sin(a))])
    for poly in polys:
        G.polyline_clipped(d, poly, rect, 0.01, mat)


def dashed_arrow(d, a, b, mat, n=7, radius=0.012):
    for i in range(n):
        t0, t1 = i / n, (i + 0.55) / n
        G.line(d, (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
               (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), radius, mat)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (1, -1):
        G.line(d, b, (b[0] - 0.15 * math.cos(ang + s * 0.5), b[1] - 0.15 * math.sin(ang + s * 0.5)), radius, mat)


# --- lecture -----------------------------------------------------------------------------------

def read(scene, gp_name="GP_Practice", drawing_layer="USER_Drawing", arrow_layer="USER_Arrows"):
    rects = json.loads(scene.get("bcma_panels", "[]"))
    note_h = float(scene.get("bcma_note_h", 0.5))
    info = {"rects": rects, "per_panel": [0] * len(rects), "arrows": 0, "notes": [], "header": False}
    ob = bpy.data.objects.get(gp_name)
    if ob is not None and ob.type == "GREASEPENCIL":
        lay = {l.name: l for l in ob.data.layers}
        if drawing_layer in lay:
            for fr in lay[drawing_layer].frames:
                for s in fr.drawing.strokes:
                    xs = [p.position.x for p in s.points]; zs = [p.position.z for p in s.points]
                    cx, cz = sum(xs) / len(xs), sum(zs) / len(zs)
                    for i, (x0, z0, x1, z1) in enumerate(rects):
                        if x0 <= cx <= x1 and z0 <= cz <= z1:
                            info["per_panel"][i] += 1
        if arrow_layer in lay:
            info["arrows"] = sum(len(fr.drawing.strokes) for fr in lay[arrow_layer].frames)
    for t in bpy.data.objects:
        if t.type != "FONT":
            continue
        body = t.data.body
        if re.search(r"page\s*\d+", body, re.I):
            info["header"] = True
        m = CODE.search(body)
        if not m:
            continue
        x, z = t.matrix_world.translation.x, t.matrix_world.translation.z
        panel = next((i for i, (x0, z0, x1, z1) in enumerate(rects)
                      if x0 - 0.2 <= x <= x1 and z0 - note_h - 0.05 <= z <= z0), None)
        v, mv, du = VALUE.search(body), MOVE.search(body), DUR.search(body)
        info["notes"].append({"name": t.name, "code": m.group(0), "value": v.group(1) if v else None,
                              "move": mv.group(1) if mv else None,
                              "duration": float(du.group(1).replace(",", ".")) if du else None, "panel": panel})
    return info
