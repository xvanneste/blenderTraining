# CH06.03 — Skinning

**Phase :** 6 — Rigging professionnel  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Le skinning relie un maillage à une armature : chaque sommet reçoit des poids qui disent quels bones l'entraînent. Ce chapitre lie un bras-tube à une armature de deux bones par Automatic Weights, puis contrôle la qualité des poids : sommets tous pesés, poids normalisés, au plus quatre influences, groupes nommés comme les bones. Le correcteur plie réellement le coude de 90° et mesure : racine immobile, bout solidaire de l'avant-bras, coude sans déchirure.

## Prérequis

- CH06.01.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Lier un maillage à une armature (Automatic Weights).
2. Lire et contrôler les poids (groupes de sommets, normalisation, influences).
3. Évaluer un skinning par un test de pliage.
4. Reconnaître les défauts typiques : poids binaires, groupes mal nommés, sommets non pesés.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C06.03.a | Skinning propre | Exercice 2 (correcteur) + croquis des poids et du pliage |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Lier et lire les poids | 2 h 30 |
| L2 | Contrôler par le mouvement | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch06_03_skinning_starter.blend` | Tube et armature non liés |
| `COMPLETED_EXAMPLES/ch06_03_skinning_solution.blend` | Tube lié par Automatic Weights, poids normalisés |
| `COMPLETED_EXAMPLES/ch06_03_skinning_reference.png` | Gauche : poids (rouge = upper, bleu = fore) ; droite : coude plié de 90° |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sommets non pesés, poids non normalisés, poids binaires, groupes inversés, trop d'influences, sans modificateur) |
| `SCRIPTS/validate_ch06_03.py` | Correcteur (skinning) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_03_skinning_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_03.py" -- --exercise skinning
```

## Livrables attendus

1. Skinning validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH06.04 — IK/FK](../CH06_04_IK_FK/README.md)
