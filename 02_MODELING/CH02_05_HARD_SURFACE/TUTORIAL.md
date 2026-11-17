# CH02.05 — Tutoriels pas à pas : le boîtier de commande

Ouvrez `STARTER_FILES/ch02_05_device_starter.blend`. `GEO_Device` : pavé 40 × 20 × 50 cm, échelle 1.

## Tutoriel 1 — Coins arrondis par Bevel Weight
1. `Tab`, mode arête (`2`), puis `Alt+A`. Orbitez autour du boîtier et sélectionnez
   les **4 arêtes verticales**. Ajoutez les suivantes avec `Shift` et un clic. Les arêtes
   horizontales doivent rester désélectionnées.
2. *Edge → Edge Bevel Weight*, tapez `1`, `Entrée`. (Viewport Overlays en Edit Mode → bouton **Bevel** : les arêtes pondérées sont colorées.)
3. `Tab`. Properties → Modifiers → *Add Modifier → Generate → Bevel* :
   **Limit Method : Weight**, **Width 0.02**, **Segments 4**. Les coins verticaux s'arrondissent ;
   le reste est intact.

## Tutoriel 2 — L'écran en creux
1. `Tab`, mode face (`3`), cliquez la face avant (−Y, vue `Numpad 1`).
2. `I` → 0.03 `Entrée` ; `E` → `-0.01` `Entrée`. Un écran en creux de 1 cm.

## Tutoriel 3 — Les boutons
1. Revenez en mode Objet (`Tab`). Ajoutez un cylindre avec `Shift+A` → *Mesh → Cylinder*.
   Ouvrez `F9` immédiatement et entrez *Vertices* 24, *Radius* 0,02 et *Depth* 0,015.
   Dans *N → Item → Location*, placez son centre en (0 ; 0 ; 0,5075). Sa base rejoint
   le dessus du boîtier, à 0,50 m.
2. Depuis le bouton central, faites `Shift+D`, `X`, `-0.1`, `Entrée`. Resélectionnez
   le bouton central pour créer la deuxième copie à `0.1` sur X.
3. Sélectionnez les 3 boutons puis `GEO_Device` en dernier (actif), **`Ctrl+J`** (*Join*).

## Tutoriel 4 — Les arêtes qui accrochent la lumière
1. *Add Modifier → Generate → Bevel* (2ᵉ) : **Limit Method : Angle** (30°), **Width 0.003**,
   **Segments 2**, panneau *Shading* → **Harden Normals**.
2. *Object → Shade Smooth*. Comparez avec et sans ce modificateur (icône écran) en Material Preview.

## Tutoriel 5 — Vérifier
`F12` et comparez avec `ch02_05_device_reference.png` et le gros plan `ch02_05_device_closeup.png`.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_05_device_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_05.py" -- --exercise device --render
```

## Variante de contrôle

Faites tourner la lumière autour du boîtier au même cadre. Repérez une arête chanfreinée où le reflet se rompt et vérifiez que le biseau touche les arêtes voulues, sans déformer les coins de l’écran. **Preuve** Vues Solid et filaire de la même zone, avec largeur, segments et échelle contrôlée.
