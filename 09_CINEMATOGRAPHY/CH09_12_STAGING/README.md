# CH09.12 — Mise en scène

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

La mise en scène règle où se placent les acteurs, les objets et la caméra, et comment tout cela bouge. Le blocking est ce plan de placement : un triangle de personnages se lit mieux qu'une file, des distances différentes à la caméra créent des plans (avant, milieu, fond), et la continuité garantit que rien ne saute entre deux plans (le raccord). Ce chapitre fait corriger le blocking d'une scène de trois personnages et d'une tasse : le correcteur évalue la scène image par image et rend le moment clé.

## Prérequis

- CH07 (clés de position), CH09.07 (composition), CH09.10 (découpage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Disposer trois personnages en triangle.
2. Étager les personnages en profondeur.
3. Assurer la continuité d'un raccord.
4. Contrôler une animation image par image.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.12.a | Régler une mise en scène continue | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Blocking et profondeur | 3 h |
| L2 | Continuité et raccord | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_12_staging_starter.blend` | Trois personnages presque alignés au même niveau à l'image 36, A saute de 2,5 m au raccord, la tasse change de place (23/62) |
| `COMPLETED_EXAMPLES/ch09_12_staging_solution.blend` | À l'image 36 : A (−2, −1,5), B (2, 0,5), C (0, 3) : triangle de 7 m², angle minimal 39°, étagement 4,5 m ; raccord sans saut ; tasse immobile |
| `COMPLETED_EXAMPLES/ch09_12_staging_reference.png` | Vue de dessus à l'image 36 : départ (gauche, personnages alignés) et solution (droite, triangle) ; la caméra est le trait blanc en bas |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (alignés, sans profondeur, téléportation, tasse déplacée, trop rapide, caché, collision) |
| `SCRIPTS/validate_ch09_12.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_12_staging_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_12.py" -- --exercise staging
```

## Livrables attendus

1. Blocking validé image par image.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet P9 — Cinq plans, cinq émotions](../PROJECT_P9/README.md)
