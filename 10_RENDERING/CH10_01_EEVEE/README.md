# CH10.01 — EEVEE en profondeur

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

EEVEE est le moteur temps réel de Blender : il rend en quelques secondes ce que Cycles calcule en minutes, au prix d'approximations. Trois réglages décident de son réalisme : les ombres (Shadows), le ray tracing (réflexions et lumière indirecte approchées) et le nombre d'échantillons (qualité contre temps). Ce chapitre fait activer ces réglages sur une scène de test : le correcteur rend l'image avec les réglages de l'élève et mesure l'ombre au sol et la réflexion sur une sphère chromée.

## Prérequis

- CH01 (rendu), CH09.01 (lumière), CH09.06 (exposition).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer et régler les ombres d'EEVEE.
2. Activer le ray tracing et reconnaître son effet sur les réflexions.
3. Choisir un nombre d'échantillons raisonnable.
4. Mesurer l'effet d'un réglage par un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.01.a | Régler EEVEE | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Ombres et ray tracing | 3 h |
| L2 | Qualité contre temps | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_01_eevee_starter.blend` | Shadows et Raytracing désactivés, 1 échantillon : pas d'ombre au sol (rapport 0,96), sphère chromée plate (0,030) ; 11/32 |
| `COMPLETED_EXAMPLES/ch10_01_eevee_solution.blend` | Shadows, Raytracing activés, 64 échantillons : ombre (rapport 0,70), sphère chromée qui reflète la scène (0,081) ; 32/32 |
| `COMPLETED_EXAMPLES/ch10_01_eevee_reference.png` | Rendu de départ (gauche) et solution (droite) : l'ombre de la boule et le reflet dans la sphère chromée apparaissent |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans ombres, sans ray tracing, trop peu d'échantillons, trop d'échantillons, mauvais moteur) |
| `SCRIPTS/validate_ch10_01.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_01_eevee_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_01.py" -- --exercise eevee
```

## Livrables attendus

1. Réglages EEVEE justifiés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.02 — Cycles en profondeur](../CH10_02_CYCLES/README.md)
