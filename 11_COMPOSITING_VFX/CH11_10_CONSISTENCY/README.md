# CH11.10 — Cohérence visuelle

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une intégration réussie ne se voit pas. Même avec la bonne ombre (CH11.09), un élément 3D se trahit s'il est trop clair, de la mauvaise couleur ou trop propre à côté d'une plaque granuleuse. Le contrôle qualité compare l'élément à la plaque sur trois critères mesurables : l'exposition (rapport de luminance), la dominante de couleur (écart de rouge moins bleu) et le grain (bruit). Ce chapitre fait corriger un cube posé sur une plaque : exposition par un nœud Exposure, dominante par un Color Balance, grain par le nombre d'échantillons de Cycles.

## Prérequis

- CH11.06 (étalonnage), CH11.09 (intégration).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Mesurer l'écart d'exposition, de couleur et de grain entre un rendu et une plaque.
2. Corriger un élément 3D seul dans le compositeur.
3. Régler le grain avec les échantillons.
4. Écrire un contrôle qualité mesurable.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.10.a | Vérifier une intégration | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Exposition et couleur | 3 h |
| L2 | Grain et contrôle qualité | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_10_consistency_starter.blend` | Intégration sans correction, 128 échantillons : rapport 1,86, dominante −0,20, bruit 0,003 ; 15/39 |
| `COMPLETED_EXAMPLES/ch11_10_consistency_solution.blend` | Exposure −2, Color Balance Gain (1,3 ; 1,0 ; 0,6), 2 échantillons : rapport 1,01, dominante +0,007, bruit 0,012 (plaque 0,011) ; 39/39 |
| `COMPLETED_EXAMPLES/ch11_10_consistency_reference.png` | La plaque (gauche), le départ (milieu : cube blanc et propre) et la solution (droite : cube raccordé en luminosité, couleur et grain) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (exposition seule, couleur seule, cube trop propre) |
| `SCRIPTS/validate_ch11_10.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_10_consistency_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_10.py" -- --exercise consistency
```

## Livrables attendus

1. Contrôle qualité chiffré de votre intégration.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet P11 — Intégration d'un élément 3D dans une prise de vue](../PROJECT_P11/README.md)
