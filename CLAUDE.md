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
- Tester en arrière-plan : `blender -b --factory-startup --python-exit-code 1 --python X.py`.
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
- Join (Ctrl+J / `bpy.ops.object.join`) : le résultat garde l'ORIGINE de l'objet actif (pas (0,0,0)) ; si vos cotes sont en
  coordonnées monde, faire `ob.data.transform(ob.matrix_world)` puis `ob.matrix_world = Matrix()` (bug CH03.05 : buste décalé de 5 cm,
  yeux « au-dessus » du visage, détecté seulement en REGARDANT le rendu).
- Boolean (5.3) solveurs : Float / Exact / Manifold. `EXACT` a renvoyé un maillage VIDE (0 sommet) sur un maillage fermé voxel-remeshé
  (CH03.05) alors que `MANIFOLD` réussit : toujours tester `len(vertices)` après `modifier_apply` (garde-fou + repli Manifold).
- Grease Pencil posé via bcma_gp : les points sont déjà en (x, 0, z) dans l'espace local ; AJOUTER `rotation_euler.x = 90°` les couche
  à plat sur le sol (vu de face = invisible). Bug trouvé dans CH03.04 ET CH03.05 par un rendu du starter : rendre aussi les starters.
- Un objet dont on a fait Ctrl+A > Location a `matrix_world.translation == 0` : pour situer un œil/une sphère, utiliser le centre de sa
  boîte englobante en coordonnées monde, pas son origine.
- Brosses sculpt 5.3 (asset essentials) : PAS de « Crease » seul → *Crease Sharp*, *Crease Polish* (Shift+C) ; *Draw Sharp* ; *Fill/Deepen* ;
  *Relax Slide* ; *Flatten/Contrast*. Raccourcis : V Draw, S Smooth, P Pinch/Magnify, I Inflate/Deflate, G Grab, Shift+T Scrape/Fill,
  C Clay Strips, K Snake Hook, M Mask ; Ctrl+clic = inverser, Shift+clic = Smooth temporaire ; Ctrl+R Voxel Remesh, R taille du voxel.
- CORRECTEUR de mesure (contre-épreuve CH03.05) : un seuil sur une grandeur « mélangée » est vert à tort (le buste sans plis passait parce
  que le grain comptait aussi) ; isoler chaque niveau (comptage de creux pour les plis, MÉDIANE pour le grain), construire des
  contre-exemples CHIRURGICAUX (un seul défaut à la fois) et exiger qu'ils échouent sur LE test visé seulement. Construire aussi une variante
  « selon le tutoriel » et la valider : elle a révélé un tutoriel qui donnait un socle refusé.
- Lissage de Taubin (λ=0,5 / μ=−0,53, ≈ 45 itérations à 2,5 mm) pour fondre des blocs sans rétrécir le volume (≠ Laplacien simple).
- Objet CACHÉ dans la vue (`hide_viewport = True`) : Blender ne l'ÉVALUE PAS. Conséquences mesurées : (1) un collider caché ne collisionne pas (le tissu
  traverse le corps, CH03.08) → `display_type = 'WIRE'` + `hide_render = True` ; (2) sa `matrix_world` n'est pas à jour à l'ouverture → utiliser
  `matrix_basis` (CH03.06, REF_Base).
- Correcteur DIFFÉRENTIEL : pour des détails de 1–5 mm sur un volume complexe, une mesure « absolue » (creux vs surface lissée, résidu d'un ajustement
  quadratique) ne sépare PAS un travail sculpté d'un travail non sculpté. Embarquer dans le starter une copie cachée (`REF_Base`) et mesurer l'écart signé
  (BVHTree.find_nearest + normale) région par région (CH03.06). Calibrer avec des contre-exemples chirurgicaux (un défaut à la fois).
- bmesh.ops.inset_region renvoie les faces de l'ANNEAU ; la région d'origine devient le centre (à supprimer pour faire un trou) (CH03.09).
- Projection (Shrinkwrap Project / ray_cast) : un sommet qui ne touche rien reste sur le plan de départ et étire les quads ; retirer ces faces d'abord ;
  mais ne pas filtrer par inclinaison les parois d'orbite / de bouche (zones protégées).
