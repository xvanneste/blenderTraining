# CH18.11 — Continuité et dialogue

**Phase :** 18 — Grease Pencil (module C : storyboard)  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 30  
**Version :** Blender 5.3.0

## Introduction

Un dialogue se raconte en champ/contrechamp, sans que le spectateur se perde : axe respecté, regards et positions constants à l'écran, entrées et sorties de champ cohérentes. Ce chapitre découpe une scène de dialogue en six plans, dessinés sur une planche puis réalisés avec des caméras 3D montées par des marqueurs de timeline — le correcteur mesure l'axe, les côtés et la variété.

## Prérequis

- CH18.10 (valeurs de plans, 180°).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Découper un dialogue : master, champ/contrechamp, amorces, plans serrés, insert.
2. Respecter axe, regards et positions à l'écran.
3. Gérer entrées et sorties de champ.
4. Monter les plans dans Blender avec marqueurs et Bind Camera to Markers.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.11.a | Découpage de dialogue sans faux raccord | Exercice 3 (correcteurs + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Découper un dialogue | 1 h |
| L2 | Les raccords | 45 min |
| L3 | Le découpage dans Blender | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_11_dialogue_starter.blend` | Plateau : A et B face à face, table, tasse |
| `STARTER_FILES/ch18_11_board_starter.blend` | Planche GP de 6 cases |
| `COMPLETED_EXAMPLES/ch18_11_dialogue_solution.blend` | 6 caméras + 6 marqueurs liés |
| `COMPLETED_EXAMPLES/ch18_11_dialogue_contact.png` | Planche-contact des 6 plans |
| `COMPLETED_EXAMPLES/ch18_11_board_solution.blend` | Découpage dessiné |
| `COMPLETED_EXAMPLES/ch18_11_board_reference.png` | Rendu de la planche |
| `SCRIPTS/validate_ch18_11.py` | Correcteur (marqueurs, 180°, côtés, variété, durées, planche) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_11_dialogue_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_11.py" --python-exit-code 1 -- --exercise dialogue
```

## Livrables attendus

1. Dialogue et planche validés.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : la traversée.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Les deux correcteurs validés.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.12 — Cadrage, composition, découpage technique](../CH18_12_TECHNICAL_BREAKDOWN/README.md)
