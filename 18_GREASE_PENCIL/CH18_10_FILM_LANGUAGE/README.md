# CH18.10 — Langage cinématographique

**Phase :** 18 — Grease Pencil (module C : storyboard)  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Avant de storyboarder, il faut parler la langue du cinéma : valeurs de plans, angles, axe et règle des 180°, focales. Ce chapitre fait les deux gestes du métier : dessiner les 8 valeurs sur une planche Grease Pencil, et les cadrer avec de vraies caméras 3D sur un personnage — chaque cadrage étant mesuré par le correcteur.

## Prérequis

- CH18.05 (composition)
- CH01.12 (caméras).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Nommer et reconnaître les 8 valeurs de plans.
2. Cadrer chaque valeur avec une caméra 3D.
3. Utiliser plongée et contre-plongée à dessein.
4. Respecter la règle des 180° en champ/contrechamp.
5. Choisir une focale selon l'effet recherché.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.10.a | Nommer et dessiner 8 valeurs de plans | Exercice 3 (correcteurs + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les valeurs de plans | 1 h 15 |
| L2 | Angles et focales | 45 min |
| L3 | L'axe et les 180° | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_10_shots_starter.blend` | Plateau : 2 mannequins, table, tasse |
| `STARTER_FILES/ch18_10_board_starter.blend` | Planche GP de 8 cadres |
| `COMPLETED_EXAMPLES/ch18_10_shots_solution.blend` | 12 caméras de référence |
| `COMPLETED_EXAMPLES/ch18_10_shots_contact.png` | Planche-contact des 12 caméras |
| `COMPLETED_EXAMPLES/ch18_10_board_solution.blend` | Planche des 8 valeurs dessinée |
| `COMPLETED_EXAMPLES/ch18_10_board_reference.png` | Rendu de la planche |
| `SCRIPTS/validate_ch18_10.py` | Correcteur (valeurs mesurées, angles, 180°, planche) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_10_shots_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_10.py" --python-exit-code 1 -- --exercise shots
```

## Livrables attendus

1. Caméras et planche validées.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : un dialogue en 8 plans.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Les deux correcteurs validés.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.11 — Continuité et dialogue](../CH18_11_CONTINUITY/README.md)
