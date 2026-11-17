# CH18.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_04_expressions_starter.blend`, `GP_Practice`, `Ctrl+Tab` → Draw Mode,
`Num 0`. Le GUIDE montre une tête de face construite (avec ses lignes) et une tête de trois-quarts.

## Tutoriel 1 — Une tête de face (USER_Heads)
1. Calque **USER_Heads** (`Y`).
2. Cercle du crâne (outil **Circle** ou main levée).
3. Axe vertical au centre ; ligne des yeux à mi-hauteur de la tête **complète** (prévoir la
   mâchoire sous le cercle).
4. Mâchoire en U jusqu'au menton sur l'axe.
5. Repères du nez et de la bouche (petites marques sur l'axe).

## Tutoriel 2 — Faire tourner la tête
1. Trois-quarts : décalez l'axe vers la droite en le courbant comme une ligne sur une balle ;
   l'œil de droite (au fond) devient plus étroit ; le nez dépasse l'axe vers la droite.
2. Profil : axe presque sur le bord du cercle ; un seul œil ; nez et menton en silhouette ;
   oreille au milieu du crâne.
3. Plongée / contre-plongée : courbez la ligne des yeux vers le bas / vers le haut.
4. Six têtes dans la bande du haut.

## Tutoriel 3 — Les six émotions (USER_Expressions)
1. Calque **USER_Expressions**. Dessinez 6 fois la même tête de face, sans les lignes de
   construction (ou très légères).
2. Pour chaque émotion, suivez le tableau du THEORY §2 : **sourcils d'abord**, puis paupières,
   puis bouche.
3. Test : cachez la bouche avec la main : l'émotion se lit-elle déjà dans les sourcils ?

## Tutoriel 4 — La feuille de modèle (USER_ModelSheet)
1. Calque **USER_ModelSheet**. Les trois lignes bleues sont : sommet du crâne, yeux, menton.
2. Dessinez votre personnage de **face** en respectant les trois lignes.
3. Puis de **trois-quarts** et de **profil** à côté : les yeux, le sommet et le menton restent
   sur les mêmes lignes.

## Tutoriel 5 — Vérifier
Enregistrez `ch18_04_expressions_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_04_expressions_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_04.py" -- --exercise expressions --render
```
Référence : `COMPLETED_EXAMPLES/ch18_04_expressions_reference.png`.

## Variante de contrôle

Dessinez une même expression sur tête de face et de trois-quarts. Gardez les axes du crâne et contrôlez la position relative des yeux et de la bouche. **Preuve** Le lecteur identifie l’expression et la direction du visage dans les deux vues.
