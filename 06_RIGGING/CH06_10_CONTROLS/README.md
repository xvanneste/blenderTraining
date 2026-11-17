# CH06.10 — Contrôleurs et ergonomie

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rig que l'animateur ne comprend pas est un mauvais rig. Ce chapitre rend lisible un rig déjà fonctionnel : trois collections de bones (Controls, Deform, Mechanism) dont deux masquées, des formes personnalisées sur les contrôleurs, des couleurs par côté, des verrous qui empêchent les gestes interdits, et une séparation nette entre les bones qui déforment et ceux qui se manipulent. Le correcteur vérifie la structure ET que le rig fonctionne toujours : tourner un contrôleur doit faire tourner le bon bone de déformation.

## Prérequis

- CH06.01–02 (armatures, contraintes), CH06.07 (Limit).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Organiser des bones en collections.
2. Créer des formes personnalisées.
3. Coder les côtés par la couleur.
4. Verrouiller les canaux inutiles.
5. Vérifier que l'ergonomie ne casse pas le rig.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.10.a | Rig agréable pour l'animateur | Exercice 2 (correcteur) + croquis |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Organiser : collections et déformation | 3 h |
| L2 | Formes, couleurs et verrous | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_10_controls_starter.blend` | Rig fonctionnel mais illisible |
| `COMPLETED_EXAMPLES/ch06_10_controls_solution.blend` | Rig organisé : collections, formes, couleurs, verrous |
| `COMPLETED_EXAMPLES/ch06_10_controls_reference.png` | Formes colorées en projection oblique, bones de déformation en gris |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans collections, non masquées, sans formes, sans couleurs, sans verrous, lien cassé, déformation sur les contrôleurs) |
| `SCRIPTS/validate_ch06_10.py` | Correcteur (controls) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_10_controls_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_10.py" -- --exercise controls
```

## Livrables attendus

1. Rig organisé validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.11 — Rigging avancé et réutilisation](../CH06_11_ADVANCED/README.md)
