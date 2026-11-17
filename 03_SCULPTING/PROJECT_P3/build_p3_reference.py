"""
build_p3_reference.py — Personnage de RÉFÉRENCE du projet P3 : sculpt (haute définition) → retopologie → UV → bake de normal map → matériau → planche de rotation.
Part du mannequin de CH03.10 (27 610 faces, 1,76 m, pose en A, origine entre les pieds) comme « sculpt » : HIGH_Hero.
  1. Retopologie : Quadriflow (object.quadriflow_remesh, 5 000 faces cibles, symétrie) → CHR_Hero_Body (tout en quads)
  2. UV : Smart UV Project + Average Islands Scale + Pack Islands sur CHR_Hero_Body
  3. Bake : normal map de HIGH_Hero sur CHR_Hero_Body (Cycles, Selected to Active) dans T_Hero_N (1 024², Non-Color, empaquetée)
  4. Matériau MAT_CHR_Hero : peau (CH04.10) + Normal Map ; HIGH_Hero caché au rendu
  5. Planche de rotation renders/p3_turnaround.png (4 vues, 1920 x 1080)
Écrit dans 03_SCULPTING/PROJECT_P3/REFERENCE/.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p3_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "CH03_10_RIG_READY", "COMPLETED_EXAMPLES", "ch03_10_char_solution.blend")
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

OUT = os.path.join(HERE, "REFERENCE")
SIZE = 1024


def main():
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(SRC))
    sc = bpy.context.scene
    hi = bpy.data.objects["CHR_Hero_Body"]
    hi.name = "HIGH_Hero"
    hi.data.name = "ME_HIGH_Hero"
    for n in ("GEO_Backdrop", "GEO_Floor"):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    for ob in list(bpy.data.objects):
        if ob.type in ("CAMERA", "LIGHT", "EMPTY"):
            bpy.data.objects.remove(ob, do_unlink=True)
    # 1. retopologie
    lo = hi.copy()
    lo.data = hi.data.copy()
    lo.name = "CHR_Hero_Body"
    lo.data.name = "ME_CHR_Hero_Body"
    hi.users_collection[0].objects.link(lo)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = lo
    lo.select_set(True)
    r = bpy.ops.object.quadriflow_remesh(target_faces=5000, use_mesh_symmetry=True, use_preserve_sharp=False, use_preserve_boundary=False, smooth_normals=True)
    assert "FINISHED" in r, r
    # 2. UV
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(margin=0.02, rotate=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    # 4. matériau (avant le bake : l'image cible doit être active)
    mat = bpy.data.materials.new("MAT_CHR_Hero")
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    for k, v in (("Base Color", (0.65, 0.42, 0.34, 1)), ("Roughness", 0.45), ("Subsurface Weight", 1.0), ("Subsurface Radius", (1.0, 0.2, 0.1)), ("Subsurface Scale", 0.05)):
        b.inputs[k].default_value = v
    img = bpy.data.images.new("T_Hero_N", SIZE, SIZE)
    img.colorspace_settings.name = "Non-Color"
    px = np.empty((SIZE, SIZE, 4), np.float32)
    px[...] = (0.5, 0.5, 1.0, 1.0)
    img.pixels = px.ravel()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.location = (-700, -300)
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.location = (-400, -300)
    nt.links.new(tex.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    nt.nodes.active = tex
    lo.data.materials.clear()
    lo.data.materials.append(mat)
    for p in lo.data.polygons:
        p.use_smooth = True
    # 3. bake
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    bk = sc.render.bake
    bk.use_selected_to_active = True
    bk.cage_extrusion = 0.03
    bk.max_ray_distance = 0.0
    bk.margin = 16
    bk.normal_space = "TANGENT"
    bpy.ops.object.select_all(action="DESELECT")
    hi.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo
    r = bpy.ops.object.bake(type="NORMAL")
    assert "FINISHED" in r, r
    img.pack()
    hi.hide_render = True
    hi.display_type = "WIRE"
    # collection et scène de rendu
    L.studio(subject_height=1.76)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    shots = {}
    for name, loc in (("CAM_Front", (0, -5.2, 1.0)), ("CAM_34", (3.7, -3.7, 1.2)), ("CAM_Side", (5.2, 0, 1.0)), ("CAM_Back", (0, 5.2, 1.0))):
        cam = L.camera(name, c, loc, 50, make_active=(name == "CAM_Front"))
        S.look_at(cam, (0, 0, 0.9))
        shots[name] = cam
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    sc.render.resolution_percentage = 100
    tiles = []
    for name in ("CAM_Front", "CAM_34", "CAM_Side", "CAM_Back"):
        sc.camera = shots[name]
        p = os.path.join(bpy.app.tempdir, name + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    top = np.concatenate([tiles[2], tiles[3]], axis=1)       # origine en bas : les deux dernières vues passent au-dessus
    bot = np.concatenate([tiles[0], tiles[1]], axis=1)
    sheet = np.concatenate([bot, top], axis=0)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels = sheet.ravel()
    out.filepath_raw = os.path.join(OUT, "renders", "p3_turnaround.png")
    out.file_format = "PNG"
    out.save()
    sc.camera = shots["CAM_Front"]
    L.save(os.path.join(OUT, "p3_character_reference.blend"))


if __name__ == "__main__":
    L.run(main)
