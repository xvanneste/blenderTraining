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
4. Ctrl+A > *Rotation & Scale* (échelle appliquée).
5. Object Data Properties > *Remesh* : *Voxel Size* 0,012 → **Voxel Remesh**. Edit Mode, L : un seul
   morceau.

## Tutoriel 2 — Essayer DynTopo (sans correcteur)
1. Sur une copie de `SCULPT_Body`, Sculpt Mode, case **Dyntopo** dans l'en-tête.
2. *Detail Size* 8 px ; Snake Hook (K) : tirez une corne depuis le front. Wireframe (Overlays) : des
   triangles apparaissent là où vous sculptez.
3. Pour finir : Dyntopo décoché, Voxel Remesh (Ctrl+R) pour régulariser.

## Tutoriel 3 — Multiresolution
Ouvrez `STARTER_FILES/ch03_03_multires_starter.blend` (`SCULPT_HeadBase`, 384 faces).
1. Modifier Properties > *Add Modifier > Generate > Multiresolution*.
2. **Subdivide** cinq fois.
3. **Levels Viewport** 3, **Sculpt** 5, **Render** 5. Sculpt Mode : sculptez quelques rides ;
   changez *Sculpt* à 2 : vous retouchez les grandes formes sans perdre les détails.
4. N'appliquez pas le modificateur : la base de 384 faces reste intacte.

## Tutoriel 4 — Décider
Text Editor : texte `DECISIONS` ; écrivez une méthode par situation (`1: VOXEL`…).

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_03_remesh_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_03.py" --python-exit-code 1 -- --exercise remesh --render
```
Puis `-- --exercise multires` et `-- --exercise decide` sur votre fichier Multires.
