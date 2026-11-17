# CH11.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_09_integration_starter.blend`. Sauvegardez sous `ch11_09_integration_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
F12 : le sol 3D remplace la plaque ; l'ombre va à gauche.

## Tutoriel 2 — Catcher et film (10 min)
Floor > Object Properties : Shadow Catcher ; Render Properties > Film > Transparent.

## Tutoriel 3 — Soleil et compositeur (15 min)
SUN : rotation X 50°, Z −50°. Compositeur : Alpha Over (Background = Image, Foreground = Render Layers).

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : cube, ombre à droite, côté gauche, sol lointain.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_09_integration_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_09.py" -- --exercise integration --debug
```

Remarque d'honnêteté : `Object.is_shadow_catcher` et `render.film_transparent` sont des propriétés vérifiées par l'API et par le rendu (le panneau Film > Transparent a été relu dans `addons_core/cycles/ui.py` ; le chemin exact « Visibility > Mask > Shadow Catcher » n'a pas été regardé dans l'interface) ; la plaque est générée par numpy (sol uniforme, poteau, ombre) : elle ne montre ni perspective ni grain ; les mesures (ombre à droite −0,067, gauche −0,003, sol lointain 0,0) sont celles de cette scène en Cycles à 32 échantillons ; la direction d'ombre a été calibrée par rendu (X 50°, Z ∓50°) ; le cube est calé à la main dans l'image, pas par un matchmoving ; la lumière HDRI capturée et le grain, cités au programme, ne sont pas évalués.

## Variante de contrôle

Comparez un objet sans ombre de contact puis avec ombre. Vérifiez direction, contraste et position à deux instants. **Preuve** Le sol et l’objet gardent une relation cohérente et le composite est évalué au cadre de livraison.
