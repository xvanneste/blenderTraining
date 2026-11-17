# CH01.11 — Matériaux simples

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

La forme dit ce qu'est un objet ; le matériau dit de quoi il est fait. Ce chapitre présente le Principled BSDF et ses réglages essentiels (couleur, métal, rugosité, transmission, émission), les emplacements de matériaux qui permettent de colorer différemment les faces d'un même objet, les modes d'affichage pour juger le résultat, et le partage des matériaux entre objets. Exercice : mettre en couleurs une maison — murs, toit, porte, gouttière métallique et lanterne lumineuse.

## Prérequis

- CH01.05 (Edit Mode, sélection de faces).
- CH01.09 (Properties).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer, nommer et régler un matériau Principled BSDF.
2. Distinguer métal et non-métal, mat et brillant, opaque et transparent, émissif.
3. Gérer plusieurs emplacements de matériaux et assigner par face.
4. Choisir le mode d'affichage adapté (Solid, Material Preview, Rendered).
5. Maîtriser le partage des matériaux et créer des variantes.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.11.a | Créer et assigner des matériaux | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Matériau et Principled BSDF | 30 min |
| L2 | Plusieurs matériaux sur un objet | 25 min |
| L3 | Voir, partager, organiser | 15 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_11_house_colors_starter.blend` | Maison grise, gouttière et lanterne sans matériau |
| `COMPLETED_EXAMPLES/ch01_11_house_colors_solution.blend` | Maison en couleurs |
| `COMPLETED_EXAMPLES/ch01_11_house_colors_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch01_11.py` | Correcteur (affectation par face, réglages) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_11_house_colors_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_11.py" -- --exercise colors --render
```

## Livrables attendus

1. ch01_11_house_colors_<prenom>_v001.blend validé.
2. Mini-projet : le village coloré.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.12 — Caméras](../CH01_12_CAMERAS/README.md)
