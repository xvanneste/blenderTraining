# CH00.04 — Tutoriels pas à pas

## Tutoriel 1 — Rapport de vos périphériques
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b `
  --python "SCRIPTS\bcma_input_report.py" -- --profile mouse3
```
Remplacez `mouse3` par `laptop` (trackpad, sans pavé) ou `tablet`.
✅ Chaque ligne marquée `→ recommandé` indique un réglage à revoir.

## Tutoriel 2 — Les gestes de navigation à la souris (5 min, scène par défaut)
1. *File → New → General*.
2. `MMB` glissé : orbite. `Shift+MMB` : panoramique. Molette : zoom.
3. `Num 1`, `Num 3`, `Num 7` : face, droite, dessus. `Ctrl+Num 1` : arrière.
4. `Num 5` : bascule perspective/orthographique (lisez le nom de la vue en haut à gauche :
   *User Perspective*, *Front Orthographic*…).
5. Sélectionnez le cube, `Num .` : cadrage. `Home` : tout cadrer.
   ✅ Vous savez revenir à n'importe quelle vue en moins de 2 secondes.

## Tutoriel 3 — Sans pavé numérique
1. Cliquez les axes **X, Y, Z** du gizmo de navigation (en haut à droite de la vue 3D) :
   la vue s'aligne. Glissez sur le gizmo : orbite.
2. Activez *Edit → Preferences → Input → Keyboard → Emulate Numpad*. Testez `1`, `3`, `7`.
3. Passez en Edit Mode (`Tab`) : `1`/`2`/`3` ne changent plus le mode de sélection →
   utilisez les trois icônes sommets/arêtes/faces de l'en-tête.

## Tutoriel 4 — Trackpad
1. *Input → Mouse → Emulate 3 Button Mouse*.
2. `Alt` + glisser au trackpad (clic maintenu) : orbite. `Shift+Alt` : panoramique.
   `Ctrl+Alt` : zoom.
3. Deux doigts : testez les gestes multi-touch (dépend de votre trackpad).

## Tutoriel 5 — Tablette graphique
1. Installez le pilote du fabricant (Wacom, XP-Pen, Huion…) depuis son site officiel.
2. *Input → Tablet → Tablet API* : laissez *Automatic*.
3. Test de pression : *File → New → 2D Animation*. Dessinez des traits en variant la
   pression. ✅ L'épaisseur du trait varie.
4. Si l'épaisseur ne varie pas : *Tablet API = Windows Ink*, recommencez ; puis *Wintab*.
   Vérifiez dans l'en-tête de l'outil que l'icône de pression de *Radius* est active.
5. Ajustez *Max Threshold* (0,7–0,8 si vous appuyez peu).
