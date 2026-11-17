# CH08.03 — Cloth

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Le Cloth simule les tissus : un maillage fin dont chaque arête résiste à l'étirement et à la flexion, qui entre en collision avec les obstacles. Ce chapitre laisse tomber un drap de 2,4 m sur une sphère posée sur un sol : le drap doit se draper (plis), ne jamais entrer dans la sphère ni traverser le sol, et se stabiliser. Les réglages décisifs : Quality, rigidité en flexion, amortissement, qualité et distance de collision. Le correcteur configure ET simule 120 images pas à pas.

## Prérequis

- CH08.01–02 (simulation pas à pas), CH03.08 (premier tissu : vêtement).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer un Cloth et ses collisions.
2. Déclarer des obstacles (Collision).
3. Régler Quality, flexion, amortissement et distance.
4. Mesurer drapé, pénétration, traversée du sol et stabilité.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.03.a | Drapé et vêtement | Exercice 2 (correcteur) + profils du drap |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Tissu et obstacles | 4 h |
| L2 | Régler et mesurer | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_03_cloth_starter.blend` | Drap (1 681 sommets), sphère et sol, sans physique |
| `COMPLETED_EXAMPLES/ch08_03_cloth_solution.blend` | Cloth et Collision configurés : le drap drape la sphère et repose sur le sol |
| `COMPLETED_EXAMPLES/ch08_03_cloth_reference.png` | Profil du drap aux images 1, 30 et 120 (cercle bleu : sphère, ligne : sol) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sphère sans collision, sol sans collision, qualité trop basse, sans gravité) |
| `SCRIPTS/validate_ch08_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_03_cloth_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_03.py" -- --exercise cloth
```

## Livrables attendus

1. Drap sur sphère validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.04 — Particules et distribution](../CH08_04_PARTICLES/README.md)
