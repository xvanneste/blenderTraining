# CH11.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_07_keying_starter.blend`. Sauvegardez sous `ch11_07_keying_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Compositeur : le nœud Image (greenscreen) va à la sortie.

## Tutoriel 2 — Keying (10 min)
Ajoutez un nœud Keying : Key Color = (0,10 ; 0,80 ; 0,15).

## Tutoriel 3 — Nouveau fond (15 min)
Ajoutez un nœud RGB bleu (0,10 ; 0,20 ; 0,80) et un nœud Alpha Over : Background = RGB, Foreground = Keying. Facultatif : un nœud Color Spill.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : coins, sujet, contamination.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_07_keying_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_07.py" -- --exercise keying --debug
```

Remarque d'honnêteté : l'image du chapitre est générée par numpy (fond vert avec un léger grain, sujet elliptique, bord doux de 4 pixels, contamination verte de 6 pixels) : elle est plus propre qu'un vrai écran vert ; les nœuds `CompositorNodeKeying` (Key Color, Tolerance…), `CompositorNodeColorSpill`, `CompositorNodeChromaMatte`, `CompositorNodeAlphaOver` et `CompositorNodeRGB` ont été vérifiés par exécution en 5.3 ; une première mesure de contamination sur un anneau trop profond ne voyait pas le défaut du départ (+0,013) : l'image a été rendue plus contaminée (+0,130) et l'anneau resserré après essai ; le nœud Keying corrige déjà la contamination (la variante sans Color Spill a été vérifiée à 34/34 : le compteur « no_spill » utilise donc Chroma Matte) ; la valeur linéaire du nœud RGB est comparée à sa valeur affichée ; les menus de création des nœuds n'ont pas été regardés.

## Variante de contrôle

Examinez l’alpha seul autour d’une mèche ou d’un bord fin. Composez ensuite sur un fond clair puis sombre. **Preuve** Le premier réglage isole le sujet et le second contrôle la frange sans découper les détails importants.
