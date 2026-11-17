# CH04.02 — Packing et UDIM

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Une texture 4K ne suffit pas pour un personnage ou un décor détaillé : la production répartit l'objet sur plusieurs tuiles UDIM (un carré UV chacune). Ce chapitre packe le coffre de CH04.01 en deux tuiles : corps et sangles en 1001, couvercle en 1002 avec plus de résolution. Le correcteur vérifie, par tuile, le chevauchement, l'occupation, l'étirement et la densité, qu'aucun îlot n'est à cheval sur deux tuiles et qu'une image UDIM possède bien toutes les tuiles utilisées.

## Prérequis

- CH04.01.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Numéroter les tuiles UDIM et placer des îlots dans la bonne tuile.
2. Packer chaque groupe dans son carré.
3. Créer et brancher une image UDIM avec les tuiles voulues.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.02.a | Packer pour la production | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Packing et marges | 2 h |
| L2 | UDIM : tuiles et images | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_02_udim_starter.blend` | UV propres mais tout dans la tuile 1001 ; matériau UDIM prêt |
| `COMPLETED_EXAMPLES/ch04_02_udim_solution.blend` | Deux tuiles : corps 1001, couvercle 1002 |
| `COMPLETED_EXAMPLES/ch04_02_udim_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/ch04_02_udim_uv_layout.png` | Deux tuiles côte à côte |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (à cheval, une seule tuile, tuile manquante, chevauchement) |
| `SCRIPTS/validate_ch04_02.py` | Correcteur (udim) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_02_udim_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_02.py" -- --exercise udim --render
```

## Livrables attendus

1. Packing UDIM validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.03 — PBR et Principled BSDF](../CH04_03_PBR_PRINCIPLED/README.md)
