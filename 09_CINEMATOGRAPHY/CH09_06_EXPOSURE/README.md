# CH09.06 — Exposition et contraste

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rendu produit des valeurs de lumière (linéaires, qui peuvent dépasser 1) ; la gestion des couleurs les transforme en image affichable entre 0 et 1. Trois réglages décident de ce que vous voyez : la vue (View Transform : Standard, AgX, Filmic, Khronos PBR Neutral…), l'exposition (Exposure, en diaphragmes) et le look (contraste, saturation). Une vue qui écrête (Standard) brûle les hautes lumières ; une vue « filmique » les comprime en gardant du détail. Ce chapitre apprend à lire une image par trois nombres : le pourcentage de pixels brûlés, la luminance moyenne et l'écart p95 − p5 (contraste).

## Prérequis

- CH09.01 (mesure par rendu), CH01 (rendu de base).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir une vue adaptée à une scène à forte dynamique.
2. Régler l'exposition au diaphragme près.
3. Lire un histogramme et des pourcentages de pixels.
4. Expliquer l'effet d'un Look.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.06.a | Exposer juste | Exercice 2 (correcteur) + histogrammes |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Vue et exposition | 3 h |
| L2 | Contraste et lecture | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_06_exposure_starter.blend` | Vue Standard, Exposure 0 : la sphère émissive brûle (4,4 % de pixels brûlés) |
| `COMPLETED_EXAMPLES/ch09_06_exposure_solution.blend` | Vue AgX, Look None, Exposure +0,5 : 0 % brûlés, moyenne 0,42, contraste 0,64 |
| `COMPLETED_EXAMPLES/ch09_06_exposure_reference.png` | Rendu Standard (à gauche) et solution AgX +0,5 (à droite) avec leurs histogrammes de luminance |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (vue qui brûle, trop sombre, trop clair, look trop sombre) |
| `SCRIPTS/validate_ch09_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_06_exposure_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_06.py" -- --exercise exposure
```

## Livrables attendus

1. Exposition validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.07 — Composition](../CH09_07_COMPOSITION/README.md)
