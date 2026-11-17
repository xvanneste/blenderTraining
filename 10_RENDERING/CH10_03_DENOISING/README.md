# CH10.03 — Bruit et débruitage

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le bruit est le grain d'un rendu Cycles qui manque d'échantillons. On peut le combattre en calculant plus (long) ou en débruitant : un algorithme (OpenImageDenoise sur CPU, OptiX sur certaines cartes NVIDIA) devine l'image propre à partir de l'image bruitée et de passes d'aide (couleur de surface, normale). Bien réglé, le débruitage rapproche un rendu à très peu d'échantillons d'une référence très échantillonnée sans lisser le détail. Le correcteur compare le rendu de l'élève à une référence de 256 échantillons sur un damier fin.

## Prérequis

- CH10.02 (Cycles, échantillons).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer et régler OpenImageDenoise.
2. Mesurer l'écart à une référence.
3. Reconnaître un débruitage inutile (préfiltre None) ou excessif.
4. Rester dans un budget d'échantillons.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.03.a | Débruiter sans perte | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le bruit et le débruiteur | 3 h |
| L2 | Mesurer la perte | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_03_denoising_starter.blend` | 4 échantillons, débruitage désactivé : EQM 0,073, contraste du damier 1,12 (bruit) ; 17/33 |
| `COMPLETED_EXAMPLES/ch10_03_denoising_solution.blend` | 4 échantillons, OpenImageDenoise, Albedo+Normal, préfiltre Accurate : EQM 0,056, contraste 1,07 ; 33/33 |
| `COMPLETED_EXAMPLES/ch10_03_denoising_reference.png` | Départ (gauche, bruité), solution (milieu, débruité) et référence de 256 échantillons (droite) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans débruitage, préfiltre None, un seul échantillon, trop d'échantillons) |
| `SCRIPTS/validate_ch10_03.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_03_denoising_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_03.py" -- --exercise denoising
```

## Livrables attendus

1. Réglages de débruitage justifiés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.04 — Passes, AOV, View Layers](../CH10_04_PASSES/README.md)
