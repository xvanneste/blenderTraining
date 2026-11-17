# CH13.01 — Python pour artistes

**Phase :** 13 — Python et automatisation  
**Niveau :** intermédiaire  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Python est le langage de Blender : tout ce que vous faites à la souris peut s'écrire en quelques lignes. Ce chapitre pose les bases dont un artiste a besoin (variables, listes, boucles, fonctions) puis crée une première scène par script, une grille de cubes. Vous écrivez cinq petites fonctions dans un texte `exercise.py` ; le correcteur EXÉCUTE votre texte et teste chaque fonction avec des cas précis, comme un test automatique.

## Prérequis

- CH01 (interface, espace de travail Scripting). Aucune notion de programmation requise.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser variables, listes, boucles et conditions.
2. Écrire et tester une fonction (arguments, valeur renvoyée).
3. Créer des objets par script avec `bpy.ops` et les nommer.
4. Lire un message d'erreur (traceback) et corriger.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C13.01.a | Écrire un script simple | Exercice 2 (correcteur) : 56/56 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les bases du langage | 4 h |
| L2 | Une première scène par script | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch13_01_python_starter.blend` | Texte exercise.py avec cinq fonctions « à compléter » : 6/56 |
| `COMPLETED_EXAMPLES/ch13_01_python_solution.blend` | Les cinq fonctions écrites : 56/56 |
| `COMPLETED_EXAMPLES/ch13_01_python_reference.png` | Grille de 5 × 3 cubes créée par la solution (vue de dessus) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (clamp aux bornes inversées, average qui plante sur [], grille transposée, noms sans zéros, cubes à l'origine) |
| `SCRIPTS/validate_ch13_01.py` | Correcteur (exécute le texte et teste chaque fonction) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch13_01_python_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch13_01.py" -- --exercise python
```

## Livrables attendus

1. Le fichier avec les cinq fonctions validées (56/56).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH13.02 — L'API bpy](../CH13_02_BPY_API/README.md)
