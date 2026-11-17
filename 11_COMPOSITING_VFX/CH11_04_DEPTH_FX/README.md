# CH11.04 — Depth, defocus, motion blur

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Deux effets optiques coûteux au rendu se fabriquent après coup : la profondeur de champ à partir de la passe Depth (nœud Defocus) et le flou de mouvement à partir de la passe Vector (nœud Vector Blur). Le gain est de temps — on rend net et on dose l'effet — mais aussi de contrôle : on change le point de mise au point ou la durée d'obturation sans re-rendre. Ce chapitre ajoute les deux effets à une scène de barres lumineuses ; le correcteur rend l'image 10 et mesure la netteté de chaque barre et la largeur de la barre qui bouge.

## Prérequis

- CH09.09 (profondeur de champ), CH10.04 (passes), CH11.01 (compositeur).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser la passe Depth pour une profondeur de champ en post.
2. Régler la mise au point de la caméra pour le nœud Defocus.
3. Utiliser la passe Vector pour un flou de mouvement.
4. Mesurer netteté et étalement.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.04.a | Réaliser des effets optiques en post | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Defocus et Depth | 3 h |
| L2 | Vector Blur | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_04_depth_fx_starter.blend` | Render Layers → Group Output : tout est net (Far 0,92), Mover de 12 pixels ; 23/39 |
| `COMPLETED_EXAMPLES/ch11_04_depth_fx_solution.blend` | Defocus (f-stop 1, mise au point 5 m) puis Vector Blur (Shutter 1) : Near 1,00, Far 0,30, Mover de 27 pixels ; 39/39 |
| `COMPLETED_EXAMPLES/ch11_04_depth_fx_reference.png` | Départ (haut : tout net) et solution (bas : Near nette, Mover étalée, Far floue) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans Defocus, mauvaise mise au point, sans Vector Blur, obturation trop faible) |
| `SCRIPTS/validate_ch11_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_04_depth_fx_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_04.py" -- --exercise depth_fx
```

## Livrables attendus

1. Arbre d'effets commenté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.05 — Glare et effets](../CH11_05_GLARE/README.md)
