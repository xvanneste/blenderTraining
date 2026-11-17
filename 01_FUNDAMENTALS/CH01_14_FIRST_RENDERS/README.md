# CH01.14 — Premiers rendus

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Tout ce que vous avez appris dans la phase 1 converge ici : produire une image finale propre. Ce chapitre compare EEVEE et Cycles, explique les réglages de qualité (seuil de bruit, échantillons, débruitage), les formats de sortie et la gestion des couleurs (AgX et ses looks, ACES, False Color), puis la façon d'enregistrer et de comparer ses rendus. Exercice : régler, rendre et enregistrer une nature morte en Full HD, vérifiée jusqu'à la présence et l'exposition du fichier image.

## Prérequis

- CH01.11 à CH01.13 (matériaux, caméra, éclairage).
- Premier rendu de CH00.01. Le GPU est facultatif.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir entre EEVEE et Cycles selon l'objectif.
2. Régler l'échantillonnage adaptatif et le débruitage de Cycles.
3. Configurer résolution, format, profondeur et chemin de sortie.
4. Choisir View Transform et Look.
5. Enregistrer, comparer (slots) et automatiser un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.14.a | Produire un rendu final propre | Exercice 3 (correcteur, image vérifiée) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | EEVEE et Cycles | 25 min |
| L2 | Qualité et bruit | 25 min |
| L3 | Sortie et couleurs | 25 min |
| L4 | Enregistrer et comparer | 15 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_14_final_render_starter.blend` | Nature morte prête, réglages par défaut |
| `COMPLETED_EXAMPLES/ch01_14_final_render_solution.blend` | Réglages de rendu final |
| `COMPLETED_EXAMPLES/renders/ch01_14_final.png` | Rendu Cycles de référence (1920×1080) |
| `COMPLETED_EXAMPLES/renders/ch01_14_eevee.png` | Même plan en EEVEE |
| `SCRIPTS/validate_ch01_14.py` | Correcteur (réglages + image produite) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_14_final_render_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_14.py" -- --exercise final
```

## Livrables attendus

1. ch01_14_final_render_<prenom>_v001.blend validé + renders/ch01_14_final.png.
2. Projet de phase P1 « Nature morte ».

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [Projet de phase P1](../PROJECT_P1/README.md), puis [Phase 18 — CH18.01](../../18_GREASE_PENCIL/README.md) et [Phase 2](../../02_MODELING/README.md)
