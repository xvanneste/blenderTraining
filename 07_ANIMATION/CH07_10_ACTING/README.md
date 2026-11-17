# CH07.10 — Acting

**Phase :** 7 — Animation 3D  
**Niveau :** expert  
**Durée estimée :** 10 h  
**Version :** Blender 5.3.0

## Introduction

Animer, ce n'est pas bouger un personnage : c'est lui donner une intention. Une pensée se lit dans le temps : une remarque est rapide, la réflexion qui suit est un MAINTIEN, la décision est précédée d'une ANTICIPATION, et le corps réagit en cascade (la tête d'abord, puis le buste, puis les hanches). Ce chapitre construit un plan d'acting muet de 72 images : le personnage remarque quelque chose sur sa gauche, y réfléchit, se prépare à agir. Le correcteur mesure le lacet de la tête, du buste et des hanches et l'inclinaison de la colonne.

## Prérequis

- CH07.05 (timing), CH07.06 (overlap), CH07.07 (posing).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une scène en temps : idle, remarque, maintien, anticipation, action.
2. Faire mener la tête et suivre le corps.
3. Maintenir pour laisser lire une pensée.
4. Préparer une action par une anticipation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.10.a | Plan d'acting muet | Exercice 2 (correcteur) + courbes de la scène |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | L'intention et le temps | 5 h |
| L2 | Construire la scène | 5 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_10_acting_starter.blend` | Mannequin FK immobile, sans animation |
| `COMPLETED_EXAMPLES/ch07_10_acting_solution.blend` | Scène muette de 72 images : idle, remarque, maintien, anticipation, action |
| `COMPLETED_EXAMPLES/ch07_10_acting_reference.png` | Lacet de la tête (orange), du buste (vert), des hanches (bleu) et inclinaison de la colonne (blanc) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (pas de maintien, pas de retard, pas d'anticipation, pas d'idle, remarque trop lente, tour de tête trop petit) |
| `SCRIPTS/validate_ch07_10.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_10_acting_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_10.py" -- --exercise acting
```

## Livrables attendus

1. Plan d'acting validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.11 — Animation faciale et lip sync](../CH07_11_FACIAL/README.md)
