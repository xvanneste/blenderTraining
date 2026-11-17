# CH00.07 — Sauvegardes, récupération, versions

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Tout le monde perd un jour du travail : plantage, mauvaise manipulation, disque qui meurt. La différence entre un amateur et un professionnel, c'est que le professionnel perd cinq minutes, pas trois semaines. Vous découvrirez les cinq filets de sécurité de Blender, la discipline des versions incrémentales, la règle de sauvegarde 3-2-1 automatisée par script, et les formats de fichiers qui circulent dans un pipeline de film. Exercice : récupérer un personnage supprimé puis enregistré par erreur.

## Prérequis

- CH00.02 (Auto Save, Save Versions)
- CH00.06 (arborescence, nommage _vNNN)

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Récupérer un travail perdu (Last Session, Auto Save, .blend1).
2. Versionner avec Save Incremental (Ctrl+Alt+S).
3. Mettre en place une sauvegarde 3-2-1 automatisée et tester une restauration.
4. Choisir le bon format d'échange (USD, Alembic, FBX, glTF, OBJ, EXR, PNG).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.07.a | Récupérer un travail perdu et versionner | Exercices 1 et 3 (correcteur) |
| C00.07.b | Appliquer une stratégie de sauvegarde 3-2-1 | Exercice 2 |
| C00.07.c | Choisir un format de fichier adapté | Exercice 4, quiz |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les filets de sécurité et la récupération | 25 min |
| L2 | Versionner | 15 min |
| L3 | Sauvegarde 3-2-1 | 25 min |
| L4 | Formats de fichiers | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch00_07_recovery/ch00_07_hero_scene_v001.blend` | Fichier enregistré après la suppression du héros |
| `STARTER_FILES/ch00_07_recovery/ch00_07_hero_scene_v001.blend1` | Copie de sauvegarde contenant encore le héros |
| `COMPLETED_EXAMPLES/ch00_07_hero_scene_v002.blend` | Version récupérée |
| `../../SCRIPTS/bcma_backup.py` | Sauvegarde zip datée, vérifiée, avec rotation |
| `SCRIPTS/validate_ch00_07.py` | Correcteur de l'exercice 3 |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "<dossier>\ch00_07_hero_scene_v002.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_07.py" -- --exercise recover
```

## Livrables attendus

1. ch00_07_hero_scene_v002.blend validé.
2. Sauvegarde 3-2-1 en place, restauration testée.
3. Fiche de poste §8 (plan de continuité).

## Critères pour passer au chapitre suivant

- Quiz ≥ 11/14.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH00.08 — Introduction au pipeline cinéma](../CH00_08_PIPELINE_INTRO/README.md)
