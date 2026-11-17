# CH10.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_05_memory_starter.blend`. Sauvegardez sous `ch10_05_memory_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Mesurer (10 min)
Lancez le correcteur sur le départ : 200 maillages, 384 000 triangles, 64 Mo.

## Tutoriel 2 — Partager (20 min)
Sélectionnez tous les rochers avec Rock_000 actif, Object > Link/Transfer Data > Link Object Data. Passez le niveau de rendu de Subdivision Surface à 0 (variante acceptée), ou fabriquez une collection source et des instances.

## Tutoriel 3 — Limiter les textures (5 min)
Properties > Render > Simplify : cochez la case de l'en-tête, Render > Texture Limit : 1024.

## Tutoriel 4 — Mesurer (10 min)
Relancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_05_memory_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_05.py" -- --exercise memory --debug
```

Remarque d'honnêteté : les panneaux Simplify et la commande Link Object Data n'ont pas été regardés dans l'interface 5.3 (l'API `Scene.cycles.texture_limit_render` et `render.use_simplify` ont été vérifiées ; la valeur « OFF » de l'énumération est mesurée) ; le correcteur compte des PROXYS (maillages différents, triangles évalués, Mo de textures effectifs) et ne mesure pas la mémoire réelle du processus ; la variante acceptée (maillage partagé au niveau 0) a été vérifiée par le calcul du correcteur (16 000 triangles, 1 maillage, 4 Mo) mais n'est pas livrée comme fichier ; les instances de collection sont une solution parmi d'autres ; le LOD n'est pas traité.

## Variante de contrôle

Mesurez d’abord le nombre de maillages de base puis les objets et les instances. Déplacez une ressource volumineuse vers une solution plus légère. **Preuve** La comparaison sépare le stockage, la consommation de mémoire et la géométrie visible. Le réglage choisi cible le poste le plus coûteux.
