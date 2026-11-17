# CH07.12 — Animation de caméra

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Une caméra est un personnage : elle a une intention (suivre, révéler, rapprocher), un timing (elle démarre et s'arrête en douceur) et parfois une humeur (la caméra à l'épaule). Ce chapitre anime une caméra sur un plan de 72 images : un TRAVELLING avant en Bezier, un SUIVI du sujet par une contrainte Track To, un léger TREMBLÉ par modificateur Noise sur X et Z, et un horizon toujours horizontal. Le correcteur lit la caméra évaluée : trajet, vitesse aux extrémités, écart de visée, tremblé, roulis.

## Prérequis

- CH07.02 (clés), CH07.04 (Graph Editor, Noise), CH06.02 (contraintes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Animer un travelling avec départ et arrivée doux.
2. Faire suivre un sujet par une contrainte.
3. Ajouter un tremblé maîtrisé.
4. Garder l'horizon horizontal.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.12.a | Mouvement de caméra motivé | Exercice 2 (correcteur) + trajectoire de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Travelling et suivi | 4 h |
| L2 | Caméra à l'épaule et horizon | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_12_camera_starter.blend` | Sujet animé (X de −1 à +1), caméra fixe à (0, −8, 1,6), sans contrainte ni animation |
| `COMPLETED_EXAMPLES/ch07_12_camera_solution.blend` | Travelling Y −8 → −4 (Bezier), Track To vers le sujet, Noise sur X et Z, horizon horizontal |
| `COMPLETED_EXAMPLES/ch07_12_camera_reference.png` | Vue de dessus (trajectoire, rayons vers le sujet) et courbes de position X (bleu) et Z (blanc) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans suivi, travelling linéaire, tremblé trop fort, sans tremblé, horizon penché, travelling trop court) |
| `SCRIPTS/validate_ch07_12.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_12_camera_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_12.py" -- --exercise camera
```

## Livrables attendus

1. Plan de caméra validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.13 — Animation non linéaire](../CH07_13_NLA/README.md)
