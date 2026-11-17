# CH09.11 — Couleur et émotion

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

La couleur porte l'émotion avant même que le spectateur ait lu l'image. Trois grandeurs la décrivent : la teinte (la couleur elle-même, en degrés sur le cercle chromatique), la saturation (son intensité) et la valeur (sa clarté). Un color script est une suite de cartes de couleur, une par moment du film, qui planifie l'émotion plan par plan avant tout rendu. Ce chapitre fait construire un color script de cinq émotions ; le correcteur rend les cartes et mesure la teinte, la saturation et la valeur réellement affichées.

## Prérequis

- CH09.06 (exposition, rendu mesuré), CH09.04 (ambiances).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Décrire une couleur par teinte, saturation, valeur.
2. Associer une émotion à une palette.
3. Faire ressortir un accent sur un fond.
4. Mesurer une palette sur un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.11.a | Construire un color script | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Teinte, saturation, valeur | 3 h |
| L2 | Le color script | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_11_color_starter.blend` | Dix plans gris moyen : aucune émotion (rendu : gris à V 0,73) |
| `COMPLETED_EXAMPLES/ch09_11_color_solution.blend` | Cinq cartes : joie jaune vif, tristesse bleu-gris sombre, colère rouge, calme turquoise doux, peur presque noire avec un accent vert |
| `COMPLETED_EXAMPLES/ch09_11_color_reference.png` | Départ (haut : cinq cartes grises) et solution (bas : cinq émotions) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (tristesse verdâtre, calme saturé, joie sombre, teintes confondues, accent invisible, peur sur fond clair) |
| `SCRIPTS/validate_ch09_11.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_11_color_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_11.py" -- --exercise color
```

## Livrables attendus

1. Color script de cinq cartes validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.12 — Mise en scène](../CH09_12_STAGING/README.md)
