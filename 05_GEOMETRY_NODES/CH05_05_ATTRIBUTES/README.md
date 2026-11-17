# CH05.05 — Attributs

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Un attribut est une donnée portée par la géométrie (par point, face, arête…) : position, normale, couleur, ou un nom que vous choisissez. Geometry Nodes peut en calculer et les stocker (Store Named Attribute) ; un shader peut les lire (nœud Attribute). Ce chapitre colorie le terrain de CH05.01 selon sa hauteur : l'arbre stocke « height » sur les points, le matériau lit « height » et choisit la couleur. Le correcteur vérifie l'attribut dans la géométrie évaluée (domaine, type, valeurs = z) et la cohérence du nom entre l'arbre et le shader.

## Prérequis

- CH05.01
- CH04.04 (nœuds de shader).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer domaine (point, arête, face, coin…) et type de données d'un attribut.
2. Stocker un champ avec Store Named Attribute.
3. Lire l'attribut dans un shader avec le nœud Attribute.
4. Contrôler l'attribut dans le Spreadsheet et par script.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.05.a | Piloter un shader par un attribut | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Attributs, domaines et types | 2 h 30 |
| L2 | Stocker dans l'arbre, lire dans le shader | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_05_attributes_starter.blend` | Terrain déplacé sans attribut ; matériau gris uni |
| `COMPLETED_EXAMPLES/ch05_05_attributes_solution.blend` | Terrain colorié par la hauteur |
| `COMPLETED_EXAMPLES/ch05_05_attributes_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans stockage, mauvais nom, mauvais domaine, shader non relié, valeur constante, nœud orphelin) |
| `SCRIPTS/validate_ch05_05.py` | Correcteur (attributes) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_05_attributes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_05.py" -- --exercise attributes --render
```

## Livrables attendus

1. Terrain colorié par attribut validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.06 — Paramètres et interfaces](../CH05_06_PARAMETERS/README.md)
