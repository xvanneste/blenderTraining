# CH04.07 — Baking

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Le baking transfère de l'information calculée dans une image : ici le relief d'un rocher de 20 480 faces (HIGH_Rock) est « cuit » dans une normal map appliquée à un rocher de 320 faces (LOW_Rock). Le moteur temps réel et les jeux utilisent cette méthode, et les films l'utilisent pour alléger des assets. La solution a été produite avec l'opérateur réel `object.bake` (Cycles, Selected to Active). Le correcteur analyse les pixels baké (couverture du relief, validité des normales), l'espace colorimétrique, le branchement Normal Map et l'intégrité des maillages.

## Prérequis

- CH04.01–02 (UV)
- CH04.04 (nœuds).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer le rôle d'une normal map et ce que « bake » signifie.
2. Régler un bake Selected to Active (Cycles).
3. Brancher correctement l'image : Non-Color, Normal Map (Tangent), Normal.
4. Vérifier un bake par mesure des pixels.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.07.a | Baker une normal map haute → basse définition | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Comprendre le baking | 2 h |
| L2 | Baker et brancher une normal map | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_07_baking_starter.blend` | HIGH + LOW, image plate branchée, rien de baké |
| `COMPLETED_EXAMPLES/ch04_07_baking_solution.blend` | Normal map bakée (Cycles) |
| `COMPLETED_EXAMPLES/ch04_07_baking_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (non baké, sRGB, sans Normal Map, bake partiel, Normal Map sur Base Color) |
| `SCRIPTS/validate_ch04_07.py` | Correcteur (baking) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_07_baking_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_07.py" -- --exercise baking --render
```

## Livrables attendus

1. Rocher baké validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.08 — Relief et displacement](../CH04_08_RELIEF/README.md)
