# CH09.04 — Dramatique et stylisé

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un éclairage n'est pas seulement correct : il exprime une intention. Le low-key (image sombre, fort contraste, grandes ombres) dit le drame, le mystère, la menace ; le high-key (image claire, ombres ouvertes, contraste doux) dit la douceur, la légèreté. La couleur ajoute le style : des teintes complémentaires (orange et bleu-vert) séparent le sujet du fond et donnent un « look de cinéma ». Ce chapitre éclaire la même sphère de deux façons dans un fichier à deux scènes (LOWKEY et HIGHKEY) et mesure les deux ambiances : ratio de contraste, luminance moyenne, contre-jour et écart de teinte.

## Prérequis

- CH09.02 (trois points, ratio, contributions par rendu).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Traduire une intention en ratio et en luminance moyenne.
2. Régler un éclairage low-key et un éclairage high-key.
3. Choisir deux teintes complémentaires.
4. Travailler avec deux scènes dans un même fichier.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.04.a | Éclairage d'intention | Exercice 2 (correcteur) + deux ambiances |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Low-key et high-key | 3 h |
| L2 | Couleur et style | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_04_dramatic_starter.blend` | Deux scènes (LOWKEY, HIGHKEY) avec les mêmes réglages neutres : Key 100 W, Fill 100 W, Rim 0 W, lampes blanches |
| `COMPLETED_EXAMPLES/ch09_04_dramatic_solution.blend` | LOWKEY : Key 70 W orange, Fill 0,5 W, Rim 250 W bleu-vert (ratio 8,8 ; moyenne 0,057). HIGHKEY : Key 250 W, Fill 150 W, Rim 100 W (ratio 0,9 ; moyenne 0,60) |
| `COMPLETED_EXAMPLES/ch09_04_dramatic_reference.png` | Les deux ambiances côte à côte : LOWKEY à gauche, HIGHKEY à droite |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (low-key pas assez sombre, pas assez contrasté, sans couleur ; high-key trop contrasté, trop sombre) |
| `SCRIPTS/validate_ch09_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_04_dramatic_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_04.py" -- --exercise dramatic
```

## Livrables attendus

1. Deux ambiances validées.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.05 — Volumétrie](../CH09_05_VOLUMETRICS/README.md)
