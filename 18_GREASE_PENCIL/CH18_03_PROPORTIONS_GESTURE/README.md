# CH18.03 — Proportions, silhouettes, gestuelle

**Phase :** 18 — Grease Pencil (module A : fondamentaux du dessin)  
**Niveau :** débutant  
**Durée estimée :** 3 h + 10 min par jour de croquis  
**Version :** Blender 5.3.0

## Introduction

Un personnage de storyboard doit se lire en une seconde : sa pose, sa direction, son intention. Ce chapitre donne trois outils qui remplacent la connaissance de l'anatomie : les proportions mesurées en têtes, le mannequin construit en volumes, et la ligne d'action qui résume toute la pose. Vous travaillerez l'équilibre, le contrapposto, la silhouette lisible en noir et le croquis gestuel chronométré, sur une feuille Grease Pencil guidée par une échelle de proportions.

## Prérequis

- CH18.01 (volumes, geste).
- CH18.02 conseillé (horizon et personnages).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Mesurer un corps en hauteurs de tête et choisir un style de proportions.
2. Construire un mannequin en volumes avec des membres de longueur constante.
3. Commencer chaque pose par une ligne d'action expressive.
4. Vérifier l'équilibre et utiliser le contrapposto.
5. Produire des silhouettes lisibles et des croquis gestuels de 30 secondes.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.03.a | Croquis gestuel en 30 s et poses lisibles | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Proportions et mannequin | 1 h |
| L2 | Ligne d'action, équilibre, contrapposto | 1 h |
| L3 | Silhouette et croquis gestuel | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_03_gesture_starter.blend` | Feuille : échelle en têtes, mannequin, lignes d'action, 3 calques de travail |
| `COMPLETED_EXAMPLES/ch18_03_gesture_solution.blend` | Feuille complétée (référence) |
| `COMPLETED_EXAMPLES/ch18_03_gesture_reference.png` | Rendu de la référence |
| `SCRIPTS/validate_ch18_03.py` | Correcteur (via bcma_gp_check + gp_spec.json) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_03_gesture_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_03.py" --python-exit-code 1 -- --exercise gesture --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : 100 croquis en 10 jours.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.04 — Expressions et personnages](../CH18_04_EXPRESSIONS_CHARACTERS/README.md)
