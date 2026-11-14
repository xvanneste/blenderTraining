"""
bcma_lib.py — Bibliothèque partagée de l'académie (Blender 5.3).

Utilisée par les scripts de construction (build_chNN_MM_files.py) et les
correcteurs (validate_chNN_MM.py) de tous les chapitres.

Import depuis un script de chapitre (NN_PHASE/CHNN_MM_NOM/SCRIPTS/x.py) :
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "SCRIPTS"))
    import bcma_lib as L

Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

import bpy

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------

def chapter_dir(script_file):
    """Dossier du chapitre à partir de __file__ d'un script de SCRIPTS/."""
    return os.path.dirname(os.path.dirname(os.path.abspath(script_file)))


def args_after_dashdash():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    a = args_after_dashdash()
    return a[a.index(name) + 1] if name in a else default


def flag(name):
    return name in args_after_dashdash()


# ---------------------------------------------------------------------------
# Scène
# ---------------------------------------------------------------------------

def reset(scene_name="Scene"):
    """Fichier vide (aucun objet)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = scene_name
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    return sc


def collection(name, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(col)
    return col


def move_to(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def material(name, color=(0.8, 0.8, 0.8), roughness=0.5, metallic=0.0,
             emission=None, emission_strength=4.0, alpha=1.0, transmission=0.0):
    """Matériau Principled BSDF (Blender 5.x : arbre de nœuds déjà présent)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if transmission:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    mat.diffuse_color = (*color, 1.0)
    return mat


def mesh(op, name, col=None, mat=None, smooth=False, **kw):
    """Ajoute une primitive via un opérateur bpy.ops.mesh.primitive_*_add."""
    op(**kw)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name.replace("GEO_", "ME_")
    if col:
        move_to(obj, col)
    if mat:
        obj.data.materials.append(mat)
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj


def cube(name, col=None, mat=None, **kw):
    return mesh(bpy.ops.mesh.primitive_cube_add, name, col, mat, **kw)


def plane(name, col=None, mat=None, **kw):
    return mesh(bpy.ops.mesh.primitive_plane_add, name, col, mat, **kw)


def sphere(name, col=None, mat=None, **kw):
    kw.setdefault("segments", 32)
    kw.setdefault("ring_count", 16)
    return mesh(bpy.ops.mesh.primitive_uv_sphere_add, name, col, mat, smooth=True, **kw)


def cylinder(name, col=None, mat=None, **kw):
    return mesh(bpy.ops.mesh.primitive_cylinder_add, name, col, mat, **kw)


def empty(name, col, location=(0, 0, 0), display="PLAIN_AXES", size=0.5):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = display
    e.empty_display_size = size
    e.location = location
    col.objects.link(e)
    return e


def light(name, col, kind="AREA", location=(0, 0, 3), energy=500, size=1.0,
          color=(1, 1, 1), target=None, visible_camera=False, rotation=None):
    data = bpy.data.lights.new(name.replace("LGT_", "LA_"), kind)
    data.energy = energy
    data.color = color
    if kind == "AREA":
        data.size = size
    elif kind == "SPOT":
        data.spot_size = math.radians(45)
    elif kind == "SUN":
        data.angle = math.radians(2)
    obj = bpy.data.objects.new(name, data)
    obj.location = location
    if rotation:
        obj.rotation_euler = [math.radians(a) for a in rotation]
    obj.visible_camera = visible_camera
    col.objects.link(obj)
    if target is not None:
        track(obj, target)
    return obj


def track(obj, target):
    c = obj.constraints.new("TRACK_TO")
    c.target = target
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return c


def camera(name, col, location=(0, -8, 2), lens=50, target=None, make_active=True):
    data = bpy.data.cameras.new(name.replace("CAM_", "CA_"))
    data.lens = lens
    data.clip_start = 0.1
    data.clip_end = 200
    obj = bpy.data.objects.new(name, data)
    obj.location = location
    col.objects.link(obj)
    if target is not None:
        track(obj, target)
    if make_active:
        bpy.context.scene.camera = obj
    return obj


