# CH03.03 — Tutoriels pas à pas

## Tutoriel 1 — Fusionner des masses par Voxel Remesh
Ouvrez `STARTER_FILES/ch03_03_remesh_starter.blend` (les 16 masses de CH03.01).
1. **Essai raté volontaire** (sur une copie) : sélectionnez seulement les masses (Alt+A pour tout
   désélectionner d'abord !), Ctrl+J, Voxel Remesh 0,012 : comptez les morceaux (Edit Mode, L sur un
   morceau). Vous en obtenez 3 : tête, buste + bras, bassin + jambes.
2. Revenez au starter. Ajoutez des **ponts** qui pénètrent leurs voisins :
   - `MASS_Neck` : cylindre de ~7 cm de rayon, du milieu de la tête jusque dans la cage ;
   - `MASS_Abdomen` : sphère étirée entre cage et bassin ;
   - `MASS_Shoulder_L/R` : sphères à la tête de chaque bras, qui touchent la cage.
3. **Alt+A** (rien de sélectionné), puis sélectionnez toutes les masses (`MASS_*` : Outliner ou
   *Select > Select Pattern*), Ctrl+J, F2 → `SCULPT_Body`.
4. En mode Objet, appliquez *Rotation & Scale* (`Ctrl+A`) pour travailler au pas prévu. En mode
   Édition, sélectionnez tout et recalculez les normales extérieures avec `Shift+N`.
5. *Object Data Properties → Remesh*. Réglez *Voxel Size* à 0,012 m, puis lancez **Voxel Remesh**.
   En mode Édition, pressez `Alt+A`, puis `L` sur le torse. Vérifiez que la sélection atteint aussi
   le crâne, les épaules et les jambes. Un volume isolé signale un contact insuffisant avant fusion.

## Tutoriel 2 — Essayer DynTopo (sans correcteur)
1. Sur une copie de `SCULPT_Body`, Sculpt Mode, case **Dyntopo** dans l'en-tête.
2. Choisissez un mode de détail relatif, réglez *Detail Size* à 8 px, puis prenez *Snake Hook*
   dans l’étagère. Tirez une corne depuis le front. Activez l’overlay Wireframe. Des
   triangles apparaissent là où vous sculptez.
3. Pour finir : Dyntopo décoché, Voxel Remesh (Ctrl+R) pour régulariser.

## Tutoriel 3 — Multiresolution
Ouvrez `STARTER_FILES/ch03_03_multires_starter.blend` (`SCULPT_HeadBase`, 384 faces).
1. Modifier Properties > *Add Modifier > Generate > Multiresolution*.
2. **Subdivide** cinq fois.
3. **Levels Viewport** 3, **Sculpt** 5, **Render** 5. Sculpt Mode : sculptez quelques rides ;
   changez *Sculpt* à 2 : vous retouchez les grandes formes sans perdre les détails.
4. Gardez le modificateur dans la pile. Vous pourrez rouvrir la cage de 384 faces et comparer
   les niveaux au même cadrage.

[Manuel Blender 5.3 des méthodes de résolution adaptative](https://docs.blender.org/manual/en/5.3/sculpt_paint/sculpting/introduction/adaptive.html)

## Tutoriel 4 — Décider
Text Editor : texte `DECISIONS` ; écrivez une méthode par situation (`1: VOXEL`…).

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_03_remesh_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_03.py" -- --exercise remesh --render
```
Puis `-- --exercise multires` et `-- --exercise decide` sur votre fichier Multires.

## Variante de contrôle

Enregistrez un état avant tout changement de résolution. Mesurez les sommets sur deux versions. Comparez jointures, bords serrés et détails larges. **Preuve** Vous identifiez à la fois une amélioration de surface et un détail perdu, et vous indiquez pourquoi vous gardez l’une des versions.
