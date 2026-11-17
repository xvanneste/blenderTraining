# CH08.05 — Fluides (Mantaflow)

**Phase :** 8 — Physique et simulations  
**Niveau :** avancé  
**Durée estimée :** 8 h  
**Version :** Blender 5.3.0

## Introduction

Mantaflow simule les fluides dans un DOMAINE : une boîte qui contient le liquide (ou le gaz), alimentée par des objets FLOW (sources) et délimitée par des obstacles (EFFECTOR). La simulation est cuite (bake) : d'abord les données du fluide, puis le maillage de sa surface. Ce chapitre fait tomber un cube de liquide de 0,6 m dans un domaine de 2 m : il tombe sur le fond et s'étale. Le correcteur cuit lui-même la simulation en arrière-plan (dossier temporaire) et lit les maillages du liquide dans le cache : présence, chute, étalement, richesse du maillage.

## Prérequis

- CH08.01–04 (simulations pas à pas).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Créer un domaine de liquide et une source (Flow).
2. Régler la résolution et le cache.
3. Cuire données puis maillage.
4. Lire la surface du liquide dans le cache.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C08.05.a | Liquide simple | Exercice 2 (correcteur) + profils du liquide |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Domaine et source | 4 h |
| L2 | Cuire et mesurer | 4 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch08_05_fluid_starter.blend` | Domaine et source comme simples maillages, sans physique |
| `COMPLETED_EXAMPLES/ch08_05_fluid_solution.blend` | Domaine liquide (résolution 32, cache 1–20, maillage) et source Flow liquide : le cube tombe et s'étale |
| `COMPLETED_EXAMPLES/ch08_05_fluid_reference.png` | Surface du liquide lue dans le cache aux images 1, 10 et 20 (boîte englobante) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (source absente, source de gaz, résolution trop basse, cache trop court) |
| `SCRIPTS/validate_ch08_05.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_05_fluid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_05.py" -- --exercise fluid
```

## Livrables attendus

1. Liquide simple validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH08.06 — Fumée et feu](../CH08_06_SMOKE_FIRE/README.md)
