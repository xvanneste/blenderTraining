"""
build_ch10_07_files.py — « Rendu distribué » (CH10.07 : ligne de commande, rendu par morceaux, réglages sûrs pour une ferme).

Scène (Workbench, 64 × 36, 24 images à 24 i/s) : un cube Cube qui tourne (une clé de rotation Z : 0° à l'image 1, 360° à l'image 24), CAM ; sortie « //renders/shot_#### » en PNG.
  Le fichier contient un TEXTE « BATCH » : une commande Blender par ligne (les lignes qui commencent par # sont des commentaires), avec deux jokers : {BLEND} (ce fichier) et {OUT} (dossier de sortie).
  Consigne : écrire le plan de rendu par morceaux pour une ferme de 3 machines : trois commandes qui rendent chacune un tiers des images (1–8, 9–16, 17–24), sans trou ni recouvrement :
      blender -b {BLEND} -o {OUT}/shot_#### -F PNG -s 1 -e 8 -a
    (l'ordre compte : les arguments sont exécutés dans l'ordre donné ; « -a » doit venir APRÈS « -s » et « -e » : mesuré, « -a -s 1 -e 2 » rend les 6 images de la scène, « -s 1 -e 2 -a » en rend 2) ;
    et régler la scène pour une ferme : Output Properties > Output : Overwrite désactivé, Placeholders activé (use_overwrite = False, use_placeholder = True).
  Le correcteur n'exécute QUE des commandes de sa liste blanche (-b, -o, -F, -s, -e, -a, -x, -t ; premier mot « blender », second {BLEND}) : il remplace {BLEND} par ce fichier et {OUT} par un dossier temporaire PAR MORCEAU, ajoute --factory-startup,
  lance Blender pour chaque ligne et compte les fichiers produits : images dans la plage, aucune hors plage, union = 1 à 24 exactement une fois.
  Départ : lignes « -a -s 1 -e 8 » (ordre faux), « -s 9 -e 16 -a » et « -s 18 -e 24 -a » (l'image 17 manque) ; Overwrite activé, Placeholders désactivé.
  STARTER_FILES/ch10_07_batch_starter.blend ; COMPLETED_EXAMPLES/ch10_07_batch_solution.blend (+ _reference.png : une image par tiers)
  COUNTER_EXAMPLES/ : wrong_order, gap, overlap, one_chunk (une seule commande 1–24), no_placeholders, forbidden_flag (--python-expr)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_07_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH10.07 — RENDU DISTRIBUÉ (Cube, CAM, texte BATCH)
Trois machines doivent se partager les 24 images. Dans le texte BATCH (Text Editor) : une commande par ligne ; {BLEND} = ce fichier, {OUT} = dossier de sortie.
Modèle : blender -b {BLEND} -o {OUT}/shot_#### -F PNG -s 1 -e 8 -a
Règles : trois commandes (1–8, 9–16, 17–24), sans trou ni recouvrement ; « -a » en DERNIER (les arguments s'exécutent dans l'ordre : « -a -s 1 -e 8 » rend tout).
Scène : Output Properties > Output : désactivez Overwrite, activez Placeholders (indispensables pour qu'une ferme n'écrase pas le travail d'une autre machine).
Vérification : SCRIPTS/validate_ch10_07.py -- --exercise batch
"""

CMD = "blender -b {BLEND} -o {OUT}/shot_#### -F PNG"
PLANS = {
    "starter": [f"{CMD} -a -s 1 -e 8", f"{CMD} -s 9 -e 16 -a", f"{CMD} -s 18 -e 24 -a"],
    "solution": [f"{CMD} -s 1 -e 8 -a", f"{CMD} -s 9 -e 16 -a", f"{CMD} -s 17 -e 24 -a"],
    "wrong_order": [f"{CMD} -a -s 1 -e 8", f"{CMD} -s 9 -e 16 -a", f"{CMD} -s 17 -e 24 -a"],
    "gap": [f"{CMD} -s 1 -e 8 -a", f"{CMD} -s 9 -e 16 -a", f"{CMD} -s 18 -e 24 -a"],
    "overlap": [f"{CMD} -s 1 -e 8 -a", f"{CMD} -s 8 -e 16 -a", f"{CMD} -s 17 -e 24 -a"],
    "one_chunk": [f"{CMD} -s 1 -e 24 -a"],
    "no_placeholders": [f"{CMD} -s 1 -e 8 -a", f"{CMD} -s 9 -e 16 -a", f"{CMD} -s 17 -e 24 -a"],
    "forbidden_flag": [f"{CMD} -s 1 -e 8 -a", f"{CMD} -s 9 -e 16 -a", "blender -b {BLEND} --python-expr print('x') -s 17 -e 24 -a"],
}


def build(kind):
    L.reset("SC_BATCH")
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.object
    cube.name = "Cube"
    cube.rotation_euler = (0, 0, 0)
    cube.keyframe_insert("rotation_euler", index=2, frame=1)
    cube.rotation_euler.z = math.radians(360)
    cube.keyframe_insert("rotation_euler", index=2, frame=24)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -6, 2)
    cam.rotation_euler = (math.radians(70), 0, 0)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    sc.frame_start, sc.frame_end = 1, 24
    sc.render.fps = 24
    sc.render.filepath = "//renders/shot_####"
    sc.render.image_settings.file_format = "PNG"
    farm = kind not in ("starter", "no_placeholders")
    sc.render.use_overwrite = not farm
    sc.render.use_placeholder = farm
    txt = bpy.data.texts.new("BATCH")
    txt.write("# Une commande par ligne. {BLEND} = ce fichier, {OUT} = dossier de sortie. Les lignes # sont des commentaires.\n" + "\n".join(PLANS[kind]) + "\n")
    sc.frame_set(1)
    L.instructions(NOTE)


def sketch(path):
    """Trois images de la solution (une par tiers : 4, 12, 20), rendues séparément, côte à côte."""
    build("solution")
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 192, 108
    sc.render.image_settings.file_format = "PNG"
    tiles = []
    for f in (4, 12, 20):
        sc.frame_set(f)
        p = os.path.join(tempfile.gettempdir(), f"bcma_ch1007_{f}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        tiles.append(np.array(im.pixels[:], np.float32).reshape(108, 192, 4)[..., :3])
        bpy.data.images.remove(im)
    img = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba.ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_07_batch_starter.blend"))
    for k in ("wrong_order", "gap", "overlap", "one_chunk", "no_placeholders", "forbidden_flag"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_07_batch_{k}.blend"))
    sketch(os.path.join(out, "ch10_07_batch_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_07_batch_solution.blend"))


if __name__ == "__main__":
    L.run(main)
