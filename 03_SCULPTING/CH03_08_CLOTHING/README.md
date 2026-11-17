# CH03.08 — Vêtements

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Un vêtement n'est pas un volume sculpté à la main : c'est un tissu qui tombe. Ce chapitre enseigne le workflow de simulation de tissu — corps simplifié (collider) et sol avec Collision, tissu à maille régulière, modificateur Cloth, simulation, puis application — sur un poncho posé sur les épaules du buste de CH03.05. Le correcteur mesure : pas de pénétration du corps, tissu non étiré, épaules couvertes, plis (rugosité), sol respecté, et que la simulation a bien été appliquée.

## Prérequis

- CH03.05 (le buste).
- CH03.03 (maillage et densité).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Préparer une scène de simulation (collider, sol, tissu à maille régulière).
2. Régler un tissu (masse, rigidités, amortissement, collisions) et lire ses défauts.
3. Appliquer et contrôler une simulation par des mesures.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.08.a | Créer un vêtement | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Préparer la simulation | 2 h |
| L2 | Régler, simuler, contrôler | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_08_poncho_starter.blend` | Buste + COLLIDER + sol Collision + tissu plat CLOTH_Poncho |
| `COMPLETED_EXAMPLES/ch03_08_poncho_solution.blend` | Poncho simulé et appliqué |
| `COMPLETED_EXAMPLES/ch03_08_poncho_reference.png` | Face, 3/4, profil |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (pénétrant, lissé, étiré, trop petit) |
| `SCRIPTS/validate_ch03_08.py` | Correcteur (poncho) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_08_poncho_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_08.py" -- --exercise poncho --render
```

## Livrables attendus

1. Poncho validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH03.09 — Retopologie personnage](../CH03_09_RETOPOLOGY/README.md)
