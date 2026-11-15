# CH02.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_10_optim_starter.blend`. Activez **Statistics**. `GEO_Statue_REF` est
cachée et verrouillée : n'y touchez pas.

## Tutoriel 1 — Decimate de la statue
1. Sélectionnez `GEO_Statue` : Statistics indique 31 488 faces, 62 976 triangles.
2. *Add Modifier → Generate → Decimate* : **Collapse**, **Ratio 0.2**. Le panneau du modificateur
   affiche le nombre de faces résultant ; Statistics : ≈ 12 600 triangles.
3. Comparez avec/sans (icône écran du modificateur) en Material Preview : la silhouette est identique.
4. Essayez Ratio 0,02 : la statue se dégrade (facettes sur les arcades, les oreilles). Revenez à 0,2.

## Tutoriel 2 — Les LOD en copies liées
1. Collection `LOD` (Outliner, clic droit → *New Collection*).
2. `GEO_Statue` sélectionnée : **`Alt+D`** puis `X` `1.3` `Entrée` ; `F2` → `GEO_Statue_LOD1` ; `M` →
   `LOD`. Dans son modificateur Decimate : Ratio **0.08**.
3. Encore `Alt+D` : `GEO_Statue_LOD2` à x = 0, Ratio **0.015**.
4. Vérifiez le partage : Object Data des trois objets → même nom de maillage (`ME_Statue`, avec le
   nombre d'utilisateurs « 3 »).

## Tutoriel 3 — Nettoyer l'import
1. `GEO_Imported`, `Tab`, `A`. Statistics : beaucoup de sommets.
2. **`M` → By Distance** : plusieurs milliers de sommets supprimés.
3. *Mesh → Clean Up → Delete Loose* : les 30 sommets et 10 arêtes isolés disparaissent.
4. `Shift+N` (normales cohérentes, CH02.04).

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_10_optim_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_10.py" --python-exit-code 1 -- --exercise optim --render
```
