"""
build_ch04_07_files.py — « Baking » (CH04.07).

Un rocher : HIGH_Rock (haute définition, relief en bosses, 20 480 faces) et LOW_Rock (320 faces, UV dépliés).
On BAKE la normal map de HIGH_Rock sur LOW_Rock (Cycles, Selected to Active) dans l'image T_Rock_N (512 x 512, Non-Color, empaquetée)
puis on la branche : Image Texture -> Normal Map -> Normal du Principled de MAT_RockLow.
  STARTER_FILES/ch04_07_baking_starter.blend : HIGH + LOW, image vierge (0,5 ; 0,5 ; 1) déjà branchée, RIEN de baké.
  COMPLETED_EXAMPLES/ch04_07_baking_solution.blend (+ _reference.png) : bake réel (opérateur object.bake)
  COUNTER_EXAMPLES/ : unbaked (image vierge), srgb (image en sRGB), no_normalmap (image reliée DIRECTEMENT à Normal), partial (moitié des îlots non bakée), direct_color (Normal Map branchée sur Base Color)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_07_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector, noise  # noqa: E402

CH = L.chapter_dir(__file__)
SIZE = 512
NOTE = """CH04.07 — BAKING (HIGH_Rock : haute définition ; LOW_Rock : 320 faces avec UV ; image T_Rock_N 512 x 512)
Bakez le relief de HIGH_Rock dans une normal map et utilisez-la sur LOW_Rock :
1. Moteur Cycles ; Bake : Bake Type Normal, Selected to Active coché (Extrusion ≈ 0,25 m), Margin ≥ 8 px.
2. Sélectionner HIGH_Rock puis LOW_Rock (actif) ; dans le matériau de LOW_Rock, le nœud Image Texture T_Rock_N doit être ACTIF ; Bake.
3. T_Rock_N en espace colorimétrique Non-Color ; la relier à Normal par un nœud Normal Map (espace Tangent).
4. Empaqueter l'image (Image > Pack), cacher HIGH_Rock au rendu.
Vérification : SCRIPTS/validate_ch04_07.py -- --exercise baking
"""


def make_high():
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=6, radius=1.0)
    for v in bm.verts:
        p = v.co.copy()
        n = noise.fractal(p * 1.6, 0.5, 2.0, 5)
        r = 1.0 + 0.16 * n
        v.co = p.normalized() * r
    me = bpy.data.meshes.new("ME_HIGH_Rock")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("HIGH_Rock", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    ob.location = (0, 0, 1.0)
    return ob


def make_low():
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    me = bpy.data.meshes.new("ME_LOW_Rock")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("LOW_Rock", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    ob.location = (0, 0, 1.0)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def setup_material(low, kind):
    mat = bpy.data.materials.new("MAT_RockLow")
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.25, 0.22, 0.19, 1.0)
    b.inputs["Roughness"].default_value = 0.85
    img = bpy.data.images.new("T_Rock_N", SIZE, SIZE)
    img.colorspace_settings.name = "sRGB" if kind == "srgb" else "Non-Color"      # AVANT d'écrire les pixels : changer l'espace colorimétrique réinitialise le tampon
    px = np.empty((SIZE, SIZE, 4), np.float32)
    px[...] = (0.5, 0.5, 1.0, 1.0)
    img.pixels = px.ravel()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.location = (-700, -250)
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.space = "TANGENT"
    nm.location = (-350, -250)
    nt.links.new(tex.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    nt.nodes.active = tex
    low.data.materials.append(mat)
    return mat, img, tex, nm, b


def uv_mask():
    low = bpy.data.objects["LOW_Rock"]
    me = low.data
    uv = me.uv_layers.active.data
    me.calc_loop_triangles()
    M = np.zeros((SIZE, SIZE), bool)
    for t in me.loop_triangles:
        P = np.array([uv[l].uv[:] for l in t.loops]) * SIZE
        x0, y0 = np.floor(P.min(0)).astype(int)
        x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, SIZE - 1), min(y1, SIZE - 1)
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (P[1, 1] - P[2, 1]) * (P[0, 0] - P[2, 0]) + (P[2, 0] - P[1, 0]) * (P[0, 1] - P[2, 1])
        if abs(d) < 1e-12:
            continue
        a = ((P[1, 1] - P[2, 1]) * (gx - P[2, 0]) + (P[2, 0] - P[1, 0]) * (gy - P[2, 1])) / d
        b = ((P[2, 1] - P[0, 1]) * (gx - P[2, 0]) + (P[0, 0] - P[2, 0]) * (gy - P[2, 1])) / d
        M[y0:y1 + 1, x0:x1 + 1] |= (a >= -0.02) & (b >= -0.02) & (1 - a - b >= -0.02)
    return M


def bake_normal(high, low, tex):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    bk = sc.render.bake
    bk.use_selected_to_active = True
    bk.cage_extrusion = 0.25
    bk.max_ray_distance = 0.0
    bk.margin = 16
    bk.normal_space = "TANGENT"
    bpy.ops.object.select_all(action="DESELECT")
    high.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    low.data.materials[0].node_tree.nodes.active = tex
    r = bpy.ops.object.bake(type="NORMAL")
    assert "FINISHED" in r, r


def build(kind):
    L.reset("SC_BAKE")
    L.studio(subject_height=2.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -6.5, 1.8), 50, make_active=True)
    S.look_at(cam, (0, 0, 1.0))
    cam2 = L.camera("CAM_Side", c, (4.5, -4.5, 3.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 1.0))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    high = make_high()
    low = make_low()
    mat, img, tex, nm, b = setup_material(low, kind)
    if kind != "starter" and kind != "unbaked":
        bake_normal(high, low, tex)
        sc.render.engine = "BLENDER_EEVEE"
        if kind == "partial":
            px = np.array(img.pixels[:], np.float32).reshape(SIZE, SIZE, 4)
            px[:, SIZE // 2:, :3] = (0.5, 0.5, 1.0)
            img.pixels = px.ravel()
        if kind == "no_normalmap":
            for l in list(mat.node_tree.links):
                if l.to_node == nm or l.from_node == nm:
                    mat.node_tree.links.remove(l)
            mat.node_tree.nodes.remove(nm)
            mat.node_tree.links.new(tex.outputs["Color"], b.inputs["Normal"])
        if kind == "direct_color":
            for l in list(mat.node_tree.links):
                if l.to_socket == b.inputs["Normal"]:
                    mat.node_tree.links.remove(l)
            mat.node_tree.links.new(nm.outputs["Normal"], b.inputs["Base Color"])
    if kind not in ("starter",):
        high.hide_render = True
        high.display_type = "WIRE"
    img.pack()
    L.instructions(NOTE)
    return sc


def views(sc, out_path):
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 800, 400
    tiles = []
    for cam in ("CAM_Front", "CAM_Side"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=0)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out_path
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out_dir = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_07_baking_starter.blend"))
    for k in ("unbaked", "srgb", "no_normalmap", "partial", "direct_color"):
        build(k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_07_baking_{k}.blend"))
    sc = build("solution")
    L.save(os.path.join(out_dir, "ch04_07_baking_solution.blend"))
    views(sc, os.path.join(out_dir, "ch04_07_baking_reference.png"))


if __name__ == "__main__":
    L.run(main)
