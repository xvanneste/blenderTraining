# CH18.08 — Calques, modificateurs, transformations

**Phase :** 18 — Grease Pencil (module B : maîtrise de Grease Pencil)  
**Niveau :** débutant → intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Un dessin de production se modifie sans cesse : il faut pouvoir épaissir un contour, teinter un décor, faire apparaître une lumière par une fenêtre ou animer un tracé, sans jamais redessiner. Ce chapitre présente les outils non destructifs du Grease Pencil : modes de fusion et opacité des calques, masques, transformations de calque, modificateurs (Thickness, Noise, Tint, Build, Line Art…) et effets visuels.

## Prérequis

- CH18.06 (calques)
- CH18.07 (matériaux, remplissages)
- CH01.10 (principe des modificateurs).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser modes de fusion, opacité et Lights des calques.
2. Masquer un calque par un autre (masque invisible mais actif).
3. Ajouter et limiter à un calque les modificateurs Thickness, Noise, Tint, Build.
4. Déplacer un calque par sa transformation sans toucher aux traits.
5. Ajouter un effet visuel (Shadow, Glow…).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.08.a | Dessin multi-calques non destructif | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Calques avancés et masques | 1 h |
| L2 | Modificateurs et effets | 1 h 15 |
| L3 | Transformations de calque | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_08_layers_starter.blend` | Pièce dessinée : 6 calques, sans modificateur ni masque |
| `COMPLETED_EXAMPLES/ch18_08_layers_solution.blend` | Solution non destructive (4 modificateurs, masque, Multiply, transformation, effet) |
| `COMPLETED_EXAMPLES/ch18_08_layers_reference.png` | Rendu image 60 |
| `COMPLETED_EXAMPLES/ch18_08_layers_build_frame20.png` | Rendu image 20 (Build en cours) |
| `SCRIPTS/validate_ch18_08.py` | Correcteur (modificateurs et filtres, masque, fusion, transformation, intégrité) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_08_layers_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_08.py" --python-exit-code 1 -- --exercise layers --render
```

## Livrables attendus

1. Scène validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : une pièce éclairée.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Scène validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.09 — Dessin dans l'espace 3D et organisation](../CH18_09_DRAWING_IN_3D/README.md)
