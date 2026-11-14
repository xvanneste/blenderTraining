# CH00.02 — Tutoriels pas à pas

## Tutoriel 1 — Sauvegarder vos préférences actuelles (avant de toucher à quoi que ce soit)
1. Fermez Blender.
2. Explorateur Windows → barre d'adresse : `%APPDATA%\Blender Foundation\Blender\5.3`.
3. Clic droit sur le dossier `config` → *Compresser en fichier ZIP*.
4. Renommez l'archive `config_5.3_AAAA-MM-JJ.zip` et rangez-la dans
   `DOCUMENTATION/backups/` de l'académie (créez le dossier).
   ✅ Vous pouvez désormais tout casser : il suffira de restaurer ce dossier.

## Tutoriel 2 — Visite guidée de la fenêtre Preferences
1. Lancez Blender 5.3. *Edit → Preferences*.
2. Cliquez chaque catégorie de la colonne de gauche, de **Interface** à **File Paths**,
   en lisant les titres de panneaux (5 minutes). Ne modifiez rien.
3. Tapez `undo` dans la barre de recherche en haut : seul *Undo Steps* (System) reste.
   Effacez la recherche.
4. Ouvrez le menu **☰** en bas à gauche : repérez *Auto-Save Preferences*,
   *Revert to Saved Preferences*, *Load Factory Preferences*.
   ✅ *Auto-Save Preferences* est coché.

## Tutoriel 3 — Interface
1. *Interface → Display → Resolution Scale* : essayez 1.25 puis revenez à la valeur
   confortable pour votre écran (le texte des menus doit se lire sans effort à 60 cm).
2. *Interface → Status Bar* : cochez **Scene Statistics**, **System Memory**,
   **Video Memory**, **Blender Version**.
   ✅ La barre d'état (bas de la fenêtre principale) affiche par exemple
   `Objects 0/3 | Vertices 8 | … | 5.3.0`.
3. *(Facultatif)* *Themes* : menu des presets en haut → essayez *Blender Light* puis
   revenez à *Blender Dark*.

## Tutoriel 4 — Navigation
1. *Navigation → Orbit & Pan* : cochez **Orbit Around Selection**.
2. Dans le même panneau, rubrique *Auto* : cochez **Depth** (Auto Depth) ;
   **Perspective** est déjà coché.
3. *Navigation → Zoom* : cochez **Zoom to Mouse Position**.
4. Si vous n'avez **pas de pavé numérique** : *Input → Keyboard → Emulate Numpad*.
5. Si vous travaillez au **trackpad** ou sans bouton central : *Input → Mouse →
   Emulate 3 Button Mouse*.
   ✅ Dans la vue 3D, sélectionnez la caméra (clic gauche) puis orbitez (bouton du milieu
   glissé, ou `Alt`+clic gauche) : la vue tourne autour de la caméra.

## Tutoriel 5 — Sécurité
1. *System → Memory & Limits → Undo Steps* : **64**.
2. *Save & Load → Blend Files* : **Save Versions = 2** ; *Auto-Save* coché, **Timer
   (Minutes) = 2**.
3. *Save & Load → Default To* : **Relative Paths** coché.
   ✅ Fermez la fenêtre Preferences : tout est enregistré (auto-save).

## Tutoriel 6 — Vérifier par script (audit)
Depuis PowerShell, dans le dossier du chapitre :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b `
  --python "SCRIPTS\bcma_prefs_profile.py" -- --audit --strict
```
✅ Le rapport se termine par `Écarts : 0 (dont 0 obligatoire(s))` ou n'affiche que des
écarts marqués `–` (facultatifs). Sans clavier numérique, ajoutez `--no-numpad`.

> **Appliquer le profil automatiquement** (méthode « pro ») :
> `… --python "SCRIPTS\bcma_prefs_profile.py" -- --apply --save`
> (pas de `--factory-startup` ici : on veut modifier **vos** préférences).

## Tutoriel 7 — Naviguer dans la ville
1. Ouvrez `STARTER_FILES/ch00_02_navigation_playground.blend`.
2. Workspace **Scripting** → éditeur de texte → menu déroulant des textes →
   `README_EXERCICE` : lisez les consignes. Revenez au workspace **Layout**.
3. **Méthode lente** : cherchez à l'œil l'aiguille rouge en orbitant/zoomant.
4. **Méthode rapide** : dans l'**Outliner** (en haut à droite), dépliez `PROPS`, cliquez
   `GEO_Needle`, placez la souris dans la vue 3D, touche `.` du pavé numérique
   (*View → Frame Selected*).
   ✅ La vue cadre une petite tige rouge dans une rue.
5. Touche `Home` (*View → Frame All*) : vous revoyez toute la ville… mais la balise bleue
   `GEO_FarBeacon` (à 1 km) éloigne beaucoup le cadrage. Sélectionnez-la, `.` : elle
   peut disparaître ou se couper → sidebar `N` → onglet *View* → *Clip End* : passez à 5000 m.

## Tutoriel 8 — Placer une caméra là où l'on regarde
1. Cadrez l'aiguille en gros plan dans la vue (étape 4 ci-dessus, puis zoom molette).
2. *View → Cameras → Set Active Object as Camera* nécessite de sélectionner la caméra :
   cliquez `CAM_Needle` dans l'Outliner, puis `Ctrl+Num 0`.
3. Revenez à votre point de vue (`Num 0` pour quitter… ou recadrez l'aiguille), puis
   *View → Align View → Align Active Camera to View* (`Ctrl+Alt+Num 0`).
   ✅ Le cadre caméra (rectangle) montre l'aiguille en gros plan.
4. Ajustez avec *Object Data (caméra) → Lens → Focal Length* (85 mm = téléobjectif court).
5. `Shift+Ctrl+S` → `ch00_02_navigation_<prenom>_v001.blend`.
