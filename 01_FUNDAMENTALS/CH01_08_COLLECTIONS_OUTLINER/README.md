# CH01.08 — Collections et Outliner

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Une scène de film contient des centaines d'objets : sans organisation, impossible de travailler. Ce chapitre installe les collections (les dossiers de la scène), les cinq interrupteurs de visibilité qu'il ne faut pas confondre (exclure, sélectionnable, œil, écran, appareil photo), l'Outliner comme centre de contrôle, et le parentage, qui fait suivre un objet par un autre. Exercice : ranger un salon livré en vrac, exclure du rendu les repères de travail et accrocher un abat-jour à son pied de lampe.

## Prérequis

- CH01.04 (objets).
- CH01.07 (origines).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer, imbriquer et utiliser des collections (M, Shift+M, Outliner).
2. Distinguer et utiliser les cinq contrôles de visibilité.
3. Naviguer dans l'Outliner (modes d'affichage, recherche, renommage).
4. Parenter et déparenter (Ctrl+P, Alt+P, Keep Transform).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.08.a | Organiser une scène (collections, visibilités, parentage) | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Collections | 25 min |
| L2 | Les cinq interrupteurs de visibilité | 25 min |
| L3 | Outliner et parentage | 25 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_08_living_room_starter.blend` | Salon de 17 objets en vrac |
| `COMPLETED_EXAMPLES/ch01_08_living_room_solution.blend` | Salon rangé, HELPERS hors rendu, lampe parentée |
| `SCRIPTS/validate_ch01_08.py` | Correcteur (23 points + rendu) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_08_living_room_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_08.py" -- --exercise organize --render
```

## Livrables attendus

1. ch01_08_living_room_<prenom>_v001.blend validé.
2. Mini-projet : un de vos fichiers remis au propre.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.09 — Éditeur de propriétés](../CH01_09_PROPERTIES_EDITOR/README.md)
