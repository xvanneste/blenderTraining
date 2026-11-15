# CH18.17 — Timing, spacing, cycles

**Phase :** 18 — Grease Pencil (module E : animation 2D)  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Le même jeu de dessins change de caractère selon son exposition : ce chapitre apprend à lire et appliquer une feuille d'exposition (en un, en deux, tenues) dans la Dope Sheet, puis à construire le cycle de base de tout animateur : la marche de profil sur place, en deux, avec contacts, positions basses, passages et positions hautes. Le correcteur mesure chaque dessin (écart des jambes, rebond, appui au sol, dérive) et vérifie la boucle.

## Prérequis

- CH18.16.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire et appliquer une feuille d'exposition.
2. Re-minuter une animation sans redessiner.
3. Construire un cycle qui boucle sans saut.
4. Animer une marche 2D : contact, bas, passage, haut.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.17.a | Cycle de marche 2D | Exercices 1–2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Feuille d'exposition et re-minutage | 1 h |
| L2 | Le cycle de marche | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_17_xsheet_starter.blend` | 8 dessins en un + feuille XSHEET |
| `COMPLETED_EXAMPLES/ch18_17_xsheet_solution.blend` | Dessins re-minutés |
| `STARTER_FILES/ch18_17_walk_starter.blend` | Feuille, guides, cycle 1–24 |
| `COMPLETED_EXAMPLES/ch18_17_walk_solution.blend` | Marche en deux (12 dessins) |
| `COMPLETED_EXAMPLES/ch18_17_walk_reference.png` | Planche des 12 dessins |
| `SCRIPTS/validate_ch18_17.py` | Correcteur (xsheet, walk) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_17_walk_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_17.py" --python-exit-code 1 -- --exercise walk --render
```

## Livrables attendus

1. Feuille d'exposition appliquée.
2. Cycle de marche validé.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercices 1 et 2 validés.

➡️ Chapitre suivant : [CH18.18 — Personnages, expressions, effets, caméra](../CH18_18_ACTING_FX/README.md)
