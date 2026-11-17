# CH13.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch13_01_python_starter.blend`, espace de travail Scripting, texte `exercise.py`. Sauvegardez sous `ch13_01_python_starter_<prenom>_v001.blend`.

## Tutoriel 1 — clamp (15 min)
Remplacez `pass` par `return max(bas, min(haut, valeur))`. Testez dans la console Python : `clamp(5, 0, 3)` doit donner 3.

## Tutoriel 2 — average (15 min)
`if not valeurs: return 0.0` puis `return sum(valeurs) / len(valeurs)`.

## Tutoriel 3 — grid_positions et numbered_names (30 min)
Deux boucles `for j in range(ny)` puis `for i in range(nx)` ; ajoutez `(i * spacing, j * spacing, 0.0)` à une liste. Pour les noms : `[f"{prefix}_{i:03d}" for i in range(1, count + 1)]`.

## Tutoriel 4 — make_cubes (30 min)
Pour chaque (indice, position) : `bpy.ops.mesh.primitive_cube_add(size=1.0, location=p)`, `ob = bpy.context.object`, `ob.name = f"Cube_{i:03d}"`, ajoutez à la liste et renvoyez-la.

## Tutoriel 5 — Lancer le correcteur (10 min)
Text > Run Script pour vérifier l'absence d'erreur ; puis le correcteur : `--exercise python`.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch13_01_python_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch13_01.py" -- --exercise python --debug
```

Remarque d'honnêteté : le correcteur exécute vraiment le texte et appelle les fonctions (solution 56/56, starter 6/56, cinq contre-exemples chacun refusé sur sa seule fonction) ; la grille de la référence a été regardée (15 cubes alignés). Text > Run Script (Alt+P) et le Text Editor sont vérifiés dans `bl_ui/space_text.py` et la keymap ; les menus n'ont pas été regardés dans l'interface. Aucune notion avancée de Python (classes, modules, exceptions) n'est traitée ici.

## Vérification sur une variante

Rejouez la fonction avec une, trois puis quatre colonnes. Comparez longueur, premier et dernier élément. Vérifiez les pas constants et l’origine à 0. Reprenez l’exercice Blender quand les valeurs attendues et obtenues concordent.
