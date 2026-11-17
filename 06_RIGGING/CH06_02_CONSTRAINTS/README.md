# CH06.02 — Contraintes

**Phase :** 6 — Rigging professionnel  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Une contrainte impose à un objet ou à un bone un comportement calculé : viser une cible, copier une rotation, limiter un angle. Elles sont la base des mécanismes d'un rig. Ce chapitre construit un rig de regard : deux yeux qui visent exactement une cible (Damped Track), une tête qui la suit à moitié (Damped Track à 50 %) puis qui est limitée à ± 35° (Limit Rotation). L'ordre de la pile compte. Le correcteur DÉPLACE la cible à trois endroits et mesure l'erreur de visée des yeux et la rotation de la tête.

## Prérequis

- CH06.01.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter des contraintes de bone et régler cible, axe, influence.
2. Comprendre l'ordre d'évaluation d'une pile de contraintes.
3. Combiner suivi et limite.
4. Valider un mécanisme en déplaçant sa cible.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.02.a | Construire un mécanisme par contraintes | Exercice 2 (correcteur) + croquis du regard |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Suivre une cible | 2 h 30 |
| L2 | Piles, influence et limites | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_02_constraints_starter.blend` | Armature de regard et cible, sans contraintes |
| `COMPLETED_EXAMPLES/ch06_02_constraints_solution.blend` | Rig de regard à contraintes |
| `COMPLETED_EXAMPLES/ch06_02_constraints_reference.png` | Croquis vue de dessus : trois positions de la cible (rouge) ; tête en jaune, yeux en orange |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans contraintes, mauvais axe, tête à 100 %, sans limite, œil sans cible, ordre inversé) |
| `SCRIPTS/validate_ch06_02.py` | Correcteur (constraints) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_02_constraints_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_02.py" -- --exercise constraints
```

## Livrables attendus

1. Rig de regard validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.03 — Skinning](../CH06_03_SKINNING/README.md)
