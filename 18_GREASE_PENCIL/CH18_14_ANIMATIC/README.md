# CH18.14 — Du scénario à l'animatique

**Phase :** 18 — Grease Pencil (module D : animatique)  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

L'animatique est le premier film complet : les images du storyboard montées à leurs durées réelles. Ce chapitre transforme une liste de plans en images exactes (24 i/s), monte la planche du CH18.13 image par image en Grease Pencil (une image clé par plan, marqueurs nommés, zoom de caméra, incrustation), puis construit une animatique 3D à caméras multiples liées aux marqueurs, dont les valeurs de plans sont mesurées.

## Prérequis

- CH18.10 à CH18.13.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Convertir une liste de plans en images de début et de fin.
2. Monter une animatique 2D image par image (clés GP, marqueurs, caméra animée).
3. Incruster code de plan et numéro d'image dans le rendu.
4. Monter une animatique 3D avec une caméra liée à chaque marqueur.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.14.a | Animatique image par image | Exercices 2 et 3 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Du scénario à la liste de plans | 45 min |
| L2 | L'animatique 2D image par image | 1 h 30 |
| L3 | L'animatique 3D à caméras multiples | 1 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_14_animatic_starter.blend` | Feuille 16:9, SHOTLIST, calque USER_Panels vide |
| `COMPLETED_EXAMPLES/ch18_14_animatic_solution.blend` | Animatique « La tasse tombe » (456 images) |
| `COMPLETED_EXAMPLES/ch18_14_animatic_contact.png` | Planche contact : une image par plan |
| `STARTER_FILES/ch18_14_layout_starter.blend` | Décor de dialogue, SHOTLIST, sans caméra |
| `COMPLETED_EXAMPLES/ch18_14_layout_solution.blend` | 6 caméras liées aux marqueurs |
| `COMPLETED_EXAMPLES/ch18_14_layout_contact.png` | Planche contact du layout |
| `SCRIPTS/validate_ch18_14.py` | Correcteur (animatic, layout) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_14_animatic_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_14.py" -- --exercise animatic --render
```

## Livrables attendus

1. Animatique 2D validée.
2. Animatique 3D validée.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Les deux exercices validés par le correcteur.

➡️ Chapitre suivant : [CH18.15 — Son, rythme, transitions, export, révision](../CH18_15_SOUND_EXPORT/README.md)
