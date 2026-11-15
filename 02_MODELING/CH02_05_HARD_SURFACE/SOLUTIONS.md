# CH02.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Aucune arête réelle n'est infiniment vive ; le petit arrondi accroche la lumière et dessine la forme au rendu. |
| Q2 | **b** — un chanfrein | 1 segment = facette (chanfrein) ; plusieurs = arrondi. |
| Q3 | — | De l'ordre de 1 à 3 mm (0,001–0,003 m), avec 2 segments. |
| Q4 | **c** — Weight | Weight : arêtes ayant un Bevel Weight. |
| Q5 | — | Edit Mode, sélectionner les arêtes, Edge → Edge Bevel Weight, valeur (ex. 1). |
| Q6 | — | Un Bevel « Weight » large pour les arrondis voulus, puis un Bevel « Angle » fin (2–3 mm, 2 segments, Harden Normals) pour toutes les autres arêtes vives. |
| Q7 | **b** — Shade Smooth | Comme Weighted Normal, il agit sur un objet lissé. |
| Q8 | — | Sinon la largeur du bevel est déformée selon les axes (biseaux irréguliers). |
| Q9 | — | Non, pas nécessairement : des pièces séparées ou jointes (Ctrl+J) sans liaison topologique suffisent pour des éléments rigides. |
| Q10 | — | Grandes formes → formes moyennes → petits détails ; garder de grandes surfaces calmes et regrouper les détails pour éviter le bruit visuel. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
(a) L'arête est une simple rupture de valeur : pas de reflet, la forme paraît « découpée dans du
papier ». (b) Un fin liseré lumineux souligne l'arête : objet manufacturé crédible. (c) Une facette
large et nette : chanfrein volontaire, aspect « usiné ».

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_05_device_solution.blend`, `ch02_05_device_reference.png`
et `ch02_05_device_closeup.png`. Réglages : Bevel Weight 1 sur les 4 arêtes verticales ;
modificateur *Bevel_Corners* (Weight, 2 cm, 4 segments) ; écran Inset 3 cm + creux 1 cm ; 3 boutons
(rayon 2 cm, hauteur 1,5 cm) joints ; modificateur *Bevel_Edges* (Angle 30°, 3 mm, 2 segments,
Harden Normals) ; Shade Smooth. Le correcteur vérifie aussi que le résultat évalué est fermé et que
les modificateurs ne sont pas appliqués.
