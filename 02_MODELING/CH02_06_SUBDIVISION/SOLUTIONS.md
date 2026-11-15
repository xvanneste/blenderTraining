# CH02.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Le maillage de contrôle léger que l'on modélise ; la subdivision en calcule une surface lisse. |
| Q2 | **c** — 16 | ×4 par niveau : 4 × 4 = 16. |
| Q3 | **b** — Ctrl+0…5 | Ctrl+0 à Ctrl+5 en Object Mode. |
| Q4 | — | La distance entre la boucle et l'arête fixe le rayon de l'arrondi : plus elle est proche, plus l'arête est nette. |
| Q5 | **a** — Shift+E | Shift+E puis valeur de 0 à 1. |
| Q6 | — | Avantage : rapide, sans géométrie supplémentaire. Limite : dépend d'un attribut parfois mal exporté, et un crease de 1 donne une arête parfaitement vive peu réaliste. |
| Q7 | — | Ils produisent des bosses et des pincements après subdivision. |
| Q8 | **a** — Use Creases dans le modificateur | Use Creases doit être coché. |
| Q9 | — | Levels Viewport 0–1 et Render 2–3. |
| Q10 | — | Render → Simplify → Max Subdivision. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Plus la boucle est proche de l'arête, plus l'arrondi est petit : la **distance boucle–arête fixe le
rayon** de l'arrondi après subdivision.

## Exercice 2
Crease : cage légère (8 à 24 sommets), réglage instantané, mais dépend de l'attribut *crease* (pas
toujours exporté, ou interprété différemment). Boucles : cage plus lourde, mais la forme est
**dans la géométrie** : c'est elle qu'on exporte (FBX, USD, autre logiciel).

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_06_subdiv_solution.blend`, rendus `ch02_06_subdiv_starter_view.png`
(avant) et `ch02_06_subdiv_reference.png` (après). Mesures du correcteur :
- GEO_Support : boucles à 5 cm des arêtes dans les 3 directions → remplissage **0,99** (0,52 sans) ;
- GEO_Crease : crease 1 sur les 4 arêtes du dessus → **0,42 m²** de dessus plat (0 sans) ;
- GEO_Pebble : Levels Viewport 1, Render 3.
