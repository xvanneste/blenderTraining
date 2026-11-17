# CH12.03 — Son

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le son fait au moins la moitié de l'impact d'un film. Trois familles se placent sur l'image : l'ambiance (le décor sonore continu), les bruitages (les sons ponctuels liés à une action visible : un coup, un pas) et la voix (la réplique, calée sur la bouche). La règle : un son synchrone doit commencer sur l'image de l'action, à une ou deux images près. Ce chapitre place trois sons générés sur une séquence de quatre secondes ; le correcteur lit les positions, mixe réellement l'ensemble et mesure l'énergie par fenêtres d'images pour vérifier que le coup et la réplique tombent au bon moment.

## Prérequis

- CH12.01 (VSE), CH12.02 (montage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Placer un son sur un marqueur de timeline.
2. Distinguer ambiance, bruitage et voix.
3. Contrôler la synchronisation par un mixage mesuré.
4. Éviter l'écrêtage.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.03.a | Habiller une séquence | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Ambiance, bruitage, voix | 3 h |
| L2 | Synchroniser et mesurer | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_03_sound_starter.blend` | HIT à l'image 30 (19 trop tôt), VOICE à 20 (41 trop tôt), AMB 11–59 : le coup et la réplique ne tombent pas sur les marqueurs ; 19/61 |
| `COMPLETED_EXAMPLES/ch12_03_sound_solution.blend` | AMB 1–100, HIT à 49, VOICE à 61 : coup 12 × l'ambiance, réplique 10 ×, crête 0,55 ; 61/61 |
| `COMPLETED_EXAMPLES/ch12_03_sound_reference.png` | Enveloppe du mixage : départ (haut) et solution (bas) ; barre jaune = IMPACT (49), barre rose = LINE (61) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (coup en retard, réplique trop tôt, ambiance trop courte, écrêtage, coup muet) |
| `SCRIPTS/validate_ch12_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_03_sound_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_03.py" -- --exercise sound
```

## Livrables attendus

1. Liste de synchronisation (son, image de départ, marqueur).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH12.04 — Mixage](../CH12_04_MIX/README.md)
