# Compatibilité de version

## Version vérifiée (audit du 14/11/2026)

| Élément | Valeur constatée | Méthode de vérification |
|---|---|---|
| Blender cible | **5.3.0** — build `02f0899d78e3`, branche `blender-v5.3-release`, compilé le 10/11/2026 | `blender.exe --version` |
| Statut officiel | Version stable publiée (annoncée le 10–11/11/2026) | Presse spécialisée (CG Channel, Phoronix, 80.lv) + notes développeur `developer.blender.org/docs/release_notes/5.3/` |
| Python embarqué | 3.13.13 | `sys.version` dans Blender |
| Moteur par défaut | `BLENDER_EEVEE` | `scene.render.engine` |
| Transformation de vue par défaut | `AgX` | `scene.view_settings.view_transform` |
| Périphériques Cycles détectés | CUDA + OptiX (RTX 3080), CPU | `preferences.addons['cycles'].preferences.devices` |
| Formats image de sortie | AVIF, JPEG, OPEN_EXR, OPEN_EXR_MULTILAYER, PNG, WEBP, TIFF, HDR, DPX, … , FFMPEG | énumération RNA |
| Accès en ligne (extensions) | désactivé par défaut (`bpy.app.online_access = False` en `--factory-startup`) | `bpy.app.online_access` |

Autres versions installées sur ce poste : **3.6, 4.4, 5.0, 5.2** (dossier
`C:\Program Files\Blender Foundation\`). Elles cohabitent sans conflit : chaque version
a son propre dossier de configuration dans
`%APPDATA%\Blender Foundation\Blender\<version>\`.

## Nouveautés 5.3 utilisées dans le cursus (à revérifier au moment du chapitre concerné)
Sources secondaires concordantes ; chaque fonctionnalité sera vérifiée dans le logiciel
avant d'être enseignée.
- **Vulkan** devient le backend GPU par défaut sous Windows/Linux (CH00.03).
- **Système de projet** optionnel : *File → Project* (CH00.06).
- **Gaussian splats** : import PLY/SPZ, rendu Workbench/EEVEE/Cycles, nœuds *Import SPZ* et
  *Set Point Cloud Type* ; export non pris en charge (CH05, CH14).
- **DLSS 4.5 Ray Reconstruction** comme débruiteur (viewport) sur GPU NVIDIA récents (CH10.03).
- **VSE** : ripple editing, support initial d'OpenTimelineIO (CH12).
- **EEVEE** : nœuds *Material Lighting* (CH10.01).

## Règle de rédaction
1. Une fonctionnalité n'est enseignée que si elle existe dans la version installée
   (vérification par l'API Python, l'interface ou le manuel officiel).
2. Les scripts indiquent en en-tête la version sur laquelle ils ont été testés.
3. Quand une notion diffère entre versions (ex. nom d'un moteur, d'un menu), le cours le
   signale dans un encadré « ⚠️ Versions ».

## Procédure de migration vers une version future (5.4+)
1. Installer la nouvelle version **à côté** de l'ancienne (zip ou installeur, jamais en
   écrasant).
2. Au premier lancement, importer les préférences de la version précédente depuis l'écran
   d'accueil, ou créer des préférences propres (*Save New Preferences*).
3. Lancer `TOOLS/run_all_tests.ps1 -Blender "<chemin du nouveau blender.exe>"` : il
   régénère tous les fichiers de démarrage et exécute tous les scripts de validation.
4. Lire les notes de version (`developer.blender.org/docs/release_notes/<version>/`), en
   particulier la section *Python API* (changements incompatibles).
5. Corriger les scripts en échec, mettre à jour ce fichier et `PROJECT_STATE.md`.
6. Les projets en cours restent sur la version d'origine jusqu'à leur livraison
   (règle studio : on ne change pas de version au milieu d'une production).
