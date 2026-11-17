# CH07.05 — Timing et spacing

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Le TIMING, c'est le nombre d'images entre deux événements ; le SPACING, c'est la distance parcourue d'une image à l'autre. Ensemble, ils donnent le poids et la vitesse. La balle rebondissante est l'exercice fondamental : une balle lâchée de 2,76 m doit rebondir trois fois puis s'arrêter, avec une gravité crédible. Le correcteur lit la hauteur de la balle à chaque image : contacts, décroissance, cohérence avec la gravité, espacement parabolique, repos final.

## Prérequis

- CH07.01 (principes), CH07.04 (Graph Editor).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer timing et spacing.
2. Calculer hauteurs et durées d'une balle qui obéit à la gravité.
3. Poser des clés et des poignées qui produisent une parabole.
4. Vérifier l'espacement par chronophotographie.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.05.a | Balle rebondissante crédible | Exercice 2 (correcteur) + chronophotographie |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Timing, spacing et gravité | 4 h |
| L2 | Poser la balle dans le Graph Editor | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_05_bounce_starter.blend` | Balle à deux clés (lâcher à 2,759 m, repos à l'image 72) : elle flotte jusqu'au sol |
| `COMPLETED_EXAMPLES/ch07_05_bounce_solution.blend` | Balle rebondissante : 7 clés, poignées exactes (sommets horizontaux, contacts raides) |
| `COMPLETED_EXAMPLES/ch07_05_bounce_reference.png` | Courbe de hauteur et chronophotographie (un carré par image) : espacement parabolique |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (linéaire, flottante, sans décroissance, durées égales, sans repos, sous le sol) |
| `SCRIPTS/validate_ch07_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_05_bounce_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_05.py" -- --exercise bounce
```

## Livrables attendus

1. Balle rebondissante validée.
2. Chronophotographie annotée.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.06 — Arcs, overlap, follow-through](../CH07_06_OVERLAP/README.md)
