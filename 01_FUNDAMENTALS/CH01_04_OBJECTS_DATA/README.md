# CH01.04 — Objets et meshes

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Dans Blender, un objet n'est pas sa forme : c'est un conteneur placé dans la scène qui pointe vers des données (un maillage, une caméra, une lumière…). Cette idée explique la moitié des comportements « étranges » des débutants et ouvre des techniques de production essentielles : plusieurs objets qui partagent une même forme, des données qu'on rend uniques, des objets qu'on joint ou qu'on sépare. Exercice : une ferme avec une clôture en duplication liée, un piquet cassé, une table à assembler et des rochers à séparer.

## Prérequis

- CH01.03 (sélection, transformations).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer objet, données (Object Data) et datablocks.
2. Lire le nombre d'utilisateurs, utiliser le Fake User, purger les orphelins.
3. Choisir entre Duplicate (Shift+D) et Duplicate Linked (Alt+D).
4. Rendre des données uniques (Make Single User) au bon moment.
5. Joindre (Ctrl+J) et séparer (P) des objets.
6. Ajouter des primitives et régler leurs paramètres.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.04.a | Distinguer objet/donnée et gérer partage, jointure, séparation | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Objet et données | 25 min |
| L2 | Dupliquer : copie ou lien | 30 min |
| L3 | Joindre, séparer, ajouter | 25 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_04_farm_starter.blend` | Piquet, table en 5 morceaux, rochers en un objet |
| `COMPLETED_EXAMPLES/ch01_04_farm_solution.blend` | Clôture liée, piquet cassé unique, table jointe, rochers séparés |
| `SCRIPTS/validate_ch01_04.py` | Correcteur (17 points) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_04_farm_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_04.py" --python-exit-code 1 -- --exercise farm
```

## Livrables attendus

1. ch01_04_farm_<prenom>_v001.blend validé.
2. Mini-projet : le potager.

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.05 — Modes Object et Edit](../CH01_05_EDIT_MODE/README.md)
