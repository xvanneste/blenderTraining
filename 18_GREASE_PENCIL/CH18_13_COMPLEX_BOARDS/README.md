# CH18.13 — Storyboards d'action, d'émotion, complexes

**Phase :** 18 — Grease Pencil (module C : storyboard)  
**Niveau :** intermédiaire → avancé  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Raconter une action en images, c'est maîtriser la clarté (une idée par case), le rythme (la durée des plans) et l'émotion (la réaction). Ce chapitre construit une planche de 12 cases normée — le projet obligatoire n° 1 de la phase 18 — vérifiée jusque dans son rythme : durée moyenne, plans courts pendant l'action, plans longs pour installer et conclure.

## Prérequis

- CH18.10 à CH18.12.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Rendre une action lisible case par case.
2. Construire le rythme par la durée et l'alternance des plans.
3. Dessiner des plans de réaction et d'émotion.
4. Garder la géographie claire avec plusieurs personnages.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.13.a | Storyboard d'action lisible | Exercice 3 = projet n° 1 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Clarté de l'action | 1 h |
| L2 | Rythme et émotion | 1 h |
| L3 | Séquences complexes (projet n° 1) | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_13_action_starter.blend` | Gabarit de 12 cases |
| `COMPLETED_EXAMPLES/ch18_13_action_solution.blend` | Séquence « La tasse tombe » |
| `COMPLETED_EXAMPLES/ch18_13_action_reference.png` | Rendu de la planche |
| `SCRIPTS/validate_ch18_13.py` | Correcteur (dessin, flèches, notes, variété, rythme) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_13_action_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_13.py" --python-exit-code 1 -- --exercise action --render
```

## Livrables attendus

1. Planche de 12 cases validée (projet obligatoire n° 1).
2. Auto-évaluation ≥ 14/20.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Planche validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.14 — Du scénario à l'animatique](../CH18_14_ANIMATIC/README.md)
