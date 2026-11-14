# CH00.03 — Performances CPU, GPU, mémoire

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant  
**Durée estimée :** 2 h (théorie 40 min · pratique 60 min · évaluation 20 min)  
**Version :** Blender 5.3.0

## Introduction

Une scène peut être magnifique et pourtant impossible à produire : trop lente à manipuler, trop lourde pour la mémoire de la carte graphique, trop longue à rendre. Ce chapitre vous apprend à penser en budget : comprendre quelle partie de l'ordinateur travaille pour chaque tâche, lire les statistiques, estimer le coût réel d'une scène au rendu, et appliquer les premiers leviers d'optimisation. Vous optimiserez une scène volontairement trop lourde — 200 galets qui représentent 16 millions de faces au rendu — sans changer son image.

## Prérequis

- CH00.01 et CH00.02 validés.
- Statistiques de la barre d'état activées (CH00.02).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer le rôle du CPU, du GPU, de la RAM et de la VRAM dans chaque tâche de Blender.
2. Choisir et changer le backend graphique (Vulkan / OpenGL) en cas de problème.
3. Lire les statistiques et estimer le coût d'une scène au rendu.
4. Partager les données entre objets (duplication liée, Link Object Data).
5. Régler la subdivision et le panneau Simplify pour respecter un budget.
6. Mesurer et documenter un gain d'optimisation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.03.a | Identifier la ressource limitante et choisir le bon périphérique | Leçons 1–2, quiz |
| C00.03.b | Mesurer et réduire le coût d'une scène | Exercice 3 (correcteur), mini-projet |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Comment Blender utilise CPU, GPU, RAM et VRAM | 20 min |
| L2 | Backend graphique : Vulkan et OpenGL | 10 min |
| L3 | Lire les statistiques et estimer le coût au rendu | 25 min |
| L4 | Les leviers d'optimisation | 35 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch00_03_heavy_scene_starter.blend` | 200 galets, données dupliquées, Subdivision 2/5 (~16,4 M faces au rendu) |
| `COMPLETED_EXAMPLES/ch00_03_heavy_scene_solution.blend` | Version optimisée (données partagées, Subdivision 1/2, Simplify) — 0,26 M faces |
| `SCRIPTS/bcma_scene_cost.py` | Estimation du coût d'une scène au rendu (réutilisable) |
| `SCRIPTS/validate_ch00_03.py` | Correcteur de l'exercice 3 |
| `SCRIPTS/build_ch00_03_files.py` | Régénère les .blend |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_03_heavy_scene_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch00_03.py" --python-exit-code 1 -- --exercise optimize --render
```

## Livrables attendus

1. ch00_03_heavy_scene_<prenom>_v001.blend validé par le correcteur.
2. Rapport d'optimisation (mini-projet).
3. Fiche de poste section 6 (goulots d'étranglement).

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH00.04 — Périphériques d'entrée](../CH00_04_INPUT_DEVICES/README.md)
