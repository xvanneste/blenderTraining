# CH01.07 — Tutoriels pas à pas

## Tutoriel 1 — Constater le problème
1. Ouvrez `STARTER_FILES/ch01_07_door_starter.blend`, cliquez `GEO_Door`.
2. `R Z 90` sans valider (bougez la souris) : la porte tourne **sur elle-même**, au milieu de
   l'encadrement. `Échap`.

## Tutoriel 2 — L'origine sur la charnière
1. `GEO_Door` sélectionnée, `Tab` (Edit Mode), mode sommets (`1`), `Alt+Z` (X-Ray).
2. Vue de face `Numpad 1`. Pressez `Alt+A` pour retirer la sélection héritée. Avec `B`,
   tracez un petit rectangle sur le coin **bas gauche**. L’option X-Ray permet d’inclure
   les deux sommets, avant et arrière, qui se recouvrent dans cette vue.
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
5. Annulez cette rotation avec `Ctrl+Z`. Choisissez **Median Point** et lancez `R Z 45`
   sans confirmer. Le groupe pivote autour du centre de ses trois positions. Pressez
   `Échap`, puis faites le même aperçu avec **Individual Origins**. Les boulons tournent
   autour de leurs propres centres en conservant leur position.
6. Annulez l’aperçu et rétablissez le pivot **3D Cursor** pour appliquer la rotation de
   l’étape 4. Remettez ensuite le pivot sur *Median Point* pour le chapitre suivant.

## Tutoriel 4 — Remettre le curseur à l'origine du monde
`Shift+S` → **Cursor to World Origin** (ou `Shift+C`, qui recentre aussi la vue).

## Tutoriel 5 — Vérifier
Enregistrez `ch01_07_door_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_07_door_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_07.py" -- --exercise door
```

## Contrôle de transfert

Orientez la porte à 30° puis à 75° autour de Z en repartant de la même version initiale. Posez un repère visuel au niveau de la charnière. Si les rotations déplacent la charnière, vérifiez le point orange de la porte et le pivot de la vue. **Réussite** Le bord de la porte pivote autour d’un même axe, et vous pouvez expliquer pourquoi déplacer l’origine ne déplace pas les sommets à l’écran.
