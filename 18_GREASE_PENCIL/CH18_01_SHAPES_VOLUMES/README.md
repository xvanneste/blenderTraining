# CH18.01 — Formes et volumes

**Phase :** 18 — Grease Pencil : dessin 2D, storyboard, animatique et animation hybride (module A)  
**Niveau :** débutant absolu (aucune pratique du dessin requise)  
**Durée estimée :** 3 h 30 + 10–15 min par jour d'échauffement  
**Version :** Blender 5.3.0

## Introduction

Storyboarder ne demande pas d'être illustrateur : il faut des traits assurés, des volumes justes et des valeurs lisibles. Ce premier chapitre du module dessin part de zéro : le geste qui part de l'épaule, les quatre volumes primaires (boîte, cylindre, sphère, cône), les ellipses, et la lumière qui rend un volume lisible (terminateur, ombre propre, ombre portée, trois valeurs). Vous travaillez directement dans Grease Pencil, sur une feuille d'exercices préparée avec guides, ligne d'horizon et points de fuite.

## Prérequis

- CH01.01–CH01.02 (interface, navigation).
- Tablette conseillée (CH00.04), non obligatoire.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Tracer des lignes et des ellipses d'un seul geste.
2. Construire boîtes, cylindres, sphères et cônes en perspective simple.
3. Décomposer un objet du quotidien en volumes primaires.
4. Rendre un volume lisible avec trois valeurs (lumière, ombre propre, ombre portée).
5. Dessiner, effacer, lisser et changer de calque/matériau dans Grease Pencil.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.01.a | Construire un objet en volumes | Exercice 3 (correcteur + grille d'auto-évaluation) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le geste et les lignes | 1 h |
| L2 | Les volumes primaires | 1 h 30 |
| L3 | Lumière et valeurs | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_01_volumes_starter.blend` | Feuille GP : guides verrouillés, 3 calques de travail, caméra orthographique |
| `COMPLETED_EXAMPLES/ch18_01_volumes_solution.blend` | Feuille complétée (référence technique) |
| `COMPLETED_EXAMPLES/ch18_01_volumes_reference.png` | Rendu de la référence |
| `SCRIPTS/gp_spec.json` | Spécification de correction (quantités, zones, remplissages) |
| `SCRIPTS/validate_ch18_01.py` | Correcteur (via SCRIPTS/bcma_gp_check.py) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_01_volumes_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_01.py" -- --exercise volumes --render
```

## Livrables attendus

1. Feuille complétée et validée.
2. Grille d'auto-évaluation ≥ 14/20.
3. Carnet de 7 jours (mini-projet).

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Feuille validée par le correcteur.
- Auto-évaluation ≥ 14/20 (refaite à J+7).

➡️ Chapitre suivant : [CH18.02 — Perspective](../CH18_02_PERSPECTIVE/README.md)
