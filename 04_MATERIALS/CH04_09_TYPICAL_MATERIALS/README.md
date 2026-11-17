# CH04.09 — Matériaux types

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Une bibliothèque de base évite de réinventer le même matériau à chaque plan. Ce chapitre construit cinq matériaux de référence — bois, pierre, plastique, verre, acier brossé — chacun avec la recette qui le rend crédible (texture qui varie, bump, vernis, anisotropie), puis les marque comme assets pour l'Asset Browser. Le correcteur contrôle les graphes et les valeurs de chaque matériau et la présence des métadonnées d'asset.

## Prérequis

- CH04.03–05 (Principled, nœuds, textures procédurales).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Reconnaître la recette d'un matériau courant.
2. Construire bois, pierre, plastique, verre et acier brossé.
3. Marquer des matériaux comme assets avec une description.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.09.a | Constituer une bibliothèque de matériaux de base | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Recettes de matériaux | 2 h 30 |
| L2 | Construire et publier la bibliothèque | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_09_materials_starter.blend` | Cinq sphères, matériaux par défaut |
| `COMPLETED_EXAMPLES/ch04_09_materials_solution.blend` | Cinq matériaux, marqués assets |
| `COMPLETED_EXAMPLES/ch04_09_materials_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (bois uni, pierre sans bump, acier isotrope, matériau non marqué, plastique mat) |
| `SCRIPTS/validate_ch04_09.py` | Correcteur (materials) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_09_materials_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_09.py" -- --exercise materials --render
```

## Livrables attendus

1. Bibliothèque de cinq matériaux validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.10 — Matériaux de personnages](../CH04_10_CHARACTER_MATERIALS/README.md)
