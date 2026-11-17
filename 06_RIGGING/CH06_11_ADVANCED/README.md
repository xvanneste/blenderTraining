# CH06.11 — Rigging avancé et réutilisation

**Phase :** 6 — Rigging professionnel  
**Niveau :** expert  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Deux techniques de production. Les BENDY BONES découpent un bone en segments qui se courbent : un tube se plie en arche lisse au lieu de pivoter en bloc. La RÉUTILISATION d'un rig passe par une bibliothèque : le rig vit dans un fichier, chaque plan le LIE, puis crée un LIBRARY OVERRIDE pour le placer et l'animer sans jamais modifier l'original. Le correcteur mesure l'arche du tube (volet A) et vérifie la chaîne bibliothèque, override, action, chemin relatif (volet B).

## Prérequis

- CH06.03 (skinning), CH06.10 (organisation du rig).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer et courber un bendy bone.
2. Lier une collection depuis une bibliothèque (chemin relatif).
3. Créer un library override éditable.
4. Animer un rig overridé par une Action.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.11.a | Réutiliser un rig dans plusieurs plans | Exercices 2 et 3 (correcteur, deux volets) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Bendy bones | 2 h |
| L2 | Bibliothèque, link et override | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_11_bendy_starter.blend` | Volet A : tube sur un bone rigide (1 segment) |
| `COMPLETED_EXAMPLES/ch06_11_bendy_solution.blend` | Volet A : 8 segments |
| `COMPLETED_EXAMPLES/ch06_11_bendy_reference.png` | Tube droit et courbé : 1 segment contre 8 |
| `STARTER_FILES/ch06_11_rig_library.blend` | Volet B : la BIBLIOTHÈQUE (COL_Rig : RIG_Lib, GEO_Lib) — à LIER, pas à modifier |
| `STARTER_FILES/ch06_11_shot_starter.blend` | Volet B : plan vide (à sauvegarder à côté de la bibliothèque) |
| `COMPLETED_EXAMPLES/ch06_11_shot_solution.blend` | Volet B : plan avec rig lié, overridé, placé et posé (chemin //../STARTER_FILES/…) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (volet A : 1 segment, 2 segments, sans modificateur, sans déformation ; volet B : lien nu, copie locale, chemin absolu, rig non posé) |
| `SCRIPTS/validate_ch06_11.py` | Correcteur (bendy, override) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_11_bendy_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_11.py" -- --exercise bendy

& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_11_shot_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_11.py" -- --exercise override
```

## Livrables attendus

1. Tube bendy validé.
2. Plan avec rig overridé validé.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 2 et 3 validés.

➡️ Chapitre suivant : [Projet P6 — Personnage contrôlable](../PROJECT_P6/README.md)
