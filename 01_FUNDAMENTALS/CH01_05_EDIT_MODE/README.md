# CH01.05 — Modes Object et Edit

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 2 h  
**Version :** Blender 5.3.0

## Introduction

Jusqu'ici vous avez déplacé des objets entiers. En Edit Mode, vous prenez le ciseau : vous modifiez la géométrie elle-même, sommet par sommet, arête par arête, face par face. Ce chapitre présente les modes de Blender, la structure d'un maillage, les sélections spécifiques (boucles, anneaux, parties connectées, X-Ray), les premières opérations d'édition (déplacer, extruder, écraser sur un axe, fusionner) et l'édition proportionnelle. Exercice : transformer un cube en maison à toit à deux pans et sculpter une colline dans une grille.

## Prérequis

- CH01.03 (G, R, S, axes, saisie numérique).
- CH01.04 (objet vs données).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Basculer entre les modes et connaître leur rôle.
2. Identifier sommets, arêtes et faces et changer de mode de sélection.
3. Sélectionner boucles, anneaux, parties connectées, à travers l'objet (X-Ray).
4. Transformer et extruder des composants, aligner avec une échelle nulle.
5. Utiliser l'édition proportionnelle et régler son rayon.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.05.a | Éditer un maillage simple | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Modes et composants | 25 min |
| L2 | Sélections d'Edit Mode | 25 min |
| L3 | Éditer : transformer, extruder, fusionner | 30 min |
| L4 | Édition proportionnelle | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_05_house_starter.blend` | Cube-maison et grille d'entraînement |
| `COMPLETED_EXAMPLES/ch01_05_house_solution.blend` | Toit à deux pans et colline |
| `SCRIPTS/validate_ch01_05.py` | Correcteur (géométrie) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_05_house_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_05.py" --python-exit-code 1 -- --exercise house
```

## Livrables attendus

1. ch01_05_house_<prenom>_v001.blend validé.
2. Mini-projet : le hameau.

## Critères pour passer au chapitre suivant

- Quiz ≥ 10/12.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.06 — Transformations avancées](../CH01_06_TRANSFORMS_ADVANCED/README.md)
