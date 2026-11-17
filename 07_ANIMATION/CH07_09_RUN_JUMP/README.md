# CH07.09 — Course, saut, interactions

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 10 h  
**Version :** Blender 5.3.0

## Introduction

La course et le saut sont des mouvements balistiques : pendant le vol, le corps n'a plus d'appui et obéit à la gravité. Ce chapitre présente la course (un cycle comme la marche, avec une phase aérienne), puis fabrique un saut crédible en 40 images : ANTICIPATION (flexion), IMPULSION, VOL parabolique, RÉCEPTION amortie, retour debout. Les interactions (pousser, tirer) sont présentées en théorie. Le correcteur mesure les hanches et les chevilles sur les 40 images : flexion, durée du vol, hauteur, gravité, amortissement, pieds plantés.

## Prérequis

- CH07.05 (timing et gravité), CH07.07 (posing), CH07.08 (marche).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer course et marche.
2. Construire un saut en quatre phases.
3. Faire obéir le vol à la gravité (parabole).
4. Amortir une réception.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.09.a | Saut crédible | Exercice 2 (correcteur) + courbes de hauteur |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Course et phase aérienne | 5 h |
| L2 | Le saut | 5 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_09_jump_starter.blend` | Mannequin FK debout, sans animation |
| `COMPLETED_EXAMPLES/ch07_09_jump_solution.blend` | Saut sur place de 40 images : flexion, impulsion, vol parabolique, réception amortie |
| `COMPLETED_EXAMPLES/ch07_09_jump_reference.png` | Hauteur des hanches (orange) et de la cheville gauche (bleu) sur 40 images |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans anticipation, sans réception, vol flottant, saut trop bas, pieds qui glissent, sans retour debout) |
| `SCRIPTS/validate_ch07_09.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_09_jump_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_09.py" -- --exercise jump
```

## Livrables attendus

1. Saut validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.10 — Acting](../CH07_10_ACTING/README.md)
