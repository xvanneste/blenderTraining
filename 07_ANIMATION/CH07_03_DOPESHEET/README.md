# CH07.03 — Dope Sheet et Action

**Phase :** 7 — Animation 3D  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le Dope Sheet montre les clés d'une animation comme des losanges sur une grille d'images : on y sélectionne, déplace et met à l'échelle le TEMPS. Ce chapitre apprend à retimer une animation (doubler sa durée), à dupliquer une action et à la décaler, et à comprendre ce qu'est une action (un bloc de données indépendant) et un slot (Blender 5.x : le lien entre une action et un objet). Le correcteur lit les clés (images et valeurs), l'indépendance des deux actions et l'animation évaluée.

## Prérequis

- CH07.02 (clés et timeline).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire un Dope Sheet.
2. Retimer par mise à l'échelle autour d'une image.
3. Dupliquer et décaler une action.
4. Distinguer action, slot et utilisateurs.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.03.a | Retimer une animation | Exercice 2 (correcteur) + croquis du Dope Sheet |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lire et retimer | 3 h |
| L2 | Actions et slots | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_03_dopesheet_starter.blend` | Caisse A animée aux images 1, 13, 25 (action Slide) ; caisse B sans animation |
| `COMPLETED_EXAMPLES/ch07_03_dopesheet_solution.blend` | A retimée (1, 25, 49) ; B avec sa propre action Slide_Late (25, 49, 73) |
| `COMPLETED_EXAMPLES/ch07_03_dopesheet_reference.png` | Dope Sheet en numpy : départ (gris), A retimée (vert), B décalée (orange) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (non retimée, mauvais pivot, action partagée, copie non décalée, plage non étendue, valeurs inversées) |
| `SCRIPTS/validate_ch07_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_03_dopesheet_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_03.py" -- --exercise dopesheet
```

## Livrables attendus

1. Deux actions retimées et décalées validées.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.04 — Graph Editor](../CH07_04_GRAPHEDITOR/README.md)
