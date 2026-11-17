# CH04.11 — Gestion des couleurs

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Une image n'a de couleur que par son espace colorimétrique. Ce chapitre ferme la phase 4 par les règles qui évitent les erreurs invisibles : couleurs en sRGB, données (rugosité, normales) en Non-Color, un View Transform adapté aux hautes lumières, une exposition raisonnable, un gamma à 1 et une sortie maître en OpenEXR. Le correcteur contrôle tous ces réglages sur une planche d'essai à trois textures et un panneau lumineux.

## Prérequis

- CH04.03 (PBR)
- CH04.07 (Non-Color pour les normales).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer une donnée d'une couleur et choisir l'espace de chaque image.
2. Choisir un View Transform et un Look.
3. Expliquer pourquoi gamma 1 et exposition modérée.
4. Choisir une sortie maître linéaire.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.11.a | Choisir le bon espace colorimétrique | Exercice 2 (correcteur) + comparaison de rendus |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Couleur ou donnée ? | 2 h |
| L2 | View Transform, exposition, sortie maître | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_11_color_starter.blend` | Planche d'essai : images en sRGB, vue Standard, sortie PNG (tout à corriger) |
| `COMPLETED_EXAMPLES/ch04_11_color_solution.blend` | Réglages corrects (AgX, EXR) |
| `COMPLETED_EXAMPLES/ch04_11_color_reference.png` | Deux vues sous AgX |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (albedo en Non-Color, rugosité en sRGB, vue Standard, vue Raw, exposition +4, gamma 2,2, sortie PNG) |
| `SCRIPTS/validate_ch04_11.py` | Correcteur (color) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_11_color_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_11.py" -- --exercise color --render
```

## Livrables attendus

1. Planche d'essai correctement réglée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : Projet P4 — bibliothèque de 25 matériaux (ou [PHASE 5](../../05_GEOMETRY_NODES/README.md) une fois ce projet réalisé)
