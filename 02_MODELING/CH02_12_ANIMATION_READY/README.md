# CH02.12 — Modélisation pour l'animation

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 1 h 45  
**Version :** Blender 5.3.0

## Introduction

Un personnage plie aux articulations : sa topologie doit le permettre. Ce chapitre montre, mesures à l'appui, pourquoi un coude à 4 segments s'écrase (12,5 % de volume perdu) et comment trois boucles bien placées le sauvent, puis fixe les règles d'échelle, de transformations et de pose pour livrer un maillage prêt au rigging.

## Prérequis

- CH02.01 (pôles)
- CH02.02 (Loop Cut)
- CH02.09 (densité).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer la perte de volume au pli d'une articulation.
2. Placer des boucles d'articulation efficaces.
3. Respecter échelle réelle, transformations appliquées et pose de référence.
4. Tester la déformation avec une armature simple.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.12.a | Préparer un mesh déformable | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Pourquoi un maillage plie mal | 30 min |
| L2 | Boucles d'articulation | 45 min |
| L3 | Échelle, transformations, test précoce | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_12_arm_starter.blend` | Bras à 4 segments + armature 2 os |
| `COMPLETED_EXAMPLES/ch02_12_arm_solution.blend` | Bras avec 4 boucles au coude |
| `COMPLETED_EXAMPLES/ch02_12_arm_bent_starter.png` | Coude plié, avant |
| `COMPLETED_EXAMPLES/ch02_12_arm_bent_solution.png` | Coude plié, après |
| `SCRIPTS/validate_ch02_12.py` | Correcteur (boucles, quads, volume au pli de 90°) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_12_arm_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_12.py" -- --exercise arm --render
```

## Livrables attendus

1. Bras validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : la main.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Bras validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.13 — Assets réutilisables](../CH02_13_ASSETS/README.md)