def world(color=(0.05, 0.05, 0.06), strength=1.0, name="WO_Neutral"):
    sc = bpy.context.scene
    wo = bpy.data.worlds.get(name) or bpy.data.worlds.new(name)
    sc.world = wo
    bg = next(n for n in wo.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (*color, 1.0)
    bg.inputs["Strength"].default_value = strength
    return wo


def studio(subject_height=1.0, key=600, fill=150, rim=500):
    """Studio standard : sol + fond, éclairage 3 points, caméra 50 mm, monde neutre."""
    col_set = collection("SET")
    col_l = collection("LIGHTS")
    col_c = collection("CAMERAS")
    m = material("MAT_Studio_Grey", (0.18, 0.18, 0.18), roughness=0.6)
    plane("GEO_Floor", col_set, m, size=20)
    plane("GEO_Backdrop", col_set, m, size=20, location=(0, 6, 10),
          rotation=(math.radians(90), 0, 0))
    tgt = empty("EMP_Target", col_c, (0, 0, subject_height * 0.6))
    light("LGT_Key", col_l, "AREA", (-3, -3, 4), key, 2.0, (1.0, 0.95, 0.88), tgt)
    light("LGT_Fill", col_l, "AREA", (3.5, -2.5, 2), fill, 3.0, (0.85, 0.9, 1.0), tgt)
    light("LGT_Rim", col_l, "SPOT", (1.8, 2.6, 3.2), rim, target=tgt)
    cam = camera("CAM_Main", col_c, (0, -8, 2.2), 50, tgt)
    world()
    return {"target": tgt, "camera": cam}


def render_defaults(engine="BLENDER_EEVEE", percent=50, samples=64, out="//renders/render_"):
    sc = bpy.context.scene
    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.resolution_percentage = percent
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = out
    sc.view_settings.view_transform = "AgX"
    if engine == "CYCLES":
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
    return sc


def text_note(body, name="TXT_Note", col=None, location=(0, 0, 0), size=0.2):
    """Objet texte 3D (consignes visibles dans la scène)."""
    cu = bpy.data.curves.new(name.replace("TXT_", "CU_"), type="FONT")
    cu.body = body
    cu.size = size
    obj = bpy.data.objects.new(name, cu)
    obj.location = location
    (col or bpy.context.scene.collection).objects.link(obj)
    return obj


def instructions(text, name="README_EXERCICE"):
    """Bloc de texte interne au .blend (lisible dans le Text Editor)."""
    t = bpy.data.texts.get(name) or bpy.data.texts.new(name)
    t.clear()
    t.write(text)
    t.use_fake_user = True
    return t


def save(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0  # pas de .blend1
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=True)
    print(f"[BCMA] saved {path}")
    return path


def run(main):
    """Exécute main() avec code de retour propre en mode arrière-plan."""
    try:
        code = main() or 0
    except Exception:
        import traceback
        traceback.print_exc()
        code = 1
    sys.exit(code)


# ---------------------------------------------------------------------------
# Correction automatique
# ---------------------------------------------------------------------------

class Report:
    """Collecte des vérifications et affiche une note détaillée."""

    def __init__(self, title):
        self.title = title
        self.items = []

    def check(self, ok, label, hint="", points=1, mandatory=True):
        try:
            ok = bool(ok)
        except Exception:
            ok = False
        self.items.append((ok, label, hint, points, mandatory))
        return ok

    def finish(self):
        got = sum(i[3] for i in self.items if i[0])
        total = sum(i[3] for i in self.items)
        print(f"\n================ BCMA — CORRECTION {self.title} ================")
        for ok, label, hint, pts, mand in self.items:
            tag = "✔" if ok else ("✘" if mand else "–")
            print(f" {tag} [{pts} pt] {label}")
            if not ok and hint:
                print(f"      → piste : {hint}")
        failed = [i for i in self.items if i[4] and not i[0]]
        print(f"------------------------------------------------------------\n Score : {got}/{total}")
        print(" RÉSULTAT :", "VALIDÉ" if not failed else
              f"À CORRIGER ({len(failed)} point(s) obligatoire(s))")
        print("============================================================\n")
        return 0 if not failed else 1


def obj(name):
    return bpy.data.objects.get(name)


def objects_of(kind):
    return [o for o in bpy.context.scene.objects if o.type == kind]


def mean_luminance(path):
    img = bpy.data.images.load(path)
    px = img.pixels[:]
    n = len(px) // 4
    lum = sum(0.2126 * px[i * 4] + 0.7152 * px[i * 4 + 1] + 0.0722 * px[i * 4 + 2]
              for i in range(0, n, 7)) / max(n // 7, 1)
    bpy.data.images.remove(img)
    return lum


def quick_render(percent=20, samples=8, engine=None):
    """Rendu de contrôle rapide (ne modifie pas le fichier sur disque)."""
    sc = bpy.context.scene
    if engine:
        sc.render.engine = engine
    sc.render.resolution_percentage = percent
    if sc.render.engine == "CYCLES":
        sc.cycles.samples = samples
        sc.cycles.use_denoising = False
        sc.cycles.device = "CPU"
    elif sc.render.engine == "BLENDER_EEVEE":
        sc.eevee.taa_render_samples = samples
    path = os.path.join(tempfile.gettempdir(), f"bcma_qr_{os.getpid()}.png")
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    return mean_luminance(path)


def evaluated_mesh_stats(o):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    stats = (len(me.vertices), len(me.edges), len(me.polygons))
    ev.to_mesh_clear()
    return stats
