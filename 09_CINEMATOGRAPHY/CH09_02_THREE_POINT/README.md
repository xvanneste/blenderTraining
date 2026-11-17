# CH09.02 — Trois points et variantes

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

L'éclairage à trois points est la base du portrait : une lumière principale (Key) qui modèle le volume, un déboucheur (Fill) qui adoucit l'ombre sans l'effacer, et un contre-jour (Rim) qui détache le sujet du fond. Le rapport de luminance entre le flanc éclairé et le flanc d'ombre (ratio key : fill) règle l'ambiance : proche de 1 pour une image plate, 2 à 5 pour un portrait classique, beaucoup plus pour une image dramatique. Ce chapitre l'applique à une sphère grise et le mesure en ôtant les lampes une à une.

## Prérequis

- CH09.01 (intensité, distance, mesure par rendu).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Placer et régler Key, Fill et Rim.
2. Mesurer un ratio key : fill sur un rendu linéaire.
3. Isoler la contribution d'une lampe par rendu comparatif.
4. Choisir un ratio selon l'intention.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.02.a | Éclairage portrait | Exercice 2 (correcteur) + trois rendus du sujet |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Key, Fill, Rim | 3 h |
| L2 | Ratio et variantes | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_02_three_point_starter.blend` | Sphère, caméra et trois lampes de zone en place : Key 100 W, Fill 100 W, Rim 0 W (éclairage plat sans contre-jour) |
| `COMPLETED_EXAMPLES/ch09_02_three_point_solution.blend` | Key 250 W, Fill 35 W, Rim 300 W : ratio 2,9 ; la Fill apporte 73 % de l'ombre ; la Rim 29 % du bord haut |
| `COMPLETED_EXAMPLES/ch09_02_three_point_reference.png` | Le sujet rendu avec la Key seule, Key + Fill, puis Key + Fill + Rim |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (éclairage plat, sans Fill, sans Rim, Key du mauvais côté) |
| `SCRIPTS/validate_ch09_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_02_three_point_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_02.py" -- --exercise three_point
```

## Livrables attendus

1. Éclairage trois points validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.03 — Naturel et HDRI](../CH09_03_NATURAL_HDRI/README.md)
