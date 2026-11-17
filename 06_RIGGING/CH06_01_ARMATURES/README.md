# CH06.01 — Armatures et bones

**Phase :** 6 — Rigging professionnel  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Un rig commence par un squelette bien construit : des bones aux bons endroits, bien nommés, bien parentés, symétriques. Ce chapitre construit l'armature humanoïde de 25 bones du mannequin de CH03.10 (1,76 m, pose en A) : colonne, cou, tête, bras et jambes en .L/.R, hiérarchie et connexions conformes, roll nul, symétrie au millimètre, pose de repos propre. Le correcteur vérifie noms, côtés, parents, connexions, miroirs, taille, pieds au sol, déformation et pose de repos.

## Prérequis

- CH03.10 (personnage prêt pour le rig).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer des bones en Edit Mode et comprendre tête, queue et roll.
2. Appliquer la convention de nommage (.L/.R, spine.001…).
3. Construire la hiérarchie et choisir les connexions (Connected).
4. Obtenir une symétrie exacte et une pose de repos propre.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.01.a | Construire une armature | Exercice 2 (correcteur) + croquis comparé au mannequin |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Bones, hiérarchie, nommage | 3 h |
| L2 | Symétrie, pose de repos, vérification | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_01_armature_starter.blend` | Armature sale (noms Bone.00x, pas de côté droit) + mannequin REF_Body |
| `COMPLETED_EXAMPLES/ch06_01_armature_solution.blend` | Armature RIG_Hero de 25 bones |
| `COMPLETED_EXAMPLES/ch06_01_armature_reference.png` | Croquis de face et de profil : bones sur le mannequin (orange .L, bleu .R, jaune axe) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (côté droit manquant, noms, asymétrie, bone non parenté, colonne déconnectée, pose sale, root qui déforme) |
| `SCRIPTS/validate_ch06_01.py` | Correcteur (armature) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_01_armature_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_01.py" -- --exercise armature
```

## Livrables attendus

1. Armature validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.02 — Contraintes](../CH06_02_CONSTRAINTS/README.md)