- Pour séparer des doigts/orteils : compter les PICS de la silhouette (profil y max par tranche de x) avec proéminence ; garder ≥ 5 mm entre orteils
  (le Voxel Remesh referme les écarts < 2 voxels) ; calculer les positions à partir des RAYONS (CH03.07).
- Couper un ellipsoïde pour obtenir une semelle plane : faire des PATINS plats centrés sur z = 0 (couper près du pôle donne 39 cm², et déplacer les ellipsoïdes
  disloque le maillage) (CH03.07). `bm.verts[::k]` n'existe pas : boucler sur des indices.
- Simulation de tissu en arrière-plan : `sc.frame_set(f)` en boucle puis `bpy.ops.object.modifier_apply(modifier="Cloth")` fonctionne (≈ 20 s pour 120 images, 1 700 sommets).
  Réglages stables : Quality 12, Bending 0,4, damping 5, collision Quality 5 / Distance 5 mm, auto-collision OFF (sinon vibration/dentelures) ; tissu de 0,66 m
  sur le buste (plus grand : nappe sur le sol). Mesures de contrôle : sommets dans le corps, arête / repos, couverture, rugosité locale (90e centile).
- Guides Grease Pencil à plat (vue de dessus) : rotation −90° autour de X (z → y) ; vérifier en RENDANT le starter (CH03.07 : le 1er guide était décentré / tourné).
- Starter ET solution à rendre : un fichier de départ dont la consigne visuelle est invisible n'est pas livrable (bug trouvé 3 fois en phase 3).
- Ne jamais citer un ouvrage dont le titre n'est pas vérifié (retiré de CH03.08/09/10) ; vérifier les libellés Physics > Cloth, Shrinkwrap (API/bl_ui) avant de les écrire.
- Les .py de documents contenant des apostrophes : les écrire avec l'outil Write puis les exécuter (les heredocs bash échouent).
- `bpy.ops.object.transform_apply` ÉCHOUE SILENCIEUSEMENT sans objet sélectionné/actif : pour déplacer/remettre à l'échelle des sommets en script, utiliser
  `ob.data.transform(Matrix)` puis remettre `ob.location = (0, 0, 0)`. Bug de CH03.05 (translation de −5 mm restée sur l'objet, plis décalés de 5 mm, seuils calibrés
  sur des positions fausses) : après correction, TOUT ce qui en dépendait a été recalibré (CH03.05, 06, 08, 09). Toujours relire les mesures après un changement de fond.
- Une mesure de correcteur doit être SPÉCIFIQUE à sa zone : la région « narines » attrapait la ligne de bouche et les plis dès qu'ils ont été remis à leur vraie place ;
  resserrer la région et vérifier que le contre-exemple « sans X » tombe à 0 (pas seulement « plus bas »).
- Tissu simulé : un carré de 0,54 m (maille 1,6 cm) tombe sur les épaules sans toucher le sol ; un disque découpé dans la grille donne un bord en escalier PIRE
  (dentelures régulières) : garder le carré.

