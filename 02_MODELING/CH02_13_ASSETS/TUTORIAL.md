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
1. *Edit → Preferences → Asset Libraries* → **+**. Sélectionnez le dossier contenant
   le `.blend` enregistré et le fichier de catalogues. Donnez un nom reconnaissable à
   la bibliothèque dans les préférences.
2. Dans un nouveau `.blend`, ouvrez l’Asset Browser et choisissez cette bibliothèque.
   Glissez le tabouret dans la scène après avoir choisi *Link* comme méthode d’import.
3. Recommencez dans une deuxième scène avec *Append*. Comparez dans l’Outliner la
   référence liée et la copie locale. Enregistrez et rouvrez chaque scène avec la
   bibliothèque à la même place pour vérifier qu’elle reste utilisable.

[Manuel Blender 5.3 des bibliothèques d’assets](https://docs.blender.org/manual/en/5.3/editors/preferences/asset_libraries.html)

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "ASSETS\ch02_13_library_<prenom>.blend" `
  --python-exit-code 1 --python "02_MODELING\CH02_13_ASSETS\SCRIPTS\validate_ch02_13.py" -- --exercise library --render
```

## Variante de contrôle

Ouvrez une seconde scène et utilisez un seul asset depuis la bibliothèque prévue. Rouvrez la scène enregistrée et vérifiez la provenance du datablock. Comparez Link, qui garde une dépendance, et une copie locale adaptée à l’exercice. **Preuve** Identifiant, fichier source, emplacement dans le catalogue et comportement à la réouverture.
