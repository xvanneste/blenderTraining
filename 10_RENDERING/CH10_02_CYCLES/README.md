# CH10.02 — Cycles en profondeur

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Cycles est le moteur de rendu physique de Blender : il suit des rayons de lumière qui rebondissent dans la scène. Trois réglages gouvernent sa qualité et son coût : le nombre de rebonds (la lumière indirecte, par exemple le plafond d'une pièce éclairé par les murs), le nombre d'échantillons (moins de bruit) et l'échantillonnage adaptatif (dépenser plus d'échantillons là où l'image est bruitée). Le correcteur rend une pièce blanche deux fois avec deux graines aléatoires et mesure la lumière du plafond et le bruit.

## Prérequis

- CH09.01 (lumière), CH10.01 (EEVEE).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler les rebonds diffus pour la lumière indirecte.
2. Activer l'échantillonnage adaptatif et choisir un seuil.
3. Mesurer le bruit par deux rendus.
4. Choisir un nombre d'échantillons maximal raisonnable.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.02.a | Régler Cycles | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Rebonds et lumière indirecte | 3 h |
| L2 | Échantillons et bruit | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_02_cycles_starter.blend` | Diffuse 0 rebond (plafond noir : 0,01), échantillonnage adaptatif désactivé, 4 échantillons ; 18/36 |
| `COMPLETED_EXAMPLES/ch10_02_cycles_solution.blend` | Diffuse 4, adaptatif activé, seuil 0,02, 64 échantillons : plafond à 0,33, bruit 0,0097 ; 36/36 |
| `COMPLETED_EXAMPLES/ch10_02_cycles_reference.png` | Départ (gauche : plafond noir, piqué de lucioles) et solution (droite : plafond éclairé par les murs) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans rebonds diffus, trop peu d'échantillons, sans adaptatif, seuil trop large, trop d'échantillons) |
| `SCRIPTS/validate_ch10_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_02_cycles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_02.py" -- --exercise cycles
```

## Livrables attendus

1. Réglages Cycles justifiés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.03 — Bruit et débruitage](../CH10_03_DENOISING/README.md)
