# CH07.07 — Posing et silhouette

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Une bonne animation commence par de bonnes poses : lisibles d'un coup d'œil, vivantes, en équilibre. Ce chapitre apprend à poser un mannequin avec trois outils : le CONTRAPPOSTO (épaules et hanches inclinées en sens opposés), l'APPUI (une jambe porte le poids, l'autre se détend) et la LIGNE D'ACTION (une colonne courbe en C), puis à juger la SILHOUETTE (un rendu plat, de face, doit se lire sans détail). Le correcteur mesure les bones de la pose enregistrée et rend la silhouette en Workbench pour en calculer la solidité.

## Prérequis

- CH06.01 (armatures), CH07.01 (principes), CH07.02 (clés).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Incliner épaules et hanches en sens opposés.
2. Équilibrer le poids sur une jambe.
3. Courber la colonne en ligne d'action.
4. Juger une silhouette à plat.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.07.a | Poses lisibles | Exercice 2 (correcteur) + silhouettes |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Contrapposto, appui, ligne d'action | 4 h |
| L2 | La silhouette | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_07_posing_starter.blend` | Mannequin FK en T-pose (13 bones, lié par groupes de sommets) |
| `COMPLETED_EXAMPLES/ch07_07_posing_solution.blend` | Mannequin posé : contrapposto, appui sur la jambe droite, colonne en C, bras dégagés |
| `COMPLETED_EXAMPLES/ch07_07_posing_reference.png` | Silhouettes de face (rendu Workbench) : T-pose puis pose |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans bascule, bascule parallèle, deux jambes pliées, déséquilibre, colonne droite, bras collés) |
| `SCRIPTS/validate_ch07_07.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_07_posing_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_07.py" -- --exercise posing
```

## Livrables attendus

1. Pose du mannequin validée.
2. Trois silhouettes de poses différentes.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.08 — Cycles de marche](../CH07_08_WALK/README.md)
