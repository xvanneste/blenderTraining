# CH00.07 — Cours théorique : sauvegardes, récupération, versions, formats

## 1. Les cinq filets de sécurité de Blender
| Filet | Ce qu'il protège | Durée de vie | Où |
|---|---|---|---|
| **Annulation** `Ctrl+Z` / `Shift+Ctrl+Z` | Les dernières actions | Jusqu'à la fermeture | Mémoire (Undo Steps, CH00.02) |
| **Auto Save** | Le travail non enregistré si Blender plante | Écrasé toutes les N minutes | Dossier temporaire (`%TEMP%`), fichier `<pid>_autosave.blend` ou `<nom>.blend` en autosave |
| **quit.blend** | La session au moment où l'on a quitté | Écrasé à chaque fermeture | Dossier temporaire → *File → Recover → Last Session* |
| **.blend1, .blend2** (*Save Versions*) | L'avant-dernier enregistrement | Écrasé à chaque `Ctrl+S` | À côté du `.blend` |
| **Versions incrémentales** `_v001`, `_v002`… | Tout l'historique décidé | Permanent | Vos dossiers |

Récupérer :
- *File → Recover → Last Session* : rouvre l'état au moment où vous avez quitté.
- *File → Recover → Auto Save…* : choisit un fichier d'auto-sauvegarde.
- `.blend1` : *File → Open*, puis dans le navigateur de fichiers afficher les sauvegardes
  (menu de filtre ⏷ → cocher **Backup .blend1** … selon la version) ou, plus simple,
  **copier** le `.blend1` dans l'explorateur et renommer la copie en `.blend`.
⚠️ Limites documentées de l'Auto Save : il n'enregistre pas les changements en cours en
mode Sculpt, Texture Paint et Edit Mode. Sortez régulièrement de ces modes.

## 2. Versionner : la règle d'or de production
- On **n'écrase jamais** une version publiée : on crée la suivante (`Ctrl+Alt+S` = *Save
  Incremental*, qui transforme `…_v003.blend` en `…_v004.blend`).
- Quand incrémenter : avant une modification risquée, à chaque étape validée, en fin de
  séance, avant d'envoyer un fichier.
- Notez ce qui a changé (fichier `CHANGELOG.md` du plan, ou note dans le Text Editor du `.blend`).
- Stockage : un `.blend` de 50 Mo × 100 versions = 5 Go. On **archive** (`99_archive/`) ou
  on supprime les versions intermédiaires d'un plan livré, jamais celles en cours.

## 3. Sauvegarder pour de vrai : la règle 3-2-1
- **3** copies de vos données (l'original + 2 sauvegardes),
- sur **2** supports différents (disque interne + disque externe / NAS),
- dont **1** hors site (cloud, disque gardé ailleurs).
Pourquoi : un disque meurt, un câble arrache un disque externe, un cambriolage ou un
dégât des eaux emporte tout ce qui est au même endroit, un rançongiciel chiffre tout ce qui
est branché. Un fichier synchronisé n'est **pas** une sauvegarde : une suppression se
synchronise aussi. Vérifiez vos sauvegardes en **restaurant** de temps en temps.

Outil de l'académie : `SCRIPTS/bcma_backup.py` (zip daté, vérifié, rotation des N
dernières archives, exclusion des fichiers régénérables comme les rendus et les `.blend1`).
Planification possible avec le *Planificateur de tâches* Windows (CH13 automatisera
davantage).

### Git et Git LFS (aperçu)
Git versionne les **scripts** et les fichiers texte à merveille. Pour les `.blend` (binaires,
lourds), Git **LFS** (*Large File Storage*) est nécessaire et les fusions sont impossibles :
Git sert alors d'historique, pas d'outil de travail collaboratif sur le même fichier.
Recommandation : Git pour `SCRIPTS/`, `TOOLS/`, documentation ; sauvegardes zip + versions
incrémentales pour les `.blend`. (Approfondi en CH16.03.)

## 4. Les formats de fichiers à connaître
| Format | Type | Contient | Usage dans le pipeline |
|---|---|---|---|
| `.blend` | Natif Blender | Tout (scènes, données, réglages) | Travail quotidien |
| **USD** (`.usd/.usda/.usdc/.usdz`) | Ouvert (Pixar) | Scènes, hiérarchies, matériaux, animation, variantes | Échanges de studio, assemblage de scènes |
| **Alembic** (`.abc`) | Ouvert | Géométrie animée « cuite » (cache) | Passer l'animation au lighting/FX sans le rig |
| **FBX** (`.fbx`) | Propriétaire (Autodesk) | Maillages, squelettes, animations | Moteurs de jeu, autres logiciels |
| **glTF 2.0** (`.glb/.gltf`) | Ouvert (Khronos) | Maillages PBR, animations | Web, temps réel, partage |
| **OBJ** (`.obj` + `.mtl`) | Ouvert, simple | Maillage statique + matériaux basiques | Échange universel de modèles |
| STL / PLY | Ouverts | Maillage (PLY : couleurs de sommets, splats) | Impression 3D, scans |
| **OpenEXR** (`.exr`) | Ouvert | Images en virgule flottante, multicouches | Rendu pour compositing |
| PNG | Ouvert | Image 8/16 bits sans perte, transparence | Textures, rendus finaux 8 bits |
| JPEG | Ouvert | Image compressée avec perte | Références, aperçus (jamais pour le compositing) |
| WAV / FLAC | Ouverts | Audio sans perte | Son de production |
Règles : **travail en `.blend`**, **échange en USD/Alembic/FBX/glTF selon la cible**, **rendus
en EXR** (production) ou PNG (simple), **jamais de JPEG dans la chaîne de fabrication**.
