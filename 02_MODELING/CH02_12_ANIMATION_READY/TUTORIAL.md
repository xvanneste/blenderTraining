# CH02.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_12_arm_starter.blend` : `GEO_Arm` (bras simplifié), `ARM_Arm` (deux os),
`EMP_Elbow` (repère du coude).

## Tutoriel 1 — Constater le problème
1. Sélectionnez `ARM_Arm`, `Ctrl+Tab` (Pose Mode), cliquez l'os **Forearm**.
2. `R` `X` `90` `Entrée` : le coude s'écrase et se vrille.
3. `Alt+R` (efface la rotation) : retour à la pose de repos. `Ctrl+Tab` pour sortir.

## Tutoriel 2 — Ajouter les boucles d'articulation
1. Sélectionnez `GEO_Arm`, `Tab`, vue de face (`Numpad 1`). Vérifiez que l’orientation
   est *Global* et que la boucle du coude se situe autour de z = 0,30 m.
2. `Ctrl+R` sur une arête verticale près du coude. Glissez une coupe vers z ≈ 0,33.
   Pour la placer numériquement après confirmation, lisez le Z médian dans *N → Item*,
   puis déplacez la boucle de la **différence** avec `G`, `Z`. Recommencez pour 0,36,
   0,27 et 0,24 sans croiser les boucles voisines.
3. Vous avez 5 boucles entre z = 0,24 et z = 0,36, resserrées autour du coude.

## Tutoriel 3 — Vérifier la déformation
1. `Tab`, `ARM_Arm`, Pose Mode, Forearm `R X 90` : le pli garde son volume.
2. `Alt+R`, sortez du Pose Mode, enregistrez **en pose de repos**.

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_12_arm_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_12.py" -- --exercise arm --render
```
Le correcteur applique une flexion simulée à 90°, avec sa propre interpolation autour
du coude. Il mesure le volume conservé (≥ 95 %) dans ce cas. La pose dans Blender
sert à inspecter séparément la déformation réelle du rig et de ses poids.

## Variante de contrôle

Après avoir ajouté les boucles d’articulation, comparez les mêmes poses neutre et fléchie du contrôle. Observez l’intérieur du pli et la continuité extérieure. Une boucle supplémentaire améliore le contrôle quand son espacement sert la flexion. **Preuve** Deux images au même cadre avec filaire et commentaire sur volume, pli et zone à reprendre.
