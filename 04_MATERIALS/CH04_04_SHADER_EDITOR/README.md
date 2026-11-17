# CH04.04 — Shader Editor et nœuds

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Un matériau réaliste n'est jamais une couleur unie : il varie dans l'espace. Le Shader Editor permet de construire cette variation avec des nœuds. Ce chapitre construit un acier rouillé : un bruit, passé dans une rampe de couleurs, pilote en même temps la couleur, le caractère métallique et la rugosité. Le correcteur lit le graphe de nœuds lui-même : liens, types en amont de chaque entrée, nœuds orphelins, valeurs clés.

## Prérequis

- CH04.03.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire et construire un graphe de nœuds (liens, flux de gauche à droite).
2. Utiliser Texture Coordinate, Mapping, Noise Texture, Color Ramp, Mix et Map Range.
3. Piloter plusieurs entrées du Principled BSDF avec un même masque.
4. Garder un graphe propre : pas de nœud orphelin.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.04.a | Construire un graphe de matériau | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lire un graphe de nœuds | 2 h |
| L2 | Un masque, plusieurs entrées | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_04_nodes_starter.blend` | Sphère SPH_Rust, Principled BSDF par défaut |
| `COMPLETED_EXAMPLES/ch04_04_nodes_solution.blend` | Acier rouillé par nœuds |
| `COMPLETED_EXAMPLES/ch04_04_nodes_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (orphelin, Metallic constant, sans Mapping, sortie non reliée, rampe plate, échelle excessive) |
| `SCRIPTS/validate_ch04_04.py` | Correcteur (nodes) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_04_nodes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_04.py" -- --exercise nodes --render
```

## Livrables attendus

1. Graphe de rouille validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.05 — Textures procédurales](../CH04_05_PROCEDURAL_TEXTURES/README.md)
