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
- Après chaque chapitre : `python TOOLS/build_site.py` (application SITE/, testée le 14/11/2026).
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
- Grease Pencil 5.3, REMPLISSAGES : portés PAR TRAIT (attribut de courbe `fill_id` ≠ 0 ; `hide_stroke`
  pour un aplat sans contour) ; `material.grease_pencil.show_fill/show_stroke` sont des vestiges sans
  effet (plus dans l'UI). bcma_gp.polyline(fill=True) gère cela (corrigé en CH18.07 ; l'ancienne note
  « fills impossibles par script » était fausse).
- Calques GP : `use_lights` = True par défaut → sur une feuille sans lampe, couleurs assombries ;
  bcma_gp.sheet() met use_lights = False. Mesurer des couleurs de rendu en tenant compte de cela.
- Renvois entre chapitres : vérifier le **numéro de phase** dans le tableau de CURRICULUM.md
  (0 Setup, 1 Fondamentaux, 2 Modélisation, 3 Sculpt, 4 UV/matériaux, 5 GN, 6 Rigging,
  7 Animation, 8 Simulations, 9 Lighting/ciné, 10 Rendu, 11 Compo/VFX, 12 Montage/son,
  13 Python, 14 IA, 15 Courts, 16 Longs, 17 Spécialisations, 18 Grease Pencil) ;
  citer de préférence le code de chapitre (ex. CH07.14).
- Grease Pencil au RENDU final (EEVEE/Workbench/Cycles, -b ou F12) : sans `view_layer.use_pass_z = True`,
  le GP est dessiné PAR-DESSUS les maillages (viewport correct). Constaté 5.2 et 5.3.0 (CH18.06).
  `stroke_depth_order` n'y change rien. Toute scène hybride : activer la passe Z.
- L'outil Read peut renvoyer une image en cache pour un même chemin : pour revoir un rendu
  régénéré, le copier sous un nouveau nom (scratchpad) avant de le lire.
- Masques de calque GP (5.3) : un calque masque CACHÉ (hide) n'agit plus ; le rendre invisible
  avec opacity = 0 (mesuré, CH18.08). Filtre de calque des modificateurs GP : `tree_node_filter`.
- Libellés 5.3 : onglet Properties « Effects » (pas Visual Effects) ; transform de calque
  « Translation » ; pinceau GP « Size » et « Stroke Mode » (Stroke/Fill/Both).
- Spin (5.3) : Auto Merge soude la couture mais PAS les sommets d'un profil posé sur l'axe → `A`, `M` By Distance
  (mesuré avec l'opérateur réel, CH02.03). Après Spin, seule la dernière copie est sélectionnée.
- Knife modal (5.3) : Shift maintenu = milieux, Ctrl maintenu = sans aimant, A = angles, C = à travers,
  clic droit = nouvelle ligne. Toujours relire la keymap modale avant d'écrire des touches modales.
- Générer les solutions avec les OPÉRATEURS de l'interface quand la consigne les utilise (Grid Fill, Spin) :
  le bmesh peut diverger (grid_fill vide, spin sans doublons d'axe).
- Decimate (Ratio) et moteurs comptent en TRIANGLES (un quad = 2) : mesurer `loop_triangles`, pas les faces.
- `bmesh.ops.create_icosphere(subdivisions=n)` : 20 × 4^(n-1) faces (6 → 20 480) — différent de l'opérateur UI.
- CH02.13 réutilise (append) les solutions de CH02.02/03/05/08/11 : regénérer celles-ci avant CH02.13 ;
  un seul `libraries.load` par fichier source (sinon matériaux dupliqués .001).
- Toujours faire une CONTRE-ÉPREUVE du correcteur (fichier faux refusé), pas seulement starter vide.
- Marqueurs liés à des caméras : ils imposent la caméra active selon l'image ; pour rendre un plan, `scene.frame_set(image du marqueur)`.
- Metadata (stamp) 5.3 : Date, Time, Render Time, Frame, Camera, Scene, Filename… sont COCHÉS par défaut ; pour une
  incrustation propre, tout décocher puis Marker/Frame (bcma : CH18.14 stamp()). Animatique : contact sheets via numpy.
- Line Art GP (5.3) : `radius` du modificateur en MÈTRES (0,004 = invisible à 8 m ; 0,02 lisible) ; évaluer via
  `ob.evaluated_get(depsgraph)` pour compter les traits générés. GP dans un décor : passe Z obligatoire (CH18.19).
- VSE 5.3 : `sequence_editor.strips` / `strips_all`, chemins d'animation `sequence_editor.strips_all["X"].volume` ;
  actions par couches (layers > strips > channelbags > fcurves) ; un export FFmpeg ajoute la plage au nom (…0001-0456.mp4).
- SCULPT 5.3 en arrière-plan (-b) : `mode_set('SCULPT')` passe, mais les opérateurs sculpt/paint (mask_flood_fill,
  face_sets_init…) font PLANTER Blender (EXCEPTION_ACCESS_VIOLATION). Solutions : écrire les attributs directement —
  masque `.sculpt_mask` (POINT, FLOAT), Face Sets `.sculpt_face_set` (FACE, INT) — et déplacer les sommets par script ;
  le dire honnêtement dans SOLUTIONS. Garder la position d'origine dans un attribut (`bcma_orig`) pour mesurer le sculpt.
- Sculpt 5.3 : H = cacher le Face Set actif (HIDE_ACTIVE), Shift+H = bascule isoler/tout montrer, Alt+H = tout afficher ;
  Alt+M = effacer le masque, Ctrl+I = inverser. Vérifier les PROPRIÉTÉS des entrées de keymap, pas seulement la touche.
