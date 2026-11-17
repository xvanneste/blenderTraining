# CH18.20 — Workflow 2D → 3D

**Phase :** 18 — Grease Pencil (module F : hybride 2D/3D)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

Storyboarder directement à travers les caméras d'un décor 3D, puis réutiliser ces caméras pour le layout : chaque case du board est un objet Grease Pencil enfant de sa caméra, liée à son marqueur. Le blocking place ensuite le personnage 3D sur la silhouette dessinée, plan par plan, avec des clés Constant. Le correcteur superpose, dans l'image de chaque caméra, la silhouette dessinée et le mannequin 3D (recouvrement et pieds), et vérifie que les caméras du board n'ont pas bougé.

## Prérequis

- CH18.14 (caméras liées aux marqueurs).
- CH18.19.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Dessiner un board dans une caméra (GP enfant de la caméra).
2. Réutiliser les caméras du board pour le layout.
3. Faire un blocking 3D fidèle au board (clés Constant).
4. Choisir et unifier un style hybride.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.20.a | Caméras de board réutilisées en layout | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le board dans le décor 3D | 1 h |
| L2 | Blocking 3D d'après le board | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_20_layout_starter.blend` | Décor, 3 caméras + boards, mannequin non placé |
| `COMPLETED_EXAMPLES/ch18_20_layout_solution.blend` | Blocking des 3 plans |
| `COMPLETED_EXAMPLES/ch18_20_layout_contact.png` | Les 3 plans, board superposé |
| `SCRIPTS/validate_ch18_20.py` | Correcteur (layout) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_20_layout_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_20.py" -- --exercise layout --render
```

## Livrables attendus

1. Blocking validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH18.21 — IA pour le storyboard](../CH18_21_AI_STORYBOARD/README.md)
