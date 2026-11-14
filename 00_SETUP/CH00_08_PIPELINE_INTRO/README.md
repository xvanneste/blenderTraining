# CH00.08 — Introduction au pipeline cinéma

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Avant d'apprendre les outils, il faut voir la carte complète : comment une idée devient un film. Ce chapitre présente la préproduction, la production et la postproduction, les deux chaînes de fabrication (assets réutilisables et plans uniques), les départements d'un studio et la façon dont chaque phase de l'académie s'y insère. Vous découperez un mini-scénario de 30 secondes en plans, dans une shot list vérifiée par script, et vous estimerez la charge de travail de votre futur premier court-métrage. Ce chapitre clôt la phase 0 avec le projet « Studio prêt ».

## Prérequis

- CH00.06 (arborescence, nommage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Décrire les étapes de fabrication d'un film d'animation 3D et leurs livrables.
2. Distinguer assets et plans, et expliquer pourquoi on lie plutôt que copier.
3. Associer chaque département à une phase de l'académie.
4. Écrire une shot list (codes, durées, valeurs de plans, statuts) et la vérifier.
5. Produire une première estimation de charge.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.08.a | Expliquer le pipeline d'un plan | Leçons 1–2, quiz |
| C00.08.b | Établir une shot list et une estimation | Exercices 1–3 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Préproduction, production, postproduction | 25 min |
| L2 | Assets, plans et départements | 30 min |
| L3 | Le plan comme unité de travail : la shot list | 40 min |
| L4 | Estimer | 15 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `ASSETS/bcma_pipeline_diagram.svg` | Schéma du pipeline avec les phases de l'académie |
| `STARTER_FILES/ch00_08_shotlist_template.csv` | Modèle de shot list |
| `STARTER_FILES/ch00_08_shotlist_broken.csv` | Shot list à corriger (7 erreurs) |
| `COMPLETED_EXAMPLES/ch00_08_shotlist_solution.csv` | Découpage de référence (8 plans, 30 s) |
| `../../SCRIPTS/bcma_shotlist_check.py` | Vérificateur de shot list |

## Correcteur automatique

```powershell
python "..\..\SCRIPTS\bcma_shotlist_check.py" "ch00_08_shotlist_<prenom>.csv" --target-seconds 30 --tolerance 3
```

## Livrables attendus

1. Shot list du robot validée (30 s).
2. Shot list + estimation de votre court A.
3. Projet de phase P0 « Studio prêt » ≥ 70/100.

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/13.
- Exercice 3 réalisé sans tutoriel.
- Projet P0 ≥ 70/100 : la phase 0 est validée.

➡️ Chapitre suivant : [Phase 1 — CH01.01 L'interface](../../01_FUNDAMENTALS/CH01_01_INTERFACE/README.md)
