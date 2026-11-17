# CH11.02 — Compositing multipasse

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rendu multipasse stocke la lumière en plusieurs couches que l'on peut recomposer. Les light groups, vus en CH10.04, séparent la contribution de chaque lampe : comme la lumière s'additionne, la somme des groupes redonne l'image complète. En dosant chaque groupe dans le compositeur on relighte l'image sans la rendre à nouveau : un changement de rapport key/fill prend quelques secondes au lieu de minutes. Le correcteur mesure ce rapport sur la luminance linéaire de deux flancs d'une sphère.

## Prérequis

- CH10.04 (passes, light groups), CH11.01 (compositeur).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser les light groups d'un rendu dans le compositeur.
2. Relighter en post en dosant chaque lampe en diaphragmes.
3. Additionner des couches de lumière.
4. Mesurer un rapport d'éclairage en luminance linéaire.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.02.a | Recomposer un rendu | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Light groups dans l'arbre | 3 h |
| L2 | Relighting mesuré | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_02_multipass_starter.blend` | Render Layers (Image) → Group Output : rapport des flancs 1,17, light groups ignorés ; 20/38 |
| `COMPLETED_EXAMPLES/ch11_02_multipass_solution.blend` | Combined_key → Exposure +1, Combined_fill → Exposure −1, Mix (Add) → Group Output : rapport 4,28 ; 38/38 |
| `COMPLETED_EXAMPLES/ch11_02_multipass_reference.png` | Départ (gauche, éclairage équilibré) et solution (droite, KEY dominante à gauche) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (aucun relighting, trop fort, inversé, FILL oubliée, light groups ignorés) |
| `SCRIPTS/validate_ch11_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_02_multipass_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_02.py" -- --exercise multipass
```

## Livrables attendus

1. Arbre de relighting commenté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.03 — Masques et Cryptomatte](../CH11_03_MASKS/README.md)
