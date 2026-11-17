# CH00.06 — Tutoriels pas à pas

## Premier jalon — Retrouver le projet, le plan et sa version

Le projet regroupe les fichiers de production. Le plan nomme un morceau destiné au montage. Le fichier .blend porte aussi la tâche et le numéro de version. Dans mon_premier_film_sq010_sh0010_layout_v001.blend, sq010 est la séquence, sh0010 le plan, layout la mise en place et v001 la version.

## Tutoriel 1 — Créer l’arborescence depuis la racine du cours

Exécutez ces commandes dans PowerShell à la racine du dépôt. Le dossier Atelier Blender de votre profil utilisateur accueillera le projet. Vous pouvez renseigner à la place un autre dossier de travail.

```powershell
$blender = "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe"
$destination = Join-Path $env:USERPROFILE "Atelier Blender"
& $blender -b --factory-startup --python-exit-code 1 --python "00_SETUP/CH00_06_PROJECT_ORGANIZATION/SCRIPTS/bcma_create_project.py" -- --root $destination --name mon_premier_film --sequences 2 --shots 3
```

Le projet contient 2 × 3 plans. Dans mon_premier_film, vérifiez le dossier 03_shots/sq010/sh0010/layout, le README et le dossier Blender .blender_project. Le script peut aussi créer les dossiers avec Python système. Le projet Blender intégré demande le binaire Blender.

## Tutoriel 2 — Ouvrir le projet dans Blender
1. *File → Project → Open…* → choisissez le dossier mon_premier_film créé au tutoriel 1.
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
5. **Chemins** : enregistrez d’abord une copie du projet et gardez les ressources associées disponibles. Dans Blender, appliquez *File → External Data → Make Paths Relative*.
   Vérification : Shader Editor du sol → nœud *Image Texture* → panneau latéral `N` →
   onglet *Node* → le chemin commence par `//`.
6. Rouvrez la copie et contrôlez la texture du sol. Un chemin qui commence par // est relatif à l’emplacement du .blend. Tester une autre racine exige de déplacer ou copier aussi la texture dans le même rapport de dossiers. Enregistrez sous `ch00_06_messy_scene_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_06_messy_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_06.py" -- --exercise naming
```
✅ `RÉSULTAT : VALIDÉ`.

## Tutoriel 4 — Contrôler n'importe quel fichier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b "mon_fichier.blend" `
  --python "..\..\SCRIPTS\bcma_naming_check.py"
```
✅ Liste des problèmes (ou `0 problème(s)`).
