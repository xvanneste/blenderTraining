# CH00.05 — Tutoriels pas à pas

## Tutoriel 1 — Inventaire
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b `
  --python "SCRIPTS\bcma_extensions_report.py"
```
✅ Vous voyez l'état de l'accès en ligne, les dépôts et les add-ons activés (au minimum
`cycles` et le gestionnaire d'extensions `bl_pkg`).

## Tutoriel 2 — Activer un add-on livré : Node Wrangler
1. *Edit → Preferences → Add-ons*.
2. Champ de recherche : `node wrangler`.
3. Cochez la case de **Node Wrangler**.
   ✅ La case est cochée ; Node Wrangler sera utilisé en phase 4 (`Ctrl+Shift+clic` sur un
   nœud pour le prévisualiser, `Ctrl+T` pour ajouter des nœuds de texture…).
4. Activez de la même façon **Rigify** (phase 6).

## Tutoriel 3 — Autoriser l'accès en ligne (en connaissance de cause)
1. *Preferences → Get Extensions*. Si l'accès en ligne est refusé, un message propose
   **Allow Online Access**.
2. Ou : *Preferences → System → Network → Allow Online Access*.
3. *Get Extensions* liste maintenant le catalogue d'extensions.blender.org. Recherchez un
   terme (ex. `align`), lisez la fiche (licence, auteur, permissions) **avant** d'installer.
> L'académie ne demande d'installer **aucune** extension tierce obligatoire. Les
> extensions utiles seront proposées dans les chapitres concernés, toujours en option.

## Tutoriel 4 — Installer depuis le disque : l'extension d'exemple BCMA Hello
1. Le paquet est prêt : `ASSETS/bcma_hello-1.0.0.zip` (construit par l'outil officiel).
2. *Preferences → Get Extensions* (ou *Add-ons*) → menu ˅ en haut à droite →
   **Install from Disk…** → choisissez le `.zip`.
   (Alternative : glissez-déposez le `.zip` dans la fenêtre de Blender.)
3. Dans la vue 3D, ouvrez la sidebar (`N`) → onglet **BCMA**.
   ✅ Le panneau affiche le nombre d'objets. Sélectionnez tout (`A`), cliquez
   *Préfixer les noms (BCMA)* : `Cube` devient `GEO_Cube`, `Camera` → `CAM_Camera`,
   `Light` → `LGT_Light`. `Ctrl+Z` annule.
4. Désinstallation : *Get Extensions* (ou *Add-ons*) → section *Installed* (ou dépôt
   *User Default*) → menu de l'extension → **Uninstall**.

## Tutoriel 5 — Construire et valider une extension (méthode développeur)
```powershell
cd "00_SETUP\CH00_05_EXTENSIONS\ASSETS"
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -c extension validate bcma_hello
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -c extension build --source-dir bcma_hello --output-dir .
```
✅ `Success parsing TOML` puis `created: ".\bcma_hello-1.0.0.zip"`.

## Tutoriel 6 — Lire un paquet inconnu avant installation
1. Clic droit sur le `.zip` → *Ouvrir avec → Explorateur* (ou *Extraire* dans un dossier vide).
2. Ouvrez `blender_manifest.toml` avec le Bloc-notes : vérifiez `license`, `maintainer`,
   et la section `[permissions]`.
3. Survolez le code (`__init__.py`) : cherchez `urllib`, `requests`, `socket`,
   `subprocess`, `os.remove`… Rien d'anormal n'est pas une garantie, mais quelque chose
   d'anormal est un signal d'arrêt.
