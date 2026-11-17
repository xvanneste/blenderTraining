# CH06.07 — Rig mécanique

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rig mécanique obéit à des lois, pas à une anatomie : une roue qui roule sans glisser tourne de distance / rayon, un vérin hydraulique reste aligné entre ses deux points d'attache, une benne a une course limitée. Ce chapitre rigge un camion-benne : (1) quatre DRIVERS qui font tourner les roues d'après le déplacement de la racine, (2) un vérin à deux bones qui se visent (Damped Track), (3) une benne bornée par Limit Rotation. Le correcteur avance le camion, lève la benne et mesure les sommets évalués.

## Prérequis

- CH06.02 (contraintes), CH06.04 (driver sur influence).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Écrire un driver Scripted Expression à partir d'un Transform Channel.
2. Faire rouler une roue sans glissement.
3. Monter un vérin télescopique avec Damped Track.
4. Limiter une articulation avec Limit Rotation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.07.a | Rig de véhicule | Exercice 2 (correcteur) + croquis de profil |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Drivers : les roues | 3 h |
| L2 | Vérin et benne | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_07_truck_starter.blend` | Camion et armature sans driver ni contrainte |
| `COMPLETED_EXAMPLES/ch06_07_truck_solution.blend` | Camion complet : drivers, Damped Track, Limit Rotation |
| `COMPLETED_EXAMPLES/ch06_07_truck_reference.png` | Profil : repos, camion avancé de 0,5 m (roues tournées), benne levée de 35° (vérin aligné) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans drivers, mauvais rayon, mauvais axe, roues non parentées, sans Damped Track, sans limite) |
| `SCRIPTS/validate_ch06_07.py` | Correcteur (truck) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_07_truck_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_07.py" -- --exercise truck
```

## Livrables attendus

1. Rig de camion validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.08 — Shape keys et drivers](../CH06_08_SHAPEKEYS/README.md)
