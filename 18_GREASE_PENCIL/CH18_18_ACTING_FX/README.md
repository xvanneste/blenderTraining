# CH18.18 — Personnages, expressions, effets, caméra

**Phase :** 18 — Grease Pencil (module E : animation 2D)  
**Niveau :** intermédiaire → avancé  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Un plan animé complet de 5 secondes : un personnage qui pense, anticipe, sursaute (écrasé, étiré), reste figé de surprise puis se détend ; un effet dessiné (éclair puis fumée qui disparaît) sur son propre calque ; une caméra 2D qui tremble à l'impact et revient exactement en place. Le correcteur vérifie tenues, réaction après l'effet, déformation, vie de l'effet et tremblement synchronisé.

## Prérequis

- CH18.16 et CH18.17.
- CH18.04 (expressions dessinées).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une réaction : anticipation, take, tenue, retour.
2. Dessiner des expressions lisibles et diriger le regard.
3. Animer un effet 2D qui naît, évolue et disparaît.
4. Animer une caméra 2D (tremblement synchronisé).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.18.a | Plan animé de 5 s | Exercice 2 ou 3 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Acting et expressions | 2 h |
| L2 | Effets et caméra 2D | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_18_shot_starter.blend` | Décor, calques vides, scénario |
| `COMPLETED_EXAMPLES/ch18_18_shot_solution.blend` | Plan « L'ampoule » animé |
| `COMPLETED_EXAMPLES/ch18_18_shot_contact.png` | 8 images clés du plan |
| `SCRIPTS/validate_ch18_18.py` | Correcteur (shot) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_18_shot_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_18.py" --python-exit-code 1 -- --exercise shot --render
```

## Livrables attendus

1. Plan de 5 s validé.
2. Planche d'expressions.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Plan validé par le correcteur.

➡️ Chapitre suivant : [CH18.19 — Dessiner dans et sur la 3D](../CH18_19_DRAW_ON_3D/README.md)
