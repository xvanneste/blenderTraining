# CH03.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_01_proportions_starter.blend` : toise de 1,75 m (graduations en têtes à
gauche, repères nommés à droite), caméras de face et de profil, collection `MASSES` vide (cliquez-la
dans l'Outliner : les nouveaux objets y seront créés).

## Tutoriel 1 — La tête et le canon
1. Num 1 (vue de face), Num 5 si besoin (orthographique).
2. *Add > Mesh > UV Sphere* ; renommez **MASS_Head** (F2).
3. Sidebar (N) > *Item* : *Dimensions* X 0,16, Y 0,20, Z **0,233** (une tête = 1,75 / 7,5) ;
   *Location* Z = 1,75 − 0,117 = 1,633. Le menton tombe sur le repère « Menton 0,87 H ».

## Tutoriel 2 — Cage et bassin
1. UV Sphere → **MASS_Ribcage** : Dimensions ≈ 0,32 × 0,23 × 0,30, sous le cou (≈ 1,13 à 1,43 m).
2. UV Sphere → **MASS_Pelvis** : ≈ 0,33 × 0,23 × 0,19, son bas sur « Entrejambe 0,50 H » (0,875 m).

## Tutoriel 3 — Les membres d'un côté (_L = côté +X)
1. *Add > Mesh > Cylinder* (Vertices 16) → **MASS_Thigh_L** : de la hanche (≈ 0,95 m) au genou
   (0,49 m = 0,28 H), X ≈ 0,09.
2. **MASS_Shin_L** : du genou à la cheville (0,08 m). **MASS_Foot_L** : un cube aplati au sol, vers −Y.
3. **MASS_UpperArm_L** : de l'épaule (≈ 1,40–1,44 m) au coude (1,085 m = 0,62 H), X ≈ 0,22.
4. **MASS_Forearm_L** jusqu'au poignet (≈ 0,84 m) ; **MASS_Hand_L** jusqu'au bout des doigts (0,665 m).
Astuce : *Snap* (Shift+Tab) sur *Increment*, ou saisie directe des valeurs dans la Sidebar.

## Tutoriel 4 — Le côté droit par symétrie
1. Sélectionnez les 6 masses _L, Shift+D puis Échap (copie en place), puis **Ctrl+M**, **X**, Entrée :
   miroir sur X par rapport au point de pivot (réglez le pivot sur *3D Cursor* au centre du monde).
2. Renommez en _R (Ctrl+F2 *Batch Rename* : Find `_L.001`, Replace `_R`).

## Tutoriel 5 — Le contrapposto (exercice « gesture »)
1. Enregistrez une copie `…_gesture_v001.blend`.
2. Choisissez la jambe d'appui (droite) : déplacez bassin, cage, tête et bras pour que la tête soit
   à l'aplomb du pied droit (vue de face).
3. Bassin : R Y 8 (hanche droite plus haute) ; cage : R Y −6 (épaule droite plus basse) ; bras
   et tête suivent la cage.
4. Jambe libre (gauche) : genou avancé et plié, pied sur la pointe.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_01_proportions_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_01.py" --python-exit-code 1 -- --exercise adult --render
```
Références : `COMPLETED_EXAMPLES/ch03_01_adult_reference.png`, `…_gesture_reference.png` (face + profil).
