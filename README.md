# 🎬 Blender Cinema Master Academy

**De débutant absolu à réalisateur et superviseur de films 3D.**
Une formation personnelle, progressive et pratique, construite autour de **Blender 5.3**,
pour maîtriser à la fois le logiciel et toute la fabrication d'un film d'animation 3D.

> 👉 **Vous débutez ? Ouvrez [START_HERE.md](START_HERE.md).**

## Trois compétences, développées ensemble
1. **Artistique** : des images, personnages, décors et animations de qualité cinéma.
2. **Technique** : comprendre les outils et résoudre les problèmes de production.
3. **Production** : organiser, accélérer, automatiser et **terminer** des projets ambitieux.

## Le parcours en 18 phases (~1 650 h estimées)
| # | Phase | # | Phase |
|---|---|---|---|
| 0 | [Préparation et installation](00_SETUP/README.md) | 9 | [Lighting et cinématographie](09_CINEMATOGRAPHY/README.md) |
| 1 | [Fondamentaux absolus](01_FUNDAMENTALS/README.md) | 10 | [Rendu et optimisation](10_RENDERING/README.md) |
| 2 | [Modélisation professionnelle](02_MODELING/README.md) | 11 | [Compositing et VFX](11_COMPOSITING_VFX/README.md) |
| 3 | [Sculpting et personnages](03_SCULPTING/README.md) | 12 | [Montage, son et finition](12_EDITING_SOUND/README.md) |
| 4 | [UV, textures et matériaux](04_MATERIALS/README.md) | 13 | [Python et automatisation](13_PYTHON_AUTOMATION/README.md) |
| 5 | [Geometry Nodes](05_GEOMETRY_NODES/README.md) | 14 | [IA appliquée à Blender et au cinéma](14_AI_PRODUCTION/README.md) |
| 6 | [Rigging professionnel](06_RIGGING/README.md) | 15 | [Courts-métrages](15_SHORT_FILMS/README.md) |
| 7 | [Animation 3D](07_ANIMATION/README.md) | 16 | [Longs-métrages](16_FEATURE_FILMS/README.md) |
| 8 | [Physique et simulations](08_SIMULATIONS/README.md) | 17 | [Expertise et spécialisations](17_EXPERT_SPECIALIZATIONS/README.md) |

Programme détaillé : [CURRICULUM.md](CURRICULUM.md) · Calendriers : [ROADMAP.md](ROADMAP.md) ·
Votre suivi : [PROGRESS.md](PROGRESS.md) · État du projet : [PROJECT_STATE.md](PROJECT_STATE.md)

## État actuel
| Élément | État |
|---|---|
| Architecture, cursus, roadmap, conventions | ✅ |
| **CH00.01** Installer, lancer et vérifier Blender | ✅ complet et testé |
| CH00.02 et suivants | ⏳ production chapitre par chapitre |
| Application d'apprentissage locale | ⏳ prévue (après les premiers chapitres) |

## Organisation des dossiers
| Dossier | Contenu |
|---|---|
| `00_SETUP/` … `18_GREASE_PENCIL/` | Les 19 phases, un sous-dossier par chapitre |
| `ASSETS/` | Bibliothèque partagée (modèles, rigs, textures, HDRI, audio…) — chaque entrée est tracée dans `ASSET_MANIFEST.json` |
| `SCRIPTS/` | Scripts Python transverses (les scripts propres à un chapitre sont dans son dossier `SCRIPTS/`) |
| `TOOLS/` | Outils : `run_all_tests.py`/`.ps1`, `check_manifest.py`, `academy_status.py`, `build_site.py` |
| `SITE/` | Application de consultation hors ligne (générée) : ouvrir `SITE/index.html` |
| `TEMPLATES/` | Modèles (leçon, fiches) |
| `QUIZZES/` | Quiz au format JSON (pour l'application) |
| `CHEAT_SHEETS/` | Fiches de révision et de raccourcis |
| `PROJECTS/` | Vos projets de phase |
| `RENDERS/` | Vos rendus |
| `PORTFOLIO/` | Vos meilleures réalisations, prêtes à montrer |
| `DOCUMENTATION/` | Conventions, compatibilité de version, décisions |

## Application de consultation
```powershell
python TOOLS/build_site.py     # régénère SITE/ après chaque nouveau chapitre
```
Ouvrez `SITE/index.html` dans un navigateur : sommaire par phase avec statut réel, lecture des
documents de chaque chapitre, quiz interactifs, recherche, fiches de révision, progression et favoris
(mémorisés dans ce navigateur). Si votre navigateur bloque les fichiers locaux, servez le dossier :
`python -m http.server 8765` à la racine de l'académie, puis `http://localhost:8765/SITE/`.

## Vérifier l'intégrité de l'académie
```powershell
powershell -ExecutionPolicy Bypass -File .\TOOLS\run_all_tests.ps1
```
Régénère les fichiers `.blend`, exécute les correcteurs et vérifie le registre d'assets.

## Principes
- Aucune fonctionnalité inventée : tout est vérifié sur Blender 5.3.0 installé
  ([DOCUMENTATION/VERSION_COMPATIBILITY.md](DOCUMENTATION/VERSION_COMPATIBILITY.md)).
- Aucun script annoncé comme fonctionnel sans avoir été exécuté.
- Aucune ressource externe sans licence vérifiée et tracée.
- Les durées sont des estimations, pas des promesses.
