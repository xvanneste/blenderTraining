# CH00.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Pour insérer des plans (sh0015) sans renuméroter, et pour un tri alphabétique correct. |
| Q2 | **b** — 02_assets/rigs (ou characters) | Un asset réutilisé va dans 02_assets, jamais dans un plan. |
| Q3 | — | Un asset est réutilisable (personnage, décor, accessoire) ; un plan est une unité unique du film, qui assemble des assets. |
| Q4 | **b** — mon_court_sq010_sh0020_anim_v004.blend | projet_séquence_plan_tâche_vNNN, minuscules. |
| Q5 | — | F2. |
| Q6 | — | Edit > Batch Rename (Ctrl+F2). |
| Q7 | — | Certains outils (lignes de commande, fermes de rendu, autres logiciels, serveurs) les gèrent mal. |
| Q8 | **b** — Le dossier du fichier .blend | Chemin relatif au .blend. |
| Q9 | — | File > External Data > Make Paths Relative. |
| Q10 | — | Le .blend s'alourdit et les textures sont dupliquées dans chaque fichier : plus de stockage, mises à jour impossibles à centraliser. |
| Q11 | **b** — Dans .blender_project/project.toml à la racine | Dossier caché .blender_project, fichier project.toml. |
| Q12 | — | Nom, variables de projet, bibliothèques d'assets du projet, configuration OCIO, image d'accueil. |
<!-- QUIZ_ANSWERS_END -->

## Leçon 1 difficile
Musique temporaire → `05_sound/music/` (nommée `temp_…`) ; HDRI → `02_assets/hdri/` ;
animatique MP4 → `01_preprod/animatic/` ; contrat → `00_admin/` ; référence vidéo de
marche → `01_preprod/references/` (avec sa licence/source notée).

## Exercice 2
Le `.blend` stockait `G:\…\ASSETS\textures\tx_wood_planks.png` : une adresse fixe. Après
renommage, ce chemin n'existe plus. Un chemin relatif `//../ASSETS/textures/…` aurait
été résolu à partir de l'emplacement de la copie, où le dossier existait.

## Exercice 3 — correspondance de référence
| Starter | Solution |
|---|---|
| Collection / Collection 2 / Collection 3 / Collection.001 | SET / PROPS / LIGHTS / CAMERAS |
| Plane / Plane.001 | GEO_Floor / GEO_Wall_Back |
| Cube / Cube.002 / Cube.003 | GEO_Box_01 / GEO_Box_02 / GEO_Box_03 |
| Empty / Light / Camera | EMP_CamTarget / LGT_Key / CAM_Main |
| Material / Material.001 / Material.002 | MAT_Floor_Wood / MAT_Wall_Plaster / MAT_Box_Cardboard |
| texture en absolu | `//../ASSETS/textures/tx_wood_planks.png` |
Fichier : `COMPLETED_EXAMPLES/ch00_06_messy_scene_solution.blend`.
