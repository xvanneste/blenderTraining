# CH02.01 — Topologie

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** débutant → intermédiaire  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

La topologie, c'est la façon dont les points d'un maillage sont reliés. Elle décide si un objet se subdivise proprement, se déforme bien à l'animation, se déplie facilement et s'ombre correctement. Ce chapitre apprend à lire une topologie (triangles, quads, n-gons, boucles, pôles, densité), puis à diagnostiquer et réparer les défauts courants avec les outils de Blender 5.3, dans une « clinique » de cinq objets malades.

## Prérequis

- Phase 1 complète (Edit Mode : CH01.05).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer triangles, quads et n-gons et savoir quand chacun est acceptable.
2. Sélectionner boucles et anneaux d'arêtes, juger un flux d'arêtes.
3. Repérer et placer les pôles.
4. Diagnostiquer n-gons, triangles, doublons, trous avec Select All by Trait.
5. Réparer avec Grid Fill, Triangles to Quads, Merge by Distance, Fill.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.01.a | Diagnostiquer une topologie | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Tris, quads, n-gons et boucles | 1 h |
| L2 | Flux, pôles, densité | 1 h |
| L3 | Diagnostiquer et réparer | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_01_topology_starter.blend` | 5 patients (n-gon, triangles, doublons, trou, pôles) + texte DIAGNOSTIC |
| `COMPLETED_EXAMPLES/ch02_01_topology_solution.blend` | Patients réparés, diagnostic rempli |
| `COMPLETED_EXAMPLES/ch02_01_topology_reference.png` | Rendu avec fil de fer |
| `SCRIPTS/validate_ch02_01.py` | Correcteur (mesures bmesh : côtés des faces, doublons, non-manifold, pôles) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_01_topology_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_01.py" -- --exercise clinic --render
```

## Livrables attendus

1. Clinique validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : checklist de validation d'un asset.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Clinique validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.02 — Outils polygonaux I](../CH02_02_POLY_TOOLS_1/README.md)
