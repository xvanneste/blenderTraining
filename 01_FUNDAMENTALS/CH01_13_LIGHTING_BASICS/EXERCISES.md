# CH01.13 — Exercices

## Exercice 1 — Facile : la loi de l'inverse du carré ⏱ 10 min
Une Point de 100 W à 1 m d'un plan, puis à 2 m, puis à 4 m. Quelle puissance faut-il pour
retrouver l'éclairement initial à 2 m ? à 4 m ? Vérifiez à l'œil en mode Rendered.

## Exercice 2 — Moyen : quatre ambiances ⏱ 20 min
Même buste, une lumière principale : (a) midi (Sun blanc, Angle 1°, ombres dures) ;
(b) fenêtre nuageuse (Area 2 m, 6500 K) ; (c) bougie (Point 20 W, 1900 K, très proche) ;
(d) lampe de poche (Spot étroit, Blend 0,1). Rendus + une phrase par ambiance.

## Exercice 3 — Difficile : le buste dans le noir (SANS procédure) ⏱ 10 min
Les consignes du `README_EXERCICE`, validez (`--exercise threepoint --render`).
Barème (17 pts) : 3 lumières 2 · noms 1 · key 2 · fill 2 · rim 2 · ratio 2 · monde sombre 1 ·
exposition 3 (+ rendu).

## Défis
- **Défi 1 :** version film noir : ratio ≥ 16:1, rim froid, key dure (petite source).
- **Défi 2 :** reproduisez l'éclairage d'une photo de portrait que vous aimez (notez position,
  taille, couleur de chaque source).

## Mini-projet — Trois portraits lumineux ⏱ 30 min
Trois rendus du buste : « commercial » (2:1), « naturel » (4:1), « dramatique » (8:1 et plus).
Grille : ratios respectés 40 · qualité des ombres 30 · nommage et organisation 30.

## Tests chronométrés
| Test | Cible |
|---|---|
| Trois points complet | 3 min |
| Passer une lumière en température 3200 K | 10 s |
| Faire viser une lumière avec Track To | 15 s |
