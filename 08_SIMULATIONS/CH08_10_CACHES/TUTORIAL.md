# CH08.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_10_caches_starter.blend`.

## Tutoriel 1 — Enregistrer d'abord (5 min)
File > Save As : `ch08_10_caches_<prenom>_v001.blend`.

## Tutoriel 2 — Le cache (10 min)
EMITTER > Physics > Particles > Cache : Disk Cache coché ; vérifiez la plage de la scène (1–60) ; Bake.

## Tutoriel 3 — Vérifier (10 min)
Après *Bake*, notez les positions à l’image 40. Passez à 60 puis revenez à 40. Comparez les positions à cette même image 40. Rouvrez la scène enregistrée et répétez la vérification avec le dossier `blendcache_…` présent à côté du fichier.

## Tutoriel 4 — Le correcteur (5 min)
Lancez le correcteur sur le fichier enregistré (il lit les fichiers voisins).

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_10_caches_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_10.py" -- --exercise caches --debug
```

Remarque d'honnêteté : la solution est générée par script (`ptcache.bake` avec `temp_override(point_cache=…)`) ; `point_cache.frame_end` n'est pas réglable pour des particules (la plage suit la scène) ; `is_outdated` est resté faux après un changement de réglage (mesuré, non expliqué) ; les noms exacts des boutons du panneau Cache (Bake, Delete Bake…) n'ont pas été relus dans l'interface 5.3 ; seul le cache de particules a été testé. Courbe (numpy) regardée : relecture inverse superposée à la lecture directe.

## Variante de contrôle

Sauvegardez une scène, puis faites une seconde copie avec un petit changement de simulation. Utilisez des caches distincts et rouvrez chaque fichier. **Preuve** La même image du même calcul se retrouve après réouverture, et une note décrit ce qui oblige à recalculer.
