# CLAUDE.md — Instructions pour reprendre le développement de l'académie

## Objectif du projet
Construire **Blender Cinema Master Academy** : une formation personnelle, en français,
exhaustive et pratique, qui mène un débutant absolu jusqu'à la réalisation de films
d'animation 3D et au pilotage d'un pipeline de production. 18 phases (0 à 17). Cible :
**Blender 5.3** (installé et vérifié : 5.3.0, hash `02f0899d78e3`).

## Lire en premier à chaque session
1. `PROJECT_STATE.md` — état, décisions, prochaine action. **Source de vérité.**
2. `CURRICULUM.md` — programme et codes de compétences.
3. `TEMPLATES/LESSON_TEMPLATE.md` — structure obligatoire d'un chapitre.
4. `DOCUMENTATION/CONVENTIONS.md` et `DOCUMENTATION/VERSION_COMPATIBILITY.md`.
5. Le chapitre de référence déjà produit : `00_SETUP/CH00_01_INSTALLATION/` (copier son
   niveau de détail et sa structure).

## Environnement vérifié
- Windows 11 Pro, i9-10900 (20 threads), 64 Go RAM, RTX 3080 10 Go (pilote 621.14).
- Blender : `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe` (aussi 3.6, 4.4, 5.0, 5.2).
- Python embarqué Blender : 3.13 · Python système : `C:\Python314\python.exe`.
- Cycles : CUDA + OptiX disponibles. HIP absent (message `HIPEW` normal).
- Pas de FFmpeg système. Git et Node.js présents.
- Manuel Blender hors ligne (RST) fourni par l'extension Blender MCP :
  `%LOCALAPPDATA%\Claude-Data\…\ant.dir.gh.blender.blender-mcp\blmcp\data\manual\`
  (version ~5.1/5.2 : utile pour les libellés, mais revérifier dans 5.3).
- Sources Python de l'UI 5.3 (libellés exacts des menus) :
  `C:\Program Files\Blender Foundation\Blender 5.3\5.3\scripts\startup\bl_ui\` et
  `…\scripts\addons_core\cycles\ui.py` ; raccourcis :
  `…\scripts\presets\keyconfig\keymap_data\blender_default.py`.

## Règles non négociables
- Français clair ; termes d'interface Blender en anglais (traduits à la 1ʳᵉ occurrence).
- **Ne jamais inventer** une fonctionnalité, un menu, un raccourci : vérifier dans l'API
  (`blender -b --factory-startup --python-expr …`), les sources `bl_ui` ou le manuel.
- **Ne jamais annoncer** un script ou un fichier comme fonctionnel sans l'avoir exécuté.
- Tout `.blend` est **généré par un script** `SCRIPTS/build_chNN_MM_files.py` du chapitre,
  avec starter(s) + solution(s) distinctes, et un correcteur `validate_chNN_MM.py`.
- Tester en arrière-plan : `blender -b --factory-startup --python X.py --python-exit-code 1`.
- Ajouter chaque chapitre testable dans `TOOLS/run_all_tests.ps1` (tableau `$Chapters`).
- Enregistrer chaque ressource dans `ASSET_MANIFEST.json`, puis
  `python TOOLS/check_manifest.py --update-hashes`.
- Ressources externes : licence vérifiée (CC0/CC-BY de préférence), provenance notée,
  aucun exécutable, aucun script téléchargé exécuté sans lecture.
- Pas de fichiers vides ni de placeholders ; pas de chapitre « terminé » sans exercices,
  quiz, solutions, dépannage, ressources et mini-projet.
- Un chapitre à la fois : produire → tester → mettre à jour `PROJECT_STATE.md`,
  `PROGRESS.md`, le README de la phase, puis passer au suivant.
- Les durées sont des estimations ; ne jamais promettre qu'un solo produira vite un long-métrage studio.
- IA (phase 14) : vérifier disponibilité, licence, limites de chaque outil au moment de la rédaction.

## Pièges techniques Blender 5.3 déjà rencontrés
- `Material.use_nodes` / `World.use_nodes` : dépréciés (suppression annoncée en 6.0) ;
  les nouveaux matériaux et mondes ont déjà un arbre de nœuds — ne pas y toucher.
- `compute_device_type` des préférences Cycles est une énumération **dynamique** :
  `enum_items` est vide ; tester une liste fixe d'API dans un `try`.
- Après `bpy.ops.wm.open_mainfile`, utiliser des chemins **absolus** pour les sorties.
- Lumières Area/Spot : `obj.visible_camera = False` et viser le sujet (Track To), sinon
  disque lumineux parasite.
- Le premier rendu GPU charge les kernels : faire une passe de chauffe avant de mesurer.
- Les keymaps ne sont pas peuplées en mode `-b` : vérifier les raccourcis dans
  `blender_default.py`.
- PowerShell 5.1 : enregistrer les `.ps1` en **UTF-8 avec BOM** (sinon accents cassés).
- Les `.blend` régénérés changent d'empreinte : `check_manifest.py --update-hashes`.
- Libellés 5.3 à ne pas confondre avec d'anciens tutoriels : snapping = *Snap Base* (Closest/
  Center/Median/Active) et *Snap Target* (+ *Snap Target for Individual Elements* : Face
  Project/Nearest) ; playblast = *View → Render Playblast* ; splash = *Save New Preferences*.
- Toujours vérifier un libellé d'interface dans `5.3/scripts/startup/bl_ui/*.py` avant de l'écrire.
- Les heredocs bash avec apostrophes françaises peuvent échouer : écrire les fichiers avec l'outil Write.
- **Rendre une image de contrôle** de chaque solution et la REGARDER : le correcteur peut être
  vert alors que la scène est fausse (bug CH01.11 : le pignon pris pour la porte).
- Grease Pencil v3 par script : traits OK (rendu EEVEE/Workbench), mais le REMPLISSAGE (Fill)
  de traits créés par script ne s'affiche pas au rendu en arrière-plan (constaté 5.3.0, même
  avec fill_opacity=1 et tag_positions_changed). Exemples générés = hachures (bcma_gp.hatch_ellipse).
