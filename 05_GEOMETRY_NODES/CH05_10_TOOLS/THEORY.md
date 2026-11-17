# CH05.10 — Cours théorique : optimisation et outils

## 1. Ce qui coûte
- **Sommets × instances** : la géométrie instanciée est partagée, mais pas si elle est réalisée.
- **Nombre d'instances** : proportionnel à la densité × l'aire.
- **Nœuds coûteux** (Poisson, Boolean, Realize) évalués à chaque changement de paramètre.
Règles : garder des instances ; géométrie instanciée minimale (cône à 8 côtés, 14 triangles) ; paramètres coûteux **bornés** ; valeurs par défaut **sûres**.

## 2. Mesures de la solution (évaluées)
Défaut (Density 0,5 sur la grille de 20 × 20 m) : 195 instances de 9 sommets (14 triangles) ; la grille de base (441 sommets) subsiste. Density au maximum (5) : 2 004 instances, 28 056 triangles instanciés. Départ (starter) : cône de 64 côtés réalisé : 13 116 sommets évalués par défaut, et sans borne : 400 001 instances et 5,6 millions de triangles à Density 1 000.
Le **temps** d'évaluation n'est pas mesuré : en arrière-plan, l'évaluation est paresseuse et mise en cache (0,001 s mesuré même pour 400 001 instances), ce qui rend le chronométrage trompeur. On compte donc des sommets, instances et triangles.

## 3. Un outil modificateur
`node_group.is_modifier = True` (option Modifier de l'arbre) rend l'arbre disponible comme modificateur ; `is_tool` correspond aux outils d'édition (menus de mode). Un modificateur reçoit la géométrie de l'objet : l'arbre doit la **conserver** (Group Input [Geometry] → Join Geometry) et y ajouter ses instances.

## 4. Publier comme asset
`node_group.asset_mark()` (« Mark as Asset », libellé de l'opérateur `asset.mark`), puis `asset_data.description`, `.author`, `.license`, `.tags`, `.catalog_id`. Les catalogues sont dans `blender_assets.cats.txt` (lignes `UUID:chemin:nom`, première ligne utile `VERSION 1`), à côté du .blend. Ici : catalogue « Tools/Scatter », tags « scatter » et « instances ».

## 5. Pièges
- Cône de 64 côtés : 7 fois plus de triangles pour rien.
- Realize Instances par habitude.
- Density sans borne : 400 001 instances en un clic.
- Outil qui ignore la géométrie d'entrée : l'objet disparaît.
- Asset sans catalogue ni description : introuvable, inutilisable.
- Un matériau référencé dans l'arbre doit exister ou être embarqué avec l'asset.

## 6. Limites
Le correcteur mesure des budgets et des métadonnées ; il ne teste pas l'apparition de l'asset dans l'Asset Browser (bibliothèque déclarée) ni la performance réelle d'affichage.
