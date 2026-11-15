# CH02.10 — Optimisation

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 1 h 45  
**Version :** Blender 5.3.0

## Introduction

Chaque triangle coûte en mémoire, en affichage et en rendu. Ce chapitre apprend à mesurer (en triangles, l'unité réelle du Decimate), à alléger un objet dense sans changer sa silhouette, à créer des niveaux de détail (LOD) en copies liées, et à nettoyer un modèle importé.

## Prérequis

- CH02.01 (topologie)
- CH02.04 (normales).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Mesurer un objet en triangles avec Statistics.
2. Choisir le mode de Decimate adapté.
3. Créer des LOD en copies liées.
4. Nettoyer un import (By Distance, Delete Loose).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.10.a | Réduire un mesh sans perte visible | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Mesurer et réduire | 45 min |
| L2 | Les LOD | 30 min |
| L3 | Nettoyer un import | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_10_optim_starter.blend` | Statue dense, référence cachée, import sale |
| `COMPLETED_EXAMPLES/ch02_10_optim_solution.blend` | Statue allégée, 2 LOD liés, import nettoyé |
| `COMPLETED_EXAMPLES/ch02_10_optim_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch02_10.py` | Correcteur (triangles, écart BVH, LOD liés, nettoyage) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_10_optim_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_10.py" --python-exit-code 1 -- --exercise optim --render
```

## Livrables attendus

1. Fichier validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : budget de scène.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Fichier validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.11 — UV fondamentaux](../CH02_11_UV_BASICS/README.md)
