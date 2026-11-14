# CH01.10 — Modificateurs essentiels

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Les modificateurs sont le cœur du travail non destructif : ils répètent, symétrisent, épaississent, biseautent ou lissent un objet sans toucher à son maillage d'origine, et restent réglables à tout moment. Ce chapitre présente la pile de modificateurs et son ordre d'évaluation, six modificateurs essentiels (Array, Mirror, Solidify, Bevel, Subdivision Surface, Boolean en aperçu) et la règle d'or : n'appliquer que lorsque c'est indispensable. Exercice : un petit pont construit à partir d'une planche, d'une demi-rambarde, d'un pilier et d'un seau.

## Prérequis

- CH01.06 (échelle appliquée).
- CH01.07 (origines).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter, régler, réordonner, désactiver et appliquer des modificateurs.
2. Utiliser Array, Mirror, Solidify, Bevel et Subdivision Surface.
3. Choisir le bon ordre dans la pile.
4. Savoir quand appliquer (et quand ne pas appliquer) un modificateur.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.10.a | Construire une pile non destructive | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le principe de la pile | 20 min |
| L2 | Les six essentiels | 40 min |
| L3 | Ordre et application | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_10_bridge_starter.blend` | Planche, demi-rambarde, pilier, seau sans épaisseur |
| `COMPLETED_EXAMPLES/ch01_10_bridge_solution.blend` | Piles de modificateurs complètes |
| `COMPLETED_EXAMPLES/ch01_10_bridge_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch01_10.py` | Correcteur (géométrie évaluée, ordre de pile) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_10_bridge_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_10.py" --python-exit-code 1 -- --exercise bridge --render
```

## Livrables attendus

1. ch01_10_bridge_<prenom>_v001.blend validé.
2. Mini-projet : la passerelle.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.11 — Matériaux simples](../CH01_11_MATERIALS_BASICS/README.md)
