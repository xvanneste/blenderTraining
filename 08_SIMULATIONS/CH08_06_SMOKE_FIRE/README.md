# CH08.06 — Fumée et feu

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

La fumée et le feu sont des simulations de GAZ : un domaine (boîte) contient une grille de densité, de température et de combustible ; un foyer (Flow) l'alimente en continu ; la flamme monte par flottabilité. On les affiche avec un SHADER DE VOLUME (Principled Volume) qui lit la densité et la flamme dans les attributs du domaine. Ce chapitre construit un foyer de 0,4 m au fond d'une boîte de 3 m : domaine Gas, source Fire + Smoke en Inflow, matériau de volume. Le correcteur cuit les données en arrière-plan (dossier temporaire) et mesure la taille du cache image par image : la grille doit grossir quand le foyer produit du gaz.

## Prérequis

- CH08.05 (domaine, Flow, cache), CH04 (nœuds de matériaux).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un domaine de gaz et un foyer.
2. Choisir Smoke, Fire ou Fire + Smoke et un comportement Inflow.
3. Habiller le domaine d'un shader de volume.
4. Vérifier une simulation par la taille de son cache.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.06.a | Feu et fumée | Exercice 2 (correcteur) + courbe des tailles de cache |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Domaine de gaz et foyer | 4 h |
| L2 | Shader de volume et mesure | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_06_smoke_starter.blend` | Domaine (2 × 2 × 3 m) et foyer comme simples maillages, sans physique ni matériau |
| `COMPLETED_EXAMPLES/ch08_06_smoke_solution.blend` | Domaine Gas (32, cache 1–30), foyer Fire + Smoke en Inflow, matériau Principled Volume |
| `COMPLETED_EXAMPLES/ch08_06_smoke_reference.png` | Taille du cache par image : solution (orange, croissante) et domaine sans foyer (bleu, constant) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans foyer, fumée seule, résolution trop basse, cache trop court, sans shader de volume) |
| `SCRIPTS/validate_ch08_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_06_smoke_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_06.py" -- --exercise smoke
```

## Livrables attendus

1. Feu et fumée validés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.07 — Destruction](../CH08_07_DESTRUCTION/README.md)
