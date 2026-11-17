# CH11.06 — Color grading

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

L'étalonnage donne à un film sa couleur : on pousse les ombres vers une teinte et les hautes lumières vers une autre, sans changer l'exposition. Le nœud Color Balance en mode Lift/Gamma/Gain agit sur trois zones de tons : Lift sur les ombres, Gamma sur les tons moyens, Gain sur les hautes lumières. Ce chapitre étalonne une rampe de gris en « ombres froides, hautes lumières chaudes » ; le correcteur mesure la teinte de chaque zone et vérifie que la luminosité globale n'a pas bougé.

## Prérequis

- CH09.11 (couleur et émotion), CH11.01 (compositeur).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler Lift, Gamma et Gain d'un nœud Color Balance.
2. Pousser les ombres et les hautes lumières vers deux teintes.
3. Conserver l'exposition.
4. Mesurer un étalonnage.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.06.a | Étalonner une image | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lift, Gamma, Gain | 3 h |
| L2 | Étalonner et mesurer | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_06_grading_starter.blend` | Render Layers → Group Output : rampe de gris neutre (ombres 0,00, hautes lumières 0,00) ; 20/36 |
| `COMPLETED_EXAMPLES/ch11_06_grading_solution.blend` | Color Balance Lift/Gamma/Gain : Lift (0,96 ; 1,0 ; 1,04), Gain (1,08 ; 1,0 ; 0,92) : ombres +0,111 bleu−rouge, hautes lumières +0,060 rouge−bleu, écart de luminance −0,001 ; 36/36 |
| `COMPLETED_EXAMPLES/ch11_06_grading_reference.png` | Rampe de départ (haut, grise) et étalonnée (bas : ombres bleutées, hautes lumières chaudes) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (tout chaud, tout froid, inversé, trop clair, sans étalonnage) |
| `SCRIPTS/validate_ch11_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_06_grading_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_06.py" -- --exercise grading
```

## Livrables attendus

1. Étalonnage commenté (valeurs).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.07 — Keying](../CH11_07_KEYING/README.md)
