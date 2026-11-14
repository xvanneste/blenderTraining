# CH01.02 — Navigation 3D

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant absolu  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Naviguer dans l'espace 3D doit devenir aussi naturel que tourner la tête. Ce chapitre installe le repère X-Y-Z de Blender, les trois gestes fondamentaux (orbite, panoramique, zoom), les vues prédéfinies du pavé numérique, la différence entre perspective et orthographique, les commandes de cadrage et d'isolement, la marche à la première personne, et la méthode reine pour placer une caméra : naviguer puis aligner la caméra sur la vue. Terrain de jeu : un petit musée où se cachent une pièce de 2 cm et un objet derrière un mur.

## Prérequis

- CH01.01 (interface).
- Préférences de navigation réglées (CH00.02).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Se repérer dans le repère X, Y, Z (Z vers le haut).
2. Orbiter, faire un panoramique et zoomer à la souris et au clavier.
3. Utiliser les vues prédéfinies et basculer perspective/orthographique.
4. Cadrer (Num ., Home), isoler (vue locale), couper la vue (Alt+B).
5. Naviguer en Walk/Fly.
6. Placer une caméra par alignement sur la vue et la passer en orthographique.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.02.a | Naviguer sans hésitation et placer des caméras | Exercice 3 (correcteur), tests chronométrés |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Repère et gestes fondamentaux | 30 min |
| L2 | Vues prédéfinies, perspective et orthographique | 25 min |
| L3 | Cadrer, isoler, couper | 20 min |
| L4 | Walk et caméras | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_02_museum_starter.blend` | Musée : statue, œuvres, pièce de 2 cm, objet caché, 3 caméras à régler |
| `COMPLETED_EXAMPLES/ch01_02_museum_solution.blend` | Caméras orthographiques face/droite/dessus réglées |
| `SCRIPTS/validate_ch01_02.py` | Correcteur de l'exercice 3 |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_02_museum_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_02.py" --python-exit-code 1 -- --exercise cameras
```

## Livrables attendus

1. ch01_02_museum_<prenom>_v001.blend validé.
2. Temps des tests chronométrés dans PROGRESS.md.
3. Mini-projet : 5 images de visite guidée.

## Critères pour passer au chapitre suivant

- Quiz ≥ 11/14.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.03 — Sélection et manipulation](../CH01_03_SELECTION_TRANSFORM/README.md)
