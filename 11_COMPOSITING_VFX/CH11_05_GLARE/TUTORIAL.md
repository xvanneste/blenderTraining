# CH11.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_05_glare_starter.blend`. Sauvegardez sous `ch11_05_glare_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Lampe nette, barre droite.

## Tutoriel 2 — Glare (10 min)
Nœud Glare entre Render Layers et la sortie : prise Type : Fog Glow.

## Tutoriel 3 — Distorsion (10 min)
Nœud Lens Distortion après le Glare : Distortion 0,3.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_05_glare_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_05.py" -- --exercise glare --debug
```

Remarque d'honnêteté : les nœuds `CompositorNodeGlare` (prises Type, Quality, Threshold, Smoothness, Strength, Size, Streaks…) et `CompositorNodeLensdist` (Type, Distortion, Dispersion, Jitter, Fit) ont été vérifiés par exécution en 5.3 ; le halo du Fog Glow par défaut est très discret (anneau 0,0066) : le critère est donc bas (0,002 à 0,1) et sépare « aucun glare » de « glare trop fort » ; une première mesure sur l'anneau 15–25 pixels mélangeait l'effet de la distorsion (qui élargit la lampe) et celui du glare : la contre-épreuve (no_distortion) l'a révélé, l'anneau est maintenant à 20–30 pixels ; le signe de la courbure (+ : la barre monte au centre) est mesuré, pas déduit d'un nom (barrel / pincushion) ; pas de nœud de grain trouvé ; menus de création des nœuds non regardés.

## Variante de contrôle

Augmentez le seuil de Glare puis comparez les hautes lumières traitées et les hautes lumières préservées. Affichez aussi l’effet isolé. **Preuve** Le halo accompagne le point lumineux voulu et la texture des autres zones reste lisible.
