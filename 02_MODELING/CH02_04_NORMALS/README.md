# CH02.04 — Normales

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 15  
**Version :** Blender 5.3.0

## Introduction

Les normales décident de la façon dont la lumière glisse sur une surface. Une face retournée, un lissage mal réglé ou des normales moyennées sur un chanfrein suffisent à ruiner un rendu. Ce chapitre apprend à voir et corriger l'orientation, à lisser en gardant des arêtes vives (Shade Auto Smooth, le remplaçant de l'Auto Smooth depuis Blender 4.1) et à obtenir des surfaces hard surface parfaitement propres avec Weighted Normal — avec des valeurs mesurées.

## Prérequis

- CH02.01 à CH02.03.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Diagnostiquer l'orientation avec Face Orientation et la corriger.
2. Choisir entre Shade Flat, Smooth et Auto Smooth.
3. Marquer des arêtes vives.
4. Utiliser Weighted Normal pour des surfaces planes sur un objet chanfreiné.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.04.a | Corriger un ombrage | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Orientation des normales | 45 min |
| L2 | Lisse, plat, Smooth by Angle | 45 min |
| L3 | Weighted Normal et hard surface | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_04_normals_starter.blend` | 3 objets mal ombrés (faces retournées, lissage intégral, chanfrein taché) |
| `COMPLETED_EXAMPLES/ch02_04_normals_solution.blend` | Objets corrigés |
| `COMPLETED_EXAMPLES/ch02_04_normals_starter_view.png` | Rendu avant correction |
| `COMPLETED_EXAMPLES/ch02_04_normals_reference.png` | Rendu après correction |
| `SCRIPTS/validate_ch02_04.py` | Correcteur (orientation, normales de coin du maillage évalué) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_04_normals_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_04.py" -- --exercise normals --render
```

## Livrables attendus

1. Objets validés.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : trois props propres.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Objets validés.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.05 — Hard Surface](../CH02_05_HARD_SURFACE/README.md)
