# CH11.09 — Intégration 3D/réel

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Intégrer un objet 3D dans une prise de vue réelle (la plaque) revient à répondre à trois questions : la lumière vient-elle du même côté ? l'objet projette-t-il une ombre sur le sol réel ? le sol 3D reste-t-il invisible ? Le shadow catcher répond à la deuxième et à la troisième : un plan 3D qui ne reçoit que les ombres et le reste devient transparent grâce au film transparent. Le compositeur pose enfin le rendu sur la plaque. Le correcteur compare l'image composée à la plaque, côté ombre et côté lumière.

## Prérequis

- CH09.03 (lumière naturelle), CH11.01 (compositeur), CH11.07 (Alpha Over).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Déduire la direction du soleil d'une plaque.
2. Utiliser un shadow catcher et le film transparent.
3. Composer un rendu sur une plaque avec Alpha Over.
4. Contrôler une intégration par mesure.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.09.a | Intégrer un objet 3D dans une prise de vue | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lumière et ombre de la plaque | 3 h |
| L2 | Composer et vérifier | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_09_integration_starter.blend` | Sol opaque, fond non transparent, soleil à droite, plaque non utilisée : sol lointain +0,327 ; 23/49 |
| `COMPLETED_EXAMPLES/ch11_09_integration_solution.blend` | Shadow catcher, film transparent, soleil à gauche (X 50°, Z −50°), Alpha Over sur la plaque : ombre à droite −0,067, gauche −0,003, sol lointain 0,0 ; 49/49 |
| `COMPLETED_EXAMPLES/ch11_09_integration_reference.png` | La plaque (gauche), le départ (milieu : sol 3D opaque, ombre à gauche) et la solution (droite : cube posé dans la plaque, ombre à droite comme le poteau) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sol non catcher, film opaque, ombre du mauvais côté, plaque non composée) |
| `SCRIPTS/validate_ch11_09.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_09_integration_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_09.py" -- --exercise integration
```

## Livrables attendus

1. Plan intégré avec note sur la lumière de la plaque.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.10 — Cohérence visuelle](../CH11_10_CONSISTENCY/README.md)
