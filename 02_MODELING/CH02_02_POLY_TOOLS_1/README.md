# CH02.02 — Outils polygonaux I

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h 15  
**Version :** Blender 5.3.0

## Introduction

Six outils suffisent à modéliser la majorité des objets d'un décor : Loop Cut, Extrude, Inset, Bevel, Bridge et Fill. Ce chapitre les met en œuvre sur un objet concret, un tabouret en dimensions réelles, en suivant la méthode professionnelle du gros au fin et en réglant chaque opération par des valeurs chiffrées.

## Prérequis

- CH02.01 (topologie).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter et placer précisément des boucles avec Loop Cut and Slide.
2. Extruder en tronçons, en bloc ou faces séparées.
3. Relier deux boucles ou deux faces avec Bridge Edge Loops (et corriger une vrille).
4. Chanfreiner (Bevel) et creuser (Inset + Extrude).
5. Modéliser un prop simple en dimensions réelles.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.02.a | Modéliser un prop simple | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Loop Cut et Extrude | 1 h 15 |
| L2 | Bridge, Bevel, Inset | 1 h 15 |
| L3 | Méthode et finitions | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_02_stool_starter.blend` | Assise seule (40 × 40 × 6 cm à 42 cm du sol) |
| `COMPLETED_EXAMPLES/ch02_02_stool_solution.blend` | Tabouret complet (134 faces, 100 % quads) |
| `COMPLETED_EXAMPLES/ch02_02_stool_reference.png` | Rendu de référence |
| `SCRIPTS/validate_ch02_02.py` | Correcteur (dimensions, pieds, traverses, chanfrein, creux, fermeture) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_02_stool_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_02.py" --python-exit-code 1 -- --exercise stool --render
```

## Livrables attendus

1. Tabouret validé.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : trois props de la pièce.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Tabouret validé.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.03 — Outils polygonaux II](../CH02_03_POLY_TOOLS_2/README.md)
