# CH02.13 — Assets réutilisables

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Un studio ne remodélise jamais deux fois la même chaise : il la publie dans une bibliothèque. Ce chapitre transforme vos props des chapitres précédents en assets documentés et catalogués, déclare la bibliothèque dans les préférences et explique les différences entre Link, Append et Append (Reuse Data).

## Prérequis

- CH02.02 à CH02.12 (les props réutilisés).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Marquer des objets comme assets et les documenter (description, auteur, licence, tags).
2. Organiser des catalogues et comprendre blender_assets.cats.txt.
3. Déclarer une bibliothèque dans les préférences.
4. Choisir entre Link, Append et Append (Reuse Data).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.13.a | Publier un asset | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Marquer et documenter | 45 min |
| L2 | Bibliothèques et import | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_13_library_starter.blend` | 6 props des chapitres précédents, non marqués |
| `COMPLETED_EXAMPLES/ch02_13_library_solution.blend` | Bibliothèque : 6 assets documentés |
| `COMPLETED_EXAMPLES/blender_assets.cats.txt` | Catalogues de la bibliothèque |
| `COMPLETED_EXAMPLES/ch02_13_library_reference.png` | Rendu de la bibliothèque |
| `SCRIPTS/validate_ch02_13.py` | Correcteur (marquage, catalogues, métadonnées) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "ASSETS\ch02_13_library_<prenom>.blend" `
  --python "02_MODELING\CH02_13_ASSETS\SCRIPTS\validate_ch02_13.py" --python-exit-code 1 -- --exercise library --render
```

## Livrables attendus

1. Bibliothèque validée.
2. Auto-évaluation ≥ 14/20.
3. Projet P2.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Bibliothèque validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [Projet P2 — Décor + 10 props](../README.md)
