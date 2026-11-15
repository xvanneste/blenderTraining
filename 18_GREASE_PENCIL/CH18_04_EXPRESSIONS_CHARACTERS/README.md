# CH18.04 — Expressions et personnages

**Phase :** 18 — Grease Pencil (module A : fondamentaux du dessin)  
**Niveau :** débutant  
**Durée estimée :** 3 h 30  
**Version :** Blender 5.3.0

## Introduction

Un storyboard raconte avec des visages. Ce chapitre apprend à construire une tête (crâne, axe, ligne des yeux à mi-hauteur, mâchoire), à la faire tourner, puis à dessiner les six émotions de base avec trois zones seulement : sourcils, paupières, bouche. Vous concevrez enfin votre premier personnage et sa feuille de modèle (face, trois-quarts, profil alignés), le document qui garantit qu'il reste le même d'un plan à l'autre.

## Prérequis

- CH18.01 (volumes).
- CH18.03 (proportions, silhouette).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une tête et placer correctement yeux, nez, bouche et oreilles.
2. Dessiner la tête sous six angles.
3. Dessiner les six émotions de base et des émotions mixtes.
4. Concevoir un personnage à partir d'une forme de base et d'une silhouette.
5. Réaliser une feuille de modèle alignée (turnaround).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.04.a | Model sheet d'un personnage | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Construire et orienter la tête | 1 h |
| L2 | Les expressions | 1 h |
| L3 | Concevoir un personnage, la feuille de modèle | 1 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_04_expressions_starter.blend` | Feuille : construction de tête, repères de turnaround, 3 calques de travail |
| `COMPLETED_EXAMPLES/ch18_04_expressions_solution.blend` | Feuille complétée (référence schématique) |
| `COMPLETED_EXAMPLES/ch18_04_expressions_reference.png` | Rendu de la référence |
| `SCRIPTS/validate_ch18_04.py` | Correcteur (via bcma_gp_check + gp_spec.json) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_04_expressions_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_04.py" --python-exit-code 1 -- --exercise expressions --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : le casting (3 personnages).

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.05 — Composition et dessin cinématographique](../CH18_05_COMPOSITION/README.md)
