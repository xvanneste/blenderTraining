# CH18.22 — Mode opératoire des projets

## 1. Créer le dossier du projet
```text
MES_PROJETS/P18_05_animation/
  01_INTENTION.md        note d'intention, périmètre, jalons datés
  02_BOARD/              planches (.blend)
  03_ANIMATIC/           animatiques (.blend) + exports (.mp4)
  04_ANIM/               animation (.blend)
  05_REVIEW/             notes de revue par version
  AI_LOG.md              si une IA a été utilisée (CH18.21)
```

## 2. Partir du bon fichier
| Projet | Point de départ conseillé |
|---|---|
| 1 | `CH18_13_COMPLEX_BOARDS/STARTER_FILES/ch18_13_action_starter.blend` |
| 2 | `CH18_12_TECHNICAL_BREAKDOWN/STARTER_FILES/ch18_12_board_starter.blend` (+ cases ajoutées) ou une planche `bcma_board` de 8 cases |
| 3 | `CH18_14_ANIMATIC/STARTER_FILES/ch18_14_animatic_starter.blend` |
| 4 | votre animatique + `CH18_15_SOUND_EXPORT` (méthode du montage) |
| 5 | `CH18_16…` / `CH18_17…` / `CH18_18…` (feuille, guides, calques) |
| 6 | `CH18_19_DRAW_ON_3D/STARTER_FILES/ch18_19_hybrid_starter.blend` (votre décor dans `SET`) |
| 7 | vos planches (projet 1–2) + montage (projet 4) à l'échelle d'un court |

## 3. Vérifier à chaque jalon
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "MES_PROJETS\P18_05_animation\04_ANIM\p18_05_anim_v003.blend" `
  --python "18_GREASE_PENCIL\CH18_22_PROJECTS\SCRIPTS\validate_ch18_22.py" --python-exit-code 1 -- --exercise p5 --render
```
Remplacez `p5` par le numéro du projet. Les exemples techniques sont dans
`COMPLETED_EXAMPLES/` (ouvrez-les pour voir la structure attendue).

## 4. Revue et versions
1. Exportez (projets 3, 4, 7) ou faites un *View > Render Playblast* (projet 5).
2. Regardez en entier une fois, puis notez (code · image · remarque) dans `REVIEW_NOTES`.
3. Corrigez, incrémentez la version (`_v004`), relancez le correcteur, remplissez la grille.

## 5. Clore le projet
Un projet est clos quand : correcteur ✔ + grille ≥ seuil + export/rendu final archivé + note de fin
(ce que vous referiez autrement). Cochez-le dans votre suivi (le site hors ligne garde votre progression).
