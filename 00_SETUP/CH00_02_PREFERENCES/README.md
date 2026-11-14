# CH00.02 — Préférences essentielles

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant absolu  
**Durée estimée :** 2 h (théorie 35 min · pratique 65 min · évaluation 20 min)  
**Version :** Blender 5.3.0

## Introduction

Les préférences sont le « réglage du siège et des rétroviseurs » avant de conduire. Un artiste qui travaille 2 000 heures dans Blender gagne des dizaines d'heures en réglant une fois pour toutes la navigation, l'interface et la sécurité de ses fichiers. Dans ce chapitre, vous découvrez la fenêtre Preferences, vous appliquez le profil recommandé par l'académie, vous apprenez à revenir en arrière (réglages d'usine) et vous mesurez concrètement le gain de navigation sur une scène d'entraînement : une ville de 400 bâtiments où se cache une aiguille de 25 cm.

## Prérequis

- CH00.01 validé (Blender 5.3 installé, GPU activé).
- Savoir ouvrir un fichier .blend.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Ouvrir, parcourir et rechercher dans la fenêtre Preferences.
2. Comprendre la différence entre préférences (userpref.blend) et fichier de démarrage (startup.blend).
3. Régler l'interface : Resolution Scale, thème, langue, barre d'état.
4. Régler la navigation : Orbit Around Selection, Zoom to Mouse Position, Auto Depth, Auto Perspective, émulations.
5. Sécuriser son travail : Undo Steps, Save Versions, Auto-Save, chemins relatifs.
6. Sauvegarder, annuler et réinitialiser ses préférences sans risque.
7. Auditer et appliquer un profil de préférences par script.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.02.a | Configurer et sauvegarder ses préférences | Exercices 1–2, audit --strict |
| C00.02.b | Restaurer une configuration d'usine et récupérer ses réglages | Exercice 4, quiz |
| C00.02.c | Naviguer efficacement dans une grande scène | Exercice 3 (correcteur), test chronométré |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La fenêtre Preferences et ses sauvegardes | 25 min |
| L2 | Interface : échelle, thème, langue, barre d'état | 20 min |
| L3 | Navigation : orbite, zoom, profondeur, émulations | 35 min |
| L4 | Édition et sécurité : annulation, versions, auto-save, startup file | 25 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch00_02_navigation_playground.blend` | Ville de 400 blocs, aiguille cachée, balise à 1 km, consignes internes (Text Editor) |
| `COMPLETED_EXAMPLES/ch00_02_navigation_solution.blend` | Caméra CAM_Needle cadrant l'aiguille (solution de l'exercice 3) |
| `SCRIPTS/bcma_prefs_profile.py` | Audit / application du profil de préférences de l'académie |
| `SCRIPTS/validate_ch00_02.py` | Correcteur de l'exercice 3 |
| `SCRIPTS/build_ch00_02_files.py` | Régénère les .blend du chapitre |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_02_navigation_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch00_02.py" --python-exit-code 1 -- --exercise needle --render
```

## Livrables attendus

1. Préférences réglées selon le profil (audit sans écart obligatoire).
2. Sauvegarde zip datée de votre dossier config\ (préférences).
3. ch00_02_navigation_<prenom>_v001.blend validé par le correcteur.
4. Fiche de poste complétée, section 5 (préférences).

## Critères pour passer au chapitre suivant

- Quiz ≥ 12/15.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH00.03 — Performances CPU, GPU, mémoire](../CH00_03_PERFORMANCE/README.md)
