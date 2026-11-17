# CH01.03 — Sélection et manipulation

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant absolu  
**Durée estimée :** 2 h 30  
**Version :** Blender 5.3.0

## Introduction

Sélectionner et transformer, c'est 80 % des gestes d'un artiste 3D. Ce chapitre installe la distinction essentielle entre objets sélectionnés et objet actif, toutes les méthodes de sélection (clic, rectangle, cercle, lasso, Outliner, motif de nom), et les transformations au clavier — G, R, S, contraintes d'axe, saisie numérique — qui donnent vitesse et précision. Exercice phare : un puzzle de quatre pièces à ranger exactement dans leurs silhouettes, vérifié au centimètre près.

## Prérequis

- CH01.02 (navigation).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer objets sélectionnés et objet actif.
2. Sélectionner par clic, rectangle, cercle, lasso, Outliner et motif de nom.
3. Déplacer, tourner, mettre à l'échelle au clavier avec contraintes d'axe globales et locales.
4. Saisir des valeurs exactes et remettre à zéro les transformations.
5. Utiliser gizmos et sidebar, y compris sur plusieurs objets à la fois.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.03.a | Transformer avec précision au clavier | Exercice 3 (correcteur), tests chronométrés |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Sélectionner | 30 min |
| L2 | Transformer au clavier | 40 min |
| L3 | Gizmos, sidebar et précision | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_03_puzzle_starter.blend` | 4 pièces, 4 silhouettes cibles, 30 cailloux |
| `COMPLETED_EXAMPLES/ch01_03_puzzle_solution.blend` | Pièces rangées |
| `SCRIPTS/validate_ch01_03.py` | Correcteur (comparaison géométrique au cm) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_03_puzzle_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_03.py" -- --exercise puzzle
```

## Livrables attendus

1. ch01_03_puzzle_<prenom>_v001.blend validé.
2. Mini-projet : nature morte de primitives rendue.

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.04 — Objets et meshes](../CH01_04_OBJECTS_DATA/README.md)
