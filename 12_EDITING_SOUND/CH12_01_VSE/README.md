# CH12.01 — Video Sequencer

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le Video Sequencer (VSE) est le monteur vidéo de Blender : des strips (bandes) posés sur des canaux le long d'une ligne de temps. Un strip a un début, une durée et un canal ; plusieurs canaux se superposent, et sur un même canal les strips se suivent. Monter, c'est choisir l'ordre, couper, raccourcir et enchaîner sans trou. Ce chapitre fait monter bout à bout quatre strips de couleur ; le correcteur lit les débuts, les durées, les canaux et rend le séquenceur à quatre images pour vérifier que la bonne couleur s'affiche au bon moment.

## Prérequis

- CH01 (timeline, rendu).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire un strip : début, durée, canal.
2. Raccourcir et déplacer des strips pour un montage sans trou.
3. Distinguer plage de la scène et durée du montage.
4. Contrôler un montage par un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.01.a | Monter dans le VSE | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Strips et canaux | 3 h |
| L2 | Monter bout à bout | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_01_vse_starter.blend` | Quatre strips aux mauvaises durées (24, 41, 25, 30) avec des trous, plage 1–139 ; 15/45 |
| `COMPLETED_EXAMPLES/ch12_01_vse_solution.blend` | A_red 1–24, B_green 25–54, C_blue 55–72, D_yellow 73–96 sur le canal 1, plage 1–96 ; rouge, vert, bleu, jaune aux images 12, 40, 63, 85 ; 45/45 |
| `COMPLETED_EXAMPLES/ch12_01_vse_reference.png` | Les quatre images contrôlées du montage (12, 40, 63, 85) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (trou, mauvaises durées, mauvais ordre, mauvais canal, plage non réduite) |
| `SCRIPTS/validate_ch12_01.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_01_vse_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_01.py" -- --exercise vse
```

## Livrables attendus

1. Montage commenté (liste des strips).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH12.02 — Montage narratif](../CH12_02_EDITING/README.md)
