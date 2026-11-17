# CH11.05 — Glare et effets

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Une caméra réelle ne reproduit pas la lumière comme une simulation idéale : une source très lumineuse déborde en halo (glare) dans l'objectif, et les lignes droites se courbent près des bords (distorsion). Ces défauts, dosés avec goût, donnent du réalisme à une image trop parfaite. Ce chapitre ajoute un halo (nœud Glare) et une légère distorsion (nœud Lens Distortion) à une lampe et à une barre ; le correcteur mesure l'énergie d'un anneau autour de la lampe et la courbure de la barre.

## Prérequis

- CH11.01 (compositeur), CH09.06 (exposition).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir un type de Glare adapté.
2. Doser un halo sans noyer l'image.
3. Appliquer une distorsion d'objectif.
4. Mesurer des effets optiques.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.05.a | Finir l'image avec des effets optiques | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le Glare | 3 h |
| L2 | Distorsion et mesure | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_05_glare_starter.blend` | Render Layers → Group Output : lampe nette (anneau 0,0003) et barre droite (courbure 0) ; 21/37 |
| `COMPLETED_EXAMPLES/ch11_05_glare_solution.blend` | Glare Fog Glow (par défaut) puis Lens Distortion 0,3 : anneau 0,0066, champ lointain 0,001, cœur 1,0, courbure +7 pixels ; 37/37 |
| `COMPLETED_EXAMPLES/ch11_05_glare_reference.png` | Départ (gauche) et solution (droite : lampe élargie avec halo, barre courbée) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans halo, Bloom trop fort, Ghosts, sans distorsion, distorsion excessive) |
| `SCRIPTS/validate_ch11_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_05_glare_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_05.py" -- --exercise glare
```

## Livrables attendus

1. Réglages Glare et distorsion justifiés.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.06 — Color grading](../CH11_06_GRADING/README.md)
