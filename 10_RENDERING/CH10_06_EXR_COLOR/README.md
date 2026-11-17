# CH10.06 — EXR et couleur

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

OpenEXR est le format de l'image de rendu « scientifique » : valeurs linéaires sans limite à 1,0 (un soleil vaut 1000, pas 1), plusieurs couches dans un fichier, flottants de 16 ou 32 bits, plusieurs codecs de compression. Un mauvais réglage ne se voit pas à l'œil : il déforme les valeurs. Le correcteur écrit réellement des fichiers EXR avec vos réglages et relit la valeur d'un pixel de 1000,7 : 32 bits sans perte la restitue, 16 bits la déforme de 0,2, et le codec DWAA de plus de 0,8.

## Prérequis

- CH10.04 (passes, multicouche), CH09.06 (exposition).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir entre EXR 16 et 32 bits.
2. Choisir un codec sans perte pour les données.
3. Produire un EXR multicouche avec une passe Z.
4. Mesurer la fidélité d'un fichier écrit.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.06.a | Sortie EXR correcte | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Bits et codecs | 3 h |
| L2 | Mesurer un EXR | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_06_exr_starter.blend` | EXR monocouche, 16 bits, codec DWAA, sans passe Z : valeur relue 1001,5 au lieu de 1000,7 ; 5/32 |
| `COMPLETED_EXAMPLES/ch10_06_exr_solution.blend` | EXR multicouche, 32 bits, ZIP, passe Z : valeur relue 1000,700 ; 32/32 |
| `COMPLETED_EXAMPLES/ch10_06_exr_reference.png` | Erreur mesurée sur la valeur 1000,7 pour cinq réglages (de haut en bas : 32 bits ZIP, 32 bits PIZ, 32 bits PXR24 (0,003), 16 bits ZIP (0,2), 32 bits DWAA (0,8)) ; vert = acceptée (≤ 0,05) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (16 bits, codec avec perte, monocouche, sans passe Z) |
| `SCRIPTS/validate_ch10_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_06_exr_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_06.py" -- --exercise exr
```

## Livrables attendus

1. EXR master avec ses réglages justifiés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.07 — Rendu distribué](../CH10_07_BATCH/README.md)
