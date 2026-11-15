# CH18.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_12_board_starter.blend` : gabarit de 6 cases 16:9 avec un bandeau de notes
sous chaque case. `Num 0`.

## Tutoriel 1 — Dessiner les 6 plans
1. `GP_Practice`, Draw Mode, calque **USER_Drawing**.
2. Une séquence courte (exemple : « La tasse ») : PE d'installation, PM, PRP, insert, GP, PE final.
3. Dessinez au-delà du bord de la case puis effacez l'excédent (`Ctrl+clic`), ou arrêtez le trait au
   cadre.

## Tutoriel 2 — Les flèches
1. Calque **USER_Arrows**, matériau rouge (`U` → nouveau matériau rouge si besoin).
2. Travelling avant (case 2) : 4 petites flèches en tirets des coins vers le centre.
3. Panoramique (case 3) : flèche en tirets au-dessus de la case. Déplacement d'un personnage (case 6) :
   flèche pleine dans la case.

## Tutoriel 3 — Les annotations
1. `Ctrl+Tab` → Object Mode. Placez le curseur 3D sous la case 1 (`Shift+clic droit`).
2. *Add → Text*. Le texte est couché : `R` `X` `90` `Entrée` (face à la caméra de la feuille).
   `S` pour la taille (≈ 0,14).
3. `Tab` (édition du texte) : effacez « Text », tapez `SQ010_SH0010 · PE · fixe · 3 s`, `Tab`.
4. `F2` → `TXT_SH0010`. `Shift+D` pour dupliquer sous la case suivante, `Tab` pour modifier.
5. En haut : `TXT_Header` « Projet … — SQ010 — Page 01 ».

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_12_board_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_12.py" --python-exit-code 1 -- --exercise board --render
```
Référence : `COMPLETED_EXAMPLES/ch18_12_board_reference.png`.
