# CH00.02 — Tutoriels pas à pas

## Premier jalon — Cadrer un objet et retrouver ses réglages

Ouvrez la [ville d’exercice](STARTER_FILES/ch00_02_navigation_playground.blend). Dans l’**Outliner**, cliquez sur GEO_Needle. Dans la vue 3D, lancez **View → Frame Selected**. Avec un pavé numérique, la touche du point réalise le même geste lorsque le pointeur se trouve dans la vue 3D. L’aiguille doit être cadrée sans déplacement de l’objet ni de la caméra. Un point de vue sert à observer. La caméra sert à rendre l’image.

**À refaire sans le pas-à-pas** Sélectionnez GEO_FarBeacon et cadrez-le. Si la balise se coupe en zoomant, revenez à l’aiguille et consultez le tutoriel 7. Gardez une capture ou indiquez le geste qui vous a permis de retrouver chaque objet.

## Tutoriel 1 — Sauvegarder vos préférences

1. Fermez Blender. Dans la barre d’adresse de l’Explorateur Windows, ouvrez %APPDATA%\Blender Foundation\Blender\5.3. Une installation portable utilise le dossier portable près de l’exécutable.
2. Si le dossier config existe, compressez-le dans une archive datée et ouvrez l’archive pour confirmer son contenu. userpref.blend contient les préférences et startup.blend contient le démarrage, s’il a été enregistré.
3. Si config est absent, notez que vous partez d’un profil sans configuration locale sauvegardée. Pour créer un premier point de retour, utilisez **Save Preferences** dans le menu de la fenêtre Preferences, fermez Blender, puis archivez le dossier créé.
4. Pour répéter une restauration, utilisez un profil de test distinct. Gardez l’archive d’origine et comparez deux réglages observables avant et après. Sur Windows, la commande ci-dessous démarre une instance avec un autre dossier de ressources.

```powershell
$ancienProfil = $env:BLENDER_USER_RESOURCES
try {
  $env:BLENDER_USER_RESOURCES = "$env:TEMP\BCMA_preferences_essai"
  & "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe"
} finally {
  $env:BLENDER_USER_RESOURCES = $ancienProfil
}
```

Pour essayer la restauration dans ce profil, fermez l’instance et copiez le dossier config de l’archive à l’intérieur de BCMA_preferences_essai. Relancez avec la même commande sans option factory-startup et vérifiez les réglages de référence. Si vous expérimentez aussi avec des extensions ou des préréglages, archivez les dossiers correspondants séparément.

## Tutoriel 2 — Visite guidée de la fenêtre Preferences
1. Lancez Blender 5.3. *Edit → Preferences*.
2. Cliquez chaque catégorie de la colonne de gauche, de **Interface** à **File Paths**,
   en lisant les titres de panneaux (5 minutes). Ne modifiez rien.
3. Tapez undo dans la recherche de la fenêtre et repérez **Undo Steps** dans **System**. Effacez la recherche.
4. Ouvrez le menu **☰** en bas à gauche : repérez *Auto-Save Preferences*,
   *Revert to Saved Preferences*, *Load Factory Preferences*.
   Repérez si **Auto-Save Preferences** est coché. Sinon, enregistrez explicitement si vous souhaitez conserver une modification.

## Tutoriel 3 — Interface
1. *Interface → Display → Resolution Scale* : essayez 1.25 puis revenez à la valeur
   confortable pour votre écran (le texte des menus doit se lire sans effort à 60 cm).
2. *Interface → Status Bar* : cochez **Scene Statistics**, **System Memory**,
   **Blender Version** et **Video Memory** si le réglage est disponible.
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
   En mode Édition, cette option remplace les raccourcis 1, 2 et 3 de sélection par des vues. Utilisez alors les boutons sommet, arête et face dans l’en-tête. Le menu **View** offre aussi des commandes sans pavé numérique.
5. Si vous travaillez au **trackpad** ou sans bouton central : *Input → Mouse →
   Emulate 3 Button Mouse*.
   ✅ Dans la vue 3D, sélectionnez la caméra (clic gauche) puis orbitez (bouton du milieu
   glissé, ou `Alt`+clic gauche) : la vue tourne autour de la caméra.

## Tutoriel 5 — Sécurité
1. *System → Memory & Limits → Undo Steps* : **64**.
2. *Save & Load → Blend Files* : **Save Versions = 2** ; *Auto-Save* coché, **Timer
   (Minutes) = 2**.
3. *Save & Load → Default To* : **Relative Paths** coché.
   Vérifiez le réglage **Auto-Save Preferences**. Si vous le laissez désactivé, utilisez **Save Preferences** pour les choix que vous voulez conserver.

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
   `GEO_Needle`, placez la souris dans la vue 3D et utilisez **View → Frame Selected** ou le point du pavé numérique.
   ✅ La vue cadre une petite tige rouge dans une rue.
5. **View → Frame All** ou la touche Home : vous revoyez toute la ville… mais la balise bleue
   `GEO_FarBeacon` (à 1 km) éloigne beaucoup le cadrage. Sélectionnez-la, `.` : elle
   peut disparaître ou se couper → sidebar `N` → onglet *View* → *Clip End* : passez à 5000 m.

## Tutoriel 8 — Placer une caméra là où l'on regarde
1. Cadrez l'aiguille en gros plan dans la vue (étape 4 ci-dessus, puis zoom molette).
2. *View → Cameras → Set Active Object as Camera* nécessite de sélectionner la caméra :
   cliquez `CAM_Needle` dans l'Outliner, puis `Ctrl+Numpad 0`.
3. Revenez à votre point de vue (`Numpad 0` pour quitter… ou recadrez l'aiguille), puis
   *View → Align View → Align Active Camera to View* (`Ctrl+Alt+Numpad 0`).
   ✅ Le cadre caméra (rectangle) montre l'aiguille en gros plan.
4. Ajustez avec *Object Data (caméra) → Lens → Focal Length* (85 mm = téléobjectif court).
5. `Shift+Ctrl+S` → `ch00_02_navigation_<prenom>_v001.blend`.
