# CH12.02 — Montage narratif

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Monter, c'est raconter par le choix de l'ordre et de la durée des plans. Trois outils de base : l'alternance des échelles de plan (on évite deux plans de même échelle à la suite : le faux raccord, ou jump cut), le rythme (des plans de plus en plus courts accélèrent l'action ; un dernier plan plus long la résout) et les transitions (la coupe sèche est la règle, le fondu enchaîné est l'exception qui marque un passage). Ce chapitre fait monter six plans de couleur selon ces trois principes ; le correcteur lit les durées, les canaux, le strip Crossfade et rend le milieu du fondu.

## Prérequis

- CH12.01 (VSE), CH09.10 (échelles de plan).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Alterner les échelles de plan.
2. Régler un rythme qui accélère puis se résout.
3. Poser un fondu enchaîné entre deux plans.
4. Contrôler un montage par ses durées et son rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.02.a | Monter une séquence | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Échelles et rythme | 3 h |
| L2 | Transitions | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_02_editing_starter.blend` | Durées décousues 10, 40, 10, 40, 10, 10, aucune transition ; 17/60 |
| `COMPLETED_EXAMPLES/ch12_02_editing_solution.blend` | Durées 30, 24, 18, 12, 12 (le rythme accélère), SH6 de 28 images sur le canal 2 avec un Crossfade de 12 images, plage 1–112 ; 60/60 |
| `COMPLETED_EXAMPLES/ch12_02_editing_reference.png` | Trois images (80, 90, 100) : vert, fondu cyan-bleu à 50 %, bleu ; et les durées des six plans en barres |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (faux raccord, rythme qui ralentit, pas de résolution, pas de fondu, plage fausse) |
| `SCRIPTS/validate_ch12_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_02_editing_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_02.py" -- --exercise editing
```

## Livrables attendus

1. Plan de montage avec durées et raisons.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH12.03 — Son](../CH12_03_SOUND/README.md)
