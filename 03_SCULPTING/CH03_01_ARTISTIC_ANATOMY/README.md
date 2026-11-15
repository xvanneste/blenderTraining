# CH03.01 — Anatomie artistique

**Phase :** 3 — Sculpting et personnages  
**Niveau :** débutant → intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Avant de sculpter, il faut des proportions justes. Ce chapitre construit un personnage en 16 masses simples sur une toise : canon de 7,5 têtes, repères anatomiques (menton, épaules, entrejambe, genoux, coudes, bout des doigts), symétrie, puis un enfant de 5 têtes et une pose de contrapposto (bassin et cage inclinés en sens opposés, tête à l'aplomb du pied d'appui). Le correcteur mesure chaque masse.

## Prérequis

- Phase 1 (transformations, Sidebar, vues orthographiques).
- CH18.03 conseillé (proportions dessinées).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Mesurer un personnage en têtes et choisir un canon.
2. Placer les masses principales et les segments aux repères anatomiques.
3. Construire une symétrie propre.
4. Poser un contrapposto équilibré.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.01.a | Construire des proportions | Exercices 2–3 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Proportions et canon | 1 h 30 |
| L2 | Masses et membres | 1 h 30 |
| L3 | Geste et contrapposto | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_01_proportions_starter.blend` | Toise, repères, caméras face/profil |
| `COMPLETED_EXAMPLES/ch03_01_adult_solution.blend` | Adulte 7,5 têtes |
| `COMPLETED_EXAMPLES/ch03_01_child_solution.blend` | Enfant 5 têtes |
| `COMPLETED_EXAMPLES/ch03_01_gesture_solution.blend` | Contrapposto |
| `COMPLETED_EXAMPLES/ch03_01_adult_reference.png` | Face + profil |
| `SCRIPTS/validate_ch03_01.py` | Correcteur (adult, child, gesture) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_01_proportions_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_01.py" --python-exit-code 1 -- --exercise adult --render
```

## Livrables attendus

1. Adulte et enfant validés.
2. Contrapposto validé.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 2 et 3 validés.

➡️ Chapitre suivant : [CH03.02 — Sculpt Mode](../CH03_02_SCULPT_MODE/README.md)
