# CH09.08 — Objectifs et focales

**Phase :** 9 — Lighting et cinématographie  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

La focale ne se contente pas de « zoomer » : elle change la façon dont la profondeur est rendue. Avec un grand angle, la caméra est proche et les objets lointains paraissent minuscules ; avec un téléobjectif, la caméra est loin et les plans se compriment : un fond paraît presque aussi grand que le sujet. Ce chapitre relie focale, capteur et champ de vision par le calcul, puis le vérifie par le rendu : le correcteur mesure la hauteur apparente de deux cylindres identiques placés à 8 m et 16 m.

## Prérequis

- CH01 (caméra, rendu), CH09.07 (lecture d'une image mesurée).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Relier focale, taille du capteur et champ de vision.
2. Prévoir la hauteur apparente d'un objet : proportionnelle à focale / distance.
3. Compresser la perspective en reculant et en allongeant la focale.
4. Mesurer l'effet sur un rendu.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C09.08.a | Choisir une focale et une distance de prise de vue | Exercice 2 (correcteur) + calcul |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Focale, capteur, champ | 3 h |
| L2 | Compression de la perspective | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch09_08_lenses_starter.blend` | Focale 35 mm, caméra à 8 m du sujet : le fond (2 fois plus loin) fait 46 % de la hauteur du sujet (théorie : 50 %) |
| `COMPLETED_EXAMPLES/ch09_08_lenses_solution.blend` | Caméra reculée de 24 m (y = −24), focale 144 mm : sujet à 40 % de l'image, fond à 78 % du sujet (théorie : 80 %) |
| `COMPLETED_EXAMPLES/ch09_08_lenses_reference.png` | Rendu de départ (gauche) et solution (droite) : le sujet garde la même taille, le fond grandit |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (grand angle, recul sans zoom, zoom sans recul, focale trop courte, sujet déplacé) |
| `SCRIPTS/validate_ch09_08.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_08_lenses_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_08.py" -- --exercise lenses
```

## Livrables attendus

1. Focale et distance justifiées par le calcul.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH09.09 — Profondeur de champ](../CH09_09_DEPTH_OF_FIELD/README.md)
