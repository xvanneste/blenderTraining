# CH18.16 — Animation 2D : principes et image par image

**Phase :** 18 — Grease Pencil (module E : animation 2D)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h 30  
**Version :** Blender 5.3.0

## Introduction

Premier pas de l'animation 2D dans Grease Pencil : la balle rebondissante, exercice fondateur de tous les animateurs. Poses clés et extrêmes d'abord, intervalles « en deux » ensuite, avec onion skinning, types de clés, ralenti aux sommets, écrasement et étirement à volume constant. Le correcteur mesure chaque dessin : contacts, amortissement des rebonds, espacement, squash & stretch.

## Prérequis

- CH18.06 à CH18.08 (outils GP).
- CH07.01 conseillé (principes d'animation).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Animer image par image en deux.
2. Construire une animation pose à pose (clés, extrêmes, intervalles).
3. Maîtriser timing et espacement (ralentis).
4. Appliquer squash & stretch en conservant le volume.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.16.a | Balle rebondissante 2D | Exercices 1–2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Image par image et poses clés | 1 h 30 |
| L2 | Timing, espacement, squash & stretch | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_16_bounce_starter.blend` | Feuille, sol, départ, calque USER_Ball |
| `COMPLETED_EXAMPLES/ch18_16_keys_solution.blend` | Étape 1 : 8 poses clés |
| `COMPLETED_EXAMPLES/ch18_16_bounce_solution.blend` | Étape 2 : 32 dessins en deux |
| `COMPLETED_EXAMPLES/ch18_16_bounce_reference.png` | Superposition de toutes les images |
| `SCRIPTS/validate_ch18_16.py` | Correcteur (keys, bounce) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_16_bounce_<prenom>_v002.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_16.py" -- --exercise bounce --render
```

## Livrables attendus

1. Poses clés validées.
2. Balle complète validée.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 1 et 2 validés.

➡️ Chapitre suivant : [CH18.17 — Timing, spacing, cycles](../CH18_17_TIMING_CYCLES/README.md)
