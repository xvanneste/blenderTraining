# CH12.06 — Export et livraison

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Livrer un film, c'est produire un fichier que le destinataire peut lire : un conteneur (MP4, MKV…) qui range une piste vidéo (H.264, H.265, ProRes…) et une piste audio (AAC…), à une résolution et une cadence données. Une erreur de réglage ne se voit pas dans Blender : elle se voit dans le fichier. Le correcteur produit le fichier avec vos réglages puis lit ses boîtes MP4 (conteneur, codec vidéo, codec audio, dimensions, durée) avec un petit analyseur écrit pour l'occasion, faute de ffprobe sur la machine.

## Prérequis

- CH12.01–CH12.05 (montage, son).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler un export FFmpeg (conteneur, codecs).
2. Fixer résolution, cadence et plage.
3. Vérifier un fichier livré sans le lire.
4. Connaître les outils complémentaires (sans les tester).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.06.a | Livrer un master | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Conteneur et codecs | 3 h |
| L2 | Vérifier le fichier | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_06_export_starter.blend` | Sortie PNG, 50 %, 30 i/s, plage 1–24 : aucun .mp4 ; 3/17 |
| `COMPLETED_EXAMPLES/ch12_06_export_solution.blend` | MP4, H.264, AAC, 640 × 360, 24 i/s, plage 1–48 : fichier de 62 Ko, 2,006 s ; 53/53 |
| `COMPLETED_EXAMPLES/ch12_06_export_reference.png` | Mesures du fichier exporté de la solution : largeur 640, hauteur 360, durée 2,006 s, poids 62 Ko (barres, de haut en bas) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (mauvais codec vidéo, sans audio, mauvaise résolution, mauvaise cadence, plage trop courte) |
| `SCRIPTS/validate_ch12_06.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_06_export_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_06.py" -- --exercise export
```

## Livrables attendus

1. Fiche de livraison (conteneur, codecs, résolution, cadence, durée, poids).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet P12 — Séquence finalisée](../PROJECT_P12/README.md)
