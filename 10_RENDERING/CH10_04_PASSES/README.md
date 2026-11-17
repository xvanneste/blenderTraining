# CH10.04 — Passes, AOV, View Layers

**Phase :** 10 — Rendu et optimisation  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rendu n'est pas une seule image : c'est un paquet de couches que le compositing recombine. Les passes (profondeur, normales, couleur diffuse, index d'objet, Cryptomatte), les light groups (une couche par lumière), les AOV (des sorties personnalisées d'un matériau) et les calques de vue (View Layers : des rendus séparés du même décor) sont écrits dans un seul fichier OpenEXR multicouche. Le correcteur rend réellement la scène dans un EXR multicouche et lit les noms de canaux dans son en-tête : ce que le fichier contient vraiment.

## Prérequis

- CH10.02 (Cycles), CH10.03 (débruitage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer les passes utiles au compositing.
2. Créer des light groups et un AOV.
3. Séparer un plan en deux calques de vue.
4. Vérifier le contenu d'un EXR multicouche.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C10.04.a | Produire un rendu multi-passes | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Passes et light groups | 3 h |
| L2 | Calques de vue et EXR | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch10_04_passes_starter.blend` | Un seul calque, seulement Combined, sortie PNG (2/64) |
| `COMPLETED_EXAMPLES/ch10_04_passes_solution.blend` | Calques FG et BG, passes Z, Normal, Diffuse Color, Object Index, Cryptomatte, light groups key et fill, AOV tint, sortie EXR multicouche 16 bits : 39 canaux (69/69) |
| `COMPLETED_EXAMPLES/ch10_04_passes_reference.png` | Les deux calques de la solution rendus séparément : FG (Hero seul, Backdrop exclu) à gauche, BG (Backdrop seul, Hero exclu) à droite |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans Normal, sans light groups, sans AOV, mauvais index, sans calque BG, sortie PNG) |
| `SCRIPTS/validate_ch10_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_04_passes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_04.py" -- --exercise passes
```

## Livrables attendus

1. EXR multicouche avec la liste de ses canaux.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH10.05 — Mémoire et optimisation](../CH10_05_MEMORY/README.md)
