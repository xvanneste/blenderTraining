# CH05.10 — Optimisation et outils

**Phase :** 5 — Geometry Nodes  
**Niveau :** avancé  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Un arbre qui marche chez soi n'est pas encore un outil : il faut le rendre léger (géométrie instanciée minimale, instances conservées, bornes sur les paramètres coûteux), l'utiliser comme modificateur sur n'importe quel maillage, puis le publier comme asset avec ses métadonnées et son catalogue. Ce chapitre part d'un outil lourd (cône de 64 côtés, instances réalisées, densité sans borne) et le transforme en « Scatter Cones » publiable. Le correcteur mesure le budget (sommets par instance, nombre d'instances par défaut et au maximum), vérifie l'absence de Realize Instances et la publication.

## Prérequis

- CH05.03
- CH05.06
- CH02.13 (assets).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Repérer ce qui rend un arbre lourd.
2. Appliquer les règles d'optimisation : instances, géométrie minimale, bornes.
3. Configurer un arbre comme outil modificateur.
4. Publier un arbre comme asset avec description, tags et catalogue.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.10.a | Publier un node tool | Exercice 2 (correcteur) + vérification dans l'Asset Browser |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Mesurer et alléger | 2 h 30 |
| L2 | Un outil publiable | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_10_tools_starter.blend` | Outil lourd et non publié |
| `COMPLETED_EXAMPLES/ch05_10_tools_solution.blend` | Outil allégé et publié (asset) |
| `COMPLETED_EXAMPLES/blender_assets.cats.txt` | Catalogue « Tools/Scatter » |
| `COMPLETED_EXAMPLES/ch05_10_tools_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (cône lourd, instances réalisées, densité sans borne, non publié, sans catalogue, pas un modificateur, entrée ignorée) |
| `SCRIPTS/validate_ch05_10.py` | Correcteur (tools) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_10_tools_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_10.py" -- --exercise tools --render
```

## Livrables attendus

1. Outil publié validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : Projet P5 — outil de ville ou de forêt paramétrable (voir PROJECT_P5)
