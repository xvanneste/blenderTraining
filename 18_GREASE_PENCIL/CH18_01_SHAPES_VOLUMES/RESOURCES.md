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
**Limite constatée** : les remplissages de traits créés par script ne s'affichent pas au rendu en
mode arrière-plan ; la solution utilise donc des hachures. Dans l'interface, le remplissage
fonctionne normalement.
Ressources produites : feuille d'exercice, solution, rendu de référence (licence BCMA).
