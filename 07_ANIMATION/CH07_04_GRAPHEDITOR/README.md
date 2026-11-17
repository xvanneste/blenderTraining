# CH07.04 — Graph Editor

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Le Graph Editor montre une animation comme des courbes : la valeur d'une propriété en fonction du temps. C'est là qu'on règle la FORME du mouvement : interpolation, poignées, ralentis, répétition, frémissement. Ce chapitre polit un pendule : interpolation Bezier avec poignées Auto Clamped (ralentis aux extrémités), modificateur Cycles (répétition infinie), modificateur Noise (frémissement léger). Le correcteur lit les courbes ET mesure l'animation évaluée : vitesse aux extrémités, vitesse maximale, répétition, amplitude du bruit.

## Prérequis

- CH07.02 (clés), CH07.03 (Dope Sheet).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire une courbe d'animation.
2. Choisir interpolation et poignées.
3. Ajouter un modificateur Cycles.
4. Ajouter un modificateur Noise et en régler l'amplitude.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.04.a | Polir des courbes | Exercice 2 (correcteur) + courbes de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lire et polir une courbe | 4 h |
| L2 | Modificateurs de courbe | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_04_graph_starter.blend` | Pendule aux clés linéaires, sans modificateur, plage 1–25 |
| `COMPLETED_EXAMPLES/ch07_04_graph_solution.blend` | Pendule poli : Bezier Auto Clamped, Cycles, Noise ; plage 1–48 |
| `COMPLETED_EXAMPLES/ch07_04_graph_reference.png` | Graph Editor en numpy : rotation (orange, trois cycles) et frémissement de Z (vert) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (linéaire, constante, sans Cycles, sans Noise, bruit trop fort, mauvaises clés) |
| `SCRIPTS/validate_ch07_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_04_graph_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_04.py" -- --exercise graph
```

## Livrables attendus

1. Pendule poli validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.05 — Timing et spacing](../CH07_05_TIMING/README.md)
