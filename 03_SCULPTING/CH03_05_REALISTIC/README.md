# CH03.05 — Sculpture réaliste

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h pour le parcours essentiel, puis 3 h pour la variante  
**Version :** Blender 5.3.0

## Introduction

Réaliste ne veut pas dire « copier une photo » : c'est respecter des proportions mesurables, enchaîner des plans qui se raccordent en douceur, puis ajouter les détails dans le bon ordre — primaires (masses), secondaires (plis, sillons), tertiaires (grain de peau). Ce chapitre construit un buste à l'échelle 1 : blocage, Voxel Remesh, orbites creusées, globes oculaires, lissage des transitions, puis détails. Le correcteur MESURE le maillage : hauteur de tête, yeux à mi-hauteur, écart des yeux, nez, symétrie, creux des plis et grain de peau.

## Prérequis

- CH03.01 à CH03.04.
- CH03.03 (Voxel Remesh, Multires).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Poser les proportions d'une tête humaine et les vérifier par des mesures.
2. Construire des plans qui se raccordent par des transitions douces.
3. Distinguer et ordonner détails primaires, secondaires et tertiaires.
4. Choisir la densité de maillage adaptée au niveau de détail visé.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.05.a | Sculpter un buste réaliste | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Proportions, plans et transitions | 2 h |
| L2 | Du blocage aux détails fins | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Suivre les leçons avec les exercices 1 et 2 de [EXERCISES.md](EXERCISES.md). Les durées des exercices sont comprises dans celles des leçons. L'exercice 3 ajoute une variante autonome.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_05_bust_starter.blend` | Studio, 3 caméras, guide de proportions (GP_Guide) |
| `COMPLETED_EXAMPLES/ch03_05_bust_solution.blend` | Buste réaliste (SCULPT_Bust + EYE_L/EYE_R) |
| `COMPLETED_EXAMPLES/ch03_05_bust_reference.png` | Buste à ce stade, de face, de trois-quarts et de profil. CH03.06 reprend les traits du visage. |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (lisse, sans plis, sans grain, yeux trop hauts, asymétrique, trop petit) |
| `SCRIPTS/validate_ch03_05.py` | Correcteur (bust) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_05_bust_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_05.py" -- --exercise bust --render
```

## Livrables attendus

1. Buste réaliste validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH03.06 — Visages](../CH03_06_FACES/README.md)
