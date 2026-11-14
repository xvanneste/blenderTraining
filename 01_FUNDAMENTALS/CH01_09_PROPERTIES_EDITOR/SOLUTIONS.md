# CH01.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Output | Output > Format. |
| Q2 | **c** — Scene | Scene > Camera. |
| Q3 | — | Onglet Data (Object Data) de la caméra > Lens > Focal Length. |
| Q4 | — | Les onglets dépendent du type de l'objet actif : une lumière n'a pas de matériau. |
| Q5 | — | Backspace avec la souris au-dessus du champ (ou clic droit > Reset to Default). |
| Q6 | — | À figer l'affichage sur un datablock même si l'on sélectionne d'autres objets. |
| Q7 | — | Dans la ligne de datablock en haut de l'onglet Material (ou dans l'Outliner, mode Blender File). |
| Q8 | — | Métadonnées de plan (shot, version, artiste), paramètres de rig, données pour scripts de pipeline. |
| Q9 | **c** — 125 | 5 × 25 = 125. |
| Q10 | — | Les clés sont posées sur des numéros d'image : changer les fps ensuite modifie la durée réelle et donc le timing. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
3840 × 2160, 100 %, 24 fps, 8 s × 24 = **192 images** → Start 1, End 192 ; Output →
`//renders/sh0010_` ; File Format PNG.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_09_hunt_solution.blend`. Points d'attention :
- l'échantillonnage EEVEE s'appelle *Samples* dans *Sampling → Render* ;
- *Units → Length* n'apparaît qu'avec *Unit System* = *Metric* (déjà réglé) ;
- la propriété personnalisée doit être de type **String** (texte) ;
- poser le bouclier **avant** de retirer le matériau (sinon 0 utilisateur → supprimé à
  l'enregistrement).

## Défi 2
L'épingle fige l'éditeur sur ce datablock : on peut sélectionner d'autres objets (par exemple
pour cadrer) tout en continuant à régler la caméra.
