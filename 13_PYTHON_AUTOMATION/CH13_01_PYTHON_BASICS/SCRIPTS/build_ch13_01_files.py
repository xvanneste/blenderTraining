"""
build_ch13_01_files.py — « Python pour artistes » (CH13.01 : variables, listes, boucles, fonctions, première scène par script).

Le fichier contient un TEXTE « exercise.py » (à ouvrir dans le Text Editor, espace de travail Scripting) avec cinq fonctions à écrire :
  1. clamp(valeur, bas, haut) : ramène valeur dans [bas, haut] ;
  2. average(valeurs) : moyenne d'une liste de nombres ; liste vide : 0.0 (pas d'erreur) ;
  3. grid_positions(nx, ny, spacing) : liste de (x, y, 0.0), de nx × ny positions, y varie le plus lentement (ligne par ligne : x varie d'abord) ; origine (0, 0, 0) ;
  4. numbered_names(prefix, count) : ["prefix_001", "prefix_002", …] (numéros sur 3 chiffres à partir de 1) ;
  5. make_cubes(positions) : crée un cube de 1 m dans la scène à chaque position et renvoie la liste des objets, nommés Cube_000, Cube_001, … (numéros sur 3 chiffres à partir de 0) ; chaque cube a sa position en location.
  Le correcteur EXÉCUTE le texte (dans Blender, avec bpy) et teste chaque fonction avec des cas précis ; une erreur dans une fonction n'empêche pas de tester les autres (compte rendu de l'erreur) ; chaque appel a 5 s au plus.
  Départ : cinq fonctions « à compléter » (elles renvoient None). Solution : les cinq fonctions écrites.
  STARTER_FILES/ch13_01_python_starter.blend ; COMPLETED_EXAMPLES/ch13_01_python_solution.blend (+ _reference.png : la grille de cubes créée par la solution)
  COUNTER_EXAMPLES/ : clamp_swapped (bornes inversées), average_crash (division par zéro sur la liste vide), grid_swapped (x et y échangés), names_nopad (sans zéros : prefix_1), cubes_origin (cubes tous à l'origine)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch13_01_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH13.01 — PYTHON POUR ARTISTES (texte « exercise.py »)
Ouvrez le texte exercise.py (espace de travail Scripting, Text Editor) et écrivez les cinq fonctions :
clamp, average, grid_positions, numbered_names, make_cubes (voir les commentaires dans le texte).
Exécutez le texte (Run Script) pour tester à la main ; le correcteur l'exécute lui-même.
Vérification : SCRIPTS/validate_ch13_01.py -- --exercise python
"""

HEADER = '''"""exercise.py — CH13.01 : cinq petites fonctions. Remplacez « pass » par votre code."""
import bpy


'''

STUBS = {
    "clamp": 'def clamp(valeur, bas, haut):\n    """Renvoie valeur ramenée dans [bas, haut] : clamp(5, 0, 3) -> 3 ; clamp(-2, 0, 3) -> 0 ; clamp(1, 0, 3) -> 1."""\n    pass\n',
    "average": 'def average(valeurs):\n    """Moyenne d\'une liste de nombres ; liste vide -> 0.0 : average([1, 2, 3]) -> 2.0."""\n    pass\n',
    "grid_positions": 'def grid_positions(nx, ny, spacing):\n    """nx * ny positions (x, y, 0.0) : x varie d\'abord (ligne par ligne). grid_positions(2, 2, 3) -> [(0, 0, 0), (3, 0, 0), (0, 3, 0), (3, 3, 0)]."""\n    pass\n',
    "numbered_names": 'def numbered_names(prefix, count):\n    """numbered_names("Rock", 3) -> ["Rock_001", "Rock_002", "Rock_003"] (3 chiffres, à partir de 1)."""\n    pass\n',
    "make_cubes": 'def make_cubes(positions):\n    """Crée un cube de 1 m par position dans la scène ; renvoie les objets, nommés Cube_000, Cube_001, … ; location = la position."""\n    pass\n',
}

GOOD = {
    "clamp": 'def clamp(valeur, bas, haut):\n    """Renvoie valeur ramenée dans [bas, haut]."""\n    return max(bas, min(haut, valeur))\n',
    "average": 'def average(valeurs):\n    """Moyenne ; liste vide -> 0.0."""\n    if not valeurs:\n        return 0.0\n    return sum(valeurs) / len(valeurs)\n',
    "grid_positions": 'def grid_positions(nx, ny, spacing):\n    """nx * ny positions (x, y, 0.0), x varie d\'abord."""\n    out = []\n    for j in range(ny):\n        for i in range(nx):\n            out.append((i * spacing, j * spacing, 0.0))\n    return out\n',
    "numbered_names": 'def numbered_names(prefix, count):\n    """prefix_001, prefix_002, …"""\n    return [f"{prefix}_{i:03d}" for i in range(1, count + 1)]\n',
    "make_cubes": 'def make_cubes(positions):\n    """Un cube de 1 m par position ; Cube_000, Cube_001, …"""\n    cubes = []\n    for i, p in enumerate(positions):\n        bpy.ops.mesh.primitive_cube_add(size=1.0, location=p)\n        ob = bpy.context.object\n        ob.name = f"Cube_{i:03d}"\n        cubes.append(ob)\n    return cubes\n',
}

BAD = {
    "clamp_swapped": ("clamp", 'def clamp(valeur, bas, haut):\n    return max(haut, min(bas, valeur))\n'),
    "average_crash": ("average", 'def average(valeurs):\n    return sum(valeurs) / len(valeurs)\n'),
    "grid_swapped": ("grid_positions", 'def grid_positions(nx, ny, spacing):\n    out = []\n    for i in range(nx):\n        for j in range(ny):\n            out.append((i * spacing, j * spacing, 0.0))\n    return out\n'),
    "names_nopad": ("numbered_names", 'def numbered_names(prefix, count):\n    return [f"{prefix}_{i}" for i in range(1, count + 1)]\n'),
    "cubes_origin": ("make_cubes", 'def make_cubes(positions):\n    cubes = []\n    for i, p in enumerate(positions):\n        bpy.ops.mesh.primitive_cube_add(size=1.0)\n        ob = bpy.context.object\n        ob.name = f"Cube_{i:03d}"\n        cubes.append(ob)\n    return cubes\n'),
}


def source(kind):
    parts = [HEADER]
    for n in STUBS:
        if kind == "starter":
            parts.append(STUBS[n])
        elif kind in BAD and BAD[kind][0] == n:
            parts.append(BAD[kind][1])
        else:
            parts.append(GOOD[n])
        parts.append("\n\n")
    return "".join(parts).rstrip() + "\n"


def build(kind):
    L.reset("SC_PY")
    sc = bpy.context.scene
    t = bpy.data.texts.new("exercise.py")
    t.write(source(kind))
    sc.frame_set(1)
    L.instructions(NOTE)


def sketch(path):
    """Grille de cubes de la solution (vue de dessus, Workbench)."""
    build("solution")
    ns = {"bpy": bpy}
    exec(compile(bpy.data.texts["exercise.py"].as_string(), "exercise.py", "exec"), ns)
    cubes = ns["make_cubes"](ns["grid_positions"](5, 3, 2.0))
    sc = bpy.context.scene
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (4, 2, 12)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 12
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y = 480, 270
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return cubes


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch13_01_python_starter.blend"))
    for k in BAD:
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch13_01_python_{k}.blend"))
    sketch(os.path.join(out, "ch13_01_python_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch13_01_python_solution.blend"))


if __name__ == "__main__":
    L.run(main)
