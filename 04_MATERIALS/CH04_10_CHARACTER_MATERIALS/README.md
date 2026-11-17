# CH04.10 — Matériaux de personnages

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Peau, yeux, cheveux et tissus sont les matériaux qui font ou défont un personnage. Ce chapitre les construit sur quatre sphères d'essai : peau avec sous-surface et pores, œil avec iris et cornée humide, cheveux avec le Principled Hair BSDF, tissu avec Sheen et trame. Le correcteur vérifie les valeurs qui font la crédibilité de chacun : rayon de sous-surface rouge > vert > bleu, vernis net sur l'œil, nœud de cheveux dédié, liseré de tissu.

## Prérequis

- CH04.03–05 (Principled, nœuds, textures)
- CH04.08 recommandé (bump).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler une peau avec sous-surface et micro-relief.
2. Construire un œil (sclère, iris, cornée).
3. Utiliser le Principled Hair BSDF.
4. Rendre un tissu avec Sheen et une trame.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.10.a | Peau, yeux, cheveux et tissus crédibles | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Peau et yeux | 2 h 30 |
| L2 | Cheveux et tissus | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_10_character_starter.blend` | Quatre sphères, matériaux par défaut |
| `COMPLETED_EXAMPLES/ch04_10_character_solution.blend` | Peau, œil, cheveux, tissu (Cycles) |
| `COMPLETED_EXAMPLES/ch04_10_character_reference.png` | Deux vues Cycles |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (peau opaque, rayon uniforme, œil sec, cheveux en Principled, tissu sans Sheen) |
| `SCRIPTS/validate_ch04_10.py` | Correcteur (character) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_10_character_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_10.py" -- --exercise character --render
```

## Livrables attendus

1. Quatre matériaux de personnage validés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.11 — Gestion des couleurs](../CH04_11_COLOR_MANAGEMENT/README.md)
