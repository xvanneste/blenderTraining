# CH08.04 — Particules et distribution

**Phase :** 8 — Physique et simulations  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un système de particules émet des milliers de petits points qui obéissent à des règles : où et quand ils naissent, à quelle vitesse, combien de temps ils vivent, quelles forces les poussent, quels obstacles ils rencontrent. Ce chapitre fabrique une fontaine : 200 particules émises sur 30 images depuis les faces d'une grille, lancées vers le haut, soumises à la gravité, qui rebondissent sur un sol (Collision) et meurent à la fin de leur vie. Le correcteur configure ET simule : étalement de l'émission, hauteur, absence de traversée du sol, durée de vie.

## Prérequis

- CH08.01 (simulation pas à pas), CH05.04 (distribution par Geometry Nodes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un système de particules émettrices.
2. Régler nombre, durée d'émission, vie et vitesse.
3. Ajouter la gravité et un obstacle.
4. Mesurer émission, hauteur et durée de vie.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.04.a | Émission de particules | Exercice 2 (correcteur) + nuage de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Émettre | 3 h |
| L2 | Forces, obstacles, mesures | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_04_particles_starter.blend` | Émetteur (grille à 1 m de haut) et sol, sans physique |
| `COMPLETED_EXAMPLES/ch08_04_particles_solution.blend` | Fontaine de 200 particules émises de 1 à 30, vie 60, gravité, collision du sol |
| `COMPLETED_EXAMPLES/ch08_04_particles_reference.png` | Nuage de particules vu de côté aux images 10, 20, 40 et 60 |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans collision du sol, vie trop courte, sans gravité, trop peu de particules, émission en rafale, sans vitesse) |
| `SCRIPTS/validate_ch08_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_04_particles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_04.py" -- --exercise particles
```

## Livrables attendus

1. Fontaine de particules validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.05 — Fluides (Mantaflow)](../CH08_05_FLUIDS/README.md)
