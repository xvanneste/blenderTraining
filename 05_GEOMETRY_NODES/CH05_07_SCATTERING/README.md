# CH05.07 — Décors et végétation

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une forêt crédible n'est ni une grille ni un tapis uniforme : les arbres évitent les pentes raides, diffèrent par la forme et la taille, et se répartissent de manière contrôlable. Ce chapitre assemble tout ce qui précède (terrain, distribution, instances, attributs, interface) en un outil « Forêt » : trois variantes d'arbres, échelle aléatoire, contrainte de pente et trois paramètres (Seed, Density, Max Slope). Le correcteur règle ces paramètres et mesure le résultat : arbres sur la surface, pentes respectées, variantes, effet de chaque paramètre.

## Prérequis

- CH05.03–06.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Contraindre une distribution par la pente (Normal Z).
2. Mélanger plusieurs variantes avec Geometry to Instance et Pick Instance.
3. Varier l'échelle et la rotation.
4. Exposer et tester Seed, Density et Max Slope.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.07.a | Générer une forêt | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Contraintes de pente et masques | 3 h |
| L2 | Variantes, variation et paramètres | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_07_scattering_starter.blend` | Terrain déplacé, interface vide, arbres non dispersés |
| `COMPLETED_EXAMPLES/ch05_07_scattering_solution.blend` | Outil « Forêt » complet |
| `COMPLETED_EXAMPLES/ch05_07_scattering_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans contrainte de pente, sans variantes, Seed non branché, sans échelle aléatoire, arbres flottants) |
| `SCRIPTS/validate_ch05_07.py` | Correcteur (scattering) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_07_scattering_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_07.py" -- --exercise scattering --render
```

## Livrables attendus

1. Outil « Forêt » validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.08 — Architecture procédurale](../CH05_08_ARCHITECTURE/README.md)
