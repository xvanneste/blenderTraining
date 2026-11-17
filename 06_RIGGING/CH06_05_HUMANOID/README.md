# CH06.05 — Rig humanoïde

**Phase :** 6 — Rigging professionnel  
**Niveau :** avancé  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Rigify construit un rig humanoïde complet (IK/FK, colonne, visage, doigts, contrôleurs) à partir d'un méta-rig que l'on ajuste au personnage. Ce chapitre rigge le personnage du projet P3 : on ajoute le méta-rig humain, on le met à l'échelle du corps, on génère le rig (706 bones), puis on lie le corps par Automatic Weights. Le correcteur vérifie le rig généré, l'ajustement et la peau, puis DÉPLACE le rig : la racine entraîne tout le corps, le pied gauche levé n'entraîne que le pied gauche.

## Prérequis

- CH06.01
- CH06.03–04
- P3 (personnage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ajouter, ajuster et générer un méta-rig Rigify.
2. Lier le corps au rig généré (bones DEF-).
3. Contrôler un rig par le mouvement.
4. Connaître les limites d'un méta-rig non ajusté (bras en T/A).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.05.a | Rig humanoïde complet | Exercice 2 (correcteur) + croquis du rig et de la jambe levée |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Méta-rig et génération | 3 h |
| L2 | Peau et contrôle du rig | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_05_humanoid_starter.blend` | Corps de P3 et méta-rig non ajusté (1,98 m) |
| `COMPLETED_EXAMPLES/ch06_05_humanoid_solution.blend` | Rig généré et corps lié |
| `COMPLETED_EXAMPLES/ch06_05_humanoid_reference.png` | Croquis de face : bones DEF sur le corps, puis pied gauche levé de 0,25 m |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (rig non généré, corps non lié, méta-rig non mis à l'échelle, sans modificateur, poids partiels, rig décalé) |
| `SCRIPTS/validate_ch06_05.py` | Correcteur (humanoid) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_05_humanoid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_05.py" -- --exercise humanoid
```

## Livrables attendus

1. Rig humanoïde validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.06 — Rig quadrupède](../CH06_06_QUADRUPED/README.md)
