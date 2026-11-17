# CH11.01 — Compositor

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le compositeur retouche l'image après le rendu, par un graphe de nœuds : Render Layers fournit l'image rendue, des nœuds de traitement la transforment (exposition, flou, couleur…), une sortie la livre. Dans Blender 5.3, ce graphe est un groupe de nœuds de la scène (`scene.compositing_node_group`) dont la sortie est un nœud Group Output, et les réglages d'un nœud sont ses prises d'entrée (par exemple « Exposure » ou « Size »). Ce chapitre construit le premier arbre : Render Layers → Exposure → Blur → Group Output, et le correcteur mesure l'image rendue avec le compositeur : luminance, bruit, lisibilité.

## Prérequis

- CH10.02–CH10.04 (rendu Cycles, passes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lire et construire un arbre de compositing.
2. Régler l'exposition d'un rendu en post.
3. Réduire le bruit par un flou, sans effacer le sujet.
4. Reconnaître un nœud orphelin.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.01.a | Construire un arbre de compositing | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le graphe de nœuds | 3 h |
| L2 | Exposition et flou | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_01_compositor_starter.blend` | Render Layers → Group Output : image sombre (luminance 0,277) et bruitée (0,019) ; 29/45 |
| `COMPLETED_EXAMPLES/ch11_01_compositor_solution.blend` | Render Layers → Exposure (+1,5) → Blur (3, 3) → Group Output : luminance 0,459, bruit 0,0063, lisibilité 0,81 ; 45/45 |
| `COMPLETED_EXAMPLES/ch11_01_compositor_reference.png` | Départ (gauche, sombre et granuleux) et solution (droite, plus clair et lissé) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans exposition, sans flou, flou excessif, nœud orphelin, compositing désactivé) |
| `SCRIPTS/validate_ch11_01.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_01_compositor_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_01.py" -- --exercise compositor
```

## Livrables attendus

1. Arbre de compositing commenté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.02 — Compositing multipasse](../CH11_02_MULTIPASS/README.md)
