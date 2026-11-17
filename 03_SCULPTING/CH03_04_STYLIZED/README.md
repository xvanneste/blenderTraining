# CH03.04 — Sculpture stylisée

**Phase :** 3 — Sculpting et personnages  
**Niveau :** intermédiaire  
**Durée estimée :** 4 h  
**Version :** Blender 5.3.0

## Introduction

Styliser, c'est choisir : une intention, une forme dominante (cercle, carré, triangle), des contrastes nets de tailles. Ce chapitre construit un buste « grosse tête » : blocage en volumes qui se chevauchent (ou en métaballes), Voxel Remesh, orbites creusées par Boolean, socle plat par Bisect, puis plans nets au sculpt. Le correcteur mesure le volume fermé, le socle, le cou, la stylisation (tête, contraste tête/épaules), le relief du nez et la symétrie.

## Prérequis

- CH03.01 à CH03.03.
- CH18.03 conseillé (silhouettes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Concevoir un personnage stylisé à partir d'une idée et d'un langage de formes.
2. Bloquer rapidement par primitives, métaballes et booléens.
3. Créer un socle propre et un volume fermé.
4. Sculpter des plans nets en gardant une silhouette lisible.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.04.a | Sculpter un buste stylisé | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Design et langage des formes | 1 h |
| L2 | Bloquer et finir un buste | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_04_bust_starter.blend` | Studio, 3 caméras, planche de design |
| `COMPLETED_EXAMPLES/ch03_04_bust_solution.blend` | Buste stylisé (SCULPT_Bust) |
| `COMPLETED_EXAMPLES/ch03_04_bust_reference.png` | Face, 3/4, profil |
| `SCRIPTS/validate_ch03_04.py` | Correcteur (bust) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_04_bust_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_04.py" -- --exercise bust --render
```

## Livrables attendus

1. Buste stylisé validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH03.05 — Sculpture réaliste](../CH03_05_REALISTIC/README.md)
