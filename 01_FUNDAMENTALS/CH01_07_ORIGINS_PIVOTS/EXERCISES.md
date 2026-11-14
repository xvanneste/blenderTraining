# CH01.07 — Exercices

## Exercice 1 — Facile : origines au sol ⏱ 5 min
Ajoutez 3 primitives (cube, cylindre, Suzanne). Placez l'origine de chacune au centre de sa
base (au sol), puis posez-les à z = 0 en tapant `0` dans *Location Z*.

## Exercice 2 — Moyen : la lampe suspendue ⏱ 10 min
Un cylindre fin (le fil) et une sphère (l'ampoule) joints en un objet. Placez l'origine en
haut du fil, puis faites balancer la lampe : `R Y 20`. La lampe doit pivoter comme un pendule.

## Exercice 3 — Difficile : la porte et la roue (SANS procédure) ⏱ 6 min
Origine de la porte sur la charnière, porte ouverte à 90° ; boulons tournés de 45° autour du
centre de la roue. Validez (`--exercise door`).
Barème (15 pts) : porte présente 1 · origine 4 · angle 2 · pivot correct 3 · porte au sol 1 ·
boulons 4.

## Défis
- **Défi 1 :** horloge : cadran + aiguille des heures + aiguille des minutes ; origine des
  aiguilles au centre du cadran ; tournez-les pour afficher 10 h 10.
- **Défi 2 :** créez un escalier en colimaçon : une marche, `Shift+D`, `R Z 20` avec pivot au
  curseur placé sur l'axe central, `G Z 0.18`, puis `Shift+R` répété.

## Mini-projet — Mécanismes ⏱ 25 min
Trois objets prêts à animer : une porte, un couvercle de coffre, un moulin à vent (4 pales
autour du moyeu). Chaque origine au bon endroit ; une image par objet « ouvert ». Grille :
origines correctes 50 · rotations réalistes 30 · nommage 20.

## Tests chronométrés
| Test | Cible |
|---|---|
| Origine sur un sommet précis | 20 s |
| Rotation de 3 objets autour d'un point | 15 s |
| Curseur à l'origine du monde | 2 s |
