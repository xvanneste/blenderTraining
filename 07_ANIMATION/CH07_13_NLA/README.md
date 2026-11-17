# CH07.13 — Animation non linéaire

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

L'éditeur NLA (Non-Linear Animation) monte les actions comme des clips : on les place sur des pistes, on les décale, on les répète, on les fond l'une dans l'autre. C'est le moyen de réutiliser des cycles (marche, saut) sans toucher aux clés. Ce chapitre monte deux actions sur une caisse : un glissement répété deux fois et une rotation qui entre en fondu. Le correcteur lit les pistes, les strips (action, début, fin, répétition, fondu) et l'animation évaluée.

## Prérequis

- CH07.03 (actions et slots), CH07.08 (cycle de marche).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Pousser une action dans une piste NLA.
2. Répéter un strip.
3. Décaler un strip et le fondre en entrée.
4. Savoir qu'une action active passe par-dessus le NLA.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.13.a | Réutiliser des actions | Exercice 2 (correcteur) + éditeur NLA de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Pistes et strips | 4 h |
| L2 | Fondu, décalage, action active | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_13_nla_starter.blend` | Caisse avec l'action Slide active, l'action Spin gardée (utilisateur fictif), aucun montage NLA |
| `COMPLETED_EXAMPLES/ch07_13_nla_solution.blend` | Montage NLA : piste Move (Slide répété ×2) et piste Spin (strip de 13 à 37, fondu d'entrée de 6 images) |
| `COMPLETED_EXAMPLES/ch07_13_nla_reference.png` | Éditeur NLA en numpy : piste Move (strip de 1 à 49 avec séparateur à l'image 25) et piste Spin (strip de 13 à 37, rampe de fondu) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans répétition, Spin trop tôt, sans fondu, action active, sans piste Spin, mauvaise échelle) |
| `SCRIPTS/validate_ch07_13.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_13_nla_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_13.py" -- --exercise nla
```

## Livrables attendus

1. Montage NLA validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.14 — Motion capture](../CH07_14_MOCAP/README.md)
