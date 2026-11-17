# CH05.01 — Principes de Geometry Nodes

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Geometry Nodes construit de la géométrie par un graphe : la géométrie circule de nœud en nœud, et des champs — des valeurs calculées en chaque point, face ou arête — la pilotent. Ce chapitre construit un terrain procédural : une grille de 100 × 100 sommets déplacée par un bruit (le champ), lissée et habillée d'un matériau. Le correcteur lit le graphe et évalue la géométrie réellement produite (nombre de sommets, emprise, relief, lissage, matériau).

## Prérequis

- CH04.04–05 (nœuds et textures procédurales).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire un arbre Geometry Nodes : géométrie qui circule, nœuds, sockets.
2. Distinguer une valeur unique d'un champ évalué par point.
3. Générer un maillage (Grid), le déformer (Set Position) et vérifier le résultat.
4. Savoir pourquoi un matériau doit être réappliqué (Set Material).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.01.a | Lire et construire un arbre de nœuds | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La géométrie circule, les champs calculent | 2 h 30 |
| L2 | Construire et inspecter un terrain | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_01_principles_starter.blend` | Arbre avec la seule Grid (3 × 3 sommets) |
| `COMPLETED_EXAMPLES/ch05_01_principles_solution.blend` | Terrain procédural complet |
| `COMPLETED_EXAMPLES/ch05_01_principles_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (champ absent, sans lissage, sans matériau, grille grossière, amplitude démesurée, nœud orphelin) |
| `SCRIPTS/validate_ch05_01.py` | Correcteur (principles) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_01_principles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_01.py" -- --exercise principles --render
```

## Livrables attendus

1. Terrain procédural validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.02 — Géométrie procédurale](../CH05_02_PROCEDURAL_GEOMETRY/README.md)
