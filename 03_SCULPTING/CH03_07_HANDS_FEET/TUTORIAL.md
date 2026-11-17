# CH03.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_07_hand_starter.blend` (ou `…_foot_starter.blend`) : studio, caméras (`CAM_Top` = vue de dessus,
`CAM_Side`, `CAM_34`) et un guide `GP_Guide` : lignes horizontales (vue de dessus, Num 7).
Main : poignet (y = −0,04), crête du poignet (0), articulations de la paume (0,10), bout du majeur (0,18, en rouge).
Pied : arrière du talon (−0,015), milieu de la voûte (0,105), balle (0,19), bout du gros orteil (0,27, en rouge).

## Tutoriel 1 — La paume et le poignet
*Add > Mesh > UV Sphere* : paume (Dimensions 0,104 × 0,112 × 0,03 m à (0 ; 0,045 ; 0)), poignet (0,062 × 0,09 × 0,04 à
(0 ; −0,01 ; 0)). Ctrl+J plus tard, après avoir tout posé.

## Tutoriel 2 — Les doigts : trois phalanges
Pour chaque doigt : trois ellipsoïdes qui **se chevauchent largement** (≈ 40 %), proportions 45 / 30 / 25 %, rayon qui diminue
de 7 % à chaque phalange. Bases à x = +0,037 (index), +0,0125 (majeur), −0,0125 (annulaire), −0,0375 (auriculaire), à y = 0,095.
Longueurs totales : 7,0 / 8,0 / 7,3 / 5,7 cm. Inclinez les doigts de +8°, +1°, −6°, −14° (rotation Z) pour les écarter.
Sans chevauchement large, la jonction se pince (aspect « chapelet »).

## Tutoriel 3 — Le pouce
Trois ellipsoïdes (métacarpien épais 4,2 cm, deux phalanges de 3,2 et 2,6 cm), base à (0,046 ; 0,025), inclinaison ≈ 50° vers +X.
Le pouce doit atteindre à peu près la première articulation de l'index.

## Tutoriel 4 — Fusion, remesh, poignet
En mode Objet, sélectionnez uniquement les volumes de la main et appliquez leur échelle. Joignez-les avec `Ctrl+J`
et nommez l’objet `SCULPT_Hand`. Dans *Object Data → Remesh*, entrez *Voxel Size* = 0,0025 m et lancez **Voxel Remesh**
pour réunir les volumes qui se croisent. En mode Édition, désélectionnez tout et pressez `L` au-dessus de la paume.
La sélection liée doit atteindre chaque phalange. Si un doigt reste à part, reprenez son contact dans la copie avant remesh.
Lissez les raccords sans refermer les espaces entre les doigts. Pour aplanir la base du poignet, utilisez en mode
Édition *Mesh → Bisect* en y = −0,04 avec une normale de coupe +Y, *Clear Inner* et *Fill*.

## Tutoriel 5 — Le pied (à faire de même)
Talon (0 ; 0,035 ; 0,03 : 0,066 × 0,086 × 0,068), cheville (0 ; 0,018 ; 0,095 : 0,064 × 0,066 × 0,12), cou-de-pied/voûte
(0 ; 0,105 ; 0,05 : 0,072 × 0,156 × 0,054), balle (0 ; 0,19 ; 0,016 : 0,112 × 0,09 × 0,04), deux **patins** plats sous le talon et la
balle (centrés sur z = 0) pour la semelle. Cinq orteils de 2 segments, écartés de ≥ 5 mm. *Mesh > Bisect* à z = 0 (Clear Inner +
Fill) pour la semelle, et à z = 0,14 (Clear Outer + Fill) pour la jambe.

Contrôlez la silhouette de profil. Le talon et l’avant-pied portent sur le sol, la voûte dégage un espace entre les deux,
et le cou-de-pied rejoint la cheville par un raccord continu. Inspectez ce raccord en vue de trois quarts avant de lisser.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_07_hand_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_07.py" -- --exercise hand --render
```
Pour le pied : `-- --exercise foot`. Ajoutez `--debug` pour les pics (x, y, proéminence).

Remarque d'honnêteté : les cotes ci-dessus sont celles de la solution **générée par script** ; la solution est un mannequin
simplifié, pas un modèle anatomique ; un essai de finition à la brosse en 5.2 n'a rien changé de visible (SOLUTIONS.md). Le correcteur a été éprouvé.

## Variante de contrôle

Contrôlez la construction avant le détail. Dans la main, vérifiez la longueur de la paume et la silhouette du pouce. Dans le pied, vérifiez la ligne talon, voûte, avant-pied et le raccord à la cheville. **Preuve** Deux vues par région, et aucun joint ne dépend de deux pièces simplement superposées si le corps doit rester continu.
