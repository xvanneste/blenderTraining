# CH18.07 — Brushes, traits, remplissages, matériaux

**Phase :** 18 — Grease Pencil (module B : maîtrise de Grease Pencil)  
**Niveau :** débutant  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

Un dessin propre tient à trois choses : le bon pinceau, la bonne couleur, le bon ordre de calques. Ce chapitre présente les pinceaux livrés avec Blender 5.3 (assets Essentials), les matériaux Grease Pencil et la palette par matériaux, l'outil Fill et ses réglages, la gomme, et la méthode d'encrage des studios 2D. Il explique aussi un changement de Blender 5.3 : le remplissage est désormais choisi trait par trait.

## Prérequis

- CH18.06 (objets, calques, modes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir et régler un pinceau (Size, Strength, pression, Stroke Mode).
2. Créer une palette de matériaux GP nommés.
3. Remplir un dessin au trait avec l'outil Fill sans fuite ni liseré.
4. Gommer selon le bon mode (Dissolve, Point, Stroke).
5. Organiser un encrage SKETCH → LINE → COLOR.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.07.a | Dessin propre trait + aplat | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Pinceaux et qualité du trait | 1 h |
| L2 | Matériaux et remplissages | 1 h 15 |
| L3 | Gommer et encrer proprement | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_07_brushes_starter.blend` | Feuille : 3 bandes de traits, dessin au trait à remplir, 2 calques de travail |
| `COMPLETED_EXAMPLES/ch18_07_brushes_solution.blend` | Feuille complétée (8 matériaux, 9 aplats) |
| `COMPLETED_EXAMPLES/ch18_07_brushes_reference.png` | Rendu de la référence |
| `SCRIPTS/validate_ch18_07.py` | Correcteur (via bcma_gp_check + gp_spec.json : traits, aplats, matériaux) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_07_brushes_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_07.py" -- --exercise brushes --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : personnage encré et mis en couleur.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.08 — Calques, modificateurs, transformations](../CH18_08_LAYERS_MODIFIERS/README.md)
