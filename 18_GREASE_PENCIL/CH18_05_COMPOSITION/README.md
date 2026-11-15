# CH18.05 — Composition et dessin cinématographique

**Phase :** 18 — Grease Pencil (module A : fondamentaux du dessin)  
**Niveau :** débutant  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

Un storyboard n'est pas une suite de jolis dessins : c'est une suite de cadres pensés. Ce chapitre apprend à composer dans un cadre 16:9 (tiers, lignes directrices, symétrie, diagonale, cadre dans le cadre, espace de regard), à rendre une image lisible avec seulement trois valeurs, et à construire la profondeur d'un décor en trois plans. Ce sont les bases du storyboard (module C) et du layout 3D.

## Prérequis

- CH18.02 (perspective).
- CH18.03 (mannequin).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Composer une vignette avec une règle de composition choisie.
2. Placer horizon et sujet pour produire un effet voulu.
3. Rendre une vignette lisible en trois valeurs, au trait.
4. Construire un décor en trois plans (premier plan, plan moyen, arrière-plan).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.05.a | Vignette lisible en 3 valeurs | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le cadre et les règles de composition | 1 h |
| L2 | Les valeurs | 1 h |
| L3 | La profondeur en trois plans | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_05_composition_starter.blend` | Feuille : 6 cadres avec tiers, cadre de valeurs, exemple 3 plans, 3 calques de travail |
| `COMPLETED_EXAMPLES/ch18_05_composition_solution.blend` | Feuille complétée (référence schématique) |
| `COMPLETED_EXAMPLES/ch18_05_composition_reference.png` | Rendu de la référence |
| `SCRIPTS/validate_ch18_05.py` | Correcteur (via bcma_gp_check + gp_spec.json) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_05_composition_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_05.py" --python-exit-code 1 -- --exercise composition --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : séquence en 6 vignettes.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.06 — Grease Pencil : interface et objets](../CH18_06_GP_INTERFACE/README.md)
