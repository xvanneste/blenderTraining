# CH18.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_05_composition_starter.blend`, sélectionnez `GP_Practice`,
`Ctrl+Tab` → Draw Mode, `Num 0`. Le calque GUIDE (verrouillé) contient les cadres 16:9 et leur
grille des tiers.

## Tutoriel 1 — Six vignettes (USER_Thumbnails)
1. Calque **USER_Thumbnails** (`Y` pour changer de calque).
2. Une règle par cadre, 2 minutes maximum par vignette, de gauche à droite et de haut en bas :
   tiers, lignes directrices, symétrie, diagonale, cadre dans le cadre, gros plan avec espace de
   regard.
3. Pas de détail : des lignes, des masses, des personnages en bâtons ou en mannequins.

## Tutoriel 2 — Une vignette en trois valeurs (USER_Values)
1. Calque **USER_Values**, grand cadre en haut à droite.
2. Tracez trois lignes de masses : montagnes lointaines (haut), collines (milieu), talus ou rocher
   au premier plan.
3. **Fond clair** : hachures très espacées (ou rien). **Plan moyen** : hachures moyennes.
   **Premier plan** : hachures serrées, rayon plus gros (`F` pour la taille du pinceau).
4. Placez votre personnage sur un tiers, **sombre sur zone claire**.
5. Plissez les yeux : le personnage doit ressortir immédiatement.

## Tutoriel 3 — Un décor en trois plans (USER_Planes)
1. Observez l'exemple de gauche : réverbère épais au premier plan, maison et personnage au plan
   moyen, collines en trait fin au fond.
2. Calque **USER_Planes**, cadre de droite : composez votre propre décor (forêt, ville, intérieur…).
3. Variez l'épaisseur : épais devant, moyen au milieu, fin au fond.

## Tutoriel 4 — Vérifier
Enregistrez `ch18_05_composition_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_05_composition_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_05.py" -- --exercise composition --render
```
Référence : `COMPLETED_EXAMPLES/ch18_05_composition_reference.png`.

## Variante de contrôle

Comparez six cadres à leur taille de miniature. Choisissez trois valeurs, puis déplacez un objet secondaire dans une copie pour tester la lecture du sujet. **Preuve** La nouvelle vignette améliore le point focal sans modifier le récit.
