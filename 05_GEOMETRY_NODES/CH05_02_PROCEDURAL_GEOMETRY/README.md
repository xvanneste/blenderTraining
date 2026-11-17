# CH05.02 — Géométrie procédurale

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Les primitives, les transformations et Join Geometry suffisent à construire des objets entiers par nœuds. Ce chapitre assemble une colonne de 3 m : fût (Cylinder), base et chapiteau (Cube), anneau (Curve Circle et Curve to Mesh), chacun placé par un Transform. Le correcteur lit le graphe et mesure la géométrie évaluée : nombre de pièces, hauteur, pieds au sol, centrage, maillage fermé, matériau.

## Prérequis

- CH05.01.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Générer des maillages avec Cylinder et Cube et des courbes avec Curve Circle.
2. Placer des pièces avec Transform (Translation).
3. Transformer une courbe en maillage avec Curve to Mesh et un profil.
4. Assembler avec Join Geometry et contrôler les dimensions réelles.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.02.a | Générer un objet par nœuds | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Primitives, Transform, Join | 2 h 30 |
| L2 | Courbes en maillages et contrôle des dimensions | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_02_procedural_starter.blend` | Arbre avec le seul fût, sans Transform |
| `COMPLETED_EXAMPLES/ch05_02_procedural_solution.blend` | Colonne de 3 m complète |
| `COMPLETED_EXAMPLES/ch05_02_procedural_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans Join, sans anneau, flottante, fût trop court, chapiteau décalé) |
| `SCRIPTS/validate_ch05_02.py` | Correcteur (procedural) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_02_procedural_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_02.py" -- --exercise procedural --render
```

## Livrables attendus

1. Colonne procédurale validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.03 — Instances](../CH05_03_INSTANCES/README.md)
