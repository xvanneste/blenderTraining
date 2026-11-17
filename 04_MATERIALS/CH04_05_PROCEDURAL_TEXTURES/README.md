# CH04.05 — Textures procédurales

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Une texture procédurale est calculée par un algorithme : pas d'image, donc pas de résolution, pas d'UV, pas de répétition visible. Ce chapitre construit un mur de briques avec la seule Brick Texture : variation de briques, joint clair, rangées décalées, et joints creusés grâce à un Bump piloté par le même motif. Le correcteur lit les réglages du nœud et vérifie que le relief est bien alimenté par la texture.

## Prérequis

- CH04.04.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer l'intérêt et les limites d'une texture procédurale.
2. Régler une Brick Texture (Scale, Mortar Size, Offset, couleurs).
3. Dériver un relief (Bump) du même motif que la couleur.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.05.a | Créer un matériau procédural | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Procédural ou image ? | 2 h |
| L2 | Brique, bump et variation | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_05_procedural_starter.blend` | Mur PROP_Wall, Principled par défaut |
| `COMPLETED_EXAMPLES/ch04_05_procedural_solution.blend` | Mur de briques procédural |
| `COMPLETED_EXAMPLES/ch04_05_procedural_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans bump, bump non alimenté, briques identiques, mortier de même couleur, échelle excessive, rangées alignées) |
| `SCRIPTS/validate_ch04_05.py` | Correcteur (procedural) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_05_procedural_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_05.py" -- --exercise procedural --render
```

## Livrables attendus

1. Mur de briques validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.06 — Texture Painting](../CH04_06_TEXTURE_PAINTING/README.md)
