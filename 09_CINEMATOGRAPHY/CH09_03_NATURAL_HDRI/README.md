# CH09.03 — Naturel et HDRI

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Pour un extérieur crédible, on n'éclaire pas avec une lampe de studio : on utilise le monde. Une image d'environnement HDRI (High Dynamic Range Image) enregistre toute la lumière autour d'un point : un ciel bleu doux ET un soleil mille fois plus lumineux. C'est cette énorme différence de valeurs qui crée une ombre nette sous un ciel qui remplit l'ombre de bleu. Ce chapitre utilise une HDRI générée par script (un coucher de soleil simplifié : ce n'est pas une photo) : vous orientez l'environnement pour que le soleil vienne du bon côté, vous réglez l'exposition, et le correcteur lit l'ombre d'un poteau sur un rendu vu du dessus.

## Prérequis

- CH09.01 (mesure par rendu), CH04 (nœuds de matériaux).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire un monde à Environment Texture et Mapping.
2. Orienter un HDRI par la rotation Z.
3. Régler l'exposition par Strength.
4. Expliquer pourquoi une image 8 bits ne donne pas d'ombre nette.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.03.a | Extérieur crédible | Exercice 2 (correcteur) + vue du dessus |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | HDRI et monde | 3 h |
| L2 | Orientation et exposition | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_03_natural_hdri_starter.blend` | Le monde est déjà relié à la HDRI (rotation 0°, Strength 0,3) : soleil du mauvais côté, image sombre |
| `COMPLETED_EXAMPLES/ch09_03_natural_hdri_solution.blend` | Mapping Rotation Z 180°, Strength 1 : l'ombre part vers +X, sol à 0,59 |
| `COMPLETED_EXAMPLES/ch09_03_natural_hdri_reference.png` | Vue du dessus : solution (ombre vers la droite) et rotation de 90° (ombre vers le haut) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (mauvaise rotation, trop sombre, trop clair, sans HDRI, image 8 bits) |
| `SCRIPTS/validate_ch09_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_03_natural_hdri_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_03.py" -- --exercise hdri
```

## Livrables attendus

1. Éclairage HDRI validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.04 — Dramatique et stylisé](../CH09_04_DRAMATIC/README.md)
