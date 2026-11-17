# CH10.05 — Mémoire et optimisation

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une scène lourde ne se rend pas parce que sa mémoire est pleine : trop de maillages différents, trop de triangles évalués, des textures plus grandes que nécessaire. Trois leviers répondent à ces trois problèmes : partager les données (maillage unique, instances de collection), réduire la géométrie évaluée (niveau de Subdivision Surface, instances) et limiter les textures (Simplify > Texture Limit). Le correcteur n'estime pas : il compte les maillages, les triangles évalués dans le graphe de dépendances et les mégaoctets de textures effectifs d'une scène de 200 rochers.

## Prérequis

- CH02 (modificateurs), CH10.02 (Cycles).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Compter les triangles évalués d'une scène.
2. Partager un maillage ou instancier une collection.
3. Limiter la taille des textures au rendu.
4. Choisir parmi plusieurs optimisations.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.05.a | Rendre une scène lourde | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Partager et instancier | 3 h |
| L2 | Triangles et textures | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_05_memory_starter.blend` | 200 rochers avec 200 maillages différents, Subdivision Surface niveau 2 (384 000 triangles évalués), texture 4 096 × 4 096 sans limite (64 Mo) ; 10/34 |
| `COMPLETED_EXAMPLES/ch10_05_memory_solution.blend` | Instances de collection (un seul rocher évalué : 1 920 triangles, 1 maillage) et Texture Limit 1024 (4 Mo) ; 34/34. Variante acceptée : 200 objets partageant un maillage au niveau 0 (16 000 triangles) |
| `COMPLETED_EXAMPLES/ch10_05_memory_reference.png` | Les 200 rochers de la solution (EEVEE) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (maillages multipliés, triangles trop nombreux, texture trop lourde, rochers supprimés) |
| `SCRIPTS/validate_ch10_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_05_memory_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_05.py" -- --exercise memory
```

## Livrables attendus

1. Rapport avant / après (maillages, triangles, Mo).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.06 — EXR et couleur](../CH10_06_EXR_COLOR/README.md)
