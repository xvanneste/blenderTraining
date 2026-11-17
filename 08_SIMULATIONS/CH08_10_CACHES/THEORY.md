# CH08.10 — Cours théorique : Caches et baking

## 1. Cache de simulation
Chaque système (particules, tissu, corps souple, corps rigides, fluides) possède un cache de points (point cache). Il se remplit pendant la lecture dans l'ordre ; le bouton Bake le remplit d'un coup.

## 2. Mémoire ou disque
Disk Cache coché : un fichier `.bphys` par image dans le dossier `blendcache_<nom du fichier>` voisin du .blend (mesuré : 61 fichiers pour 60 images, numérotés de 000000). Les fluides ont leur propre cache (CH08.05–06).

## 3. L'exercice
EMITTER : 100 particules, images 1–60. Enregistrer sous `ch08_10_caches_<prenom>_v001.blend`, cocher Disk Cache, Bake.

## 4. Relecture
Cuit, on peut sauter : image 60 puis 40, puis 60, puis 40 : positions identiques (écart 0, mesuré). Une simulation non cuite n'offre pas cette garantie.

## 5. Plage
La plage cuite d'un système de particules suit la plage de la scène (mesuré : scène 1–30 pendant la cuisson : 31 fichiers ; `point_cache.frame_end` n'est pas réglable pour les particules).

## 6. Pièges
- Cuire un fichier non enregistré : pas de dossier de cache.
- Renommer le .blend sans copier le dossier.
- Modifier un réglage après la cuisson : le cache ne correspond plus (mesuré : 150 particules, `is_outdated` faux).
- Plage de la scène trop courte pendant la cuisson.

## 7. Script
`with bpy.context.temp_override(point_cache=pc): bpy.ops.ptcache.bake(bake=True)` ; `pc.use_disk_cache`, `pc.is_baked`, `pc.info`.

## 8. Limites
Un seul type de cache testé (particules) ; pas de nettoyage de cache (Delete Bake) ni de cache externe ; fluides non rebakés ici ; taille disque non étudiée.