- **Blender 5.2 EN INTERFACE via le MCP = les opérateurs de sculpt FONCTIONNENT** (alors qu'ils plantent en 5.3 `-b`). Mise en route : lancer
  `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` SANS `--factory-startup` (l'extension `mcp` est une extension utilisateur ; elle démarre seule et écoute
  `127.0.0.1:9876`), puis outils `mcp__Blender__*` (charger via ToolSearch). Le fichier de 5.3 s'ouvre avec l'avertissement « written by newer binary » (testé sur le starter CH03.06 :
  74 170 faces intactes). Ne PAS sauvegarder par-dessus les fichiers de l'académie depuis la 5.2 sans l'avoir décidé.
  Recette vérifiée : vue 3D en ORTHO face (`rv3d.view_rotation = Quaternion((√½, √½, 0, 0))`), `bpy.ops.object.mode_set(mode='SCULPT')` ; brosse par asset :
  `bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', relative_asset_identifier="brushes/essentials_brushes-mesh_sculpt.blend/Brush/Crease Sharp")` ;
  rayon en MÈTRES : `br.use_locked_size='SCENE'; br.unprojected_size=0.003` (pas `unified_paint_settings` du ToolSettings : il est sous `ts.sculpt.unified_paint_settings`) ;
  trait : `bpy.ops.sculpt.brush_stroke(stroke=[{name, location(3D surface), mouse, mouse_event, pressure, size, x_tilt, y_tilt, time, is_start}], mode='NORMAL'|'INVERT')`
  dans un `temp_override(window, area, region, active_object, object)` (PAS de clé `pen_flip` en 5.2). Pour relire les sommets : basculer OBJECT↔SCULPT.
  `paint.mask_flood_fill`, `sculpt.brush_stroke` : FINISHED. Amplitudes mesurées d'UN trait (rayon 3–4 mm, force 1) : Crease Sharp ≈ 0,4–0,8 mm, Draw Sharp ≈ 1,1 mm, Draw ≈ 1,8 mm,
  Clay Strips ≈ 0,5 mm ; Crease Sharp SATURE vers −1,2 mm au centre après ~9 passes (−2,9 mm au plus profond). Conséquence : les solutions « scriptées » (plis de 2,6–5,5 mm) sont plus
  profondes que ce qu'un apprenant obtient à la brosse ; des solutions sculptées pour de vrai demanderaient de recalibrer les seuils des correcteurs.
- **CORRECTIONS de la recette Blender 5.2 / MCP (CH03.02, prime sur les lignes précédentes)** : (1) `location` d'un élément de `sculpt.brush_stroke` = coordonnées LOCALES de l'objet
  (monde ≈ local ne se voyait pas sur un objet près de l'origine ; sinon 0 sommet déplacé sans erreur) ; (2) rayon EFFECTIF ≈ ⅓ du `unprojected_size` : pour des volumes de visage
  (1 m de rayon) utiliser 0,3–0,7 ; (3) bons outils : `Inflate/Deflate` gros rayon = volumes lisses, `Draw` trait court = arêtes, `Smooth` = fondre, `Mask` ×3 passes depuis la vue arrière
  (0,90 de moyenne), `sculpt.face_sets_create(mode='MASKED')` = Face Sets ; MAUVAIS : touches répétées au même point (pointes), longs traits de Draw (crêtes), gribouillis circulaires
  (anneaux) ; (4) `bpy.app.driver_namespace` est VIDÉ à chaque `open_mainfile` : recharger `SCRIPTS/mcp_sculpt.py` (`H={}; exec(open(...).read(), H)`) ; la 1re `mode_set` après ouverture
  échoue parfois : rappeler `enter_sculpt` ; (5) lancer Blender en fenêtre normale (`-WindowStyle Maximized`) ; (6) toujours RENDRE et REGARDER : deux versions « vertes » étaient laides.
  Solution sculptée = fichier enregistré par la 5.2 + marqueur `COMPLETED_EXAMPLES/.sculpted_with_mcp` pour que `build_*.py` ne l'écrase pas (le correcteur 5.3 la valide normalement).
- UV en script 5.3 `-b` : `uv.unwrap(method='ANGLE_BASED')`, `uv.average_islands_scale()`, `uv.pack_islands(margin, rotate, scale)` FONCTIONNENT (Edit Mode + tout sélectionné) ; pour packer un GROUPE, sélectionner ses faces (bmesh `select_set` + `select_flush`) puis `pack_islands`.
  Étirement par triangle = rapport des valeurs singulières de J = B·A⁻¹ (3D→UV) ; chevauchement = rastérisation 1024² (union / somme) ; `bpy.data.images.new(...)` n'a pas `generated_type` (l'affecter après) ; images UDIM : `new(tiled=True)` puis `tiles.new(1002, label=…)` (taille nulle tant que non utilisée).
  Piège : un index de matériau/groupe assigné par ORDRE de faces est faux après un `bisect`/`holes_fill` : l'assigner par géométrie.

- TEXTURE PAINT 5.2 via MCP (CH04.06) : `bpy.ops.paint.image_paint(stroke=[…], mode='NORMAL')` dans un `temp_override(window, area, region, active_object, object)` ; chaque élément exige
  `location` (3D monde) + `mouse`/`mouse_event` (px région, via `location_3d_to_region_2d`), PAS de `pen_flip`. Après `open_mainfile`, appeler `bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)`
  (dans un override) après chaque changement de vue, sinon la projection est périmée (peinture au mauvais endroit : seul le RENDU l'a montré). `brush.color` est LINÉAIRE (0,8 → 0,906 sRGB dans l'image) :
  convertir. Brosses : `brushes/essentials_brushes-mesh_texture.blend/Brush/Paint Hard` (liste : Paint Soft, Airbrush, Fill, Erase Hard, Blur, Smear, Clone…). Image générée → `img.pack()` avant d'enregistrer.
  `ts.image_paint.unified_paint_settings` (pas `ts.unified_paint_settings`). Marqueur `.painted_with_mcp` comme pour le sculpt.
- BAKE 5.3 `-b` (CH04.07) : `bpy.ops.object.bake(type='NORMAL')` FONCTIONNE (Cycles CPU, `render.bake.use_selected_to_active`, `cage_extrusion`, `margin`, `normal_space='TANGENT'`) : HIGH sélectionné, LOW actif, Image Texture cible ACTIVE (`nodes.active`).
  Changer `image.colorspace_settings.name` APRÈS avoir écrit les pixels d'une image générée REMET le tampon à zéro (image noire, `pack()` sans effet) : régler l'espace d'abord. `mathutils.noise.fractal(pos, H, lacunarity, octaves)`.
- GEOMETRY NODES 5.3 `-b` (CH05.01–02) : arbre = `bpy.data.node_groups.new(nom, "GeometryNodeTree")` + `ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")` ; modificateur `ob.modifiers.new("GeometryNodes", "NODES")` puis `.node_group = ng` ;
  évaluer : `ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()` (+ `to_mesh_clear()`). La géométrie GÉNÉRÉE n'a pas les matériaux du maillage d'origine : ajouter `GeometryNodeSetMaterial`.
  Les primitives sont centrées sur l'origine. Un nœud sans sortie utilisée = orphelin (`not any(o.links for o in n.outputs)`). Mesurer par composante connexe (BFS) pour détecter une pièce trop courte.
- Modificateur Nodes 5.3 : `md[id]` ne marche plus (TypeError IDProperties) ; valeurs = `md.properties.inputs[item.identifier]["value"]` (groupe d'IDProperties : value, type, attribute_name). Interface : `ng.interface.new_socket(nom, in_out, socket_type, parent=panneau)`,
  `new_panel(nom)`, attributs `default_value/min_value/max_value/description`. Tester un outil en CHANGEANT ses paramètres puis en mesurant la géométrie évaluée (sinon une entrée codée en dur passe inaperçue).
- Distribute Points on Faces : sockets selon `distribute_method` (POISSON : Distance Min, Density Max, Density Factor ; RANDOM : Density) ; `KDTree.find_n(p, 2)[1][2]` = distance au plus proche voisin.
- Geometry to Instance : une MULTI-entrée est lue en sens INVERSE de l'ordre de création des liens (l'indice 0 = la dernière géométrie reliée) : vérifier par `Pick Instance` + mesure (CH05.07, P5).
- Nœud Cone (GN) : base à z = 0 (z de 0 à Depth) ≠ Cylinder centré ; `inst.object.bound_box` d'une instance GN est peu fiable : lire `inst.object.data.vertices`. Le CHRONOMÉTRAGE en `-b` est trompeur (évaluation paresseuse) : mesurer des budgets (sommets, instances, triangles).
  Repeat zone : `ri.pair_with_output(ro)` ; `Iteration` en sortie du Repeat Input ; Caméra par défaut clip_end = 100 m (une ville de 110 m est coupée : régler `cam.data.clip_end`).
- L.studio() crée DÉJÀ un EMP_Target (visée de caméra) : un Empty du même nom devient EMP_Target.001 ; renommer celui du studio (EMP_Studio) avant (CH06.02). L.reset ne supprime pas les orphelins.
- IK en script (CH06.04) : une chaîne PARFAITEMENT droite est une singularité (le solveur la laisse droite) → pré-fléchir ; `pose_bone.location` est exprimé dans le repère de REPOS du bone (utiliser `bone.matrix_local.to_3x3().inverted() @ delta`) ; driver : `ob.driver_add('pose.bones["fore"].constraints["IK"].influence')` + variable SINGLE_PROP (data_path 'pose.bones["switch"]["ik_fk"]').
- Rigify en 5.3 -b (CH06.05) : `bpy.ops.preferences.addon_enable(module='rigify')`, `armature_human_metarig_add()` (159 bones, 1,98 m, bras en T), `bpy.ops.pose.rigify_generate()` (5 s, 706 bones, objet « rig » ou RIG_* selon le fichier) ; la génération place le rig à l'ORIGINE (la position du méta-rig est ignorée) ; `parent_set(ARMATURE_AUTO)` ne pèse que sur les DEF-.

- **Phase 6/7 (rigging, animation) — pièges 5.3** :
  - Générateur de documents : `TOOLS/docgen.py` (`make(SPEC)` produit chapter.json, quiz, THEORY, TUTORIAL, LESSON, EXERCISES, SOLUTIONS, TROUBLESHOOTING, RESOURCES, fiche et tests.json depuis un dictionnaire ; exemple : `TOOLS/docgen_example_spec_ch07_15.py`) ; l'écrire avec l'outil Write (les heredocs bash avec apostrophes échouent parfois).
  - Actions 5.x : `action.fcurves` n'existe pas (couches) → `[f for l in act.layers for s in l.strips for cb in s.channelbags for f in cb.fcurves]` ; `anim.action_slot = action.slots[0]` à assigner à la main après `anim.action = …` ; `nla_tracks.new()`, `track.strips.new(nom, début, action)` assigne le slot tout seul ; une action ACTIVE masque le NLA ; `keyframe_insert` ignore l'interpolation par défaut des préférences → régler `kp.interpolation` ; un bone dont la pose n'est pas keyframée n'est PAS conservé dans un override de bibliothèque (Action requise).
  - Library override : `coll.override_hierarchy_create(scene, view_layer, do_fully_editable=True)` (sinon override « système » non éditable) ; liens avec chemin relatif (`libraries.load(link=True, relative=True)`, enregistrer avec relative_remap).
  - Rigify -b : poids par `parent_set(ARMATURE_AUTO)` sur les DEF- seulement ; collections ORG/MCH/DEF masquées par défaut ; bendy bones : `bone.bbone_segments`, `pose_bone.bbone_curveinx/outx`.
  - Noise (FModifier) : amplitude crête à crête ≈ 0,4 × Strength ; mettre des phases différentes sur les axes ; Damped Track conserve le roulis initial (Track To : Up Y).
  - Orienter un bone par script : `pb.matrix = Matrix.Translation(tête) @ (R @ rest3x3).to_4x4()` avec R = rotation la plus courte depuis la direction de repos ; pivoter en monde : `pb.matrix = T(h) @ R @ T(-h) @ pb.matrix`.
  - Rendu Workbench en -b (silhouette) : pixels en lignes de BAS en HAUT (ne pas retourner à l'écriture) ; `read_factory_settings` vide `bpy.app.tempdir`.
  - Mesures de correcteur : toujours normaliser par un PLANCHER d'amplitude (courbes de pur bruit), ajuster une droite sur la plus longue série d'images au sol (glissement de pied), séparer les contre-exemples chirurgicaux ; un croquis numpy : un index négatif dans un slice (`img[0:y+2]` avec y < 0) remplit des barres → borner x et y.
  - BVH : `bpy.ops.import_anim.bvh(filepath, rotate_mode='NATIVE', axis_forward='-Z', axis_up='Y', use_fps_scale=False)` ; opérateurs du Graph Editor : `graph.gaussian_smooth`, `graph.decimate`, `graph.clean`.
- **Rigid Body en 5.3 -b (sondes de CH08.01, NON terminées)** : la simulation ne s'avance que par `scene.frame_set(f)` SÉQUENTIEL de la première image (`frame_set(150)` direct ne simule rien) + `view_layer.update()` ; une bille cinématique (`rigid_body.kinematic` + clés de location et de `kinematic`) puis lâchée projette bien les corps. Une colonne de cubes de 1 m (friction 0,5) GLISSE au lieu de s'effondrer (déplacement < 1 m à 6 m/s, 15 kg) ; un mur de briques 0,3 × 0,6 × 0,3 m a EXPLOSÉ dès l'image 12 (cause non trouvée : essayer des briques plus grosses, `collision_margin`, un espacement de 5 mm, `substeps_per_frame` 20) ; à définir d'abord un cas stable et robuste avant d'écrire le correcteur (qualitatif : tour stable sans impact, ≥ N corps déplacés après impact, aucun corps sous le sol, sol passif absent → chute à −170 m en 150 images).

- **Phase 8 (simulations) — pièges 5.3 -b** : toute simulation (rigid body, cloth, particules, hair dynamics) ne s'avance que par `frame_set` SÉQUENTIEL depuis la 1 ; Cell Fracture n'est PAS livrée en 5.3 de base ;
  `bpy.ops.rigidbody.connect` n'a pas de réglage de distance (une paire à la fois, SELECTED_TO_ACTIVE) ; la rupture d'une contrainte n'est pas visible dans l'API (mesurer les distances entre voisines) ;
  un boulet kinematic rapide (5 m/s) avec peu de sous-étapes FAIT EXPLOSER un mur contraint (30 sous-étapes + boulet à ~2,5 m/s) ; `ps.use_hair_dynamics` est sur ParticleSystem ; enfants de cheveux lus par `ps.co_hair(ob, particle_no=nb_parents+j, step=0..4)` ;
  Wind souffle selon Z local (rotation Y +90° → +X) ; `effector_weights` par système (le monde rigide a les siens) ; cache particules : enregistrer avant de cuire, `temp_override(point_cache=pc)` + `ptcache.bake(bake=True)`, plage = plage de la scène, dossier `blendcache_<nom>` ;
  gaz : cache MODULAR (sinon une seule image cuite), mesure par la taille des .vdb ; liquide : `bake_data()` puis `bake_mesh()`, maillages `.bobj.gz`. Workbench rend les particules en type Object (instance_object non lié à la scène).

- **Phases 9–10 (lighting, rendu) — pièges 5.3 -b** : EEVEE FONCTIONNE en `-b` ici (≈ 0,2 s à 240 × 135) ; `scene.eevee.use_raytracing` est FAUX par défaut, `use_fast_gi` n'a eu aucun effet mesurable ; le Workbench ne rend PAS la profondeur de champ en `-b` (utiliser Cycles) ;
  un monde créé par `worlds.new` n'est pas noir (0,05) : mettre le nœud Background à 0 ; mesurer par RENDU (Workbench plat segmenté par couleur pour la géométrie, Cycles bas-résolution pour la lumière) ; une barre FINE (rayon 3 cm) mesure un flou, une barre large reste « nette » en son centre ;
  Cycles : bruit = écart-type de la différence de DEUX rendus à graines différentes / √2 ; une lampe trop forte sature (bruit mesuré 0) : calibrer l'exposition d'abord ; OIDN fonctionne sur CPU en `-b` (l'énumération `denoiser` est vide, mais `denoiser="OPENIMAGEDENOISE"` s'assigne) ;
  SORTIE EXR multicouche en 5.3 : `image_settings.media_type = 'MULTI_LAYER_IMAGE'` (file_format devient OPEN_EXR_MULTILAYER ; l'assigner directement échoue) ; l'EXR est multi-parties : lire TOUS les en-têtes `channels\0chlist\0` pour les noms de canaux (« Calque.Passe.Composante ») ;
  caméra : `Camera.shift_x` positif = sujet vers la gauche (0,167 → tiers gauche), `shift_y` négatif = l'horizon monte ; marqueurs de timeline : `scene.timeline_markers.new(nom, frame=)` puis `marker.camera = cam` (libellé « Bind Camera to Markers ») ;
  `Object.color` est LINÉAIRE (gris 0,5 → rendu 0,73 en Standard) ; la contre-épreuve trouve des bugs de correcteur : un critère d'accent « valeur seule » refusait la solution (CH09.11).
