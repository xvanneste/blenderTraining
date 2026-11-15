# CH02.08 — Modélisation organique

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Arbres, rochers, créatures : les formes organiques se pensent en volumes et en silhouettes, pas en faces. Ce chapitre présente le blocking par volumes, le box modeling avec subdivision, et le modificateur Skin qui transforme un simple squelette d'arêtes en volume lisse — démontré sur un arbre construit à partir d'un seul sommet.

## Prérequis

- CH02.06 (subdivision)
- CH18.03 (silhouettes) conseillé.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Bloquer une forme en volumes simples et juger sa silhouette.
2. Modéliser une forme organique en box modeling.
3. Construire un squelette d'arêtes et l'habiller avec Skin + Subdivision.
4. Régler les rayons du Skin pour un rythme crédible.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.08.a | Modéliser une forme organique | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Blocking par volumes | 45 min |
| L2 | Box modeling | 1 h |
| L3 | Le modificateur Skin | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_08_tree_starter.blend` | GEO_Tree : un seul sommet |
| `COMPLETED_EXAMPLES/ch02_08_tree_solution.blend` | Arbre : squelette, Skin, Subdivision |
| `COMPLETED_EXAMPLES/ch02_08_tree_reference.png` | Rendu du volume |
| `COMPLETED_EXAMPLES/ch02_08_tree_skeleton.png` | Rendu du squelette seul |
| `SCRIPTS/validate_ch02_08.py` | Correcteur (squelette, embranchements, pile, rayons, fermeture) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_08_tree_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_08.py" --python-exit-code 1 -- --exercise tree --render
```

## Livrables attendus

1. Arbre validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : la créature.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Arbre validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.09 — Retopologie](../CH02_09_RETOPOLOGY/README.md)
