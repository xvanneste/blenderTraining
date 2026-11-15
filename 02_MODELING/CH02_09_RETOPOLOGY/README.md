# CH02.09 — Retopologie

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 15  
**Version :** Blender 5.3.0

## Introduction

Sculptures, scans et booléens donnent des maillages trop denses et désordonnés pour l'animation et les UV. La retopologie reconstruit une cage légère en quads par-dessus. Ce chapitre présente la méthode rapide au Shrinkwrap (avec un piège mesuré : la cage doit envelopper la forme) et la méthode manuelle au Poly Build avec aimantation sur la surface.

## Prérequis

- CH02.01 (topologie)
- CH02.06 (subdivision).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir une densité selon l'usage.
2. Retopologiser une forme simple avec Shrinkwrap.
3. Configurer l'aimantation Face Project et Poly Build.
4. Contrôler écart et couverture d'une cage.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.09.a | Retopologiser un sculpt simple | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Pourquoi et combien | 30 min |
| L2 | Retopologie rapide (Shrinkwrap) | 45 min |
| L3 | Retopologie manuelle | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_09_retopo_starter.blend` | Rocher sculpté de 20 480 faces |
| `COMPLETED_EXAMPLES/ch02_09_retopo_solution.blend` | Cage de 216 quads + Shrinkwrap |
| `COMPLETED_EXAMPLES/ch02_09_retopo_reference.png` | Rendu de la cage |
| `COMPLETED_EXAMPLES/ch02_09_retopo_wire.png` | Rendu fil de fer |
| `SCRIPTS/validate_ch02_09.py` | Correcteur (densité, quads, écart et couverture BVH) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_09_retopo_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_09.py" --python-exit-code 1 -- --exercise retopo --render
```

## Livrables attendus

1. Cage validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : retopologie de la créature.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Cage validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.10 — Optimisation](../CH02_10_OPTIMIZATION/README.md)
