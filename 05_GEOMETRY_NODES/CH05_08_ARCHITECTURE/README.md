# CH05.08 — Architecture procédurale

**Phase :** 5 — Geometry Nodes  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un bâtiment est une grille : des étages, des travées, des fenêtres régulières. Ce chapitre construit un outil « Immeuble » à cinq paramètres (étages, travées, hauteur d'étage, largeur de travée, profondeur) où la façade se recompose toute seule : le corps est un cube dimensionné par les paramètres, les fenêtres sont des instances posées au centre de chaque travée et de chaque étage par une Grid. Le correcteur règle l'outil sur deux configurations différentes et mesure le nombre de fenêtres, les dimensions du corps et la régularité de la façade.

## Prérequis

- CH05.03
- CH05.06.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Traduire des dimensions réelles en nœuds mathématiques.
2. Placer des éléments sur une grille régulière (Grid centrée sur les travées).
3. Garder un modèle cohérent quand les paramètres changent.
4. Valider un outil architectural par mesures.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.08.a | Générer un bâtiment | Exercice 2 (correcteur) + rendu des deux réglages |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | De la grille au bâtiment | 3 h |
| L2 | Façade paramétrique | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_08_architecture_starter.blend` | Immeuble 5 × 4 en dur, sans interface |
| `COMPLETED_EXAMPLES/ch05_08_architecture_solution.blend` | Outil « Immeuble » à cinq paramètres |
| `COMPLETED_EXAMPLES/ch05_08_architecture_reference.png` | Deux immeubles : défaut (bas) et 7 étages × 3 travées (haut) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (nombre de fenêtres fixe, hauteur du corps fixe, espacement faux, fenêtres hors façade) |
| `SCRIPTS/validate_ch05_08.py` | Correcteur (architecture) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_08_architecture_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_08.py" -- --exercise architecture --render
```

## Livrables attendus

1. Outil « Immeuble » validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.09 — Boucles et simulation](../CH05_09_LOOPS/README.md)
