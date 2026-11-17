# CH11.03 — Masques et Cryptomatte

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Pour corriger une seule partie de l'image — l'objet seul, le fond seul — il faut un masque : une image en noir et blanc qui dit où agir. Deux familles : l'index d'objet (chaque objet porte un entier, le nœud ID Mask isole un entier) et Cryptomatte (chaque objet, matériau ou asset est identifié par un nom haché, on le choisit par son nom, avec des bords anti-aliasés propres). Ce chapitre garde en couleur une sphère verte et grise le reste ; le correcteur mesure la saturation sur chaque sphère.

## Prérequis

- CH10.04 (passes), CH11.01–02 (compositeur).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Isoler un objet avec un nœud ID Mask.
2. Isoler un objet avec Cryptomatte.
3. Combiner un masque et un Mix.
4. Mesurer l'effet d'un masque.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.03.a | Isoler un objet | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Index d'objet et ID Mask | 3 h |
| L2 | Cryptomatte et mesure | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_03_masks_starter.blend` | Render Layers → Group Output : trois sphères en couleur (saturations 0,47 / 0,59 / 0,42) ; 27/41 |
| `COMPLETED_EXAMPLES/ch11_03_masks_solution.blend` | Image désaturée + ID Mask (Index 2) + Mix : B en couleur (0,59), A et C en gris (0,00) ; 41/41. Variante vérifiée : Cryptomatte V2 (matte_id « Sphere_B ») à la place de l'ID Mask : 41/41 |
| `COMPLETED_EXAMPLES/ch11_03_masks_reference.png` | Départ (haut : trois sphères en couleur) et solution (bas : seule la sphère verte reste en couleur) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (mauvais index, pas de masque, masque inversé, nœud de masque absent) |
| `SCRIPTS/validate_ch11_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_03_masks_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_03.py" -- --exercise masks
```

## Livrables attendus

1. Arbre de masquage commenté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.04 — Depth, defocus, motion blur](../CH11_04_DEPTH_FX/README.md)
