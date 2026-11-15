# CH18.21 — IA pour le storyboard

**Phase :** 18 — Grease Pencil (module G : IA)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

L'IA peut proposer des références, des découpages, des variantes ou des scripts ; elle ne garantit ni la continuité, ni les droits, ni l'intention. Ce chapitre traite une liste de plans « proposée par une IA » qui contient quatre erreurs typiques (code en double, axe franchi, durée nulle, total faux), la corrige, lit puis exécute un script de préparation des plans écrit avec une IA (caméras, focales mesurées, marqueurs, boards), et documente chaque décision dans un journal d'usage. Aucun outil d'IA n'est installé ni requis.

## Prérequis

- CH18.11, CH18.14, CH18.20.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Situer l'apport et les risques de l'IA à chaque étape du storyboard.
2. Contrôler une proposition générée avec des règles vérifiables.
3. Lire, tester et utiliser un script écrit avec une IA.
4. Tenir un journal d'usage (outil, accepté, refusé, corrigé, droits).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.21.a | Storyboard assisté contrôlé | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Ce que l'IA peut apporter, et ses risques | 1 h |
| L2 | Contrôler une proposition et un script | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_21_assist_starter.blend` | Décor, proposition erronée, journal vide, script embarqué |
| `COMPLETED_EXAMPLES/ch18_21_assist_solution.blend` | Liste corrigée, plans générés, journal |
| `COMPLETED_EXAMPLES/ch18_21_assist_contact.png` | Les 6 plans générés |
| `SCRIPTS/shot_prep.py` | Préparation des plans (écrit avec une IA, testé) |
| `SCRIPTS/validate_ch18_21.py` | Correcteur (assist) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_21_assist_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_21.py" --python-exit-code 1 -- --exercise assist --render
```

## Livrables attendus

1. Storyboard assisté validé.
2. Journal AI_LOG.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH18.22 — Projets de la phase](../CH18_22_PROJECTS/README.md)
