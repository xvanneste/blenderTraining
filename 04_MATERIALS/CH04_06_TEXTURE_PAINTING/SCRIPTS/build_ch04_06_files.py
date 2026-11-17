"""
build_ch04_06_files.py — « Texture Painting » (CH04.06).

Une boîte de conserve PROP_Can (cylindre à UV automatiques), matériau MAT_Can dont Base Color vient de l'image T_Can (512 x 512, crème, EMPAQUETÉE dans le .blend).
  STARTER_FILES/ch04_06_painting_starter.blend : image vierge crème, branchée.
  COMPLETED_EXAMPLES/ch04_06_painting_solution.blend : peinte pour de vrai en Texture Paint (Blender 5.2 piloté par le MCP) :
      bande rouge autour de la boîte + pastilles bleues. Marqueur COMPLETED_EXAMPLES/.painted_with_mcp : ce script ne l'écrase pas.
      (Repli scripté en numpy si le marqueur est absent.)
  COUNTER_EXAMPLES/ : blank (rien peint), one_color, flood (tout repeint), spill (peinture hors des îlots UV), unlinked (image non branchée)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
SIZE = 512
BASE = (0.80, 0.74, 0.58)
RED = (0.80, 0.08, 0.06)
BLUE = (0.10, 0.20, 0.80)
NOTE = """CH04.06 — TEXTURE PAINTING (PROP_Can, image T_Can 512 x 512 branchée sur Base Color de MAT_Can)
Peignez l'image directement sur la boîte (mode Texture Paint, brosse Draw) :
1. Une bande rouge qui fait le tour de la boîte à mi-hauteur.
2. Quelques pastilles bleues (au moins deux couleurs peintes).
3. La peinture reste dans les îlots UV (pas de bavure hors de l'objet) et couvre entre 3 % et 50 % de la surface dépliée.
4. EMPAQUETEZ l'image dans le .blend (Image > Pack) avant d'enregistrer : sinon la peinture est perdue.
Vérification : SCRIPTS/validate_ch04_06.py -- --exercise painting
"""


def make_can():
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.5, depth=1.2, location=(0, 0, 0.6))
    ob = bpy.context.active_object
    ob.name = "PROP_Can"
    for p in ob.data.polygons:
        p.use_smooth = len(p.vertices) == 4
    return ob


def make_image(fill=BASE):
    img = bpy.data.images.new("T_Can", SIZE, SIZE)
    img.generated_color = (*fill, 1.0)
    px = np.empty((SIZE, SIZE, 4), np.float32)
    px[...] = (*fill, 1.0)
    img.pixels = px.ravel()
    return img


def side_bbox(ob):
    """Boîte UV de l'îlot « côté » (faces dont la normale est horizontale)."""
    me = ob.data
    uv = me.uv_layers.active.data
    pts = [uv[li].uv[:] for p in me.polygons if abs(p.normal.z) < 0.5 for li in p.loop_indices]
    a = np.array(pts)
    return a.min(0), a.max(0)


def scripted_paint(img, ob, kind):
    """Repli numpy : bande rouge + pastilles bleues (ou la variante fausse `kind`)."""
    (u0, v0), (u1, v1) = side_bbox(ob)
    px = np.array(img.pixels[:], np.float32).reshape(SIZE, SIZE, 4)
    ys, xs = np.mgrid[0:SIZE, 0:SIZE]
    U, V = (xs + 0.5) / SIZE, (ys + 0.5) / SIZE
    band = (U >= u0) & (U <= u1) & (V >= v0 + 0.4 * (v1 - v0)) & (V <= v0 + 0.55 * (v1 - v0))
    if kind in ("solution", "one_color", "spill", "unlinked"):
        px[band, :3] = RED
    if kind in ("solution", "spill", "unlinked"):
        for fx in (0.2, 0.5, 0.8):
            cx, cy = u0 + fx * (u1 - u0), v0 + 0.8 * (v1 - v0)
            d = (U - cx) ** 2 + (V - cy) ** 2 < 0.03 ** 2
            px[d, :3] = BLUE
    if kind == "flood":
        px[..., :3] = RED
        px[(U < 0.5), :3] = BLUE
    if kind == "spill":
        out = ~uv_mask(ob)
        px[(out & (U > 0.5)), :3] = (0.1, 0.6, 0.2)             # gros aplat vert hors des îlots
    img.pixels = px.ravel()


def uv_mask(ob):
    """Masque booléen (SIZE x SIZE) des pixels couverts par au moins un triangle UV."""
    me = ob.data
    uv = me.uv_layers.active.data
    me.calc_loop_triangles()
    M = np.zeros((SIZE, SIZE), bool)
    for t in me.loop_triangles:
        P = np.array([uv[l].uv[:] for l in t.loops]) * SIZE
        x0, y0 = np.floor(P.min(0)).astype(int)
        x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, SIZE - 1), min(y1, SIZE - 1)
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (P[1, 1] - P[2, 1]) * (P[0, 0] - P[2, 0]) + (P[2, 0] - P[1, 0]) * (P[0, 1] - P[2, 1])
        if abs(d) < 1e-12:
            continue
        a = ((P[1, 1] - P[2, 1]) * (gx - P[2, 0]) + (P[2, 0] - P[1, 0]) * (gy - P[2, 1])) / d
        b = ((P[2, 1] - P[0, 1]) * (gx - P[2, 0]) + (P[0, 0] - P[2, 0]) * (gy - P[2, 1])) / d
        c = 1 - a - b
        ins = (a >= -0.02) & (b >= -0.02) & (c >= -0.02)
        M[y0:y1 + 1, x0:x1 + 1] |= ins
    return M


def build(kind, paint=True):
    L.reset("SC_PAINT")
    L.studio(subject_height=1.2)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (0, -4.2, 1.1), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.6))
    cam2 = L.camera("CAM_Side", c, (3.0, -3.4, 2.0), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.6))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    ob = make_can()
    img = make_image()
    mat = bpy.data.materials.new("MAT_Can")
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.location = (-400, 0)
    if kind != "unlinked":
        nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.45
    ob.data.materials.append(mat)
    if kind != "starter" and paint:
        scripted_paint(img, ob, kind)
    img.pack()
    L.instructions(NOTE)
    return sc, ob


def views(sc, out_path):
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_06_painting_starter.blend"))
    for k in ("blank", "one_color", "flood", "spill", "unlinked"):
        build("starter" if k == "blank" else k)
        L.save(os.path.join(out_dir, "COUNTER_EXAMPLES", f"ch04_06_painting_{k}.blend"))
    sol = os.path.join(out_dir, "ch04_06_painting_solution.blend")
    if os.path.exists(os.path.join(out_dir, ".painted_with_mcp")) and os.path.exists(sol):
        print("[build] solution peinte au MCP conservée")
        return
    sc, ob = build("solution")
    L.save(sol)
    views(sc, os.path.join(out_dir, "ch04_06_painting_reference.png"))


if __name__ == "__main__":
    L.run(main)
