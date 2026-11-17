# CH18.22 — Projets de la phase

**Phase :** 18 — Grease Pencil (projets obligatoires)  
**Niveau :** avancé  
**Durée estimée :** 100–200 h (indicatif, projets compris)  
**Version :** Blender 5.3.0

## Introduction

Les 7 projets obligatoires de la phase 18 : planche de 12 cases, dialogue storyboardé, scène d'action de 30 s, animatique d'une minute, animation Grease Pencil de 15 à 30 s, scène hybride 2D/3D, puis storyboard et animatique d'un court de 3 à 5 minutes (repris en phase 15). Un correcteur unique vérifie la structure de chaque projet (--exercise p1 à p7) ; les grilles jugent la qualité. Des exemples techniques montrent la structure attendue, sans servir de modèle artistique.

## Prérequis

- CH18.01 à CH18.21.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Cadrer un projet : intention, périmètre, jalons, versions.
2. Enchaîner board, animatique, son, animation et hybride sur des durées réalistes.
3. Vérifier la structure par le correcteur et la qualité par les grilles.
4. Préparer le projet long réutilisé en phase 15.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.22.a | Projets 1 à 7 de la phase 18 | Correcteur p1–p7 + grilles |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Cadrer un projet | 1 h |
| L2 | Produire et vérifier (projets 1–6) | 60–100 h |
| L3 | Le projet long (n° 7) | 40–80 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_22_project_starter.blend` | Fichier vierge |
| `COMPLETED_EXAMPLES/ch18_22_p2_dialogue_example.blend` | Exemple technique projet 2 |
| `COMPLETED_EXAMPLES/ch18_22_p3_action_example.blend` | Exemple technique projet 3 |
| `COMPLETED_EXAMPLES/ch18_22_p4_animatic_example.blend` | Exemple technique projet 4 |
| `COMPLETED_EXAMPLES/ch18_22_p5_animation_example.blend` | Exemple technique projet 5 |
| `COMPLETED_EXAMPLES/ch18_22_p7_short_example.blend` | Exemple technique projet 7 |
| `SCRIPTS/validate_ch18_22.py` | Correcteur des 7 projets |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "MES_PROJETS\...\mon_projet_v001.blend" `
  --python-exit-code 1 --python "18_GREASE_PENCIL\CH18_22_PROJECTS\SCRIPTS\validate_ch18_22.py" -- --exercise p5
```

## Livrables attendus

1. 7 projets validés (correcteur + grille).
2. Dossiers de projet organisés et versionnés.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- 7 projets validés.

➡️ Chapitre suivant : Phase 18 terminée. Suite : phase 15 (courts métrages) — le projet 7 y est repris.
