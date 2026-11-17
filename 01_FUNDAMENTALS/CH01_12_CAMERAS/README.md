# CH01.12 — Caméras

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

En cinéma 3D, rien n'existe hors du cadre : la caméra est le regard du spectateur. Ce chapitre vous apprend à placer et activer une caméra, à choisir une focale (grand-angle, normale, téléobjectif) en comprenant ce qu'elle change, à composer avec la règle des tiers et la hauteur de caméra, et à guider l'œil avec la profondeur de champ. Exercice : le portrait d'un gardien de phare, tête sur les tiers, arrière-plan flou mais lisible.

## Prérequis

- CH01.02 (navigation, Ctrl+Alt+Num 0).
- CH01.09 (Properties).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter, activer et placer une caméra (alignement sur la vue, Lock Camera to View).
2. Choisir une focale selon l'intention.
3. Composer avec les guides (tiers) et la hauteur de caméra.
4. Régler la profondeur de champ (Focus on Object, F-Stop).
5. Choisir une résolution et un format d'image.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.12.a | Cadrer un plan avec intention | Exercice 3 (correcteur), mini-projet |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Placer et activer une caméra | 20 min |
| L2 | Focale et capteur | 25 min |
| L3 | Composition, hauteur, format | 25 min |
| L4 | Profondeur de champ | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_12_portrait_starter.blend` | Gardien, phare, caméra mal placée |
| `COMPLETED_EXAMPLES/ch01_12_portrait_solution.blend` | Portrait cadré aux tiers avec profondeur de champ |
| `COMPLETED_EXAMPLES/ch01_12_portrait_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch01_12.py` | Correcteur (projection, focale, DOF) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_12_portrait_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_12.py" -- --exercise portrait --render
```

## Livrables attendus

1. ch01_12_portrait_<prenom>_v001.blend validé.
2. Mini-projet : trois plans, trois émotions.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.13 — Éclairage élémentaire](../CH01_13_LIGHTING_BASICS/README.md)
