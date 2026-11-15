# CH02.08 — Tutoriels pas à pas : l'arbre au modificateur Skin

Ouvrez `STARTER_FILES/ch02_08_tree_starter.blend`. `GEO_Tree` ne contient qu'un sommet, à l'origine.

## Tutoriel 1 — Le squelette
1. Sélectionnez `GEO_Tree`, `Tab`, mode sommet (`1`), `A`.
2. Tronc : `E` `Z` `0.8` `Entrée`, puis `E` `Z` `0.7` `Entrée` (sommet du haut à 1,5 m).
3. Branches : sélectionnez le sommet du haut ; `E` puis déplacez en diagonale (vue de face `Num 1`
   puis de côté `Num 3`), ≈ 0,8 m ; continuez avec 1 ou 2 extrusions pour courber la branche.
   Revenez au sommet du haut et recommencez dans 2 autres directions, plus une flèche centrale.
4. Racines : sélectionnez le sommet de la base, 3 extrusions courtes (≈ 35 cm) presque à plat.
5. Vous avez un squelette d'arêtes, sans faces.

## Tutoriel 2 — La chair (Skin + Subdivision)
1. `Tab` (Object Mode). *Add Modifier → Generate → Skin* : un volume carré apparaît autour.
2. *Add Modifier → Generate → Subdivision Surface* : *Levels* 1, *Render* 2. Le Skin doit être
   **au-dessus** du Subdivision dans la pile.
3. Skin : *Branch Smoothing* ≈ 0,6.

## Tutoriel 3 — Les rayons
1. `Tab`, sélectionnez le sommet de la base, **`Ctrl+A`** (*Skin Resize*) : agrandissez jusqu'à
   ≈ 18 cm.
2. Sommets des pointes : `Ctrl+A` vers ≈ 2–3 cm. Sommets intermédiaires : valeurs dégressives.
3. Vérifiez la silhouette en vue de face : le tronc s'affine, les branches s'effilent.
4. `Tab`, *Object → Shade Smooth*.

## Tutoriel 4 — Vérifier
Comparez avec `ch02_08_tree_reference.png` et le squelette `ch02_08_tree_skeleton.png`.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_08_tree_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_08.py" --python-exit-code 1 -- --exercise tree --render
```
