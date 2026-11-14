# CH00.06 — Cours théorique : organiser un projet

## 1. Pourquoi l'organisation est une compétence artistique
Un court-métrage de 3 minutes peut compter 40 plans, 60 assets, 300 fichiers `.blend`,
3 000 images rendues, des dizaines de versions de chaque fichier. Sans règles, on perd des
heures à chercher, on écrase la bonne version, on livre une texture manquante. Les films
terminés sont ceux dont l'organisation permet d'avancer sans friction.

## 2. L'arborescence de production BCMA
```
mon_court/
├── .blender_project/        ← créé par Blender 5.3 (File → Project → New)
├── README.md
├── 00_admin/                ← planning, budget, notes de production
├── 01_preprod/
│   ├── script/  design/  storyboard/  animatic/  references/
├── 02_assets/
│   ├── characters/  props/  sets/  materials/  textures/  hdri/  rigs/
├── 03_shots/
│   └── sq010/               ← séquence 010
│       └── sh0010/          ← plan 0010
│           ├── layout/  anim/  fx/  lighting/  comp/  render/
├── 04_edit/   05_sound/{dialogue,sfx,music}/   06_deliveries/   99_archive/
```
Principes :
- **Numéros espacés** (sq010, sq020 ; sh0010, sh0020) : on peut insérer sq015 ou sh0015
  sans renuméroter.
- Préfixes `00_`, `01_`… : l'ordre des dossiers suit l'ordre de fabrication.
- **Assets** (réutilisés dans plusieurs plans) séparés des **plans** (uniques).
- Une **tâche** = un dossier = un fichier de travail versionné.
Le script `bcma_create_project.py` crée cette structure en une commande.

## 3. Le nommage
```
<projet>_<séquence>_<plan>_<tâche>_v<NNN>.blend    mon_court_sq010_sh0010_anim_v003.blend
<projet>_<type>_<nom>_v<NNN>.blend                  mon_court_chr_robot_v012.blend
```
Types d'assets : `chr` personnage, `prp` accessoire, `set` décor, `mat` matériau,
`rig` rig, `fx` effet. Règles : minuscules, `_` comme séparateur, pas d'espace ni d'accent
(certains outils les gèrent mal), version sur 3 chiffres.

**Dans Blender** (DOCUMENTATION/CONVENTIONS.md) : objets `GEO_`, `CAM_`, `LGT_`, `EMP_`,
`CRV_`, `RIG_`, `GP_`, `TXT_` ; collections en MAJUSCULES ; matériaux `MAT_` ; côtés `.L`/`.R`.
Un nom comme `Cube.047` ne dit rien ; `GEO_Table_Leg_FL` dit tout.

Outils de renommage :
- `F2` : renommer l'objet actif.
- Double-clic dans l'Outliner : renommer n'importe quel élément.
- *Edit → Batch Rename…* (`Ctrl+F2`) : renommer en masse (rechercher/remplacer, préfixe,
  suffixe, casse) sur les objets, matériaux, collections… sélectionnés.

## 4. Chemins relatifs et absolus
- **Absolu** : `G:\Films\mon_court\02_assets\textures\bois.png` — casse dès que le projet
  est déplacé, copié sur un autre disque ou envoyé à quelqu'un.
- **Relatif** : `//../../02_assets/textures/bois.png` — `//` signifie « le dossier du
  `.blend` ». Le projet entier peut être déplacé.
- Préférence *Relative Paths* (activée par défaut, CH00.02) : les nouveaux liens sont relatifs.
- Réparer : *File → External Data → Make Paths Relative* ; trouver les fichiers manquants :
  *File → External Data → Find Missing Files* ; rapport : *Report Missing Files*.
- *Pack Resources* (empaqueter les fichiers dans le `.blend`) est pratique pour envoyer un
  fichier unique, mais alourdit le `.blend` et duplique les textures : à éviter en production.

## 5. Le système de projet de Blender 5.3
Nouveauté 5.3 : *File → Project → New… / Open… / Close*.
- Un projet est un **dossier racine** marqué par un sous-dossier caché
  `.blender_project/` contenant `project.toml` (nom, variables, bibliothèques d'assets…).
- Paramètres du projet (quand un projet est ouvert : menu *Project → Settings…*) : nom,
  **variables** de projet (texte, nombres), **bibliothèques d'assets** propres au projet,
  configuration de couleurs (OCIO), image d'accueil (*splash*) personnalisée.
- Préférences liées : *Save & Load → Startup → Remember Last Project* ; sauvegarde
  automatique de la configuration du projet (*Auto-save Project*).
- C'est un système **optionnel et récent** : les notes de version annoncent que d'autres
  fonctions (add-ons par projet…) viendront plus tard. L'arborescence de dossiers et le
  nommage restent la base ; le projet Blender s'y ajoute.

## 6. Bibliothèques d'assets (aperçu)
*Preferences → File Paths → Asset Libraries* (globales) ou bibliothèques du projet : des
dossiers que l'**Asset Browser** affiche pour glisser-déposer matériaux, objets, poses…
Pour l'académie : `ASSETS/` à la racine. Approfondi en CH02.13.

## 7. En production
- Le pipeline (scripts, outils de suivi) **dépend** des noms : un fichier mal nommé est
  invisible pour les outils de rendu automatique, de montage, de contrôle qualité.
- Un **contrôle automatique** (comme `bcma_naming_check.py`) est lancé avant toute
  publication d'un fichier.
