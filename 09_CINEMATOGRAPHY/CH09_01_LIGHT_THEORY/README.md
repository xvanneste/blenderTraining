# CH09.01 — Théorie de la lumière

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Éclairer, c'est contrôler quatre choses : la quantité de lumière (intensité), d'où elle vient (direction et distance), la dureté de l'ombre qu'elle projette (taille de la source) et sa couleur. Ce chapitre les rend mesurables : le correcteur rend lui-même une scène minimaliste (un plan gris, une lampe, un cube qui projette une ombre, un monde noir) et lit les pixels. Vous y vérifiez la loi de l'inverse du carré (trois fois plus loin, neuf fois moins de lumière), l'effet du rayon d'une lampe sur la pénombre, et l'effet de la couleur de la lampe sur la couleur reçue.

## Prérequis

- CH01 (scène, objets, rendu de base), CH04 (matériaux).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Énoncer et appliquer la loi de l'inverse du carré.
2. Régler Power, Radius et Color d'une lampe.
3. Prévoir la douceur d'une ombre.
4. Mesurer une exposition sur un rendu linéaire.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.01.a | Analyser un éclairage | Exercice 2 (correcteur) + profils d'ombre |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Intensité et distance | 3 h |
| L2 | Dureté et couleur | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_01_light_starter.blend` | Une lampe blanche de 10 W à 1 m au-dessus du plan, Radius 0 : la référence d'exposition |
| `COMPLETED_EXAMPLES/ch09_01_light_solution.blend` | Lampe à 3 m, 100 W, Radius 0,5 m, couleur chaude (1 ; 0,85 ; 0,65) : même exposition que la référence |
| `COMPLETED_EXAMPLES/ch09_01_light_reference.png` | Profil de luminance le long d'une ligne traversant l'ombre : source étendue (orange, bord progressif) et source ponctuelle (bleu, bord net) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sous-exposé, surexposé, trop près, ombre dure, lumière froide) |
| `SCRIPTS/validate_ch09_01.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_01_light_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_01.py" -- --exercise light
```

## Livrables attendus

1. Éclairage mesuré validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.02 — Trois points et variantes](../CH09_02_THREE_POINT/README.md)
