# CH11.08 — Tracking et matchmoving

**Phase :** 11 — Compositing et VFX  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Pour poser un objet 3D dans une prise de vue réelle, il faut savoir comment la caméra réelle a bougé. Le tracking suit des points de l'image d'une image à l'autre ; le solveur de caméra (matchmoving) en déduit la position et l'orientation de la caméra à chaque image et la position 3D des points. Ce chapitre traite un plan de synthèse (48 points 3D, caméra qui avance en translation, donc avec de la parallaxe) : vous réglez la focale, détectez et suivez des points, résolvez la caméra. Le correcteur relit vos pistes et relance lui-même la résolution.

## Prérequis

- CH11.01 (compositeur), CH09.08 (focale, capteur).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler la caméra d'un clip (focale, capteur).
2. Détecter et suivre des points.
3. Résoudre la caméra et lire l'erreur de reprojection.
4. Reconnaître un solveur impossible (peu de pistes).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C11.08.a | Résoudre un tracking | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Pistes et caméra du clip | 3 h |
| L2 | Solveur et erreur | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch11_08_tracking_starter.blend` | Clip chargé, aucune piste, focale 24 mm ; 6/36 |
| `COMPLETED_EXAMPLES/ch11_08_tracking_solution.blend` | Focale 35 mm, 15 pistes suivies sur les 40 images, caméra résolue : erreur 0,75 pixel ; 36/36 |
| `COMPLETED_EXAMPLES/ch11_08_tracking_reference.png` | Image 1 du clip avec les pistes (croix rouges) : elles se posent sur les points |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (suivi trop court, mauvaise focale, non résolu, trop peu de pistes) |
| `SCRIPTS/validate_ch11_08.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_08_tracking_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_08.py" -- --exercise tracking
```

## Livrables attendus

1. Pistes et solution commentées (focale, nombre de pistes, erreur).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH11.09 — Intégration 3D/réel](../CH11_09_INTEGRATION/README.md)
