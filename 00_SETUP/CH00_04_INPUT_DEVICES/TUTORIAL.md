# CH00.04 — Tutoriels pas à pas

## Premier jalon — Revenir à une vue connue

Ouvrez **File → New → General** et placez le pointeur dans la vue 3D. Sélectionnez le cube. Exécutez **View → Viewpoint → Front**, puis **View → Frame Selected**. Vous devez voir le cube centré et la mention **Front Orthographic**. Changez ensuite de vue et reproduisez le cadrage. Le cube et la caméra doivent conserver leur position.

## Tutoriel 1 — Choisir le trajet qui convient à votre matériel

| Objectif | Pavé numérique, keymap Blender | Menu de la vue 3D |
|---|---|---|
| Face, droite, dessus | Numpad 1, 3, 7 | View → Viewpoint → Front, Right, Top |
| Arrière, gauche, dessous | Ctrl+Numpad 1, 3, 7 | View → Viewpoint → Back, Left, Bottom |
| Perspective ou orthographique | Numpad 5 | View → Perspective/Orthographic |
| Voir par la caméra active | Numpad 0 | View → Cameras → Active Camera |
| Cadrer la sélection | Numpad Decimal | View → Frame Selected |
| Cadrer la scène | Home | View → Frame All |

Dans l’Outliner, Numpad Decimal a un autre rôle. Replacez le pointeur dans la vue 3D avant de cadrer. Avec une souris, glissez avec le bouton du milieu pour orbiter, avec Shift pour panoramiquer et faites rouler la molette pour zoomer.

## Tutoriel 2 — Sans pavé, avec ou sans émulation

1. Essayez le menu View et le gizmo en haut à droite. Cliquez sur l’axe Z pour la vue de dessus. Glissez sur le gizmo pour orbiter. Les icônes main et loupe donnent le panoramique et le zoom.
2. Si vous souhaitez utiliser les chiffres du clavier principal, activez **Edit → Preferences → Input → Keyboard → Emulate Numpad**. Vérifiez que 1, 3 et 7 changent la vue, le pointeur dans la vue 3D.
3. Sur le cube, entrez en **Edit Mode** avec Tab. Avec l’émulation active, les touches 1, 2 et 3 servent à la navigation. Pour passer d’une sélection de sommets à une sélection de faces, utilisez les trois icônes dans l’en-tête de la vue 3D. Désactivez l’émulation si vous préférez garder les raccourcis de sélection.

## Tutoriel 3 — Avec un trackpad

Vérifiez d’abord les gestes multi-touch dans les préférences. Si vous décidez d’émuler le bouton du milieu, activez **Input → Mouse → Emulate 3 Button Mouse**. Avec le modificateur Alt, faites **Alt+clic gauche glissé** pour orbiter. Ajoutez **Shift** pour déplacer la vue ou **Ctrl** pour zoomer. Si votre système intercepte le geste ou si une commande Alt+clic devient inaccessible, revenez au gizmo et au menu View.

## Tutoriel 4 — Lire le rapport des réglages

Depuis le dossier du chapitre, lancez le script dans Blender en arrière-plan. Il affiche les réglages et les compare au profil choisi. Il ne détecte pas le type de périphérique physique à votre place.

```powershell
& "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b --python-exit-code 1 --python "SCRIPTS/bcma_input_report.py" -- --profile mouse3
```

Utilisez laptop pour un portable ou tablet pour un stylet. La navigation au menu reste possible même si le rapport recommande une émulation. Vérifiez au moins l’orbite et le cadrage sur votre machine.

## Tutoriel 5 — Tablette graphique
1. Installez le pilote du fabricant (Wacom, XP-Pen, Huion…) depuis son site officiel.
2. *Input → Tablet → Tablet API* : laissez *Automatic*.
3. Test de pression : *File → New → 2D Animation*. Dessinez des traits en variant la
   pression. ✅ L'épaisseur du trait varie.
4. Si l'épaisseur ne varie pas : *Tablet API = Windows Ink*, recommencez ; puis *Wintab*.
   Vérifiez dans l'en-tête de l'outil que l'icône de pression de *Radius* est active.
5. Ajustez *Max Threshold* (0,7–0,8 si vous appuyez peu).
