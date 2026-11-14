# CH01.01 — L'interface

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant absolu  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Blender n'a pas une interface figée : c'est un atelier que l'on reconfigure selon la tâche. Comprendre sa logique — workspaces, zones, éditeurs, régions — vous évitera la principale frustration des débutants : « je ne trouve pas » et « le raccourci ne marche pas ». Vous partirez à la chasse au trésor dans une scène préparée, apprendrez à diviser, fusionner et maximiser les zones, à trouver n'importe quelle commande avec F3, et vous construirez votre propre workspace d'étude.

## Prérequis

- Phase 0 validée (Blender 5.3 installé, préférences réglées).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Nommer les parties de l'interface : topbar, workspaces, zones, éditeurs, régions, status bar.
2. Reconnaître les éditeurs essentiels et leur rôle.
3. Afficher/masquer Toolbar (T) et Sidebar (N), utiliser Adjust Last Operation (F9).
4. Diviser, fusionner, maximiser une zone et changer son éditeur.
5. Trouver une commande avec F3 et comprendre le principe du survol.
6. Créer et enregistrer un workspace personnel.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.01.a | Nommer et réorganiser les éditeurs | Exercices 1–3, tests chronométrés |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Zones, éditeurs, workspaces | 30 min |
| L2 | Régions et Adjust Last Operation | 20 min |
| L3 | Manipuler les zones | 25 min |
| L4 | Trouver une commande, principe du survol | 15 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_01_interface_starter.blend` | Scène par défaut + chasse au trésor (Text Editor : README_EXERCICE) |
| `COMPLETED_EXAMPLES/ch01_01_interface_solution.blend` | Fichier contenant un workspace BCMA_Study |
| `SCRIPTS/validate_ch01_01.py` | Correcteur de l'exercice 3 |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_01_interface_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_01.py" --python-exit-code 1 -- --exercise workspace
```

## Livrables attendus

1. Réponses de la chasse au trésor.
2. ch01_01_interface_<prenom>_v001.blend validé.
3. Capture annotée « Mon atelier ».

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.02 — Navigation 3D](../CH01_02_NAVIGATION/README.md)
