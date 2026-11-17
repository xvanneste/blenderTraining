# CH06.08 — Shape keys et drivers

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le skinning linéaire écrase les articulations : un coude plié à 90° perd du volume (rayon de l'anneau du coude : 4,08 cm au lieu de 5,00 cm). Un shape key correctif remet le volume, et un driver le déclenche automatiquement en fonction de la pose. Ce chapitre construit ce mécanisme sur un bras-tube : shape key limité par un groupe de sommets, valeur pilotée par la rotation du bone fore. Le correcteur plie le bras à 45° et 90° et mesure les sommets évalués.

## Prérequis

- CH06.03 (skinning), CH06.07 (drivers).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un shape key relatif à Basis.
2. Le limiter par un groupe de sommets.
3. Le piloter par un driver lié à une pose.
4. Mesurer l'effet sur le maillage évalué.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.08.a | Corrective shape keys | Exercice 2 (correcteur) + croquis du coude |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le shape key correctif | 3 h |
| L2 | Le driver et la mesure | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_08_shapekeys_starter.blend` | Bras lié (Automatic Weights), sans shape key ni driver |
| `COMPLETED_EXAMPLES/ch06_08_shapekeys_solution.blend` | Shape key elbow_fix, groupe elbow, driver sur fore |
| `COMPLETED_EXAMPLES/ch06_08_shapekeys_reference.png` | Vue de dessus à 90° : coude écrasé (gauche) puis corrigé (droite) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans shape key, sans driver, toujours actif, trop faible, sans groupe, mauvais bone) |
| `SCRIPTS/validate_ch06_08.py` | Correcteur (shapekeys) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_08_shapekeys_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_08.py" -- --exercise shapekeys
```

## Livrables attendus

1. Shape key correctif piloté validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.09 — Rig facial](../CH06_09_FACIAL/README.md)
