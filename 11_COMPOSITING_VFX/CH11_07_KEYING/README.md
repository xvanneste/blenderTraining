# CH11.07 — Keying

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le keying (incrustation) remplace un fond de couleur uniforme, souvent vert ou bleu, par une autre image. Il demande trois choses : un matte (un masque du sujet, avec des bords doux), un nettoyage (le contour garde une trace du fond) et une correction de la contamination (spill : le vert du fond se reflète sur le sujet). Ce chapitre incruste un sujet sur un nouveau fond bleu à partir d'une image générée pour l'occasion ; le correcteur mesure la couleur des coins, du centre du sujet et d'un anneau contaminé.

## Prérequis

- CH11.01 (compositeur), CH11.03 (masques).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Extraire un sujet d'un fond vert avec le nœud Keying.
2. Retirer la contamination verte.
3. Composer le sujet sur un nouveau fond (Alpha Over).
4. Mesurer la qualité d'une incrustation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.07.a | Réaliser une incrustation | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Matte et nettoyage | 3 h |
| L2 | Spill et composition | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_07_keying_starter.blend` | Image → Group Output : le fond vert (écart des coins au bleu 0,44) et la contamination (+0,130) ; 18/34 |
| `COMPLETED_EXAMPLES/ch11_07_keying_solution.blend` | Image → Keying (Key Color vert) → Color Spill → Alpha Over sur un fond bleu : écart des coins 0,006, sujet 0,001, contamination −0,028 ; 34/34. Variante vérifiée : Keying sans Color Spill (le nœud Keying corrige déjà la contamination) : 34/34 |
| `COMPLETED_EXAMPLES/ch11_07_keying_reference.png` | Départ (gauche : sujet sur fond vert) et solution (droite : sujet sur fond bleu) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans keying, mauvaise couleur de clé, sans correction de contamination, sans nouveau fond) |
| `SCRIPTS/validate_ch11_07.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_07_keying_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_07.py" -- --exercise keying
```

## Livrables attendus

1. Arbre d'incrustation commenté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.08 — Tracking et matchmoving](../CH11_08_TRACKING/README.md)
