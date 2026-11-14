# CH00.06 — Tutoriels pas à pas

## Tutoriel 1 — Créer l'arborescence d'un film en une commande
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  --python "SCRIPTS\bcma_create_project.py" -- --root "G:\_formation\blender\BLENDER_CINEMA_MASTER_ACADEMY\PROJECTS" --name mon_premier_film --sequences 2 --shots 3
```
✅ `PROJECTS\mon_premier_film\` contient `00_admin` … `99_archive`, `03_shots\sq010\sh0010\layout`…,
un `README.md` et le dossier caché `.blender_project` (affichez les éléments masqués dans
l'explorateur : *Affichage → Afficher → Éléments masqués*).
(Avec `python bcma_create_project.py …` hors de Blender, seuls les dossiers sont créés.)

## Tutoriel 2 — Ouvrir le projet dans Blender
1. *File → Project → Open…* → choisissez `PROJECTS\mon_premier_film`.
2. Un menu **Project** apparaît dans la barre du haut → *Settings…* : nom, variables,
   bibliothèques d'assets.
3. Enregistrez un premier fichier dans `03_shots\sq010\sh0010\layout\` sous
   `mon_premier_film_sq010_sh0010_layout_v001.blend`.
   ✅ *File → Project* affiche le projet dans la liste des projets récents.

## Tutoriel 3 — Remettre une scène aux normes
1. Ouvrez `STARTER_FILES/ch00_06_messy_scene_starter.blend`.
2. **Collections** : dans l'Outliner, double-clic sur `Collection` → `SET`, puis
   `Collection 2` → `PROPS`, `Collection 3` → `LIGHTS`, `Collection.001` → `CAMERAS`.
3. **Objets** : cliquez un objet, `F2`, tapez le nouveau nom (ex. `GEO_Floor`), `Entrée`.
   Pour les trois boîtes : sélectionnez-les, *Edit → Batch Rename* (`Ctrl+F2`) →
   *Find* `Cube` / *Replace* `GEO_Box` ; puis corrigez les `.001` restants à la main
   (`GEO_Box_01`, `_02`, `_03`).
4. **Matériaux** : *Properties → Material* : double-clic sur le nom → `MAT_Floor_Wood`,
   `MAT_Wall_Plaster`, `MAT_Box_Cardboard`. (Ou Outliner en mode *Blender File* →
   *Materials*.)
5. **Chemins** : *File → External Data → Make Paths Relative*.
   Vérification : Shader Editor du sol → nœud *Image Texture* → panneau latéral `N` →
   onglet *Node* → le chemin commence par `//`.
6. Enregistrez sous `ch00_06_messy_scene_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_06_messy_scene_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch00_06.py" --python-exit-code 1 -- --exercise naming
```
✅ `RÉSULTAT : VALIDÉ`.

## Tutoriel 4 — Contrôler n'importe quel fichier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b "mon_fichier.blend" `
  --python "..\..\SCRIPTS\bcma_naming_check.py"
```
✅ Liste des problèmes (ou `0 problème(s)`).
