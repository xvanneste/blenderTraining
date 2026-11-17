# CH09.07 — Composition

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Composer, c'est décider où placer les choses dans le cadre. La règle des tiers divise l'image en neuf par deux lignes verticales et deux lignes horizontales ; on place le sujet sur une ligne ou une intersection, et l'horizon sur une ligne horizontale plutôt qu'au milieu. Ce n'est pas une loi : c'est un point de départ qui évite la composition statique du centre. Ce chapitre recompose un plan avec la caméra seule : les décalages d'objectif (Shift X et Shift Y) déplacent le cadre sans changer la perspective. Le correcteur segmente un rendu plat par couleur et mesure la position du sujet et de l'horizon.

## Prérequis

- CH01 (caméra, rendu), CH09.06 (lecture de l'image).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Placer un sujet sur le tiers gauche ou droit.
2. Placer l'horizon sur un tiers.
3. Utiliser Shift X et Shift Y d'une caméra.
4. Mesurer une composition sur un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.07.a | Composer un plan | Exercice 2 (correcteur) + grille des tiers |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Tiers, horizon, marges | 3 h |
| L2 | Shift et mesure | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_07_composition_starter.blend` | Sujet au centre (50 %) et horizon au milieu (51 %) : composition statique |
| `COMPLETED_EXAMPLES/ch09_07_composition_solution.blend` | Shift X +0,167, Shift Y −0,1 : sujet à 33 % de la largeur, horizon à 33 % de la hauteur, sujet entier (de 29 % à 68 %) |
| `COMPLETED_EXAMPLES/ch09_07_composition_reference.png` | Rendu de départ (gauche) et solution (droite) avec la grille des tiers en blanc et la ligne verticale du tiers gauche en jaune |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sujet à droite, horizon au milieu, sujet coupé, sujet trop petit, tout centré) |
| `SCRIPTS/validate_ch09_07.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_07_composition_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_07.py" -- --exercise composition
```

## Livrables attendus

1. Composition validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.08 — Objectifs et focales](../CH09_08_LENSES/README.md)
