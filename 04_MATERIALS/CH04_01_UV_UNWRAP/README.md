# CH04.01 — UV Unwrapping avancé

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Les UV sont le « patron de couture » qui permet de poser une image sur un objet 3D. De mauvaises UV étirent les textures, les font se chevaucher ou gaspillent la résolution. Ce chapitre apprend à couper (seams), déplier (Unwrap), égaliser la densité de texels (Average Islands Scale) et packer, sur un coffre aux UV volontairement mauvaises. Un damier (UV Grid) rend la distorsion visible ; le correcteur la MESURE : étirement, densité, chevauchement, limites, occupation.

## Prérequis

- CH02 (modélisation)
- CH01 (Edit Mode, sélection).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir où couper (seams) sur un objet à arêtes vives et surfaces courbes.
2. Déplier sans distorsion et lire un damier.
3. Égaliser la densité de texels et packer sans chevauchement dans [0, 1].

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.01.a | UV propres | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Seams, îlots, distorsion | 2 h 30 |
| L2 | Densité de texels et packing | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_01_chest_starter.blend` | Coffre aux UV mauvaises + damier |
| `COMPLETED_EXAMPLES/ch04_01_chest_solution.blend` | UV propres (22 îlots) |
| `COMPLETED_EXAMPLES/ch04_01_chest_reference.png` | Deux vues avec damier |
| `COMPLETED_EXAMPLES/ch04_01_chest_uv_layout.png` | Disposition UV |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (chevauchement, densité inégale, hors limites, trop petit) |
| `SCRIPTS/validate_ch04_01.py` | Correcteur (uv) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_01_chest_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_01.py" -- --exercise uv --render
```

## Livrables attendus

1. UV propres validées.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.02 — Packing et UDIM](../CH04_02_PACKING_UDIM/README.md)
