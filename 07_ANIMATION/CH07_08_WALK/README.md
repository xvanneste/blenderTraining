# CH07.08 — Cycles de marche

**Phase :** 7 — Animation 3D  
**Niveau :** avancé  
**Durée estimée :** 10 h  
**Version :** Blender 5.3.0

## Introduction

La marche est le cycle de référence de l'animation : deux pas qui se répètent sans couture. Ce chapitre construit une marche SUR PLACE (le sol défile) en 24 images : CONTACT, DESCENTE, PASSAGE, MONTÉE de chaque côté, pieds posés sans glisser, hanches qui montent et descendent, bras opposés aux jambes, boucle parfaite. La solution est calculée par une cinématique inverse à deux segments écrite en script ; le correcteur mesure les chevilles, les hanches et les poignets sur les 25 images et valide aussi une version à neuf clés (les huit poses et la boucle).

## Prérequis

- CH07.02 (clés), CH07.05 (timing), CH07.07 (posing).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Connaître les quatre poses d'un pas.
2. Faire boucler un cycle (image 25 = image 1).
3. Poser le pied d'appui sans glissement.
4. Régler le rebond des hanches et le balancement des bras.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.08.a | Walk cycle | Exercice 2 (correcteur) + poses du cycle |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les poses d'un pas | 5 h |
| L2 | Le cycle et ses réglages | 5 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_08_walk_starter.blend` | Mannequin FK (13 bones) en T-pose, bras abaissés, sans animation |
| `COMPLETED_EXAMPLES/ch07_08_walk_solution.blend` | Marche sur place : 25 images clés par bone, IK analytique calculée en script |
| `COMPLETED_EXAMPLES/ch07_08_walk_reference.png` | Huit images du cycle de profil : contact, descente, passage, montée, puis l'autre côté |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans boucle, appui irrégulier, sans rebond, bras du même côté, pieds qui traînent, pas trop court) |
| `SCRIPTS/validate_ch07_08.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_08_walk_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_08.py" -- --exercise walk
```

## Livrables attendus

1. Cycle de marche validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.09 — Course, saut, interactions](../CH07_09_RUN_JUMP/README.md)
