# CH07.06 — Arcs, overlap, follow-through

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Un corps souple ne bouge pas d'un bloc : quand la base s'arrête, la pointe continue (FOLLOW-THROUGH), chaque partie atteint son extrême un peu après la précédente (OVERLAP), et la pointe décrit une courbe (ARC). Ces trois principes donnent vie aux queues, antennes, cheveux, vêtements. Ce chapitre les applique à une antenne de quatre bones en chaîne : retard de 2 images par bone, suite du mouvement après l'arrêt de la base, dépassement du repos puis stabilisation. Le correcteur lit les angles évalués image par image.

## Prérequis

- CH07.04 (Graph Editor), CH07.05 (timing).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Décaler les clés le long d'une chaîne (overlap).
2. Prolonger le mouvement après l'arrêt du parent (follow-through).
3. Ajouter un dépassement et une stabilisation.
4. Vérifier un arc sur la trajectoire de la pointe.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.06.a | Overlap convaincant | Exercice 2 (correcteur) + courbes d'angle |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Overlap et arcs | 4 h |
| L2 | Follow-through et dépassement | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_06_overlap_starter.blend` | Antenne de quatre bones : seule la base est animée (aller-retour de 25°) |
| `COMPLETED_EXAMPLES/ch07_06_overlap_solution.blend` | Overlap de 2 images par bone, follow-through, dépassement de −6°, repos final |
| `COMPLETED_EXAMPLES/ch07_06_overlap_reference.png` | Courbes d'angle des quatre bones (cascade) et trajectoire de la pointe (arc) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans overlap, retards trop longs, sans follow-through, sans dépassement, sans repos, queue raide) |
| `SCRIPTS/validate_ch07_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_06_overlap_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_06.py" -- --exercise overlap
```

## Livrables attendus

1. Antenne souple validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.07 — Posing et silhouette](../CH07_07_POSING/README.md)
