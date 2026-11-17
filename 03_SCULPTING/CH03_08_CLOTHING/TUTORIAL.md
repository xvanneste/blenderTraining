# CH03.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_08_poncho_starter.blend` : le buste de CH03.05 (`SCULPT_Bust`), un **collider** simplifié
`COLLIDER` (affichage Wire, modificateur Collision, caché au rendu seulement), le sol `GEO_Floor` avec Collision, et `CLOTH_Poncho` :
un tissu **plat** à maille de 1,6 cm (≈ 0,54 × 0,54 m), troué au col, 20 cm au-dessus du sol. Sauvegardez sous
`ch03_08_poncho_<prenom>_v001.blend`.

## Tutoriel 1 — Lire la scène (15 min)
Num 1 puis Num 3 : le tissu doit être **au-dessus** des épaules, sans les toucher, avec un trou plus large que le cou. Sélectionnez
`COLLIDER` : Properties > Physics doit montrer *Collision* actif. Vérifiez qu'il n'est **pas** masqué (œil/écran barrés) : un objet
masqué dans la vue n'est pas évalué et le tissu le traverserait.

## Tutoriel 2 — Ajouter Cloth (20 min)
Sélectionnez `CLOTH_Poncho` > Properties > Physics > **Cloth**. Réglez : *Quality Steps* 12 ; *Physical Properties* : *Vertex Mass* 0,3,
*Air Viscosity* 2 ; *Stiffness* : *Tension* 15, *Compression* 15, *Shear* 5, *Bending* 0,4 ; *Damping* : *Tension* 5, *Compression* 5, *Shear* 5,
*Bending* 0,5 ; *Collisions* : *Quality* 5 ; *Object Collisions* : *Distance* 0,005 ; *Self Collisions* **décochées**.

## Tutoriel 3 — Simuler (20 min)
Revenez à l’image 1. Lancez la lecture ou avancez séquentiellement jusqu’à 120 pour laisser le solveur calculer les états
intermédiaires. Le tissu se pose sur les épaules. Si une face traverse le corps, inspectez le dégagement initial, les normales
du collider et la distance de collision. Rejouez depuis le début après chaque changement de réglage.

## Tutoriel 4 — Appliquer (5 min)
Gardez une copie du `.blend` avec la simulation modifiable. Dans le fichier à rendre, restez à l’image 120 et passez
en mode Objet. Dans le menu du modificateur **Cloth**, choisissez **Apply**. Revenez à l’image 1 et vérifiez que la
forme reste celle de l’image 120. Le correcteur attend ce maillage figé.

## Tutoriel 5 — Retoucher (facultatif, 40 min)
Sculpt Mode sur `CLOTH_Poncho` : brosses « Cloth » (*Pinch Folds Cloth*…), *Smooth*, *Draw Sharp* pour affirmer un pli. Vérifiez que le
tissu reste hors du corps.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_08_poncho_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_08.py" -- --exercise poncho --render
```
Ajoutez `--debug` pour les grandeurs brutes. Référence : `COMPLETED_EXAMPLES/ch03_08_poncho_reference.png`.

Remarque d'honnêteté : la simulation est exécutée par script ; la retouche du tutoriel 5 a été réalisée en vrai (Blender 5.2 via MCP : *Smooth* sur l'ourlet, *Crease Sharp* pour deux plis) ; les brosses *Cloth* n'ont pas été essayées. Le correcteur a été éprouvé (SOLUTIONS.md).

## Variante de contrôle

Comparez le tissu plat à l’image 1 et le drapé à l’image 120, sur la même scène avant application. Repérez un contact de
soutien à l’épaule, un pli libre et le passage au col. **Preuve** Deux vues de profil au même cadrage et une zone de contact
inspectée en vue rapprochée.
