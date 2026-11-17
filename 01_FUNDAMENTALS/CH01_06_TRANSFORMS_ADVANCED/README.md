# CH01.06 — Transformations avancées

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Une caisse peut mesurer 2 mètres parce que son maillage mesure 2 mètres, ou parce qu'on a étiré un cube d'un mètre : même image, mais des biseaux, des simulations et des exports qui se comportent différemment. Ce chapitre explique la différence entre échelle et dimensions et pourquoi on applique les transformations, puis les orientations (global, local, normal…) et le snapping, l'aimantation qui permet de poser, plaquer et aligner sans approximation. Exercice : un déménagement où rien ne doit flotter ni traverser.

## Prérequis

- CH01.03 (G, R, S, axes).
- CH01.04 (données partagées).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer échelle et dimensions ; appliquer les transformations (Ctrl+A) et savoir quand.
2. Choisir une orientation de transformation (Global, Local, Normal, View…).
3. Configurer et utiliser le snapping (Snap Target, Snap Base, Ctrl temporaire).
4. Poser et plaquer des objets avec précision.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.06.a | Appliquer échelle/rotation à bon escient, aligner par snapping | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Échelle, dimensions, appliquer | 25 min |
| L2 | Orientations | 20 min |
| L3 | Snapping | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_06_moving_starter.blend` | Caisse étirée, livre flottant, étagère, planche tournée |
| `COMPLETED_EXAMPLES/ch01_06_moving_solution.blend` | Tout posé et aligné |
| `SCRIPTS/validate_ch01_06.py` | Correcteur (18 points) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_06_moving_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_06.py" -- --exercise moving
```

## Livrables attendus

1. ch01_06_moving_<prenom>_v001.blend validé.
2. Mini-projet : la chambre rangée.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.07 — Origines, pivots, curseur 3D](../CH01_07_ORIGINS_PIVOTS/README.md)
