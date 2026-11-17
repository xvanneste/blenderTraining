# CH09.05 — Volumétrie

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Dans l'air pur, un faisceau de lumière est invisible : on ne voit que ce qu'il éclaire. Avec de la brume, de la poussière ou de la fumée, chaque particule diffuse un peu de lumière vers la caméra et le faisceau devient visible : ce sont les « rayons de lumière » (god rays) des films. Dans Blender, on met un volume de brouillard (un maillage dont le matériau n'a qu'un shader de volume : Principled Volume) autour de la scène. Sa densité règle tout : trop mince, rien ne se voit ; trop dense, la lumière s'éteint et l'image devient opaque. Ce chapitre règle cette densité sous un spot et la mesure sur un rendu.

## Prérequis

- CH09.01 (mesure par rendu), CH04 (nœuds de matériaux).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un volume de brouillard avec un Principled Volume.
2. Régler la densité pour un faisceau lisible.
3. Expliquer l'effet d'un brouillard trop dense ou trop mince.
4. Mesurer un faisceau sur un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.05.a | Atmosphère | Exercice 2 (correcteur) + rendus comparés |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Brouillard et faisceau | 3 h |
| L2 | Densité et lisibilité | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_05_volumetrics_starter.blend` | Cube de brouillard à Density 0 (aucun faisceau) autour d'un spot au-dessus d'un sol |
| `COMPLETED_EXAMPLES/ch09_05_volumetrics_solution.blend` | Density 0,08, Anisotropy 0,3 : faisceau conique lisible (luminance du centre 0,088) |
| `COMPLETED_EXAMPLES/ch09_05_volumetrics_reference.png` | Trois rendus (éclaircis ×4) : sans brouillard, Density 0,08 et Density 1,5 |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (brouillard trop mince, trop dense, spot trop large, spot éteint) |
| `SCRIPTS/validate_ch09_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_05_volumetrics_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_05.py" -- --exercise volumetrics
```

## Livrables attendus

1. Faisceau validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.06 — Exposition et contraste](../CH09_06_EXPOSURE/README.md)
