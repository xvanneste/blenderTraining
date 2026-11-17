# CH06.09 — Rig facial

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un visage se rigge avec deux familles d'outils : des BONES pour les mouvements de masse (la mâchoire qui s'ouvre) et des SHAPE KEYS pour les formes fines (sourire, paupières), le tout piloté par des contrôleurs ergonomiques. Ce chapitre construit un rig facial minimal sur une tête simple : une mâchoire à poids lisses, deux shape keys limités chacun à leur zone, deux glissières bornées par Limit Location et reliées aux shape keys par des drivers. Le correcteur ouvre la mâchoire, déplace les glissières et mesure les sommets : chaque commande n'agit que sur sa zone.

## Prérequis

- CH06.03 (skinning), CH06.07 (drivers, Limit), CH06.08 (shape keys et drivers).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir bones ou shape keys selon le mouvement.
2. Lisser les poids d'une mâchoire.
3. Isoler chaque expression dans sa zone (pas de diaphonie).
4. Borner un contrôleur et le relier à un shape key.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.09.a | Rig facial simple | Exercice 2 (correcteur) + croquis |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La mâchoire et les zones | 3 h |
| L2 | Contrôleurs et drivers | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_09_facial_starter.blend` | Tête, armature et poids de peau, sans shape keys ni drivers ni limites |
| `COMPLETED_EXAMPLES/ch06_09_facial_solution.blend` | Rig facial complet |
| `COMPLETED_EXAMPLES/ch06_09_facial_reference.png` | Profil repos/mâchoire ouverte, face repos/sourire + clignement |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans drivers, diaphonie, sans limite, driver faible, sans poids de mâchoire, poids binaires) |
| `SCRIPTS/validate_ch06_09.py` | Correcteur (facial) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_09_facial_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_09.py" -- --exercise facial
```

## Livrables attendus

1. Rig facial validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.10 — Contrôleurs et ergonomie](../CH06_10_CONTROLS/README.md)
