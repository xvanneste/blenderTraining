# CH06.11 — Cours théorique : rigging avancé et réutilisation

## 1. Bendy Bones
Un bone peut être découpé en `bbone_segments` segments qui suivent une courbe de Bézier : le maillage qu'il déforme se courbe en arche au lieu de pivoter en bloc. Propriétés de pose : `bbone_curveinx`, `bbone_curveoutx` (décalage latéral des poignées d'entrée et de sortie, axe X), `bbone_curveinz`/`bbone_curveoutz` (axe Z), `bbone_easein`/`bbone_easeout`.
Mesures (tube de 1 m, 41 anneaux) : Segments = 8 et Curve In X = Curve Out X = 0,3 : milieu décalé de 22,5 cm, extrémités fixes, virage maximal de 5,6° entre anneaux. Segments = 2 : 17°. Segments = 1 : aucun effet (0,0 cm). Curve In X = 0,5 et Curve Out X = −0,5 donne une courbe en S.

## 2. La bibliothèque de rig
Un rig réutilisable vit dans son propre fichier (ici ch06_11_rig_library.blend : collection COL_Rig, objets RIG_Lib et GEO_Lib). Les plans ne l'ouvrent pas : ils le LIENT (File > Link) : référence en lecture seule, mises à jour automatiques si la bibliothèque change. Un Append fait une copie locale indépendante.

## 3. Library override
Un objet lié n'est pas éditable. Un override en crée une version locale qui reste liée à l'original : on peut la placer, la poser, y ajouter une Action, et seules ces différences sont stockées dans le plan. En Python : `collection.override_hierarchy_create(scene, view_layer, do_fully_editable=True)`. Sans `do_fully_editable`, les overrides sont « système » (non éditables).

## 4. Poser un rig overridé
Mesuré en 5.3 en arrière-plan : la position de l'objet (location) est conservée ; une rotation de bone saisie directement n'est PAS conservée à la réouverture ; un keyframe (Action portée par l'override : `animation_data`) l'est. Dans l'exercice, arm est tourné de 30° autour de Z par un keyframe à l'image 1.

## 5. Chemins relatifs
`bpy.data.libraries.load(path, link=True, relative=True)` ; à l'enregistrement du plan (Remap Relative), le chemin devient `//../STARTER_FILES/ch06_11_rig_library.blend`. Un chemin absolu fonctionne sur la machine de l'auteur puis casse.

## 6. Mesures du volet B
Solution : une bibliothèque relative, overrides éditables, Action sur arm.rotation_euler, 30° à l'image 1, bout du tube décalé de 28,8 cm en Y (0,6 × sin 30° = 30 cm), rig à 2 m de l'origine.

## 7. Pièges
- Ouvrir la bibliothèque et la modifier depuis un plan.
- Lier sans override puis chercher à poser.
- Garder un chemin absolu.
- Poser un rig overridé sans keyframe : la pose disparaît à la réouverture.
- Déplacer la bibliothèque sans les plans (chemin relatif cassé).

## 8. Limites
Les bendy bones testés sont le cas le plus simple (un bone, un axe) ; pas de Bendy Bones chaînés ni de pont entre bones. Pas de test de mise à jour de la bibliothèque (changer l'original et voir le plan suivre) ni de proxies d'anciens pipelines. Le chemin « Object > Library Override > Make » de l'interface n'a pas été relu dans l'interface 5.3.
