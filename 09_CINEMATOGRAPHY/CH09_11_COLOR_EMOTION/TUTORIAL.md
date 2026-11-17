# CH09.11 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_11_color_starter.blend`. Sauvegardez sous `ch09_11_color_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Rendu F12 : cinq cartes grises.

## Tutoriel 2 — Colorer (20 min)
Sélectionnez BG_JOY > Properties > Object > Viewport Display > Color (libellés relus dans `bl_ui/properties_object.py`). Réglez la couleur, puis lancez le correcteur : il affiche la teinte, la saturation et la valeur rendues. Répétez pour les dix objets.

## Tutoriel 3 — Le contraste d'accent (10 min)
Pour chaque ACC_, choisissez une valeur très différente ou une teinte à 120° ou plus.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : cinq émotions et les teintes distinctes.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_11_color_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_11.py" -- --exercise color --debug
```

Remarque d'honnêteté : le rendu de contrôle est du Workbench plat (couleurs d'objet) ; les teintes mesurées correspondent aux consignes à 2° près (la peur à H 268° au lieu de 270°, la valeur très basse du fond rend la teinte bruitée) ; une première version du critère d'accent (valeur seule) refusait à tort la joie (fond jaune, accent bleu de valeur voisine) : trouvé par la contre-épreuve, corrigé par une exception de teinte ≥ 120° ; le libellé Object > Viewport Display > Color a été relu dans `bl_ui/properties_object.py` mais n'a pas été regardé à l'écran ; les plages d'émotion sont une convention assumée, pas une vérité.

## Variante de contrôle

Gardez un matériau témoin fixe et faites deux variations d’éclairage coloré. Regardez les miniatures en couleur puis en gris. **Preuve** Vous distinguez l’effet de la teinte de l’éclairage de la hiérarchie de valeurs.
