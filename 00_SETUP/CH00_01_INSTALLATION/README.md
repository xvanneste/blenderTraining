# CH00.01 — Installer, lancer et vérifier Blender

**Phase :** 0 — Préparation et installation
**Niveau :** débutant absolu
**Durée estimée :** 2 h à 2 h 30 (théorie 40 min · pratique 70 min · évaluation 20 min)
**Version :** Blender 5.3.0 (testé le 14/11/2026 sous Windows 11, i9-10900, RTX 3080, 64 Go)

## Introduction
Avant de modéliser un seul cube, un studio s'assure d'une chose : **tout le monde travaille
sur la même version de Blender, configurée de la même manière, sur une machine dont on
connaît les performances**. Un rendu qui sort noir, un fichier qui ne s'ouvre plus, une
carte graphique ignorée… ces problèmes coûtent des jours en production et viennent presque
toujours d'une installation mal comprise.

Dans ce chapitre, vous allez découvrir d'où vient Blender, l'installer proprement, faire
cohabiter plusieurs versions, le lancer en ligne de commande, vérifier que votre carte
graphique est bien utilisée et générer le **rapport système** de votre poste. Vous
terminerez par un exercice de « dépannage » sur une scène volontairement cassée — votre
premier réflexe de technicien.

## Prérequis
- Savoir utiliser l'explorateur de fichiers Windows (copier, décompresser un zip, créer un dossier).
- Avoir des droits administrateur **ou** savoir utiliser une version zip (expliqué dans le cours).
- Aucune connaissance de Blender n'est nécessaire.

## Objectifs pédagogiques
À la fin du chapitre, vous saurez :
1. Expliquer ce qu'est Blender, sa licence et son cycle de versions (stable, LTS, daily).
2. Choisir entre installeur, zip, version portable, Microsoft Store et Steam.
3. Faire cohabiter plusieurs versions sans conflit et savoir où sont leurs préférences.
4. Lancer Blender en ligne de commande (mode arrière-plan, réglages d'usine, script Python).
5. Vérifier que Cycles voit votre GPU (CUDA / OptiX / HIP / oneAPI) et mesurer le gain de vitesse.
6. Diagnostiquer les 5 causes les plus courantes d'un rendu noir ou vide.

## Compétences évaluées
| Code | Compétence | Validé par |
|---|---|---|
| C00.01.a | Installer Blender et identifier précisément sa version | Exercice 1, quiz Q1–Q5 |
| C00.01.b | Choisir le bon mode d'installation selon le contexte | Quiz Q6–Q9, défi 1 |
| C00.01.c | Vérifier et activer le GPU pour Cycles | Exercice 2, benchmark |
| C00.01.d | Lancer Blender et un script en ligne de commande | Exercice 2, mini-projet |
| C00.01.e | Diagnostiquer un rendu noir ou vide | Exercice 3 (sans tutoriel) |

## Plan du chapitre
| Leçon | Titre | Durée |
|---|---|---|
| L1 | L'écosystème Blender | 20 min |
| L2 | Les méthodes d'installation sous Windows | 25 min |
| L3 | Plusieurs versions côte à côte, préférences et dossiers | 20 min |
| L4 | Premier lancement, ligne de commande, GPU et benchmark | 35 min |
| L5 | Rapport système et diagnostic | 20 min |
| — | Exercices, mini-projet, quiz | 40 min |

## Contenu du dossier
| Fichier / dossier | Rôle |
|---|---|
| [LESSON.md](LESSON.md) | Les 5 leçons au format A→I |
| [THEORY.md](THEORY.md) | Cours théorique détaillé |
| [TUTORIAL.md](TUTORIAL.md) | Pas à pas guidés |
| [EXERCISES.md](EXERCISES.md) | Exercices facile / moyen / difficile, défis, mini-projet, tests chronométrés |
| [QUIZ.md](QUIZ.md) | 20 questions |
| [SOLUTIONS.md](SOLUTIONS.md) | Corrigés |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Erreurs fréquentes et solutions |
| [RESOURCES.md](RESOURCES.md) | Sources officielles et licences |
| `STARTER_FILES/ch00_01_testcard_starter.blend` | Mire de test (réglages par défaut) |
| `STARTER_FILES/ch00_01_broken_render_starter.blend` | Mire avec 5 pannes cachées |
| `COMPLETED_EXAMPLES/ch00_01_testcard_solution.blend` | Mire réglée Cycles + GPU |
| `COMPLETED_EXAMPLES/ch00_01_broken_render_solution.blend` | Mire réparée |
| `COMPLETED_EXAMPLES/ch00_01_testcard_reference_render.png` | Rendu de référence |
| `COMPLETED_EXAMPLES/system_report_reference/` | Rapport système de référence (poste de l'auteur) |
| `COMPLETED_EXAMPLES/benchmark_reference/` | Benchmark de référence CPU/CUDA/OptiX |
| `SCRIPTS/bcma_system_report.py` | Génère votre rapport système |
| `SCRIPTS/bcma_render_benchmark.py` | Mesure CPU vs GPU |
| `SCRIPTS/validate_ch00_01.py` | Correcteur automatique des exercices |
| `SCRIPTS/build_ch00_01_files.py` | Régénère tous les .blend du chapitre |
| `ASSETS/` | Fiche de poste à remplir (`workstation_sheet_template.md`) |

## Livrables attendus
1. `ch00_01_testcard_<prenom>_v001.blend` validé par le correcteur (exercices 1–2).
2. `ch00_01_broken_render_<prenom>_v001.blend` réparé et validé (exercice 3).
3. Votre rapport système (`system_report_<date>.md`) et votre benchmark (`benchmark_<date>.md`).
4. Votre fiche de poste remplie (mini-projet).

## Critères pour passer au chapitre suivant
- Quiz ≥ 16/20.
- Exercice 3 validé par le correcteur **sans avoir lu la solution**.
- Rapport système généré sur **votre** machine.
