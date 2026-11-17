# CH08.07 — Destruction

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Détruire un décor, c'est faire éclater un objet en morceaux qui tiennent ensemble jusqu'au choc. Avec les corps rigides (CH08.01), on obtient cela en reliant des pièces voisines par des contraintes Fixed cassables : tant que la force reste sous le seuil, la pièce tient ; au-dessus, la liaison saute. Ce chapitre construit un mur de 24 briques frappé par un boulet de 40 kg. Une précision d'honnêteté importante : l'extension Cell Fracture (qui découpe un maillage en éclats) n'est PAS livrée avec Blender 5.3 (le dossier des extensions de base ne la contient pas ; elle serait à télécharger) : nous partons donc de pièces déjà séparées, ce qui est aussi la méthode des films quand le décor a été fracturé à l'avance.

## Prérequis

- CH08.01 (corps rigides, monde, Animated).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Relier des corps rigides par des contraintes Fixed (opérateur Connect).
2. Rendre une contrainte cassable et choisir son seuil.
3. Mesurer une destruction par les liaisons cassées.
4. Reconnaître une simulation instable (mur qui explose).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.07.a | Destruction | Exercice 2 (correcteur) + vue de dessus des briques |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Contraintes et seuil de rupture | 4 h |
| L2 | Mesurer et stabiliser | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_07_destruction_starter.blend` | Sol, 24 briques actives, boulet animé et monde réglé ; aucune contrainte (le mur est simplement empilé) |
| `COMPLETED_EXAMPLES/ch08_07_destruction_solution.blend` | 38 contraintes Fixed cassables (seuil 1) : le mur se fracture (13 liaisons sur 38 cassées) sans tout disperser |
| `COMPLETED_EXAMPLES/ch08_07_destruction_reference.png` | Vue de dessus à l'image 120 : à gauche la solution (mur fracturé, trou du boulet), à droite un seuil de 20 (mur poussé d'un bloc) ; gris = position de départ |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (contraintes non cassables, seuil trop haut, sans contraintes, sol sans physique) |
| `SCRIPTS/validate_ch08_07.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_07_destruction_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_07.py" -- --exercise destruction
```

## Livrables attendus

1. Mur cassable validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.08 — Cheveux et fourrure](../CH08_08_HAIR_FUR/README.md)
