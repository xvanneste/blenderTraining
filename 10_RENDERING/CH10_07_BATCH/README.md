# CH10.07 — Rendu distribué

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une ferme de rendu fait rendre à plusieurs machines des morceaux d'une animation. Le principe est simple : une ligne de commande Blender par morceau (blender -b fichier -s début -e fin -a), des réglages qui évitent les collisions (pas d'écrasement, des placeholders), et une orchestration (à la main, par script, ou avec un gestionnaire comme Flamenco). Ce chapitre se concentre sur la base : le correcteur EXÉCUTE réellement vos commandes (liste blanche d'options) et compte les images produites.

## Prérequis

- CH10.04 (sortie), CH13 non requis.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Écrire une commande Blender de rendu en arrière-plan.
2. Découper une animation sans trou ni recouvrement.
3. Respecter l'ordre des arguments (-a en dernier).
4. Régler Overwrite et Placeholders pour une ferme.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.07.a | Rendre en batch | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La ligne de commande | 3 h |
| L2 | Morceaux et ferme | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_07_batch_starter.blend` | Première commande avec « -a » avant « -s » (rend les 24 images), l'image 17 manque, Overwrite activé, Placeholders désactivé ; 13/39 |
| `COMPLETED_EXAMPLES/ch10_07_batch_solution.blend` | Trois commandes 1–8, 9–16, 17–24 avec « -a » en dernier ; Overwrite désactivé, Placeholders activé ; 39/39 |
| `COMPLETED_EXAMPLES/ch10_07_batch_reference.png` | Trois images de la solution (4, 12, 20), une par morceau |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (-a trop tôt, trou, recouvrement, un seul morceau, réglages de ferme, option interdite) |
| `SCRIPTS/validate_ch10_07.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_07_batch_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_07.py" -- --exercise batch
```

## Livrables attendus

1. Plan de rendu en trois commandes exécutées.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet P10 — Scène optimisée en EXR multicouche](../PROJECT_P10/README.md)
