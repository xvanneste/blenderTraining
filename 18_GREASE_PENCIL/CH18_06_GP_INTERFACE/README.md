# CH18.06 — Grease Pencil : interface et objets

**Phase :** 18 — Grease Pencil (module B : maîtrise de Grease Pencil)  
**Niveau :** débutant  
**Durée estimée :** 2 h 30  
**Version :** Blender 5.3.0

## Introduction

Le Grease Pencil n'est pas un logiciel de dessin plat : chaque trait est une suite de points en 3D, rangée dans des calques d'un objet de la scène. Ce chapitre apprend à créer et organiser des objets Grease Pencil (modes, calques, groupes, collections), à choisir où atterrissent les traits, et à placer des dessins devant et derrière des objets 3D — sans tomber dans le piège du rendu sans passe Z.

## Prérequis

- Phase 1 (interface, Outliner, collections).
- Module A de la phase 18 conseillé.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un objet Grease Pencil (Blank, Stroke, Monkey, Line Art).
2. Passer d'un mode à l'autre et savoir à quoi sert chacun.
3. Organiser calques, groupes de calques, verrous et opacité.
4. Placer un dessin à une profondeur voulue dans une scène 3D.
5. Obtenir un rendu où la 3D cache correctement le dessin (passe Z).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.06.a | Créer et organiser un objet GP | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | L'objet Grease Pencil et ses modes | 45 min |
| L2 | Calques, groupes, organisation | 45 min |
| L3 | Dessiner dans la scène 3D | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_06_gp_scene_starter.blend` | Décor 3D (sol, maison, arbre), caméra CAM_Shot, sans objet GP |
| `COMPLETED_EXAMPLES/ch18_06_gp_scene_solution.blend` | Scène complétée : 2 objets GP organisés, passe Z |
| `COMPLETED_EXAMPLES/ch18_06_gp_scene_reference.png` | Rendu de la référence (occlusion correcte) |
| `SCRIPTS/validate_ch18_06.py` | Correcteur (noms, calques, groupe, profondeurs, cadre, passe Z) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_06_gp_scene_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_06.py" --python-exit-code 1 -- --exercise organize --render
```

## Livrables attendus

1. Scène validée par le correcteur.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : un plan en trois profondeurs.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Scène validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.07 — Brushes, traits, remplissages, matériaux](../CH18_07_BRUSHES_MATERIALS/README.md)
