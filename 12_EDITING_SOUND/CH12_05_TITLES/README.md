# CH12.05 — Titres et sous-titres

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Le Video Sequencer sait écrire : un strip de texte (type TEXT) affiche un texte à une position et une taille données, pendant une durée donnée. Deux usages : le carton-titre (un titre centré, grand, au début du film) et les sous-titres (un texte court en bas de l'image, synchronisé sur la parole). Blender sait aussi exporter les strips de texte au format de sous-titres SRT : le correcteur s'en sert pour comparer vos sous-titres à une référence, texte et temps compris, puis il rend l'image pour vérifier la position et la lisibilité.

## Prérequis

- CH12.01 (VSE), CH12.03 (synchronisation).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un strip de texte et régler son texte, sa taille, sa position.
2. Caler des sous-titres sur des temps donnés.
3. Exporter des sous-titres en SRT.
4. Contrôler la lisibilité par un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.05.a | Titrer une séquence | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le carton-titre | 3 h |
| L2 | Sous-titres et SRT | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_05_titles_starter.blend` | Carton « TITRE » minuscule en haut à gauche, sous-titres sans point, mal placés, en haut ; 3/45 |
| `COMPLETED_EXAMPLES/ch12_05_titles_solution.blend` | Titre « LE LONG VOYAGE » centré (taille 56), sous-titres « Bonjour. » 2,000→3,500 et « Il fait nuit. » 3,750→5,000 en bas (taille 30) ; 45/45 |
| `COMPLETED_EXAMPLES/ch12_05_titles_reference.png` | Le titre (image 18), le premier sous-titre (image 66) et le second (image 105) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (faute de frappe, sous-titre en retard, sous-titres en haut, titre minuscule, titre décentré) |
| `SCRIPTS/validate_ch12_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_05_titles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_05.py" -- --exercise titles
```

## Livrables attendus

1. Fichier SRT exporté.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH12.06 — Export et livraison](../CH12_06_EXPORT/README.md)
