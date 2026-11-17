# CH03.03 — Résolution dynamique

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

Adapter la densité du maillage à l'étape du sculpt : Voxel Remesh pour fusionner des masses en un volume régulier, DynTopo pour ajouter du détail là où l'on sculpte, Multiresolution pour détailler en gardant une base légère. On découvre pourquoi le mannequin du CH03.01 donne trois morceaux au remesh (masses qui ne se chevauchent pas) et comment le réparer. Le correcteur compte les morceaux, les arêtes non fermées, les quads, la densité, les niveaux Multires et vérifie vos choix de méthode.

## Prérequis

- CH03.01 et CH03.02.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Fusionner des masses par Voxel Remesh (chevauchements, taille de voxel).
2. Utiliser DynTopo en connaissant ce qu'il détruit.
3. Régler un Multiresolution fluide sur une base légère.
4. Choisir la méthode adaptée à chaque situation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.03.a | Choisir la bonne méthode | Exercices 1–3 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Voxel Remesh | 1 h |
| L2 | DynTopo et Multiresolution | 1 h 30 |
| L3 | Choisir | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_03_remesh_starter.blend` | 16 masses séparées (CH03.01) |
| `COMPLETED_EXAMPLES/ch03_03_remesh_solution.blend` | SCULPT_Body remeshé, un seul volume |
| `COMPLETED_EXAMPLES/ch03_03_remesh_reference.png` | Rendu de contrôle |
| `STARTER_FILES/ch03_03_multires_starter.blend` | Tête de base 384 faces + DECISIONS |
| `COMPLETED_EXAMPLES/ch03_03_multires_solution.blend` | Multires 5 niveaux + réponses |
| `SCRIPTS/validate_ch03_03.py` | Correcteur (remesh, multires, decide) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_03_remesh_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_03.py" -- --exercise remesh --render
```

## Livrables attendus

1. Remesh validé.
2. Multires validé.
3. Décisions validées.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Les trois exercices validés.

➡️ Chapitre suivant : [CH03.04 — Sculpture stylisée](../CH03_04_STYLIZED/README.md)
