# CH02.11 — UV fondamentaux

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 15  
**Version :** Blender 5.3.0

## Introduction

Pour poser une texture image sur un objet 3D, il faut le déplier comme un patron de couture : ce sont les UV. Ce chapitre explique coutures et îles, les méthodes de dépliage de Blender 5.3, le contrôle par damier et la densité de texels, sur une caisse et une boîte de conserve — avec un correcteur qui mesure chevauchements et étirements.

## Prérequis

- CH02.01 à CH02.03.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Expliquer espace UV, coutures, îles et étirement.
2. Placer des coutures et déplier (Unwrap, Smart UV Project).
3. Ranger les îles (Pack Islands) et harmoniser la densité.
4. Contrôler un dépliage avec un damier.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.11.a | Déplier un objet simple | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | UV, coutures, îles | 45 min |
| L2 | Méthodes de dépliage | 1 h |
| L3 | Contrôler la qualité | 30 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_11_uv_starter.blend` | Caisse et boîte sans UV, matériau damier |
| `COMPLETED_EXAMPLES/ch02_11_uv_solution.blend` | Caisse (Smart UV) et boîte (coutures + Unwrap) |
| `COMPLETED_EXAMPLES/ch02_11_uv_starter_view.png` | Rendu sans UV |
| `COMPLETED_EXAMPLES/ch02_11_uv_reference.png` | Rendu avec UV |
| `SCRIPTS/validate_ch02_11.py` | Correcteur (bornes, occupation, chevauchement, étirement, coutures) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_11_uv_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_11.py" --python-exit-code 1 -- --exercise uv --render
```

## Livrables attendus

1. Dépliages validés.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : déplier trois props.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Dépliages validés.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.12 — Modélisation pour l'animation](../CH02_12_ANIMATION_READY/README.md)
