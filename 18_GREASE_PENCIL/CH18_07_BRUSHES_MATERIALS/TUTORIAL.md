# CH18.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_07_brushes_starter.blend`, sélectionnez `GP_Practice`, `Ctrl+Tab` →
Draw Mode, `Num 0`. Le GUIDE (verrouillé) contient 3 bandes et un dessin au trait (maison, tasse,
poisson). Le calque `USER_Fills` est déjà **sous** le GUIDE.

## Tutoriel 1 — Trois pinceaux (USER_Lines)
1. Calque **USER_Lines** (`Y`).
2. Étagère d'assets en bas du viewport (ou sélecteur de pinceau dans l'en-tête) → **Pencil**.
   Bande du haut : 5 traits ondulés.
3. Pinceau **Ink Pen** → bande du milieu : 5 traits, en appuyant plus fort au milieu (tablette)
   pour obtenir un trait fin → épais → fin.
4. Pinceau **Marker Bold** → bande du bas : 5 traits.
5. Comparez Size et Strength des trois pinceaux dans l'en-tête.

## Tutoriel 2 — Une palette de matériaux
1. Properties → **Material** : bouton **+** → *New*. Renommez `MAT_GP_Wall`.
2. Panneau **Fill** → *Base Color* : beige. Panneau **Stroke** → *Base Color* : noir.
3. Recommencez pour `MAT_GP_Roof` (rouge), `MAT_GP_Cup` (bleu), `MAT_GP_Fish` (orange)…
   au moins 4 matériaux de couleur.

## Tutoriel 3 — Remplir le dessin guide (USER_Fills)
1. Calque **USER_Fills**.
2. Outil **Fill** (barre d'outils ou pinceau « Fill »). En-tête : **Layer Mode : Visible**
   (les traits du GUIDE servent de frontières).
3. `U` → `MAT_GP_Wall`, clic dans le mur. `U` → `MAT_GP_Roof`, clic dans le toit. Continuez :
   porte, fenêtre, tasse, café, poisson, queue, œil (au moins 8 zones).
4. Liseré blanc entre aplat et trait ? Augmentez **Dilate/Contract** (1 ou 2 px) et recommencez.
5. Zone qui « fuit » (tout l'écran se remplit) : `Ctrl+Z`, la forme n'est pas fermée ; dessinez
   un guide de fermeture avec `Alt+glisser`, ou réglez **Gap Closure**.

## Tutoriel 4 — Gommer
1. Calque USER_Lines, `Ctrl+clic gauche` sur un trait : gomme (mode du pinceau gomme actif).
2. Pinceau **Eraser Stroke** : un clic supprime un trait entier. `Ctrl+Z` pour annuler l'essai.

## Tutoriel 5 — Vérifier
Enregistrez `ch18_07_brushes_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_07_brushes_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_07.py" -- --exercise brushes --render
```

## Variante de contrôle

Utilisez deux matériaux et le même trait sur une copie. Faites varier couleur ou contour avec un seul changement à la fois. **Preuve** Vous distinguez le réglage du pinceau du matériau affecté aux traits après réouverture.
