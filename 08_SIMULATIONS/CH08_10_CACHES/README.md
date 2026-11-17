# CH08.10 — Caches et baking

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une simulation ne se calcule qu'en avançant image par image : sauter à l'image 40 ne donne rien de fiable tant qu'on n'a pas joué les 39 précédentes. Le cache (point cache) mémorise les résultats ; le baking (cuisson) le remplit de l'image 1 à la dernière et l'écrit, au choix, en mémoire ou sur disque (Disk Cache). Ce chapitre cuit une simulation de 100 particules sur 60 images et vérifie qu'on peut ensuite la relire dans n'importe quel ordre, à l'identique. Pièges mesurés : le fichier doit être enregistré avant de cuire ; le cache disque est lié au NOM du .blend ; la plage cuite d'un système de particules suit la plage de la scène.

## Prérequis

- CH08.04 (particules), CH08.01 (monde de corps rigides).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Cuire un cache de particules sur disque.
2. Expliquer pourquoi le fichier doit être enregistré avant.
3. Vérifier un cache : fichiers, relecture aléatoire.
4. Éviter un cache perdu ou périmé.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.10.a | Pipeline de cache | Exercice 2 (correcteur) + courbe de relecture |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Cache mémoire, cache disque, bake | 3 h |
| L2 | Vérifier et gérer les caches | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_10_caches_starter.blend` | L'émetteur de 100 particules, rien de cuit |
| `COMPLETED_EXAMPLES/ch08_10_caches_solution.blend` | Cache cuit sur disque (61 fichiers .bphys dans `blendcache_ch08_10_caches_solution`), relecture identique en sautant d'une image à l'autre |
| `COMPLETED_EXAMPLES/ch08_10_caches_reference.png` | Hauteur moyenne des particules par image : lecture directe (orange) et relecture inverse depuis le cache (bleu) : superposées (écart 0) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (non cuit, cuit sur trop peu d'images, cuit en mémoire seulement, réglage changé après la cuisson) |
| `SCRIPTS/validate_ch08_10.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_10_caches_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_10.py" -- --exercise caches
```

## Livrables attendus

1. Cache cuit validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet de phase 8 — Séquence d'action](../PROJECT_P8/README.md)
