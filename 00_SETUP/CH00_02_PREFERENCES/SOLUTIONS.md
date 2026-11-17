# CH00.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Edit > Preferences | Edit > Preferences. |
| Q2 | **b** — Il est enregistré automatiquement dans userpref.blend | Les préférences sont enregistrées automatiquement (bouton ☰ en bas à gauche de la fenêtre). |
| Q3 | — | Revert to Saved Preferences. |
| Q4 | **b** — Non, dans userpref.blend du dossier de configuration | Elles vivent dans %APPDATA%\Blender Foundation\Blender\5.3\config\userpref.blend. |
| Q5 | — | Interface > Display > Resolution Scale (ex. 1,25 ou 1,5). |
| Q6 | — | Pour surveiller en permanence le nombre d'objets/faces/triangles et détecter une scène trop lourde avant qu'elle ralentisse ou fasse planter le rendu. |
| Q7 | **c** — Orbit Around Selection | Navigation > Orbit & Pan > Orbit Around Selection. |
| Q8 | **b** — Emulate Numpad | Input > Keyboard > Emulate Numpad. Attention : les touches 1-2-3 servent alors aux vues et plus aux modes de sélection en Edit Mode. |
| Q9 | — | Alt + clic gauche (glisser). |
| Q10 | — | Le sélectionner (par ex. dans l'Outliner) puis View > Frame Selected (touche . du pavé numérique). |
| Q11 | **b** — scene.blend, scene.blend1, scene.blend2 | .blend1 = version précédente, .blend2 = celle d'avant. |
| Q12 | — | .blend1/.blend2 sont des copies automatiques écrasées à chaque enregistrement (filet de sécurité court) ; Save Incremental crée un nouveau fichier numéroté (v002…) qui reste : c'est un vrai historique de versions. |
| Q13 | — | Oui : chaque étape d'annulation consomme de la mémoire vive, surtout sur des scènes lourdes. |
| Q14 | **b** — Fait de la scène et de l'interface actuelles le point de départ de File > New | Il écrit startup.blend dans le dossier config. |
| Q15 | — | Parce qu'on enregistrerait des préférences d'usine (modifiées) par-dessus vos vraies préférences : vous perdriez votre configuration. |
<!-- QUIZ_ANSWERS_END -->

## Exercices de leçon
- **L1 moyen :** avec *Auto-Save Preferences* actif, le changement de thème est déjà
  enregistré : *Revert to Saved Preferences* revient à… l'état qui l'inclut. Pour pouvoir
  annuler, décochez l'auto-save avant d'expérimenter, ou restaurez votre archive.
- **L2 difficile :** *Interface → Translation* : *Language = Français*, cocher
  *Interface*, décocher *Tooltips*. Les menus sont lisibles en français, et les infobulles
  donnent les termes anglais officiels à chercher dans la documentation et les forums.

## Exercice 1
Valeurs attendues : Orbit Around Selection ✔, Zoom to Mouse Position ✔, Auto Depth ✔,
Auto Perspective ✔, Undo Steps 64, Auto-Save ✔ (2 min), Save Versions 2, Relative Paths ✔,
Status Bar : Scene Statistics, System Memory, Video Memory, Blender Version.

## Exercice 2
Sélectionnez GEO_Needle puis GEO_FarBeacon dans l’Outliner et utilisez View → Frame Selected dans la vue 3D. La vue se centre sur l’objet sélectionné. Les transformations et le cadrage caméra restent inchangés. Si le second geste est plus rapide, tenez compte de la mémorisation du décor.

## Exercice 3
Fichier de référence : `COMPLETED_EXAMPLES/ch00_02_navigation_solution.blend`.
- `CAM_Needle` active (`Ctrl+Num 0` avec la caméra sélectionnée).
- Position ≈ 0,6 m de l'aiguille (20,45 ; −30,45 ; 0,32), focale 85 mm, contrainte
  *Track To* vers `EMP_NeedleTarget` (facultative : `Ctrl+Alt+Num 0` suffit).
- L'aiguille mesure 25 cm : à 50 mm de focale il faut être à moins de ~1 m.

## Exercice 4 — Vérifier une restauration

Dans un profil isolé, notez deux valeurs avant modification, par exemple la rotation autour de la sélection et l’échelle d’affichage. Sauvegardez cette configuration. Modifiez les deux valeurs et vérifiez que le profil d’essai les a retenues. Fermez Blender, remettez la copie du dossier config dans le profil d’essai et relancez sans paramètres d’usine. La restauration réussit si les deux valeurs correspondent de nouveau au point de départ. Si un fichier startup.blend faisait partie de l’archive, comparez aussi sa scène de démarrage.
