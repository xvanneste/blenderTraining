# CH03.07 — Mains et pieds

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Les mains et les pieds sont les parties où l'on voit le plus vite qu'un personnage est mal construit. Ce chapitre fixe la structure : cinq doigts de trois phalanges (le pouce en a deux) aux longueurs relatives justes, un pouce qui part du poignet, un pied avec talon étroit, voûte plantaire, avant-pied large et cinq orteils décroissants. Le correcteur compte les doigts et les orteils sur la silhouette vue de dessus et vérifie longueurs, pouce, effilement, voûte et semelle.

## Prérequis

- CH03.01 à CH03.06.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une main avec ses proportions (majeur le plus long, pouce court, auriculaire court).
2. Construire un pied avec voûte, talon et orteils décroissants.
3. Garder les doigts et orteils séparés tout en gardant un volume fermé.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.07.a | Sculpter une main | Exercice 2 (correcteur) + grille ; le pied : exercice 3 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La main | 3 h |
| L2 | Le pied | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_07_hand_starter.blend` | Studio, 3 caméras, guide de la main (à plat) |
| `STARTER_FILES/ch03_07_foot_starter.blend` | Studio, 3 caméras, guide du pied (à plat) |
| `COMPLETED_EXAMPLES/ch03_07_hand_solution.blend` | Main (SCULPT_Hand) |
| `COMPLETED_EXAMPLES/ch03_07_foot_solution.blend` | Pied (SCULPT_Foot) |
| `COMPLETED_EXAMPLES/ch03_07_hand_reference.png` | Main : dessus, 3/4, profil |
| `COMPLETED_EXAMPLES/ch03_07_foot_reference.png` | Pied : dessus, 3/4, profil |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (moufle, 4 doigts, doigts égaux, sans pouce, pied plat, orteils fusionnés, etc.) |
| `SCRIPTS/validate_ch03_07.py` | Correcteur (hand, foot) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_07_hand_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_07.py" -- --exercise hand --render
```

## Livrables attendus

1. Main validée (hand) et pied validé (foot).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 2 et 3 validés.

➡️ Chapitre suivant : [CH03.08 — Vêtements](../CH03_08_CLOTHING/README.md)
