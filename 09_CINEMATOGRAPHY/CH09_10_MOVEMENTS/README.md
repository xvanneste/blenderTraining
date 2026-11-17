# CH09.10 — Mouvements et grammaire

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

La grammaire du plan est l'ensemble des règles qui rendent un découpage lisible : l'échelle de plans (large, moyen, gros plan), la ligne d'action (la droite qui relie deux personnages : on ne la traverse pas, sinon la gauche et la droite s'inversent à l'écran) et le mouvement de caméra (un travelling avant resserre le plan). Ce chapitre fait corriger une séquence de trois plans : le correcteur rend chaque plan, mesure la taille et la position des personnages, et vérifie les repères de timeline liés aux caméras.

## Prérequis

- CH07 (timeline, clés), CH09.07 (composition), CH09.08 (focales).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir l'échelle d'un plan (large, moyen, gros plan).
2. Respecter la ligne d'action.
3. Lier des caméras à des repères de timeline.
4. Animer un travelling avant.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.10.a | Découper une séquence cohérente | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Plans et ligne d'action | 3 h |
| L2 | Repères et travelling | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_10_movements_starter.blend` | Gros plan de l'autre côté de la ligne (A passe à droite de B), aucun repère, CAM_MED fixe |
| `COMPLETED_EXAMPLES/ch09_10_movements_solution.blend` | CAM_CLOSE en (0, −4, 0,9), repères aux images 1 / 25 / 49, travelling de CAM_MED de y = −8 à −6 (hauteur de A 58 % → 78 %) |
| `COMPLETED_EXAMPLES/ch09_10_movements_reference.png` | Les quatre images contrôlées (large, moyen au début et à la fin du travelling, gros plan) : départ en haut (gros plan inversé), solution en bas |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (ligne traversée, sans repères, ordre inversé, plan fixe, recul, pas de progression) |
| `SCRIPTS/validate_ch09_10.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_10_movements_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_10.py" -- --exercise movements
```

## Livrables attendus

1. Séquence de trois plans cohérente.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.11 — Couleur et émotion](../CH09_11_COLOR_EMOTION/README.md)
