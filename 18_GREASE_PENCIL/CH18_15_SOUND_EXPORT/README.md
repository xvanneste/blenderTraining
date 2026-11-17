# CH18.15 — Son, rythme, transitions, export, révision

**Phase :** 18 — Grease Pencil (module D : animatique)  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h 30  
**Version :** Blender 5.3.0

## Introduction

Une animatique se juge avec le son. Ce chapitre monte, dans le Video Sequencer, les 12 plans de l'animatique du CH18.14 avec une musique en fondu, des bruitages et une réplique temporaire synchronisés sur les marqueurs, un fondu enchaîné et un fondu au noir, puis l'exporte réellement en MPEG-4 / H.264 / AAC et la révise par des notes précises (code · image · remarque). Le correcteur exporte lui-même une vidéo de contrôle et vérifie qu'elle contient bien le son.

## Prérequis

- CH18.14.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Poser et synchroniser dialogues temporaires, bruitages et musique.
2. Créer fondu enchaîné et fondu au noir sans changer la durée.
3. Exporter une vidéo MPEG-4 / H.264 / AAC avec incrustation.
4. Rédiger des notes de révision exploitables et versionner.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C18.15.a | Animatique sonore exportée | Exercices 1–3 (correcteur avec export réel) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le son de l'animatique | 1 h 15 |
| L2 | Rythme et transitions | 1 h |
| L3 | Export et révision | 1 h 15 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch18_15_edit_starter.blend` | Montage : 12 plans + marqueurs, sans son |
| `ASSETS/ch18_15_audio/` | 4 sons générés (musique, 2 bruitages, réplique temporaire) |
| `ASSETS/ch18_15_panels/` | 12 images de plans (1280 × 720) |
| `COMPLETED_EXAMPLES/ch18_15_edit_solution.blend` | Montage complet |
| `COMPLETED_EXAMPLES/ch18_15_animatic_v001.mp4` | Vidéo exportée (H.264 + AAC) |
| `COMPLETED_EXAMPLES/ch18_15_edit_contact.png` | Images 140, 354, 446 |
| `SCRIPTS/validate_ch18_15.py` | Correcteur (--render : export réel et contrôle du son) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_15_edit_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_15.py" -- --exercise edit --render
```

## Livrables attendus

1. Montage validé.
2. Vidéo v001 exportée + notes de révision.
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Montage validé avec --render.

➡️ Chapitre suivant : [CH18.16 — Animation 2D : principes et image par image](../CH18_16_2D_ANIMATION/README.md)
