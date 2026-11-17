"""
build_ch00_07_files.py — Scénario de récupération (CH00.07).

  STARTER_FILES/ch00_07_recovery/ch00_07_hero_scene_v001.blend
      Le fichier ENREGISTRÉ APRÈS une erreur : le personnage GEO_Hero a été supprimé.
  STARTER_FILES/ch00_07_recovery/ch00_07_hero_scene_v001.blend1
      La copie de sauvegarde automatique (Save Versions) : elle contient encore GEO_Hero.
  COMPLETED_EXAMPLES/ch00_07_hero_scene_v002.blend
      Version récupérée et ré-enregistrée en v002.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch00_07_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
REC = os.path.join(CH, "STARTER_FILES", "ch00_07_recovery")

NOTE = """CH00.07 — RÉCUPÉRATION
Catastrophe : le personnage GEO_Hero a été supprimé PUIS le fichier a été enregistré.
Ctrl+Z ne peut plus rien (le fichier a été rouvert).
Votre mission : retrouver GEO_Hero sans rien refaire, et enregistrer la version
récupérée sous ch00_07_hero_scene_v002.blend (dans votre dossier de travail).
"""


def build():
    L.reset("SC_Hero")
    tg = L.studio(subject_height=1.6)["target"]
    props = L.collection("PROPS")
    chars = L.collection("CHARACTERS")
    m = L.material("MAT_Hero_Skin", (0.85, 0.55, 0.4), 0.45)
    hero = L.mesh(bpy.ops.mesh.primitive_monkey_add, "GEO_Hero", chars, m, size=1.2, location=(0, 0, 1.2))
    hero.modifiers.new("Subdivision", "SUBSURF").render_levels = 2
    for p in hero.data.polygons:
        p.use_smooth = True
    L.cube("GEO_Crate", props, L.material("MAT_Crate", (0.4, 0.3, 0.2)), size=0.6, location=(1.4, 0.4, 0.3))
    L.cylinder("GEO_Barrel", props, L.material("MAT_Barrel", (0.2, 0.25, 0.3), 0.4, 0.6),
               radius=0.3, depth=0.9, location=(-1.4, 0.4, 0.45))
    L.render_defaults("BLENDER_EEVEE", 50, out="//renders/hero_")
    L.instructions(NOTE)
    return hero


def main():
    os.makedirs(REC, exist_ok=True)
    for f in os.listdir(REC):
        os.remove(os.path.join(REC, f))
    path = os.path.join(REC, "ch00_07_hero_scene_v001.blend")
    build()
    prefs = bpy.context.preferences.filepaths
    prefs.save_version = 1
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)       # 1er enregistrement (avec le héros)
    bpy.data.objects.remove(bpy.data.objects["GEO_Hero"], do_unlink=True)  # l'erreur
    bpy.ops.wm.save_mainfile()                                      # 2e : v001.blend1 = version intacte
    # Solution : la version récupérée, enregistrée en v002
    build()
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch00_07_hero_scene_v002.blend"))
    print("[BCMA] .blend1 présent :", os.path.exists(path + "1"))
    return 0 if os.path.exists(path + "1") else 1


if __name__ == "__main__":
    L.run(main)
