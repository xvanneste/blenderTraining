# CH03.09 — Retopologie personnage

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un sculpt à 75 000 faces ne s'anime pas : il faut une topologie légère, tout en quads, dont les boucles suivent les muscles qui bougent — des anneaux autour des yeux et de la bouche. Ce chapitre fait la retopologie du visage de CH03.06 : une grille de quads resserrée autour des yeux et de la bouche (Inset Faces), des ouvertures aux bons endroits, collée au sculpt par Shrinkwrap. Le correcteur mesure la topologie (quads, valence, trous, densité) et l'adhérence à la surface.

## Prérequis

- CH03.06 (le visage).
- CH03.03 (densité).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une topologie de quads avec des boucles autour des yeux et de la bouche.
2. Coller un maillage léger à un sculpt (Shrinkwrap, Snap).
3. Contrôler une retopologie par des mesures (quads, pôles, densité, adhérence).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.09.a | Retopologie d'un personnage | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Principes : quads, boucles, pôles, budget | 2 h |
| L2 | Construire et coller la retopo | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_09_retopo_starter.blend` | Visage sculpté de CH03.06 + yeux, sans retopo |
| `COMPLETED_EXAMPLES/ch03_09_retopo_solution.blend` | RETOPO_Face (404 quads) sur SCULPT_Bust |
| `COMPLETED_EXAMPLES/ch03_09_retopo_reference.png` | Face, 3/4, profil (retopo en fil de fer) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (grille uniforme, triangulée, flottante, trop dense, boucles décalées) |
| `SCRIPTS/validate_ch03_09.py` | Correcteur (retopo) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_09_retopo_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_09.py" -- --exercise retopo --render
```

## Livrables attendus

1. Retopologie validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH03.10 — Préparation au rigging](../CH03_10_RIG_READY/README.md)
