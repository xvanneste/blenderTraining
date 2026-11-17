# CH08.01 — Rigid Bodies

**Phase :** 8 — Physique et simulations  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Les corps rigides (Rigid Bodies) simulent des objets indéformables qui tombent, se heurtent et s'empilent. Un corps ACTIF obéit à la physique ; un corps PASSIF (le sol) sert d'obstacle. Ce chapitre rend physique un mur de 30 briques et une boule lancée contre lui : sol passif, briques actives (masse, friction, forme de collision, marge), boule lourde lâchée par l'option Animated, monde réglé sur 150 images. Le correcteur configure ET simule la scène, image après image, et mesure la stabilité avant l'impact, l'effondrement, la chute sous le sol et le repos final.

## Prérequis

- CH07.02 (clés), CH07.03 (actions).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer corps actif et passif.
2. Régler masse, friction, forme et marge.
3. Lancer un corps par une trajectoire animée puis le lâcher (Animated).
4. Régler le monde (cache, sous-étapes) et mesurer une simulation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.01.a | Effondrement | Exercice 2 (correcteur) + vue de dessus de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Actif, passif, paramètres | 3 h |
| L2 | Lancer, simuler, mesurer | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_01_rigid_starter.blend` | Sol, 30 briques et boule (trajectoire animée), sans physique |
| `COMPLETED_EXAMPLES/ch08_01_rigid_solution.blend` | Corps rigides configurés : mur stable, effondrement à l'impact (21 briques déplacées de plus de 0,6 m) |
| `COMPLETED_EXAMPLES/ch08_01_rigid_reference.png` | Vue de dessus : mur à l'image 1 (gauche), briques dispersées à l'image 150 (droite), boule en bleu |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans sol, briques passives, boule légère, boule non lâchée, friction nulle, cache trop court) |
| `SCRIPTS/validate_ch08_01.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_01_rigid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_01.py" -- --exercise rigid
```

## Livrables attendus

1. Simulation de corps rigides validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.02 — Soft Bodies](../CH08_02_SOFT_BODIES/README.md)
