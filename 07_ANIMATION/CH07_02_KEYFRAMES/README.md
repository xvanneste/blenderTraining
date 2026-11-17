# CH07.02 — Keyframes et timeline

**Phase :** 7 — Animation 3D  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Animer dans Blender, c'est poser des clés (keyframes) : à une image donnée, une propriété prend une valeur ; entre deux clés, Blender interpole. Ce chapitre apprend à régler la timeline (plage, cadence), à insérer des clés de position et de rotation, à créer un maintien (deux clés de même valeur), à choisir l'interpolation (Bezier ou linéaire) et à poser des marqueurs. Le correcteur lit les clés (images et valeurs) et l'animation évaluée : maintien, vitesse de rotation, absence de dépassement.

## Prérequis

- CH07.01 (principes), CH01 (objets, transformations).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler la plage et la cadence.
2. Insérer des clés de position et de rotation.
3. Créer un maintien.
4. Choisir une interpolation.
5. Poser et nommer des marqueurs.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.02.a | Animer un objet | Exercice 2 (correcteur) + courbes de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La timeline et les clés | 3 h |
| L2 | Interpolation, maintien et marqueurs | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_02_keyframes_starter.blend` | Caisse avec une seule clé, plage par défaut 1–250 |
| `COMPLETED_EXAMPLES/ch07_02_keyframes_solution.blend` | Caisse animée : aller, rotation sur place, retour ; marqueurs |
| `COMPLETED_EXAMPLES/ch07_02_keyframes_reference.png` | Courbes X (vert) et rotation Z (orange, linéaire), clés blanches, marqueurs |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (mauvaise plage, pas de maintien, rotation en Bezier, sans marqueurs, clés décalées, sans rotation) |
| `SCRIPTS/validate_ch07_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_02_keyframes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_02.py" -- --exercise keyframes
```

## Livrables attendus

1. Animation de la caisse validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.03 — Dope Sheet et Action](../CH07_03_DOPESHEET/README.md)
