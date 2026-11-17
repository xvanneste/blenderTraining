# CH05.06 — Paramètres et interfaces

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Un arbre qui ne se règle qu'en rouvrant ses nœuds n'est pas un outil. L'interface de l'arbre expose des entrées (hauteur, rayon, nombre, espacement) qui apparaissent dans le modificateur, avec des bornes, des descriptions et des panneaux. Ce chapitre transforme une rangée de piliers en outil. Le correcteur ne se contente pas de lire l'interface : il CHANGE les paramètres du modificateur et vérifie que la géométrie suit (nombre de piliers, hauteur, largeur, étendue).

## Prérequis

- CH05.02–03.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer des entrées (Float, Integer…) avec défaut, minimum, maximum et description.
2. Ranger les entrées dans des panneaux.
3. Brancher chaque entrée aux nœuds concernés.
4. Vérifier qu'un outil réagit à ses paramètres.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.06.a | Créer un outil paramétrable | Exercice 2 (correcteur) + rendu des deux réglages |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | L'interface de l'arbre | 2 h 30 |
| L2 | Brancher et tester les paramètres | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_06_parameters_starter.blend` | Arbre fonctionnel mais sans interface (valeurs en dur) |
| `COMPLETED_EXAMPLES/ch05_06_parameters_solution.blend` | Outil « Rangée de piliers » à quatre paramètres |
| `COMPLETED_EXAMPLES/ch05_06_parameters_reference.png` | Deux réglages : défaut (haut), Height 3,5 / Count 12 / Radius 0,3 / Spacing 1,0 (bas) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans panneaux, sans descriptions, entrée inutilisée, valeur codée en dur, bornes absurdes) |
| `SCRIPTS/validate_ch05_06.py` | Correcteur (parameters) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_06_parameters_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_06.py" -- --exercise parameters --render
```

## Livrables attendus

1. Outil paramétrable validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.07 — Décors et végétation](../CH05_07_SCATTERING/README.md)
