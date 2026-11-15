# CH03.02 — Sculpt Mode

**Phase :** 3 — Sculpting et personnages  
**Niveau :** débutant  
**Durée estimée :** 3 h 30  
**Version :** Blender 5.3.0

## Introduction

Premier sculpt : un visage simple sur une sphère dense. Le chapitre présente les brosses de base de Blender 5.3 (Draw, Clay Strips, Inflate, Grab, Snake Hook, Crease Polish, Smooth…), le réglage du rayon et de la force, la symétrie Mirror X, les masques qui protègent et les Face Sets qui organisent. Le correcteur compare chaque sommet à sa position d'origine : relief du nez, orbites creusées, symétrie, zone masquée intacte, Face Sets.

## Prérequis

- CH03.01.
- Phase 1 (navigation, modes).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser les brosses de base, leur rayon, leur force et leur inversion.
2. Sculpter en symétrie.
3. Protéger une zone par un masque.
4. Organiser un sculpt en Face Sets.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C03.02.a | Sculpter un volume simple | Exercice 2 (correcteur) + grille |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Brosses, rayon, force | 1 h 30 |
| L2 | Symétrie, masques, Face Sets : le premier visage | 2 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch03_02_face_starter.blend` | Sphère dense, positions d'origine mémorisées |
| `COMPLETED_EXAMPLES/ch03_02_face_solution.blend` | Visage simple (généré par script) |
| `COMPLETED_EXAMPLES/ch03_02_face_reference.png` | Rendu de contrôle |
| `SCRIPTS/validate_ch03_02.py` | Correcteur (face) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_02_face_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_02.py" --python-exit-code 1 -- --exercise face --render
```

## Livrables attendus

1. Visage simple validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH03.03 — Résolution dynamique](../CH03_03_DYNAMIC_RESOLUTION/README.md)
