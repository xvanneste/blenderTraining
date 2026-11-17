# CH18.10 — Tutoriels pas à pas

## Partie A — Les caméras (`STARTER_FILES/ch18_10_shots_starter.blend`)
Plateau : `CHR_A` (rouge, x = −1) et `CHR_B` (bleu, x = +1), 1,75 m, tournés vers −Y (la caméra
d'étude) ; une table et une tasse `PROP_Cup` devant A ; `CAM_00_Exemple`.

### Tutoriel 1 — Méthode de cadrage
1. `Shift+A` → *Camera*. `F2` → `CAM_02_PM`.
2. *View → Cameras → Set Active Object as Camera* (`Ctrl+Num 0`) : la vue passe par cette caméra.
3. `N` → onglet *View* → *View Lock* → **Lock : Camera to View** : naviguer déplace la caméra.
4. Cadrez A en pied : la tête et les pieds dans l'image, A remplit 55–95 % de la hauteur.
   Décochez *Camera to View* pour ne pas dérégler la caméra ensuite.
5. Astuce chiffrée (objectif 50 mm, image 16:9) : pour cadrer une hauteur H, placez la caméra à
   **d ≈ 2,47 × H** du sujet, à la hauteur du centre de la zone voulue.

### Tutoriel 2 — Les 7 valeurs sur A
Répétez pour `CAM_01_PE` (A minuscule), `CAM_03_PA` (bas de l'image à mi-cuisse ≈ 0,70 m),
`CAM_04_PRT` (taille ≈ 1,0 m), `CAM_05_PRP` (poitrine ≈ 1,3 m), `CAM_06_GP` (sous le menton),
`CAM_07_TGP` (les yeux seulement). Gardez A au centre horizontalement.

### Tutoriel 3 — Insert, angles, 180°
1. `CAM_08_INS` : très près de la tasse, qui occupe au moins le tiers du cadre.
2. `CAM_09_PLONGEE` : caméra à plus de 2,1 m, inclinée vers A. `CAM_10_CONTREPLONGEE` : caméra
   sous 1 m, inclinée vers le haut.
3. `CAM_11_CHAMP` : derrière l'épaule de A, cadre B. `CAM_12_CONTRECHAMP` : derrière l'épaule de B,
   cadre A. **Les deux du côté y < 0** (même côté de la ligne A–B).

### Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_10_shots_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_10.py" -- --exercise shots
```
Le correcteur affiche, pour chaque caméra, la valeur mesurée et la hauteur de coupe.

## Partie B — La planche (`STARTER_FILES/ch18_10_board_starter.blend`)
1. `GP_Practice`, Draw Mode, `Num 0`, calque **USER_Shots**.
2. Dans les 8 cadres : PE, PM, PA, PRT, PRP, GP, TGP, Insert — le même personnage, **coupé par le bord
   du cadre** au bon endroit (dessinez au-delà puis effacez, ou arrêtez le trait au cadre).
3. Vérification : `-- --exercise board --render`. Référence : `ch18_10_board_reference.png`.

## Variante de contrôle

Cadrez la même action en plan large et en détail en gardant l’axe de regard. Présentez les deux images séparément. **Preuve** Chaque image répond à une question différente et le lecteur peut situer le détail grâce au plan large.
