"""
mcp_sculpt.py — utilitaires de sculpt RÉEL pour Blender 5.2 en interface, pilotée via le MCP (mcp__Blender__execute_blender_code).
Usage dans le MCP :   H = {}; exec(open(r"…/SCRIPTS/mcp_sculpt.py", encoding="utf-8").read(), H)
Contient : vue orthographique (face/dos), entrée en Sculpt Mode, activation d'une brosse par nom d'asset, trait projeté sur la surface,
relecture des sommets. Voir CLAUDE.md (recette 5.2).
"""
import math

import bpy
import numpy as np
from bpy_extras import view3d_utils
from mathutils import Quaternion, Vector

RAY = {"dir": (0, 1, 0), "y0": -6.0}


def ctx():
    win = bpy.context.window_manager.windows[0]
    area = next(a for a in win.screen.areas if a.type == 'VIEW_3D')
    region = next(r for r in area.regions if r.type == 'WINDOW')
    return win, area, region, area.spaces.active.region_3d


def front_view(center, dist):
    win, area, region, rv3d = ctx()
    rv3d.view_perspective = 'ORTHO'
    rv3d.view_rotation = Quaternion((math.sqrt(0.5), math.sqrt(0.5), 0, 0))
    rv3d.view_location = Vector(center)
    rv3d.view_distance = dist
    RAY["dir"], RAY["y0"], RAY["mode"] = (0, 1, 0), -6.0, "front"


def back_view(center, dist):
    win, area, region, rv3d = ctx()
    rv3d.view_perspective = 'ORTHO'
    rv3d.view_rotation = Quaternion((0, 0, 1), math.pi) @ Quaternion((math.sqrt(0.5), math.sqrt(0.5), 0, 0))
    rv3d.view_location = Vector(center)
    rv3d.view_distance = dist
    RAY["dir"], RAY["y0"], RAY["mode"] = (0, -1, 0), 6.0, "front"


def enter_sculpt(name):
    win, area, region, rv3d = ctx()
    ob = bpy.data.objects[name]
    for o in bpy.data.objects:
        o.select_set(o.name == name)
    bpy.context.view_layer.objects.active = ob
    with bpy.context.temp_override(window=win, area=area, region=region, active_object=ob, object=ob):
        if bpy.context.mode != 'SCULPT':
            bpy.ops.object.mode_set(mode='SCULPT')
    return ob


def brush(name):
    win, area, region, rv3d = ctx()
    ob = bpy.context.view_layer.objects.active
    with bpy.context.temp_override(window=win, area=area, region=region, active_object=ob, object=ob):
        bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', relative_asset_identifier=f"brushes/essentials_brushes-mesh_sculpt.blend/Brush/{name}")
        return bpy.context.tool_settings.sculpt.brush.name


def hit(ob, x, z, y0=None):
    """(x, z) = les deux coordonnées du PLAN DE LA VUE : face/dos -> (x, z) ; dessous -> (x, y) ; droite -> (y, z)."""
    mode = RAY.get("mode", "front")
    if mode == "top":
        o, d0 = Vector((x, z, 6.0)), Vector((0, 0, -1))
    elif mode == "bottom":
        o, d0 = Vector((x, z, -6.0)), Vector((0, 0, 1))
    elif mode == "right":
        o, d0 = Vector((6.0, x, z)), Vector((-1, 0, 0))
    else:
        y0 = RAY["y0"] if y0 is None else y0
        o, d0 = Vector((x, y0, z)), Vector(RAY["dir"])
    inv = ob.matrix_world.inverted()
    ok, loc, nor, i = ob.ray_cast(inv @ o, (inv.to_3x3() @ d0).normalized())
    return (ob.matrix_world @ loc) if ok else None


def top_view(center, dist):
    win, area, region, rv3d = ctx()
    rv3d.view_perspective = 'ORTHO'
    rv3d.view_rotation = Quaternion((1, 0, 0, 0))
    rv3d.view_location = Vector(center)
    rv3d.view_distance = dist
    RAY["mode"] = "top"


def bottom_view(center, dist):
    win, area, region, rv3d = ctx()
    rv3d.view_perspective = 'ORTHO'
    rv3d.view_rotation = Quaternion((0, 1, 0, 0))
    rv3d.view_location = Vector(center)
    rv3d.view_distance = dist
    RAY["mode"] = "bottom"


def right_view(center, dist):
    win, area, region, rv3d = ctx()
    rv3d.view_perspective = 'ORTHO'
    rv3d.view_rotation = Quaternion((0.5, 0.5, 0.5, 0.5))
    rv3d.view_location = Vector(center)
    rv3d.view_distance = dist
    RAY["mode"] = "right"


def stroke(path, radius, strength=1.0, invert=False, step=None, brush_name=None):
    """path : liste de (x, z) en coordonnées MONDE, projetée sur la surface de l'objet actif le long de la vue."""
    win, area, region, rv3d = ctx()
    ob = bpy.context.view_layer.objects.active
    step = step or max(radius * 0.4, 0.0005)
    pts = []
    for a, b in zip(path[:-1], path[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    pts.append(path[-1])
    els = []
    for i, (x, z) in enumerate(pts):
        loc = hit(ob, x, z)
        if loc is None:
            continue
        m = view3d_utils.location_3d_to_region_2d(region, rv3d, loc)
        loc_local = ob.matrix_world.inverted() @ loc          # l'élément de trait attend la position en coordonnées LOCALES de l'objet
        els.append({"name": "s", "location": tuple(loc_local), "mouse": tuple(m), "mouse_event": tuple(m), "pressure": 1.0, "size": 20,
                    "x_tilt": 0, "y_tilt": 0, "time": i * 0.01, "is_start": i == 0})
    with bpy.context.temp_override(window=win, area=area, region=region, active_object=ob, object=ob):
        if brush_name:
            brush(brush_name)
        br = bpy.context.tool_settings.sculpt.brush
        br.use_locked_size = 'SCENE'
        br.unprojected_size = radius
        br.strength = strength
        r = bpy.ops.sculpt.brush_stroke(stroke=els, mode='INVERT' if invert else 'NORMAL')
    return list(r), len(els)


def refresh():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='SCULPT')


def coords(ob):
    me = ob.data
    a = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", a)
    return a.reshape(-1, 3).copy()
