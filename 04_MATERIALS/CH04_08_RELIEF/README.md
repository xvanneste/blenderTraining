# CH04.08 — Relief : bump, normal map, displacement

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Trois techniques donnent du relief à une surface : le bump (hauteur → normale perturbée), la normal map (normales stockées, CH04.07) et le displacement (la géométrie est réellement déplacée). Ce chapitre compare leurs usages puis réalise un vrai displacement : un sol de terrain rendu en Cycles, dont la silhouette ondule. Le correcteur contrôle le moteur, le branchement du nœud Displacement, l'amplitude, le réglage du matériau et la subdivision du maillage.

## Prérequis

- CH04.04–05 (nœuds, textures procédurales)
- CH04.07.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir entre bump, normal map et displacement selon le besoin.
2. Brancher un Displacement et régler Scale et Midlevel.
3. Régler la méthode de displacement du matériau et subdiviser le maillage.
4. Reconnaître les limites de chaque technique (silhouette, coût).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.08.a | Choisir et régler la technique de relief | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Bump, normal map, displacement | 2 h |
| L2 | Un vrai displacement avec Cycles | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_08_relief_starter.blend` | Plan 6 x 6 m, Principled seul, EEVEE |
| `COMPLETED_EXAMPLES/ch04_08_relief_solution.blend` | Sol en displacement (Cycles) |
| `COMPLETED_EXAMPLES/ch04_08_relief_reference.png` | Deux vues Cycles, soleil rasant |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (méthode Bump, sans subdivision, échelle excessive, hauteur constante, non relié, EEVEE) |
| `SCRIPTS/validate_ch04_08.py` | Correcteur (relief) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_08_relief_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_08.py" -- --exercise relief
```

## Livrables attendus

1. Sol en displacement validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.09 — Matériaux types](../CH04_09_TYPICAL_MATERIALS/README.md)
