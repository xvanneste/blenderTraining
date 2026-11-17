# CH18.12 — Cadrage, composition, découpage technique

**Phase :** 18 — Grease Pencil (module C : storyboard)  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Un storyboard professionnel est un document technique : cases au format de l'image, plans numérotés, valeur, mouvement, durée, flèches de caméra et de personnage. Ce chapitre construit une planche normée dans Blender — dessin Grease Pencil, flèches, annotations en objets texte — vérifiée par un correcteur qui contrôle la norme de chaque note.

## Prérequis

- CH18.10 (valeurs de plans)
- CH18.11 (continuité).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Rédiger un découpage technique numéroté (SQ/SH).
2. Composer et dessiner une planche de 6 cases au format de l'image.
3. Distinguer flèches de caméra et flèches de personnage.
4. Annoter chaque case selon une norme et paginer la planche.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.12.a | Planche de storyboard normée | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le découpage technique | 45 min |
| L2 | La planche dessinée | 1 h 15 |
| L3 | Annoter dans Blender | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_12_board_starter.blend` | Gabarit : 6 cases + bandeaux de notes |
| `COMPLETED_EXAMPLES/ch18_12_board_solution.blend` | Planche normée « La tasse » |
| `COMPLETED_EXAMPLES/ch18_12_board_reference.png` | Rendu de la planche |
| `SCRIPTS/validate_ch18_12.py` | Correcteur (dessin par case, flèches, notes normées, en-tête) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_12_board_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_12.py" -- --exercise board --render
```

## Livrables attendus

1. Planche validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : deux pages.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Planche validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.13 — Storyboards d'action, d'émotion, complexes](../CH18_13_COMPLEX_BOARDS/README.md)
