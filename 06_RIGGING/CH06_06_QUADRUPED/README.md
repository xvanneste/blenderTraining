# CH06.06 — Rig quadrupède

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un quadrupède n'est pas un humain à quatre pattes : colonne horizontale, pattes à quatre segments (cuisse, jambe, pied, orteils) avec le talon haut, queue. Rigify fournit pour cela des méta-rigs (Basic Quadruped, Cat, Horse, Wolf, Bird, Shark). Ce chapitre rigge une créature avec le méta-rig Basic Quadruped (34 bones, 283 une fois généré) : remise du méta-rig sur la créature, génération, skinning. Le correcteur vérifie rig, ajustement et peau, puis déplace la racine et lève la patte avant gauche : seule cette patte monte.

## Prérequis

- CH06.03–05.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir et poser un méta-rig quadrupède.
2. Ajuster méta-rig et créature (échelle, position).
3. Générer le rig et lier la créature.
4. Contrôler un rig par le mouvement d'une patte.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.06.a | Rig quadrupède | Exercice 2 (correcteur) + croquis de profil |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le méta-rig quadrupède | 3 h |
| L2 | Peau et contrôle des pattes | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_06_quadruped_starter.blend` | Créature et méta-rig mal placé (échelle 1,4, décalé) |
| `COMPLETED_EXAMPLES/ch06_06_quadruped_solution.blend` | Rig généré et créature liée |
| `COMPLETED_EXAMPLES/ch06_06_quadruped_reference.png` | Profil : bones DEF sur la créature, puis patte avant gauche levée |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (rig non généré, créature non liée, méta-rig non ajusté, sans modificateur, poids partiels, rig décalé) |
| `SCRIPTS/validate_ch06_06.py` | Correcteur (quadruped) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_06_quadruped_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_06.py" -- --exercise quadruped
```

## Livrables attendus

1. Rig quadrupède validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.07 — Rig mécanique](../CH06_07_MECHANICAL/README.md)
