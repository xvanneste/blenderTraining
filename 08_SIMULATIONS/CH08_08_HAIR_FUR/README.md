# CH08.08 — Cheveux et fourrure

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Les cheveux et la fourrure sont des milliers de brins : on en simule quelques centaines (les parents) et on en déduit des milliers d'autres (les enfants) qui les suivent. Ce chapitre utilise le système de particules de type Hair, qui existe toujours dans Blender 5.3 : racines sur un groupe de sommets, longueur, enfants interpolés, mèches (Clumping) et Hair Dynamics (pesanteur et rigidité). Une précision d'honnêteté : Blender 5.3 propose aussi le nouvel objet Curves (opérateurs `object.curves_empty_hair_add`, `curves.convert_from_particle_system`) et des outils de nœuds pour les cheveux ; nous n'avons pas testé ces outils ici : le correcteur mesure les particules Hair.

## Prérequis

- CH08.04 (particules), CH08.03 (tissu : la dynamique de cheveux réutilise le moteur de tissu).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un système de cheveux sur une zone choisie.
2. Régler longueur, enfants et mèches.
3. Activer la dynamique et vérifier que les cheveux retombent.
4. Mesurer des cheveux sans les rendre.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.08.a | Coiffure par particules | Exercice 2 (correcteur) + vue de face aux images 1 et 30 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Parents, enfants et mèches | 4 h |
| L2 | Dynamique et mesure | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_08_hair_starter.blend` | La tête (sphère de 1 m) et son groupe de sommets « scalp » ; aucun système de particules |
| `COMPLETED_EXAMPLES/ch08_08_hair_solution.blend` | Hair 300 × 0,5 m, densité « scalp », enfants interpolés ×10, Clumping 0,5, Hair Dynamics |
| `COMPLETED_EXAMPLES/ch08_08_hair_reference.png` | Les 300 cheveux parents vus de face : image 1 (dressés) et image 30 (retombés) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans groupe, sans enfants, sans mèches, sans dynamique, trop courts, trop peu nombreux) |
| `SCRIPTS/validate_ch08_08.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_08_hair_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_08.py" -- --exercise hair
```

## Livrables attendus

1. Chevelure validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.09 — Forces](../CH08_09_FORCES/README.md)
