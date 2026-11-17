"""
build_ch00_01_files.py — Génère les fichiers .blend du chapitre CH00.01.

Fichiers produits :
  STARTER_FILES/ch00_01_testcard_starter.blend      Scène « mire de test » (réglages par défaut)
  STARTER_FILES/ch00_01_broken_render_starter.blend Même scène avec 5 pannes de rendu cachées
  COMPLETED_EXAMPLES/ch00_01_testcard_solution.blend Scène réglée : Cycles, GPU, échantillons, sortie
  COMPLETED_EXAMPLES/ch00_01_broken_render_solution.blend  Scène réparée

Usage (depuis n'importe quel dossier) :
  blender -b --factory-startup --python-exit-code 1 --python build_ch00_01_files.py

Testé avec : Blender 5.3.0 (Windows 11).
"""
import math
import os
import sys

import bpy

CHAPTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STARTER_DIR = os.path.join(CHAPTER_DIR, "STARTER_FILES")
SOLUTION_DIR = os.path.join(CHAPTER_DIR, "COMPLETED_EXAMPLES")


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
def reset_scene():
    """Repart d'un fichier vide (aucun objet, aucune donnée orpheline)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def new_collection(name, parent=None):
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def link(obj, col):
    col.objects.link(obj)
    return obj


def make_material(name, color, roughness=0.5, metallic=0.0, emission=None):
    mat = bpy.data.materials.new(name)
    # Depuis Blender 5.0, un nouveau matériau possède toujours un arbre de nœuds
    # (Principled BSDF + Material Output). 'Material.use_nodes' est déprécié
    # (suppression annoncée pour Blender 6.0) : on ne l'utilise donc pas.
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 4.0
    mat.diffuse_color = (*color, 1.0)  # couleur en mode Solid du viewport
    return mat


def add_mesh(op, name, col, mat=None, **kwargs):
    op(**kwargs)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name.replace("GEO_", "ME_")
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj


def add_text(body, name, col, location, size=0.18, mat=None):
    curve = bpy.data.curves.new(name.replace("TXT_", "CU_"), type="FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.extrude = 0.005
    obj = bpy.data.objects.new(name, curve)
    obj.location = location
    obj.rotation_euler = (math.radians(90), 0, 0)
    if mat:
        curve.materials.append(mat)
    return link(obj, col)


# ---------------------------------------------------------------------------
# Construction de la mire de test
# ---------------------------------------------------------------------------
def build_testcard():
    reset_scene()
    scene = bpy.context.scene
    scene.name = "SC_Testcard"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    col_set = new_collection("SET")
    col_props = new_collection("PROPS")
    col_lights = new_collection("LIGHTS")
    col_cams = new_collection("CAMERAS")

    # Matériaux
    m_floor = make_material("MAT_Floor_Grey", (0.18, 0.18, 0.18), roughness=0.6)
    m_white = make_material("MAT_White_Clay", (0.8, 0.8, 0.8), roughness=0.45)
    m_metal = make_material("MAT_Chrome", (0.9, 0.9, 0.9), roughness=0.08, metallic=1.0)
    m_gold = make_material("MAT_Gold", (1.0, 0.71, 0.29), roughness=0.25, metallic=1.0)
    m_glow = make_material("MAT_Emission_Cyan", (0.05, 0.6, 0.8), emission=(0.05, 0.6, 0.8))
    m_text = make_material("MAT_Text_Dark", (0.02, 0.02, 0.02), roughness=0.8)

    # Sol en arrondi (cyclorama simplifié) : plan + mur courbé
    floor = add_mesh(bpy.ops.mesh.primitive_plane_add, "GEO_Floor", col_set, m_floor, size=12)
    wall = add_mesh(bpy.ops.mesh.primitive_plane_add, "GEO_Backdrop", col_set, m_floor,
                    size=12, location=(0, 4, 6), rotation=(math.radians(90), 0, 0))

    # Sujets : tête de singe (Suzanne), sphère chrome, cube doré, tore émissif
    suz = add_mesh(bpy.ops.mesh.primitive_monkey_add, "GEO_Suzanne", col_props, m_white,
                   size=1.2, location=(0, 0, 0.8))
    suz.rotation_euler = (math.radians(8), 0, math.radians(-15))
    sub = suz.modifiers.new("Subdivision", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.context.view_layer.objects.active = suz
    bpy.ops.object.shade_smooth()

    add_mesh(bpy.ops.mesh.primitive_cylinder_add, "GEO_Pedestal", col_props, m_floor,
             radius=0.35, depth=0.3, location=(0, 0.1, 0.15), vertices=48)
    add_mesh(bpy.ops.mesh.primitive_uv_sphere_add, "GEO_Sphere_Chrome", col_props, m_metal,
             radius=0.45, location=(-1.6, 0.4, 0.45), segments=48, ring_count=24)
    bpy.ops.object.shade_smooth()
    cube = add_mesh(bpy.ops.mesh.primitive_cube_add, "GEO_Cube_Gold", col_props, m_gold,
                    size=0.7, location=(1.6, 0.3, 0.35))
    cube.rotation_euler.z = math.radians(30)
    bev = cube.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.04
    bev.segments = 3
    add_mesh(bpy.ops.mesh.primitive_torus_add, "GEO_Torus_Glow", col_props, m_glow,
             location=(0, 1.6, 0.25), major_radius=0.5, minor_radius=0.08)

    # Nuancier : 6 pastilles de gris (vérification de l'exposition)
    # Valeurs d'albédo linéaires ≈ gris perçus réguliers (noir → blanc)
    for i, v in enumerate((0.03, 0.09, 0.19, 0.36, 0.59, 0.9)):
        m = make_material(f"MAT_Chart_{i}", (v, v, v), roughness=0.9)
        add_mesh(bpy.ops.mesh.primitive_cube_add, f"GEO_Chart_{i}", col_props, m,
                 size=0.3, location=(-1.25 + i * 0.5, 3.6, 1.6),
                 scale=(1, 0.1, 1))

    add_text("BCMA · TEST CARD · Blender 5.3", "TXT_Title", col_set, (0, 3.55, 2.3), mat=m_text)

    # Lumières : key (area), fill (area), rim (spot) — watts réalistes
    def area(name, loc, rot, power, size, color=(1, 1, 1)):
        data = bpy.data.lights.new(name.replace("LGT_", "LA_"), "AREA")
        data.energy = power
        data.size = size
        data.color = color
        obj = bpy.data.objects.new(name, data)
        obj.location = loc
        obj.rotation_euler = [math.radians(a) for a in rot]
        obj.visible_camera = False  # la surface de l'Area light ne doit pas apparaître à l'image
        return link(obj, col_lights)

    area("LGT_Key", (-3.0, -3.0, 4.0), (50, 0, -45), 600, 2.0, (1.0, 0.95, 0.88))
    area("LGT_Fill", (3.5, -2.5, 2.0), (70, 0, 55), 150, 3.0, (0.85, 0.9, 1.0))
    rim = bpy.data.lights.new("LA_Rim", "SPOT")
    rim.energy = 800
    rim.spot_size = math.radians(45)
    rim_obj = bpy.data.objects.new("LGT_Rim", rim)
    rim_obj.location = (1.8, 2.6, 3.2)
    rim_obj.visible_camera = False
    link(rim_obj, col_lights)

    # Monde : gris neutre faible
    world = bpy.data.worlds.new("WO_Neutral")
    scene.world = world
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0.05, 0.05, 0.06, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    # Caméra 50 mm, vise Suzanne
    cam_data = bpy.data.cameras.new("CA_Main")
    cam_data.lens = 50
    cam_data.clip_start = 0.1
    cam_data.clip_end = 100
    cam = bpy.data.objects.new("CAM_Main", cam_data)
    cam.location = (0, -7.5, 2.4)
    link(cam, col_cams)
    target = bpy.data.objects.new("EMP_CamTarget", None)
    target.location = (0, 0.6, 0.9)
    link(target, col_cams)
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    # Le spot de contre-jour vise lui aussi la cible (sinon sa tache lumineuse
    # tombe sur le fond et forme une ellipse blanche parasite).
    rim_track = rim_obj.constraints.new("TRACK_TO")
    rim_track.target = target
    rim_track.track_axis = "TRACK_NEGATIVE_Z"
    rim_track.up_axis = "UP_Y"
    scene.camera = cam

    # Réglages de rendu « par défaut raisonnables » (le starter reste en EEVEE)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 50
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 48
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = "//renders/ch00_01_testcard_"
    scene.view_settings.view_transform = "AgX"
    return scene


def configure_cycles_gpu(scene, samples=128):
    """Réglages de la solution : Cycles, GPU, échantillons, débruitage."""
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU"
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02
    scene.cycles.use_denoising = True
    scene.cycles.preview_samples = 32
    scene.render.resolution_percentage = 100


def inject_faults(scene):
    """Cinq pannes classiques qui donnent une image noire, vide ou minuscule."""
    cam = scene.camera
    cam.data.clip_end = 0.5                                   # 1. clip end trop court
    bpy.data.objects["LGT_Key"].hide_render = True            # 2. key light désactivée au rendu
    bg = next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Strength"].default_value = 0.0                 # 3. monde éteint
    bpy.data.collections["PROPS"].hide_render = True          # 4. collection masquée au rendu
    scene.render.resolution_percentage = 10                   # 5. résolution à 10 %


def save(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Pas de copie .blend1 lors des régénérations. À régler juste avant l'enregistrement :
    # read_factory_settings() (reset_scene) recharge les préférences d'usine.
    # Réglage de session uniquement, les préférences ne sont pas sauvegardées.
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=True)
    print(f"[BCMA] saved {path}")


def main():
    # 1. Starter « mire »
    build_testcard()
    save(os.path.join(STARTER_DIR, "ch00_01_testcard_starter.blend"))

    # 2. Solution « mire » : Cycles GPU
    scene = build_testcard()
    configure_cycles_gpu(scene)
    save(os.path.join(SOLUTION_DIR, "ch00_01_testcard_solution.blend"))

    # 3. Starter « panne »
    scene = build_testcard()
    configure_cycles_gpu(scene, samples=64)
    inject_faults(scene)
    save(os.path.join(STARTER_DIR, "ch00_01_broken_render_starter.blend"))

    # 4. Solution « panne » (identique à la scène saine en 64 échantillons)
    scene = build_testcard()
    configure_cycles_gpu(scene, samples=64)
    save(os.path.join(SOLUTION_DIR, "ch00_01_broken_render_solution.blend"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
