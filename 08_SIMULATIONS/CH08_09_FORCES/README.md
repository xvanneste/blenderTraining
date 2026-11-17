# CH08.09 — Forces

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Les champs de force (Force Fields) sont des objets invisibles qui poussent, tordent ou brassent tout ce qui les écoute : particules, tissu, corps souples. Le vent (Wind) pousse selon l'axe local Z de l'objet ; la turbulence (Turbulence) ajoute des tourbillons ; chaque système choisit son degré d'écoute par ses Field Weights. Ce chapitre fait dériver un nuage de 300 particules vers +X avec un vent de force 5, puis le brasse avec une turbulence. Le correcteur simule 60 images et mesure la dérive moyenne et la dispersion latérale.

## Prérequis

- CH08.04 (particules).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter et orienter un champ Wind.
2. Ajouter une Turbulence et régler sa taille.
3. Utiliser les Field Weights.
4. Mesurer l'effet d'une force sur un nuage.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.09.a | Utiliser les forces | Exercice 2 (correcteur) + vue de dessus |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Wind, Turbulence et poids | 4 h |
| L2 | Mesurer une force | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_09_forces_starter.blend` | L'émetteur de 300 particules seul (aucun champ) |
| `COMPLETED_EXAMPLES/ch08_09_forces_solution.blend` | Wind de force 5 vers +X + Turbulence de force 5, taille 0,5 |
| `COMPLETED_EXAMPLES/ch08_09_forces_reference.png` | Vue de dessus à l'image 60 : sans force, vent seul, vent + turbulence |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans vent, vent à l'envers, vent faible, sans turbulence, vent ignoré par les poids) |
| `SCRIPTS/validate_ch08_09.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_09_forces_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_09.py" -- --exercise forces
```

## Livrables attendus

1. Forces validées.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.10 — Caches et baking](../CH08_10_CACHES/README.md)
