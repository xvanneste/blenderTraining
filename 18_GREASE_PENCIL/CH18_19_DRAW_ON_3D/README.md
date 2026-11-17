# CH18.19 — Dessiner dans et sur la 3D

**Phase :** 18 — Grease Pencil (module F : hybride 2D/3D)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h  
**Version :** Blender 5.3.0

## Introduction

Grease Pencil dessine en 3D : ce chapitre place un personnage 2D debout dans un décor 3D (Stroke Placement, Drawing Plane, curseur 3D), peint des éléments directement sur les surfaces (placement Surface), génère les contours du décor avec Line Art et règle l'occlusion au rendu final par la passe Z. Le correcteur mesure pieds au sol, échelle, profondeur, part cachée vue de la caméra (lancer de rayons) et distance des dessins aux surfaces.

## Prérequis

- CH18.06 à CH18.09.
- Phase 1 (navigation 3D, curseur 3D).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Choisir Stroke Placement et Drawing Plane selon l'intention.
2. Dessiner sur des surfaces 3D.
3. Générer des contours avec Line Art.
4. Intégrer un personnage 2D dans un décor 3D avec une occlusion correcte.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.19.a | Personnage 2D dans un décor 3D | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Placement des traits et dessin sur surface | 1 h 30 |
| L2 | Line Art et occlusion | 1 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_19_hybrid_starter.blend` | Décor 3D, objets GP vides, passe Z coupée |
| `COMPLETED_EXAMPLES/ch18_19_hybrid_solution.blend` | Line Art, personnage, décors peints |
| `COMPLETED_EXAMPLES/ch18_19_hybrid_reference.png` | Rendu final (occlusion visible) |
| `SCRIPTS/validate_ch18_19.py` | Correcteur (hybrid) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_19_hybrid_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_19.py" -- --exercise hybrid --render
```

## Livrables attendus

1. Scène hybride validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH18.20 — Workflow 2D → 3D](../CH18_20_2D_TO_3D/README.md)
