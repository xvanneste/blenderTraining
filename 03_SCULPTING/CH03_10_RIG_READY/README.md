# CH03.10 — Préparation au rigging

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Avant d'être riggé, un personnage doit être « rig-ready » : bien nommé, à l'échelle réelle, transformations appliquées, origine au sol entre les pieds, face vers −Y, symétrique, en pose A ou T avec les jambes écartées, maillage propre. Ce chapitre part d'un mannequin volontairement sale (nom « Mannequin.001 », échelle 100 non appliquée, origine au centre, penché de 4°) et le livre propre. Le correcteur vérifie chaque point par mesure.

## Prérequis

- CH03.01 à CH03.09.
- CH01 (transformations, origine, collections).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Nommer, ranger et appliquer les transformations d'un personnage.
2. Fixer l'origine, l'échelle et l'orientation.
3. Choisir et contrôler une pose de rig (A ou T) et la symétrie.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.10.a | Livrer un personnage rig-ready | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Conventions : nom, échelle, origine, orientation | 2 h |
| L2 | Pose, symétrie, propreté | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_10_char_starter.blend` | Mannequin sale à nettoyer |
| `COMPLETED_EXAMPLES/ch03_10_char_solution.blend` | CHR_Hero_Body prêt pour le rig (pose A) |
| `COMPLETED_EXAMPLES/ch03_10_char_reference.png` | Face, profil |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (échelle, nom, origine, bras le long du corps, asymétrie, flottant) + une pose en T VALIDE |
| `SCRIPTS/validate_ch03_10.py` | Correcteur (rigready) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_10_char_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_10.py" -- --exercise rigready --render
```

## Livrables attendus

1. Personnage rig-ready validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Phase 4 — UV, matériaux, textures](../../04_MATERIALS/README.md)
