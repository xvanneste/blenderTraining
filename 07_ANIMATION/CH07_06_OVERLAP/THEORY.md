# CH07.06 — Cours théorique : Arcs, overlap, follow-through

## 1. Overlap
Dans une chaîne (colonne, queue, antenne), un mouvement se propage : chaque segment atteint son extrême un peu après son parent. L'écart (retard) donne la sensation de souplesse : 1 à 4 images ici ; trop long, la queue paraît indépendante.

## 2. Follow-through
Quand le corps s'arrête, la pointe continue sur sa lancée, dépasse parfois la position de repos et se stabilise. C'est l'inertie.

## 3. Arcs
Un point d'un corps qui pivote décrit un arc ; la pointe d'une chaîne animée avec retard décrit une courbe plus riche. Une trajectoire rectiligne paraît mécanique.

## 4. L'exercice
RIG_Antenna : quatre bones en chaîne verticale (0,4 m chacun), rotation X locale. Base : 0 → +25° (image 13) → 0 (image 25). Pointe tail_3 : retard de 6 images (maximum à 19), retour à 0 à l'image 31, dépassement −6° à l'image 35, repos à l'image 44. Plage 1–48.

## 5. Mesures
Solution : 28/28. Maxima aux images 13, 15, 17, 19 ; amplitudes 18°, 14°, 10° ; à l'image 26 : tail_3 à 7,2° ; minimum −6,0° ; repos 0,0° ; écart de la pointe à la droite : 51 cm. Contre-exemples : maxima tous à 13 ; retards de 6 images ; retour au repos à l'image 25 (tail_3 à −1,6° à l'image 26) ; pas de dépassement (minimum 0,0°) ; tail_3 à 5° à la fin ; queue immobile.

## 6. Pièges
- Copier les clés du parent sans décalage.
- Retards irréguliers ou trop longs.
- Oublier le dépassement ou la stabilisation.
- Stabiliser trop tôt (la queue s'arrête avec la base).
- Animer toutes les amplitudes identiques (effet de câble rigide).

## 7. Limites
Quatre bones sur un seul axe ; aucune contrainte physique (CH08) ; la pointe est vérifiée par sa trajectoire, pas par son rendu ; pas de maillage lié (le rig est seul).
