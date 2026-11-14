# CH00.05 — Extensions et add-ons

**Phase :** 0 — Préparation et installation  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Blender s'enrichit d'add-ons : certains sont livrés avec lui (Node Wrangler, Rigify, importeurs), des milliers d'autres sont distribués sous forme d'extensions depuis la plateforme officielle extensions.blender.org. Une extension, c'est du code exécuté avec vos droits : ce chapitre vous apprend à les activer, à les évaluer et à les installer en sécurité, puis à comprendre comment elles sont construites, à partir d'une petite extension de l'académie (BCMA Hello) que vous installerez vous-même.

## Prérequis

- CH00.02 validé (préférences sauvegardées).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer add-on, extension et dépôt.
2. Activer les add-ons livrés utiles à la formation (Node Wrangler, Rigify).
3. Gérer l'accès en ligne et installer une extension depuis le catalogue ou depuis le disque.
4. Évaluer une extension : source, licence, permissions, lecture du paquet.
5. Comprendre la structure d'une extension (manifeste, register) et la construire avec l'outil officiel.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C00.05.a | Installer, évaluer et désinstaller une extension en sécurité | Exercices 1–3, quiz |
| C00.05.b | Lire et construire une extension simple | Leçon 3, défi 1 |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le système d'extensions et les add-ons livrés | 25 min |
| L2 | Installer en sécurité | 30 min |
| L3 | Anatomie d'une extension | 20 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `ASSETS/bcma_hello/` | Source de l'extension d'exemple (manifeste + code commenté) |
| `ASSETS/bcma_hello-1.0.0.zip` | Paquet installable construit par `blender -c extension build` |
| `SCRIPTS/bcma_extensions_report.py` | Inventaire des dépôts et add-ons activés |
| `SCRIPTS/test_bcma_hello.py` | Test automatique de l'extension sans l'installer |

## Livrables attendus

1. Node Wrangler et Rigify activés.
2. Extension BCMA Hello installée, testée puis désinstallée.
3. Politique d'extensions (mini-projet).

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH00.06 — Organisation de projet](../CH00_06_PROJECT_ORGANIZATION/README.md)
