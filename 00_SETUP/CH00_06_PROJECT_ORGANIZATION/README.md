# CH00.06 — Organisation de projet

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Les films terminés sont ceux dont l'organisation permet d'avancer sans friction. Ce chapitre installe les réflexes de studio : une arborescence de production claire (assets séparés des plans, une tâche par dossier), un nommage lisible par les humains et par les scripts, des chemins relatifs qui survivent au déplacement d'un projet, et le tout nouveau système de projet de Blender 5.3. Vous remettrez aux normes une scène en désordre, validée par un correcteur automatique.

## Prérequis

- CH00.02 (Relative Paths activé).
- CH00.05 utile (extension BCMA Hello).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer l'arborescence d'un film (préproduction, assets, plans, montage, son, livraisons).
2. Nommer fichiers, objets, collections et matériaux selon des conventions de studio.
3. Renommer vite : F2, Outliner, Batch Rename.
4. Utiliser et réparer les chemins relatifs (Make Paths Relative, Find Missing Files).
5. Créer et ouvrir un projet Blender 5.3 (File > Project), comprendre project.toml.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.06.a | Créer une arborescence et appliquer les conventions de nommage | Exercices 1 et 3 (correcteur) |
| C00.06.b | Gérer les chemins relatifs et les fichiers manquants | Exercice 2 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Arborescence de production | 25 min |
| L2 | Conventions de nommage | 25 min |
| L3 | Chemins relatifs et fichiers externes | 20 min |
| L4 | Le système de projet Blender 5.3 | 15 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch00_06_messy_scene_starter.blend` | Scène en désordre (noms par défaut, chemin absolu) |
| `COMPLETED_EXAMPLES/ch00_06_messy_scene_solution.blend` | Scène conforme |
| `ASSETS/textures/tx_wood_planks.png` | Texture générée utilisée par la scène |
| `SCRIPTS/bcma_create_project.py` | Crée l'arborescence d'un film (+ Blender Project dans Blender) |
| `../../SCRIPTS/bcma_naming_check.py` | Contrôle des conventions (réutilisable dans tout le cursus) |
| `SCRIPTS/validate_ch00_06.py` | Correcteur de l'exercice 3 |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_06_messy_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_06.py" -- --exercise naming
```

## Livrables attendus

1. PROJECTS/mon_premier_film (ou le nom de votre court A) créé et ouvert comme projet Blender.
2. ch00_06_messy_scene_<prenom>_v001.blend validé.
3. README de projet (mini-projet).

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH00.07 — Sauvegardes, récupération, versions](../CH00_07_BACKUP_VERSIONS/README.md)
