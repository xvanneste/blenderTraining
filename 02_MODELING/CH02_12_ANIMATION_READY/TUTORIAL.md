# CH02.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_12_arm_starter.blend` : `GEO_Arm` (bras simplifié), `ARM_Arm` (deux os),
`EMP_Elbow` (repère du coude).

## Tutoriel 1 — Constater le problème
1. Sélectionnez `ARM_Arm`, `Ctrl+Tab` (Pose Mode), cliquez l'os **Forearm**.
2. `R` `X` `90` `Entrée` : le coude s'écrase et se vrille.
3. `Alt+R` (efface la rotation) : retour à la pose de repos. `Ctrl+Tab` pour sortir.

## Tutoriel 2 — Ajouter les boucles d'articulation
1. Sélectionnez `GEO_Arm`, `Tab`, vue de face (`Num 1`).
2. `Ctrl+R` en survolant une arête **verticale** près du coude : 1 coupe, glissez pour la placer à
   z ≈ 0,33 (ou validez puis `G` `Z` et tapez la valeur). Répétez pour 0,36, 0,27, 0,24.
3. Vous avez 5 boucles entre z = 0,24 et z = 0,36, resserrées autour du coude.

## Tutoriel 3 — Vérifier la déformation
1. `Tab`, `ARM_Arm`, Pose Mode, Forearm `R X 90` : le pli garde son volume.
2. `Alt+R`, sortez du Pose Mode, enregistrez **en pose de repos**.

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_12_arm_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_12.py" --python-exit-code 1 -- --exercise arm --render
```
Le correcteur plie le bras lui-même à 90° et mesure le volume conservé (≥ 95 %).
