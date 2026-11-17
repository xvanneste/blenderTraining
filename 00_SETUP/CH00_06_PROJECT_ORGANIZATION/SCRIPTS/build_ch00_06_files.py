"""
build_ch00_06_files.py — Scène « en désordre » à remettre aux normes (CH00.06).

  ASSETS/textures/tx_wood_planks.png      texture générée (grille UV colorée)
  STARTER_FILES/ch00_06_messy_scene_starter.blend
      Noms par défaut (Cube.001…), collections « Collection 2 », matériaux « Material.002 »,
      texture liée en CHEMIN ABSOLU.
  COMPLETED_EXAMPLES/ch00_06_messy_scene_solution.blend
      Même scène conforme : GEO_/CAM_/LGT_, collections SET/PROPS/LIGHTS/CAMERAS, MAT_,
      chemin relatif.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch00_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
TEX = os.path.join(CH, "ASSETS", "textures", "tx_wood_planks.png")

NOTE = """CH00.06 — SCÈNE EN DÉSORDRE
Remettez cette scène aux normes de DOCUMENTATION/CONVENTIONS.md :
- objets préfixés (GEO_, CAM_, LGT_) avec des noms parlants, sans .001
- collections en MAJUSCULES : SET, PROPS, LIGHTS, CAMERAS
- matériaux MAT_Nom
- texture en chemin relatif (File > External Data > Make Paths Relative)
- enregistrez sous ch00_06_messy_scene_<prenom>_v001.blend
"""


def make_texture():
    os.makedirs(os.path.dirname(TEX), exist_ok=True)
    img = bpy.data.images.new("tx_tmp", 512, 512)
    img.generated_type = "COLOR_GRID"
    img.filepath_raw = TEX
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def build(clean):
    L.reset("SC_Room")
    n = (lambda a, b: b if clean else a)
    set_c = L.collection(n("Collection", "SET"))
    props = L.collection(n("Collection 2", "PROPS"))
    lights = L.collection(n("Collection 3", "LIGHTS"))
    cams = L.collection(n("Collection.001", "CAMERAS"))
    m_floor = L.material(n("Material", "MAT_Floor_Wood"), (0.5, 0.35, 0.2), 0.6)
    m_wall = L.material(n("Material.001", "MAT_Wall_Plaster"), (0.8, 0.78, 0.72), 0.8)
    m_box = L.material(n("Material.002", "MAT_Box_Cardboard"), (0.6, 0.45, 0.28), 0.7)
    # texture image sur le sol
    img = bpy.data.images.load(TEX)
    img.name = "tx_wood_planks.png"
    nt = m_floor.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    L.plane(n("Plane", "GEO_Floor"), set_c, m_floor, size=6)
    L.plane(n("Plane.001", "GEO_Wall_Back"), set_c, m_wall, size=6, location=(0, 3, 3),
            rotation=(1.5708, 0, 0))
    for i in range(3):
        L.cube(n(f"Cube.00{i + 1}" if i else "Cube", f"GEO_Box_{i + 1:02d}"), props, m_box, size=0.5,
               location=(-1 + i, 0.5 * i, 0.25 + 0.5 * (i == 2)))
    tgt = L.empty(n("Empty", "EMP_CamTarget"), cams, (0, 0.5, 0.5))
    L.light(n("Light", "LGT_Key"), lights, "AREA", (-2, -2, 3), 300, 1.5, target=tgt)
    L.camera(n("Camera", "CAM_Main"), cams, (3, -5, 2), 35, tgt)
    L.render_defaults("BLENDER_EEVEE", 50, out="//renders/room_")
    L.instructions(NOTE)


def main():
    make_texture()
    build(False)
    path = os.path.join(CH, "STARTER_FILES", "ch00_06_messy_scene_starter.blend")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    # relative_remap=False : on garde volontairement le chemin ABSOLU de la texture
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=False)
    build(True)
    path = os.path.join(CH, "COMPLETED_EXAMPLES", "ch00_06_messy_scene_solution.blend")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_mainfile()
    print("[BCMA] fichiers CH00.06 enregistrés")


if __name__ == "__main__":
    L.run(main)
