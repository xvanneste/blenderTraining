# CH02.06 — Subdivision Surface

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 15  
**Version :** Blender 5.3.0

## Introduction

La subdivision transforme une cage légère en surface parfaitement lisse : c'est la base des personnages et de nombreux objets de cinéma. Mais elle arrondit tout. Ce chapitre apprend à contrôler la forme avec des boucles de maintien et des creases — en mesurant le résultat — et à régler les niveaux pour garder un viewport fluide et un rendu lisse.

## Prérequis

- CH02.01 (topologie)
- CH02.02 (Loop Cut).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer cage, surface limite et coût de chaque niveau.
2. Garder une forme nette avec des boucles de maintien bien placées.
3. Utiliser le crease et connaître ses limites.
4. Régler Levels Viewport / Render et Simplify.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.06.a | Contrôler une subdivision | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Cage et subdivision | 45 min |
| L2 | Boucles de maintien et crease | 1 h |
| L3 | Performances | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_06_subdiv_starter.blend` | 3 cubes subdivisés devenus des boules |
| `COMPLETED_EXAMPLES/ch02_06_subdiv_solution.blend` | Boucles de maintien, crease, niveaux optimisés |
| `COMPLETED_EXAMPLES/ch02_06_subdiv_starter_view.png` | Rendu avant |
| `COMPLETED_EXAMPLES/ch02_06_subdiv_reference.png` | Rendu après |
| `SCRIPTS/validate_ch02_06.py` | Correcteur (forme évaluée, crease, niveaux) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_06_subdiv_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_06.py" -- --exercise subdiv --render
```

## Livrables attendus

1. Trois cubes validés.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : la souris d'ordinateur.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Cubes validés.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.07 — Booléens et non destructif](../CH02_07_BOOLEANS/README.md)
