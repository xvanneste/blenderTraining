# CH13.02 — L’API bpy

**Phase :** 13 — Python et automatisation  
**Niveau :** intermédiaire  
**Durée estimée :** 3 h de parcours essentiel, puis 45 min de variante  
**Version :** Blender 5.3.0

## Introduction

Deux caisses identiques partagent un maillage. En recolorer une sans affecter l’autre permet d’apprendre à distinguer l’objet de ses données. Vous ajoutez ensuite un repère depuis la console et vérifiez quel objet est actif.

## Prérequis

- CH13.01 (variables et fonctions).
- CH01.04 (objets et données) est utile pour comprendre les copies liées.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Retrouver un objet avec bpy.data indépendamment de la sélection.
2. Lire et régler la sélection et l’objet actif.
3. Copier un datablock maillé au bon moment.
4. Inspecter un opérateur, vérifier son contexte et conserver une référence au résultat.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C13.02.a | Manipuler une scène avec bpy | Exercice 2 et changement de cible expliqué |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Données, sélection et contexte | 1 h 15 |
| L2 | Opérateurs et vérification de la scène | 1 h 45 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices 1 et 2 de [EXERCISES.md](EXERCISES.md) avec les leçons. Le troisième exercice ajoute une variante autonome de 45 min.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch13_02_bpy_starter.blend` | Deux caisses et leur maillage partagé |
| `COMPLETED_EXAMPLES/ch13_02_bpy_solution.blend` | Atelier avec caisses indépendantes et repère |
| `COMPLETED_EXAMPLES/ch13_02_bpy_reference.png` | Image de contrôle |
| `SCRIPTS/validate_ch13_02.py` | Correcteur de la scène |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch13_02_bpy_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch13_02.py" -- --exercise bpy
```

## Livrables attendus

1. Une copie du fichier validée et une phrase expliquant la différence entre objet actif et objet nommé.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.
- Refaire le changement de cible sans le tutoriel et constater que l’autre caisse garde son matériau.

➡️ Chapitre suivant : [CH13.03 — Génération d’objets et matériaux](../CH13_03_MESH_MATERIALS/README.md)
