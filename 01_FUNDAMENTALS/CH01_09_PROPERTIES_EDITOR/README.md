# CH01.09 — Éditeur de propriétés

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Presque tous les réglages de Blender vivent dans l'éditeur Properties : moteur de rendu, résolution, cadence, caméra active, couleur du monde, affichage d'un objet, focale d'une caméra, puissance d'une lumière, matériaux… Ce chapitre vous donne la carte de ses onglets, du plus général (la scène) au plus particulier (le matériau), les gestes de saisie efficaces, la ligne de datablock (utilisateurs, bouclier) et les propriétés personnalisées qui serviront plus tard aux scripts de pipeline. Exercice : une chasse aux propriétés en 11 consignes vérifiées automatiquement.

## Prérequis

- CH01.04 (datablocks).
- CH01.08 (visibilités).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Retrouver un réglage dans le bon onglet (scène, objet, données, matériau).
2. Saisir et réinitialiser des valeurs efficacement (glisser, Ctrl, Shift, Backspace, RMB).
3. Utiliser la ligne de datablock : utilisateurs, Fake User, épingle.
4. Créer des propriétés personnalisées.
5. Configurer résolution, cadence, plage d'images et unités d'un plan.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.09.a | Retrouver et régler un paramètre | Exercice 3 (correcteur), tests chronométrés |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les onglets et leur logique | 25 min |
| L2 | Manipuler les champs et les datablocks | 20 min |
| L3 | Propriétés personnalisées et réglages de plan | 25 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_09_hunt_starter.blend` | Scène de plan aux réglages par défaut |
| `COMPLETED_EXAMPLES/ch01_09_hunt_solution.blend` | Les 11 consignes réalisées |
| `SCRIPTS/validate_ch01_09.py` | Correcteur (13 points) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_09_hunt_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_09.py" -- --exercise hunt
```

## Livrables attendus

1. ch01_09_hunt_<prenom>_v001.blend validé.
2. Mini-projet : gabarit de plan dans TEMPLATES/.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.10 — Modificateurs essentiels](../CH01_10_MODIFIERS/README.md)
