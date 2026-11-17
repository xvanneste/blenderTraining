# CH06.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Une autre position pour chaque sommet, mélangée selon une valeur | Chaque shape key est un jeu de positions de sommets ; la Value (0 à 1) dose le mélange avec Basis. |
| Q2 | **b** — À la forme de référence : les autres shape keys sont relatifs à elle | Basis est la forme de repos ; elbow_fix = déplacement relatif à Basis. |
| Q3 | **b** — Pour qu'il n'agisse qu'autour du coude | Sans groupe, le gonflement s'applique à tout le tube (écart de 11 mm mesuré loin du coude). |
| Q4 | — | Le skinning linéaire mélange deux rotations : les sommets de l'anneau du coude sont interpolés en ligne droite entre leurs deux positions, ce qui les rapproche de l'axe (rayon 4,08 cm côté moyen, 2,5 cm côté intérieur). |
| Q5 | — | Que le maillage évalué est identique à celui sans le shape key (≤ 0,01 mm) : la correction ne doit agir que quand le coude plie. |
| Q6 | **b** — a / 1.5708 | 90° = π/2 ≈ 1,5708 rad ; l'API et le driver travaillent en radians. |
| Q7 | **b** — Transform Channel | Transform Channel : bone fore, Z Rotation, Local Space. |
| Q8 | — | upper ne tourne pas : la valeur reste à 0, le coude reste écrasé (mesuré : 4,08 cm). |
| Q9 | — | Parce que le résultat visible dépend du skinning, du shape key et du driver combinés ; les propriétés seules ne prouvent rien. |
| Q10 | — | Plis de la peau, muscle qui gonfle, correction d'épaule, ou expressions faciales (CH06.09). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_08_shapekeys_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_08_files.py`) : skinning Automatic Weights, shape key écrit sommet par sommet (gonflage calibré : 22 %), groupe de sommets, driver. Score 48/48 ; starter 4/9 (arrêt anticipé).
Croquis regardé : à 90°, coude écrasé à gauche, volume restauré à droite, reste du tube identique.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_key` | aucun shape key | Shape keys présents (arrêt anticipé) |
| `…_no_driver` | key à 0, sans driver | driver ; valeurs à 45° et 90° ; rayon du coude |
| `…_always_on` | key fixé à 1, sans driver | driver ; repos identique ; valeur à 45° |
| `…_weak` | gonflage de 5 % seulement | rayon du coude ; déplacement au coude (seuls) |
| `…_no_group` | pas de groupe de sommets | groupe de sommets ; sommets loin du coude (seuls) |
| `…_wrong_bone` | driver lit upper | bone lu ; valeurs ; rayon du coude |
Aussi refusé : le starter.

## Limites
- Gonflage radial simple, pas de sculpt ; mesure sur l'anneau du coude uniquement.
- Un seul driver et un seul key ; les rigs réels combinent plusieurs correctifs.
