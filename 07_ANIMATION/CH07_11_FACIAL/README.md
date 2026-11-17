# CH07.11 — Animation faciale et lip sync

**Phase :** 7 — Animation 3D  
**Niveau :** expert  
**Durée estimée :** 10 h  
**Version :** Blender 5.3.0

## Introduction

Le lip sync fait parler un visage : à chaque phonème correspond une forme de bouche, un VISÈME, atteinte légèrement avant le son. On n'anime pas chaque lettre mais des formes clés : bouche fermée (M, B, P), ouverte (A), arrondie (O), étirée (E). Ce chapitre fait parler le visage de CH06.09 sur une piste de huit phonèmes (48 images) : mâchoire et sourire suivent les visèmes, sans saut, et un clignement ponctue la phrase. Le correcteur lit la mâchoire, le sourire et le clignement sur les 48 images.

## Prérequis

- CH06.09 (rig facial), CH07.05 (timing), CH07.10 (acting).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Connaître les visèmes de base.
2. Synchroniser une bouche sur une piste de phonèmes.
3. Atteindre la forme une image avant le son.
4. Poser un clignement naturel.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.11.a | Lip sync | Exercice 2 (correcteur) + courbes de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Phonèmes et visèmes | 5 h |
| L2 | Synchroniser et clignoter | 5 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_11_lipsync_starter.blend` | Visage de CH06.09 sans animation, avec le texte PHONEMES (piste de huit phonèmes) |
| `COMPLETED_EXAMPLES/ch07_11_lipsync_solution.blend` | Visèmes M, A, O, E synchronisés (une image avant le son), clignement à l'image 19 |
| `COMPLETED_EXAMPLES/ch07_11_lipsync_reference.png` | Courbes de mâchoire (orange), sourire (vert) et clignement (bleu) ; visèmes cibles en blanc |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (en retard, bouche ouverte sur M, sans variété, bouche qui saute, sans clignement, clignement lent) |
| `SCRIPTS/validate_ch07_11.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_11_lipsync_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_11.py" -- --exercise lipsync
```

## Livrables attendus

1. Lip sync validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.12 — Animation de caméra](../CH07_12_CAMERA/README.md)
