# CH06.04 — IK/FK

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

En cinématique directe (FK) on tourne chaque os ; en cinématique inverse (IK) on place l'extrémité et le solveur calcule les rotations. Un bon rig de bras propose les deux et permet de basculer. Ce chapitre construit un bras IK/FK : contrainte IK sur l'avant-bras avec une cible (ik_hand) et un pôle (ik_pole) qui choisit le côté du coude, et un interrupteur (propriété ik_fk d'un bone switch) qui pilote l'influence de l'IK par un driver. Le correcteur déplace les contrôleurs et mesure : le bout atteint la cible, les longueurs ne changent pas, le coude suit le pôle, le bras se tend sans s'étirer hors de portée, et le mode FK rend le bras à la rotation.

## Prérequis

- CH06.01–02.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Poser une contrainte IK avec cible et pôle.
2. Régler Pole Angle et Chain Length.
3. Éviter l'étirement et la singularité du bras droit.
4. Commuter IK/FK par une propriété et un driver.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.04.a | Bras IK/FK | Exercice 2 (correcteur) + croquis des quatre poses |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | IK, cible et pôle | 3 h |
| L2 | Commutation IK/FK par driver | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_04_ikfk_starter.blend` | Bras et contrôleurs, sans IK ni driver |
| `COMPLETED_EXAMPLES/ch06_04_ikfk_solution.blend` | Bras IK/FK à commutateur |
| `COMPLETED_EXAMPLES/ch06_04_ikfk_reference.png` | Quatre poses : IK pôle haut, IK pôle bas, IK hors de portée, FK |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans pôle, sans driver, avec étirement, chaîne d'un os, sans IK) |
| `SCRIPTS/validate_ch06_04.py` | Correcteur (ikfk) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_04_ikfk_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_04.py" -- --exercise ikfk
```

## Livrables attendus

1. Bras IK/FK validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.05 — Rig humanoïde](../CH06_05_HUMANOID/README.md)
