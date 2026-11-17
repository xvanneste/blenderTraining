# CH18.11 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_11_dialogue_starter.blend` : A (rouge, x = −1) et B (bleu, x = +1) se font
face, une table et une tasse entre eux. Scène de 288 images (12 s).

## Tutoriel 1 — Les six caméras
Méthode de cadrage de CH18.10 (`Ctrl+Num 0`, *View Lock → Camera to View*). Toutes les caméras du
côté **y < 0** (devant la ligne A–B).
1. `CAM_SH010` (35 mm) : A et B en pied, A à gauche.
2. `CAM_SH020` : derrière l'épaule gauche de A, vise B : B dans la moitié droite, l'épaule de A en amorce.
3. `CAM_SH030` : symétrique, derrière l'épaule de B, vise A : A dans la moitié gauche.
4. `CAM_SH040` / `CAM_SH050` : plans serrés de B (moitié droite) et de A (moitié gauche).
5. `CAM_SH060` : insert, très près de la tasse.

## Tutoriel 2 — Les marqueurs
1. Timeline, image 1 : `M` (marqueur), `F2` → `SH010`.
2. Images 49, 97, 145, 193, 241 : marqueurs `SH020` … `SH060`.
3. Pour chaque plan : sélectionnez la caméra dans le viewport, puis le marqueur dans la Timeline,
   **`Ctrl+B`** (*Marker → Bind Camera to Markers*). Une petite icône caméra apparaît sur le marqueur.
4. `Espace` en vue caméra (`Num 0`) : la scène se « monte » toute seule.

## Tutoriel 3 — La planche (`STARTER_FILES/ch18_11_board_starter.blend`)
Calque `USER_Board` : dessinez les 6 plans dans les 6 cases, avec une **flèche de regard** pour chaque
personnage. A toujours à gauche, B toujours à droite.

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_11_dialogue_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_11.py" -- --exercise dialogue
```
Puis la planche : `-- --exercise board --render`. Références : `ch18_11_dialogue_contact.png`,
`ch18_11_board_reference.png`.

## Variante de contrôle

Repérez la direction du regard aux deux bords d’une coupe. Testez une coupe qui change d’axe sur une copie. **Preuve** Vous pouvez expliquer la nouvelle lecture et proposer un plan de transition lorsque celle-ci devient confuse.
