# CH02.13 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_13_library_starter.blend` : vos 6 props des chapitres précédents.
**Enregistrez d'abord une copie dans un dossier à vous** (`File → Save As`, par ex.
`ASSETS/ch02_13_library_<prenom>.blend`) : le fichier de catalogues sera écrit à côté.

## Tutoriel 1 — Marquer les assets
1. Sélectionnez les 6 objets (`A` dans le viewport).
2. *Object → Asset → Mark as Asset*. Chaque objet reçoit un petit aperçu.

## Tutoriel 2 — L'Asset Browser et les catalogues
1. Changez le type d'une zone (par ex. la Timeline) en **Asset Browser** ; bibliothèque :
   *Current File*.
2. Colonne de gauche : **+** pour créer `Props`, puis, clic droit dessus → nouveau sous-catalogue :
   `Mobilier`, `Accessoires`, `Nature`.
3. Glissez chaque asset sur son catalogue (tabouret → Mobilier ; arbre → Nature ; le reste →
   Accessoires).

## Tutoriel 3 — Documenter
1. Cliquez un asset, `N` (panneau latéral) : **Description**, **Author**, **License** ;
   **Tags** → **+** deux fois (ex. « bois », « intérieur »).
2. Aperçu : icône ⟳ sous la vignette (*Generate Preview*).
3. `Ctrl+S` : `blender_assets.cats.txt` apparaît à côté du fichier.

## Tutoriel 4 — Utiliser la bibliothèque ailleurs
1. *Edit → Preferences → Asset Libraries* → **+** → dossier de votre bibliothèque.
2. Nouveau fichier : Asset Browser → votre bibliothèque → glissez le tabouret dans la scène.
3. Testez *Link* puis *Append* (menu déroulant d'import de l'Asset Browser, ou *File → Link… /
   Append…*) et comparez dans l'Outliner (icône de lien).

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "ASSETS\ch02_13_library_<prenom>.blend" `
  --python "02_MODELING\CH02_13_ASSETS\SCRIPTS\validate_ch02_13.py" --python-exit-code 1 -- --exercise library --render
```
