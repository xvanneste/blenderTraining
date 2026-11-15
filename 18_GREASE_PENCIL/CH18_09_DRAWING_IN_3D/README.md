# CH18.09 — Dessin dans l'espace 3D et organisation

**Phase :** 18 — Grease Pencil (module B : maîtrise de Grease Pencil)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h 15  
**Version :** Blender 5.3.0

## Introduction

Le Grease Pencil prend toute sa puissance quand on dessine dans l'espace : un décor en plusieurs profondeurs, un sol dessiné à plat, des éléments qui réagissent à la caméra avec une vraie parallaxe. Ce chapitre apprend à maîtriser Stroke Placement, Drawing Plane, le curseur 3D et le Canvas, à utiliser des images de référence, puis à organiser et optimiser une scène dessinée.

## Prérequis

- CH18.06 (objets GP, passe Z).
- CH18.05 (composition).
- CH01.12 (caméras).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir Stroke Placement et Drawing Plane selon ce qu'on dessine.
2. Placer le curseur 3D précisément et utiliser la grille du Canvas.
3. Construire un décor dessiné sur plusieurs profondeurs, avec un sol à plat.
4. Utiliser et ranger des images de référence.
5. Organiser et optimiser une scène Grease Pencil.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.09.a | Décor dessiné en profondeur | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Placement et plans de dessin | 1 h |
| L2 | Un décor en profondeur | 1 h 30 |
| L3 | Références, organisation, optimisation | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_09_set_starter.blend` | Sol, caméra, référence, GP_Set vide (4 calques) |
| `COMPLETED_EXAMPLES/ch18_09_set_solution.blend` | Décor dessiné sur 4 profondeurs |
| `COMPLETED_EXAMPLES/ch18_09_set_reference.png` | Rendu caméra |
| `COMPLETED_EXAMPLES/ch18_09_set_top.png` | Vue de dessus (plans de dessin) |
| `ASSETS/ch18_09_concept.png` | Image de référence (licence BCMA) |
| `SCRIPTS/validate_ch18_09.py` | Correcteur (profondeurs mesurées, sol à plat, cadre, passe Z) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_09_set_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_09.py" --python-exit-code 1 -- --exercise set --render
```

## Livrables attendus

1. Décor validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : travelling dans un décor dessiné.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Décor validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH18.10 — Langage cinématographique](../CH18_10_FILM_LANGUAGE/README.md)
