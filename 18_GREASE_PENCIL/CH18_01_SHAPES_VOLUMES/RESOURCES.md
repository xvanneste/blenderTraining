# CH18.01 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Grease Pencil (introduction) | https://docs.blender.org/manual/en/latest/grease_pencil/introduction.html |
| Manuel — Draw Mode | https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/introduction.html |
| Drawabox (cours gratuit de dessin en volumes, en anglais) | https://drawabox.com/ |

Vérifications 5.3.0 : raccourcis de Draw Mode relevés dans `blender_default.py` (dessin `LMB`,
effacer `Ctrl+LMB`, lisser `Shift+LMB`, taille `[`/`]`, calques `Y`, matériaux `U`,
outils Line/Polyline/Box/Circle/Arc/Curve/Eyedropper) ; API Grease Pencil v3 utilisée pour
générer guides et solution (calques, images, traits, matériaux).
**Note 5.3 (vérifiée)** : le remplissage est porté par chaque trait (pinceau en mode *Fill* ou
*Both*, outil *Fill*, ou Edit Mode → *Set Stroke Type*) ; le matériau n'a plus de cases
Stroke/Fill, seulement ses panneaux *Stroke* et *Fill* (couleurs, styles). La solution combine
aplats gris et hachures.
Ressources produites : feuille d'exercice, solution, rendu de référence (licence BCMA).
