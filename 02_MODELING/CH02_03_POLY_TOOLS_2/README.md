# CH02.03 — Outils polygonaux II

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Après les outils qui ajoutent de la matière, voici ceux qui découpent, font tourner et nettoient : Knife, Bisect, Spin, Screw, Merge et Dissolve. Six postes d'atelier, un par outil, avec les vrais comportements de Blender 5.3 — y compris un piège mesuré : le Spin laisse des sommets superposés sur l'axe.

## Prérequis

- CH02.02 (outils polygonaux I).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Découper au Knife avec les bonnes touches et au Bisect avec des valeurs exactes.
2. Créer un objet de révolution avec Spin et le souder correctement.
3. Créer une hélice non destructive avec le modificateur Screw.
4. Fusionner (Merge) et simplifier (Dissolve, Limited Dissolve) sans trouer.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.03.a | Découper et nettoyer | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Couper : Knife et Bisect | 1 h |
| L2 | Tourner : Spin et Screw | 1 h |
| L3 | Nettoyer : Merge et Dissolve | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_03_cutting_starter.blend` | 6 postes : barre, cube encombré, profil, cube, cercle, carreau |
| `COMPLETED_EXAMPLES/ch02_03_cutting_solution.blend` | Les 6 postes réalisés |
| `COMPLETED_EXAMPLES/ch02_03_cutting_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch02_03.py` | Correcteur (cote, fermeture, faces, secteurs, doublons, modificateur, diagonale) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_03_cutting_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_03.py" --python-exit-code 1 -- --exercise atelier --render
```

## Livrables attendus

1. Atelier validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : lampe de chevet tournée.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Atelier validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.04 — Normales](../CH02_04_NORMALS/README.md)
