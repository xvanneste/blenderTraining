# CH03.06 — Visages

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Un visage se juge sur ses détails de structure : paupières qui recouvrent le globe, narines creusées sous le nez, ligne de bouche aussi large que l'écart des pupilles, oreilles avec bord (hélix) et creux (conque). Ce chapitre part du buste de CH03.05 (volume lissé, orbites, yeux) et demande d'y sculpter ces quatre zones, puis une expression de base : le sourire. Le correcteur compare votre buste à une copie cachée du buste de départ (REF_Base) et mesure ce que vous avez creusé ou relevé, zone par zone.

## Prérequis

- CH03.01 à CH03.05.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Sculpter paupières, narines, bouche et oreilles avec le bon ordre de grandeur.
2. Relier la forme d'une expression aux déplacements de la bouche et des plis.
3. Vérifier un travail par mesure différentielle (avant / après).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.06.a | Sculpter un visage | Exercices 2 et 3 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Yeux, nez, bouche, oreilles | 3 h |
| L2 | Expressions de base : le sourire | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_06_face_starter.blend` | Buste de CH03.05 sans détails de visage + REF_Base caché |
| `COMPLETED_EXAMPLES/ch03_06_face_solution.blend` | Visage neutre (sculpté à la brosse, Blender 5.2 via MCP) |
| `COMPLETED_EXAMPLES/ch03_06_smile_solution.blend` | Visage souriant (sculpté à la brosse, Blender 5.2 via MCP) |
| `COMPLETED_EXAMPLES/ch03_06_face_reference.png` | Neutre : face, 3/4, profil |
| `COMPLETED_EXAMPLES/ch03_06_smile_reference.png` | Sourire : face, 3/4, profil |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans paupières, narines, bouche, oreilles ; moue) |
| `SCRIPTS/validate_ch03_06.py` | Correcteur (face, smile) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_06_face_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_06.py" -- --exercise face --render
```

## Livrables attendus

1. Visage validé (face) et sourire validé (smile).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 2 et 3 validés.

➡️ Chapitre suivant : [CH03.07 — Mains et pieds](../CH03_07_HANDS_FEET/README.md)
