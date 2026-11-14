# CH01.14 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Cycles | Cycles. |
| Q2 | — | EEVEE : previz, animation stylisée, look dev rapide. Cycles : rendus réalistes, images finales. |
| Q3 | — | Ctrl+F12. |
| Q4 | — | Échantillonnage adaptatif : Cycles arrête d'échantillonner un pixel quand son bruit passe sous le seuil. |
| Q5 | **b** — Rendre avec moins d'échantillons | Il nettoie le bruit restant. |
| Q6 | — | Temps de rendu inutilement long ; quelques dizaines à centaines d'échantillons + débruitage suffisent pour juger. |
| Q7 | **a** — PNG | PNG (JPEG perd de la qualité). |
| Q8 | — | En cas de plantage, tout est perdu ; avec des images numérotées, on reprend où l'on s'est arrêté et on monte ensuite. |
| Q9 | — | Diagnostiquer l'exposition : visualiser les zones sous- et surexposées. |
| Q10 | — | Non. Dans la fenêtre de rendu : Image > Save As (Shift+Alt+S). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1 (mesures de référence, RTX 3080)
Rendu de construction du chapitre (1920 × 1080) : Cycles OptiX 128 échantillons adaptatifs +
débruitage et EEVEE 64 échantillons ont été produits ensemble en ≈ 13 s (chargement compris).
Différences attendues : ombres de contact plus douces et lumière rebondie (teinte du bois sur
la tasse) en Cycles ; reflets d'environnement plus précis en Cycles.

## Exercice 2
Repère : avec le débruitage, 64 à 128 échantillons suffisent souvent pour une animation ; au-delà,
le gain visible est faible et le temps double à chaque doublement d'échantillons (hors seuil
adaptatif). Pour 2 880 images, chaque seconde gagnée par image = 48 minutes.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_14_final_render_solution.blend` ; images de référence :
`COMPLETED_EXAMPLES/renders/ch01_14_final.png` (Cycles) et `ch01_14_eevee.png` (EEVEE).
