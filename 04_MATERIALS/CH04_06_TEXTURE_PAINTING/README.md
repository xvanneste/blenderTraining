# CH04.06 — Texture Painting

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Quand le détail doit être placé à la main (une bande, un logo, de l'usure), on peint directement sur l'objet : Blender projette le pinceau sur la surface et écrit dans l'image, via les UV. Ce chapitre peint une boîte de conserve en Texture Paint : une bande rouge qui fait le tour, des pastilles bleues. La solution a été réellement peinte à la brosse (Blender 5.2 piloté par le MCP, opérateur de peinture d'image). Le correcteur analyse les pixels de l'image : couverture, couleurs, peinture hors des îlots UV, et que l'image est empaquetée.

## Prérequis

- CH04.01 (UV propres : la peinture passe par les UV).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Passer en Texture Paint, choisir un pinceau et une couleur.
2. Peindre en vue orthographique sur plusieurs côtés d'un objet.
3. Empaqueter l'image : sans cela la peinture est perdue.
4. Vérifier une peinture par mesure des pixels.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.06.a | Peindre une texture sur un objet | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Principes de la peinture de texture | 2 h |
| L2 | Peindre, empaqueter, vérifier | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_06_painting_starter.blend` | Boîte PROP_Can, image T_Can crème branchée |
| `COMPLETED_EXAMPLES/ch04_06_painting_solution.blend` | Peinte au pinceau (Texture Paint, Blender 5.2) |
| `COMPLETED_EXAMPLES/ch04_06_painting_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (vierge, une couleur, tout repeint, peinture hors UV, image non branchée) |
| `SCRIPTS/validate_ch04_06.py` | Correcteur (painting) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_06_painting_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_06.py" -- --exercise painting --render
```

## Livrables attendus

1. Boîte peinte et validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.07 — Baking](../CH04_07_BAKING/README.md)
