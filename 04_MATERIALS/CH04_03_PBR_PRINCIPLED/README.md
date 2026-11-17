# CH04.03 — PBR et Principled BSDF

**Phase :** 4 — UV, textures et matériaux  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Le rendu physiquement plausible (PBR) décrit un matériau avec quelques paramètres mesurables : couleur de base, métal ou non, rugosité, indice de réfraction, transmission, sous-surface. Ce chapitre règle quatre sphères (or poli, caoutchouc, verre, cire) avec le nœud Principled BSDF. Le correcteur contrôle la plausibilité physique de chaque matériau : un métal reste clair et métallique, un caoutchouc n'est ni blanc ni noir pur, le verre transmet, la cire diffuse davantage le rouge que le bleu, et Metallic reste proche de 0 ou de 1.

## Prérequis

- CH01.xx (interface et rendu de base).
- CH04.01 recommandé.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer diélectriques et métaux, et régler Base Color en conséquence.
2. Régler Roughness, IOR, Transmission et Subsurface.
3. Reconnaître un matériau non plausible (métal sombre, blanc pur, Metallic intermédiaire).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C04.03.a | Régler un Principled BSDF plausible | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Principes du PBR | 2 h |
| L2 | Principled BSDF : métal, verre, cire | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch04_03_pbr_starter.blend` | Quatre sphères, matériaux Principled par défaut |
| `COMPLETED_EXAMPLES/ch04_03_pbr_solution.blend` | Or, caoutchouc, verre, cire réglés |
| `COMPLETED_EXAMPLES/ch04_03_pbr_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (métal sombre, Metallic 0,5, verre opaque, cire blanche, matériau partagé) |
| `SCRIPTS/validate_ch04_03.py` | Correcteur (pbr) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch04_03_pbr_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch04_03.py" -- --exercise pbr --render
```

## Livrables attendus

1. Quatre matériaux validés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH04.04 — Shader Editor](../CH04_04_SHADER_EDITOR/README.md)
