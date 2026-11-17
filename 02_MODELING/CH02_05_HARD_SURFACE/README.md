# CH02.05 — Hard Surface

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 45  
**Version :** Blender 5.3.0

## Introduction

Un objet manufacturé se lit par ses arêtes et ses reflets. Ce chapitre installe le workflow hard surface non destructif : arêtes « cassées » qui accrochent la lumière, coins arrondis choisis par Bevel Weight, deux modificateurs Bevel empilés, Harden Normals, détails mécaniques et hiérarchie des formes — sur un boîtier de commande en dimensions réelles.

## Prérequis

- CH02.02 à CH02.04.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer pourquoi une arête doit être biseautée pour le rendu.
2. Poser des Bevel Weights et utiliser Limit Method Weight / Angle.
3. Empiler deux Bevels et activer Harden Normals.
4. Ajouter panneaux en creux et pièces jointes sans casser la topologie.
5. Respecter échelle réelle et hiérarchie des détails.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.05.a | Modéliser un objet mécanique | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Arêtes et lumière | 45 min |
| L2 | Bevel modificateur : Weight et Angle | 1 h |
| L3 | Détails mécaniques | 1 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_05_device_starter.blend` | Pavé 40 × 20 × 50 cm |
| `COMPLETED_EXAMPLES/ch02_05_device_solution.blend` | Boîtier complet (2 Bevels, écran, boutons) |
| `COMPLETED_EXAMPLES/ch02_05_device_reference.png` | Rendu de référence |
| `COMPLETED_EXAMPLES/ch02_05_device_closeup.png` | Gros plan sur les arêtes |
| `SCRIPTS/validate_ch02_05.py` | Correcteur (poids, modificateurs, creux, boutons, fermeture) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_05_device_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_05.py" -- --exercise device --render
```

## Livrables attendus

1. Boîtier validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : le talkie-walkie.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Boîtier validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.06 — Subdivision Surface](../CH02_06_SUBDIVISION/README.md)
