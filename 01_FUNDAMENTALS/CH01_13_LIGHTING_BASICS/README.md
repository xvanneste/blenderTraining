# CH01.13 — Éclairage élémentaire

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

La lumière ne sert pas seulement à voir : elle sculpte les formes, guide le regard et crée l'émotion. Ce chapitre présente les types de lumières de Blender (Point, Spot, Area, Sun, monde), les réglages qui comptent vraiment — puissance et loi de l'inverse du carré, température de couleur en kelvins, taille de la source qui décide de la douceur des ombres — et le schéma fondamental du cinéma et de la photo : l'éclairage trois points. Exercice : faire sortir un buste de l'obscurité avec une key, une fill et un contre-jour.

## Prérequis

- CH01.11 (matériaux).
- CH01.12 (caméra).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir le type de lumière adapté.
2. Régler puissance, température, taille de source et comprendre l'inverse du carré.
3. Construire un éclairage trois points et régler le ratio key/fill.
4. Diagnostiquer une image trop sombre, trop claire ou aux ombres dures.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.13.a | Éclairer une scène simple avec intention | Exercice 3 (correcteur + exposition) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Types de lumières et réglages | 30 min |
| L2 | L'éclairage trois points | 35 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_13_bust_starter.blend` | Buste dans le noir, sans lumière |
| `COMPLETED_EXAMPLES/ch01_13_bust_solution.blend` | Éclairage trois points |
| `COMPLETED_EXAMPLES/ch01_13_bust_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch01_13.py` | Correcteur (placement, ratio, exposition mesurée) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_13_bust_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_13.py" --python-exit-code 1 -- --exercise threepoint --render
```

## Livrables attendus

1. ch01_13_bust_<prenom>_v001.blend validé.
2. Mini-projet : trois portraits lumineux.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.14 — Premiers rendus](../CH01_14_FIRST_RENDERS/README.md)
