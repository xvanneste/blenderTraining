# CH05.04 — Distribution

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Disperser des objets sur une surface demande de décider combien, où et à quelle distance les uns des autres. Distribute Points on Faces répond à ces trois questions : méthode (Random ou Poisson Disk), densité et masque. Ce chapitre plante des arbres sur la moitié d'un sol : méthode Poisson (distance minimale de 0,5 m), densité 3 par m², masque donné par un champ (Position → X > 0). Le correcteur lit le graphe et mesure les instances évaluées : nombre, proportion du bon côté, distance minimale entre arbres.

## Prérequis

- CH05.03.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distribuer des points sur des faces avec Distribute Points on Faces.
2. Choisir entre Random et Poisson Disk.
3. Piloter la densité par un masque (champ).
4. Mesurer une distribution (nombre, distance minimale).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.04.a | Distribuer avec contrôle | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Distribute Points on Faces | 2 h 30 |
| L2 | Masques et distance minimale | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_04_distribution_starter.blend` | Sol et arbre, sans distribution |
| `COMPLETED_EXAMPLES/ch05_04_distribution_solution.blend` | 73 arbres sur la moitié x > 0 |
| `COMPLETED_EXAMPLES/ch05_04_distribution_reference.png` | Deux vues (de face et du dessus) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans masque, méthode Random, trop clairsemé, mauvais côté, nœud orphelin) |
| `SCRIPTS/validate_ch05_04.py` | Correcteur (distribution) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_04_distribution_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_04.py" -- --exercise distribution --render
```

## Livrables attendus

1. Distribution maîtrisée validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.05 — Attributs](../CH05_05_ATTRIBUTES/README.md)
