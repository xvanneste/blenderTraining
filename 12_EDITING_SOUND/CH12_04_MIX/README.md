# CH12.04 — Mixage

**Phase :** 12 — Montage, son et finition  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Mixer, c'est équilibrer les sons pour que le spectateur entende ce qu'il doit entendre. Trois gestes de base : régler les niveaux (la voix domine, la musique reste en dessous), baisser la musique pendant la voix (ducking : le volume est animé) et placer les sons dans l'espace stéréo (panoramique). Enfin le niveau global ne doit ni être trop faible ni approcher le maximum. Le correcteur mixe chaque strip seul puis l'ensemble, et mesure le RMS par fenêtres d'images, la balance gauche/droite et la crête.

## Prérequis

- CH12.03 (son).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Régler les niveaux de trois sons.
2. Animer le volume d'un strip (ducking).
3. Placer un son à gauche ou à droite (pan).
4. Contrôler un mixage par des mesures.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C12.04.a | Mixer | Exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Niveaux et ducking | 3 h |
| L2 | Panoramique et niveau global | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch12_04_mix_starter.blend` | Tous les sons à volume 1 et au centre : la musique écrase la voix (voix 0,137 pour musique 0,156), RMS global 0,157 ; 14/56 |
| `COMPLETED_EXAMPLES/ch12_04_mix_solution.blend` | MUSIC volume 0,3 avec ducking (0,1 pendant la réplique), VOICE 1, HIT pan −1 à 0,8 : musique 0,040, ducking 0,40, voix 8,7 × la musique, pan gauche, RMS 0,077, crête 0,60 ; 56/56 |
| `COMPLETED_EXAMPLES/ch12_04_mix_reference.png` | Enveloppes par strip : départ (haut : musique bleue forte sous la voix jaune) et solution (bas : musique basse, voix dominante) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans ducking, musique trop forte, sans pan, mixage trop chaud, mixage trop faible) |
| `SCRIPTS/validate_ch12_04.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_04_mix_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_04.py" -- --exercise mix
```

## Livrables attendus

1. Fiche de mixage (volumes, pan, ducking).
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH12.05 — Titres et sous-titres](../CH12_05_TITLES/README.md)
