# CH03.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Elle recouvre le haut de l'iris | Les yeux « ronds et blancs » viennent d'une paupière trop haute ; le haut de l'iris est légèrement masqué. |
| Q2 | — | Environ la largeur de l'écart entre les pupilles (ici ≈ 6,4 cm mesurés pour 6,4 cm d'écart) ; ce sont des repères moyens, pas des lois. |
| Q3 | — | À peu près entre la ligne des sourcils et la base du nez. |
| Q4 | **b** — Le bord enroulé de l'oreille et son creux central | Hélix = bord ; conque = creux près du conduit. |
| Q5 | — | On sculpte un creux qui se referme vers l'intérieur ; une ouverture traversante casse le volume fermé et complique remesh et rig. |
| Q6 | **b** — Les commissures de la bouche (relevées) et les plis naso-géniens (plus marqués) | Mesuré dans la solution : commissures +5,3 mm ; le neutre est à ≈ 0 mm ; la moue à −12,4 mm. |
| Q7 | — | Le sourire sincère engage aussi les yeux (joues remontées, œil légèrement plissé) ; relever seulement la bouche donne un sourire de façade. |
| Q8 | — | Les détails (1–5 mm) sont petits devant la forme de base ; seule la différence avant/après isole ce que le travail a ajouté. Une mesure autonome sur ces détails confond anatomie de base et sculpture. |
| Q9 | **a** — Pinch/Magnify (P) | P = Pinch/Magnify ; G = Grab ; M = Mask ; K = Snake Hook. |
| Q10 | — | Ne pas supprimer REF_Base (copie cachée du buste de départ) ; la récupérer depuis le fichier de départ (Append > Object) si elle a été effacée. |
<!-- QUIZ_ANSWERS_END -->

## Exercices 2 et 3
`COMPLETED_EXAMPLES/ch03_06_face_solution.blend` (neutre) et `ch03_06_smile_solution.blend` (sourire), avec
`_reference.png` pour chacun (face, 3/4, profil).

**Comment elles ont été produites.** Les deux solutions (neutre, sourire) sont **sculptées à la brosse**, dans Blender 5.2 LTS en interface via le MCP, à partir du starter :
paupières (*Draw* en bourrelet le long d'un cercle autour de chaque globe, 2 passes), ligne de bouche (*Draw* inversé, rayon 5 mm, 3 passes), narines (*Draw* inversé en **vue oblique du
bas vers l'avant**, 5 petits cercles, 1 passe : les narines regardent vers le bas, la vue de face ne les atteint pas), oreilles (*Draw* inversé en **vue de droite**, sillon d'hélix elliptique + creux
de conque), sourire (*Grab* court sur chaque commissure, *Smooth*, *Draw* inversé sur la courbe du sourire, *Crease Sharp* pour les plis naso-géniens). Mirror X actif partout. Les contre-exemples
restent scriptés (ce sont des défauts voulus).
Mesures du correcteur : neutre 27/27 — paupières relevées sur 22 % de l'anneau ; narines 29 / 29 sommets creusés ; ligne de bouche 8 sommets au centre, 6,4 cm de large (100 % de l'écart des yeux) ;
oreilles 72 / 71 sommets creusés ; relèvement des commissures ≈ 0 mm. Sourire 29/29 — commissures **+5,3 mm**, bouche mesurable sur 4,0 cm (62 %).
**Ce que l'essai a appris** : (1) un premier sourire (*Grab* de 20 mm) laissait des **balafres verticales** aux commissures alors que le correcteur était vert : rendu refusé, recommencé avec un glissé
de 6 mm, un rayon plus grand et un lissage ; (2) répéter une boucle de passes sans s'arrêter au seuil creuse trop (écart max jusqu'à 14,8 mm sur l'oreille, 9,5 mm sur la bouche) ; l'annulation
(`ed.undo`) n'est pas disponible via le MCP, on recharge le fichier et on rejoue ; (3) la rainure de bouche réelle est moins profonde que celle des solutions scriptées, d'où la largeur de bouche
mesurable plus courte (tolérance abaissée à 50 %).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui l'attrape (et lui seul) |
|---|---|---|
| `…_no_lids` | pas de paupières | paupières (0 %) |
| `…_no_nostrils` | pas de narines | narines (0 / 0 sommets) |
| `…_no_mouth` | pas de ligne de bouche | bouche (0 sommet) |
| `…_no_ears` | pas d'hélix ni conque | oreilles (0 / 0) |
| `…_frown` | commissures abaissées | sourire (−12,4 mm) — `--exercise smile` |
Aussi refusés : le starter ; le buste de CH03.05 (pas de `REF_Base`) ; le visage neutre à l'exercice `smile` (≈ 0 mm).
Le sourire passe l'exercice `face` (il contient tous les détails) et l'exercice `smile`.

**Ce que le développement du correcteur a appris** (consigné aussi dans CLAUDE.md) :
1. une mesure « absolue » des détails (creux par rapport à la surface lissée, résidu d'un ajustement quadratique) ne
   séparait PAS un visage sculpté d'un visage non sculpté (oreilles : mêmes valeurs avec et sans) — un creux large
   survit au lissage, et l'anatomie de base domine ; la solution a été une mesure **différentielle** vs REF_Base ;
2. REF_Base étant caché, sa `matrix_world` n'est pas évaluée à l'ouverture : utiliser `matrix_basis` ;
3. le buste porte une translation de −5 mm non appliquée : la copie de référence doit porter la même ;
4. la poursuite de la ligne de bouche sautait sur les plis naso-géniens (devenus aussi profonds en sourire) : ligne
   des lèvres rendue nettement plus profonde (4,5 mm) que les plis (≤ 2,4 mm) et seuil à 2,8 mm.

## Limites
- Il faut garder `REF_Base` ; le correcteur compare à elle. Un apprenant qui déforme massivement le buste de départ
  fausse les zones (paupières, narines…) : refaire à partir du starter.
- Seuils calibrés pour ≈ 2,5 mm d'arête ; au-delà, relire les valeurs avec `--debug`.

## Correction a posteriori (session 4)
La correction de CH03.05 (translation de −5 mm appliquée aux sommets) a remis tous les détails aux positions voulues : les mesures ont changé et ont été recalibrées —
région des narines resserrée (|x| < 2 cm, de 2 cm sous la pointe à 3 mm au-dessus), seuil ≥ 10 sommets par côté (solution 19 / 18, sans narines 0 / 0) ;
poursuite de la ligne de bouche limitée à ±3 cm (au-delà elle rejoignait les plis naso-géniens) ; sourire de la version scriptée de repli porté de 7 à 10 mm.

