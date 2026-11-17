# CH08.02 — Soft Bodies

**Phase :** 8 — Physique et simulations  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un Soft Body est un maillage qui se déforme sous la gravité comme un objet mou : chaque sommet est une masse reliée à ses voisins par des ressorts (les arêtes). Le GOAL fixe tout ou partie des sommets (poids d'un groupe de sommets) : un poids de 1 accroche le sommet, un poids de 0 le libère. Ce chapitre accroche une plaque par un bord et la laisse pendre : goal sur le groupe « pin », arêtes rigides (Pull, Push, Bending), masse modeste. Le correcteur configure ET simule (100 images) : bord accroché immobile, bord libre qui pend, arêtes non étirées.

## Prérequis

- CH08.01 (corps rigides, simulation pas à pas).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Activer un Soft Body.
2. Accrocher des sommets par un groupe (Goal).
3. Régler les ressorts d'arêtes (Pull, Push, Bending) et la masse.
4. Mesurer l'étirement d'une simulation.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.02.a | Objet mou | Exercice 2 (correcteur) + profils de la plaque |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Ressorts et goal | 3 h |
| L2 | Régler et mesurer | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_02_softbody_starter.blend` | Plaque de 2 × 2 m à 2 m de haut avec son groupe « pin » (bord gauche), sans modificateur |
| `COMPLETED_EXAMPLES/ch08_02_softbody_solution.blend` | Soft Body configuré : la plaque pend par son bord et se balance sans s'étirer |
| `COMPLETED_EXAMPLES/ch08_02_softbody_reference.png` | Profil de la plaque aux images 1, 40 et 100 (vert : bord accroché) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans goal, sans groupe, arêtes molles, masse excessive, sans arêtes) |
| `SCRIPTS/validate_ch08_02.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_02_softbody_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_02.py" -- --exercise softbody
```

## Livrables attendus

1. Plaque en Soft Body validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.03 — Cloth](../CH08_03_CLOTH/README.md)
