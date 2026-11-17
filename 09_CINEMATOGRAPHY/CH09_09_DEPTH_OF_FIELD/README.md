# CH09.09 — Profondeur de champ

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

La profondeur de champ est la zone de l'espace qui paraît nette. Une grande ouverture (petit F-Stop) la réduit : le sujet reste net et le reste se fond. C'est l'outil de base pour diriger le regard. Ce chapitre active la profondeur de champ d'une caméra Cycles, règle la distance de mise au point et l'ouverture, et le correcteur mesure le résultat par rendu : le pic d'une barre lumineuse nette vaut 1, celui d'une barre floue s'effondre.

## Prérequis

- CH09.08 (focale, distance), CH10 non requis (Cycles de base).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer la profondeur de champ d'une caméra.
2. Régler Focus Distance et F-Stop.
3. Prévoir le sens du flou (avant et arrière-plan).
4. Mesurer la netteté sur un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.09.a | Diriger le regard par la profondeur de champ | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Ouverture et mise au point | 3 h |
| L2 | Mesurer le flou | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_09_dof_starter.blend` | Profondeur de champ désactivée : les deux barres sont nettes (pics 1,00 et 1,00) |
| `COMPLETED_EXAMPLES/ch09_09_dof_solution.blend` | Depth of Field activée, Focus Distance 5 m, F-Stop 1,0 : barre proche nette (1,00), barre lointaine floue (0,31) |
| `COMPLETED_EXAMPLES/ch09_09_dof_reference.png` | Rendu de départ (gauche) et solution (droite) : la barre lointaine devient une tache floue |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (DOF désactivée, mauvaise distance, petite ouverture, mise au point intermédiaire, F-Stop sans DOF) |
| `SCRIPTS/validate_ch09_09.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_09_dof_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_09.py" -- --exercise dof
```

## Livrables attendus

1. Réglage justifié (distance, ouverture).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.10 — Mouvements et grammaire](../CH09_10_MOVEMENTS/README.md)
