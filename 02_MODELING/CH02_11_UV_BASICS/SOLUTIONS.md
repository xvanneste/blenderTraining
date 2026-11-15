# CH02.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | À indiquer, pour chaque coin de face, quel point de la texture image (coordonnées U, V de 0 à 1) s'y applique : c'est le dépliage de la surface. |
| Q2 | — | Une couture est une arête marquée où la surface est coupée pour le dépliage ; une île est un morceau déplié d'un seul tenant. |
| Q3 | **b** — 1 arête verticale + les 2 cercles des couvercles | 3 îles : un rectangle et deux disques. |
| Q4 | — | Là où elles se voient le moins : dessous, arrière, angles vifs, plis. |
| Q5 | **a** — U | U : UV Mapping. |
| Q6 | — | Pour des objets anguleux ou des props simples à déplier rapidement, sans placer de coutures à la main. |
| Q7 | — | À ranger les îles dans le carré 0–1 sans chevauchement, avec une marge. |
| Q8 | **a** — un étirement | Étirement : coutures à revoir. |
| Q9 | — | Le nombre de pixels de texture par unité de surface ; elle doit être comparable entre objets d'un même plan. |
| Q10 | — | UV → Average Islands Scale, puis Pack Islands. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Cube : 7 arêtes coupées (patron en croix) ou Smart UV. Cône : 1 génératrice + le cercle de base.
UV Sphere : 1 méridien (+ éventuellement les pôles). Tore : 1 cercle « autour du tube » + 1 cercle
« autour du trou » → une seule île rectangulaire.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_11_uv_solution.blend`, rendus `ch02_11_uv_starter_view.png`
(sans UV) et `ch02_11_uv_reference.png`. Généré avec les opérateurs de l'interface : caisse en
*Smart UV Project* (66°, marge 0,02) ; boîte avec 65 arêtes de couture (1 verticale + 2 × 32),
*Unwrap* Angle Based, *Pack Islands*. Mesures : occupation 64 % (caisse) et 55 % (boîte),
chevauchement 0 %, dispersion de densité 0,00. Contre-épreuve : une Cube Projection sans couture sur
la boîte est refusée.
