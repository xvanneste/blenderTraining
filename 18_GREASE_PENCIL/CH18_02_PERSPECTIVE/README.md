# CH18.02 — Perspective

**Phase :** 18 — Grease Pencil (module A : fondamentaux du dessin)  
**Niveau :** débutant  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

La perspective place le spectateur dans l'espace : elle dit à quelle hauteur et dans quelle direction regarde la caméra. Ce chapitre explique la ligne d'horizon, les points de fuite et les fuyantes, puis les systèmes à un, deux et trois points de fuite, la mesure en perspective, la place des personnages par rapport à l'horizon et la perspective atmosphérique. Exercice : un couloir, un coin de rue et une tour en contre-plongée sur une feuille Grease Pencil guidée.

## Prérequis

- CH18.01 (boîtes en perspective).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Placer une ligne d'horizon et des points de fuite selon le point de vue voulu.
2. Choisir entre perspective à 1, 2 ou 3 points.
3. Diviser, répéter et reporter des hauteurs en perspective.
4. Placer des personnages par rapport à l'horizon.
5. Relier perspective dessinée et focale/orientation d'une caméra 3D.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.02.a | Dessiner un décor en perspective | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Horizon, points de fuite, fuyantes | 45 min |
| L2 | Deux et trois points | 1 h |
| L3 | Mesurer, répéter, éloigner | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_02_perspective_starter.blend` | Feuille à 3 cadres guidés (1, 2, 3 points) |
| `COMPLETED_EXAMPLES/ch18_02_perspective_solution.blend` | Couloir, rue, tour (référence) |
| `COMPLETED_EXAMPLES/ch18_02_perspective_reference.png` | Rendu de la référence |
| `SCRIPTS/validate_ch18_02.py` | Correcteur (via bcma_gp_check + gp_spec.json) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_02_perspective_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_02.py" --python-exit-code 1 -- --exercise perspective --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : trois décors.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.03 — Proportions, silhouettes, gestuelle](../CH18_03_PROPORTIONS_GESTURE/README.md)
