# CH07.14 — Motion capture

**Phase :** 7 — Animation 3D  
**Niveau :** expert  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

La motion capture enregistre le mouvement d'un acteur : une clé par image sur chaque canal, avec du bruit et des glitches. L'animateur ne la joue pas telle quelle : il la NETTOIE (retirer les aberrations, lisser, décimer) pour garder la forme du mouvement avec peu de clés éditables. Ce chapitre importe un BVH synthétique bruité (bruit de 1°, trois glitches de 9°) et le nettoie dans le Graph Editor. Le correcteur compare l'action nettoyée à la copie brute : rugosité, fidélité de la forme, amplitude, glitches, nombre de clés, interpolation.

## Prérequis

- CH07.04 (Graph Editor), CH07.13 (actions).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Importer un fichier BVH.
2. Lisser et supprimer des glitches.
3. Décimer sans perdre la forme.
4. Garder une copie brute intacte.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.14.a | Nettoyer une mocap | Exercice 2 (correcteur) + courbe de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Importer et diagnostiquer | 4 h |
| L2 | Nettoyer | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_14_mocap_starter.blend` | BVH synthétique importé (RIG_Mocap, action active MOCAP de 15 courbes de 96 clés) + copie brute MOCAP_RAW ; le fichier ch07_14_mocap_noisy.bvh est fourni à côté |
| `COMPLETED_EXAMPLES/ch07_14_mocap_solution.blend` | Action MOCAP nettoyée : glitches supprimés, lissage gaussien, décimation (≤ 38 clés par courbe), clés Bezier |
| `COMPLETED_EXAMPLES/ch07_14_mocap_reference.png` | Courbe de rotation Z de Spine : brute (points gris), nettoyée (orange), clés conservées (blanc) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (non nettoyée, sur-lissée, glitches conservés, trop de clés, clés linéaires, copie brute modifiée) |
| `SCRIPTS/validate_ch07_14.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_14_mocap_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_14.py" -- --exercise mocap
```

## Livrables attendus

1. Mocap nettoyée validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.15 — Scène dialoguée](../CH07_15_DIALOGUE/README.md)
