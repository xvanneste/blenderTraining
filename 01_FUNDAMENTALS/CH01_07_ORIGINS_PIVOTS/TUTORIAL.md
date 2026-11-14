# CH01.07 — Tutoriels pas à pas

## Tutoriel 1 — Constater le problème
1. Ouvrez `STARTER_FILES/ch01_07_door_starter.blend`, cliquez `GEO_Door`.
2. `R Z 90` sans valider (bougez la souris) : la porte tourne **sur elle-même**, au milieu de
   l'encadrement. `Échap`.

## Tutoriel 2 — L'origine sur la charnière
1. `GEO_Door` sélectionnée, `Tab` (Edit Mode), mode sommets (`1`), `Alt+Z` (X-Ray).
2. Vue de face `Num 1` : sélectionnez au rectangle (`B`) le coin **bas gauche** : cela prend
   les 2 sommets (avant et arrière).
3. `Shift+S` → **Cursor to Selected** : le curseur 3D se place au milieu de cette arête,
   au sol, sur la charnière.
4. `Tab` (Object Mode), `Alt+Z`.
5. *Object → Set Origin → Origin to 3D Cursor*.
   ✅ Le point orange est sur la charnière ; la porte n'a pas bougé.
6. `R Z 90 Entrée`. ✅ La porte s'ouvre en restant accrochée au cadre.

## Tutoriel 3 — Les boulons autour de la roue
1. Cliquez `GEO_Wheel`, `Shift+S` → **Cursor to Selected** (curseur au centre de la roue).
2. `.` (menu du pivot) → **3D Cursor**.
3. Sélectionnez les 3 boulons (`Shift`+clic, ou *Select Pattern* `GEO_Bolt_*`).
4. `R Z 45 Entrée`. ✅ Les boulons tournent ensemble autour du centre de la roue.
5. Comparez : `Ctrl+Z`, pivot **Median Point**, `R Z 45` : ils tournent autour de **leur**
   centre moyen (décalé) — faux. Pivot **Individual Origins** : chacun tourne sur lui-même.
6. Remettez le pivot sur *Median Point* (défaut) en fin d'exercice.

## Tutoriel 4 — Remettre le curseur à l'origine du monde
`Shift+S` → **Cursor to World Origin** (ou `Shift+C`, qui recentre aussi la vue).

## Tutoriel 5 — Vérifier
Enregistrez `ch01_07_door_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_07_door_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_07.py" --python-exit-code 1 -- --exercise door
```
