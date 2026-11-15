# CH02.05 — Tutoriels pas à pas : le boîtier de commande

Ouvrez `STARTER_FILES/ch02_05_device_starter.blend`. `GEO_Device` : pavé 40 × 20 × 50 cm, échelle 1.

## Tutoriel 1 — Coins arrondis par Bevel Weight
1. `Tab`, mode arête (`2`). Sélectionnez les **4 arêtes verticales** (`Shift+clic`, X-ray `Alt+Z`).
2. *Edge → Edge Bevel Weight*, tapez `1`, `Entrée`. (Viewport Overlays en Edit Mode → bouton **Bevel** : les arêtes pondérées sont colorées.)
3. `Tab`. Properties → Modifiers → *Add Modifier → Generate → Bevel* :
   **Limit Method : Weight**, **Width 0.02**, **Segments 4**. Les coins verticaux s'arrondissent ;
   le reste est intact.

## Tutoriel 2 — L'écran en creux
1. `Tab`, mode face (`3`), cliquez la face avant (−Y, vue `Num 1`).
2. `I` → 0.03 `Entrée` ; `E` → `-0.01` `Entrée`. Un écran en creux de 1 cm.

## Tutoriel 3 — Les boutons
1. `Tab` (Object Mode). `Shift+A` → *Mesh → Cylinder* ; panneau : *Vertices* 24, *Radius* 0.02,
   *Depth* 0.015. Placez-le sur le dessus : `G` `Z` 0.5075 (le dessus est à 0,50 m).
2. `Shift+D` pour 2 copies décalées en X (−0,1 et +0,1).
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
  --python "SCRIPTS\validate_ch02_05.py" --python-exit-code 1 -- --exercise device --render
```
