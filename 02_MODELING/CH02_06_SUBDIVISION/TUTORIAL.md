# CH02.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_06_subdiv_starter.blend` : trois cubes de 80 cm devenus des boules par
le modificateur Subdivision Surface (Levels 2). Comparez avec `ch02_06_subdiv_starter_view.png`.

## Tutoriel 1 — Boucles de maintien (GEO_Support)
1. Sélectionnez `GEO_Support`, `Tab`, vue de face (`Num 1`), fil de fer (`Z` → Wireframe).
2. `Ctrl+R` en survolant une arête **verticale** (les coupes seront horizontales) : molette →
   **2 coupes**, clic gauche puis clic droit.
3. Les deux boucles sont sélectionnées, à ±13,3 cm du centre (coupes au tiers). Pour les placer à
   ±35 cm (5 cm des arêtes) : `S` `Z` `2.625` `Entrée` (35 / 13,33 = 2,625).
4. Même chose dans les deux autres directions (`S X`, `S Y`).
5. `Tab` : le cube a retrouvé sa forme, coins adoucis.

> Astuce de précision : au lieu d'un facteur d'échelle, glissez la boucle avec `G` `G`
> (*Edge Slide*) et tapez une valeur, ou utilisez un **Bevel** de 5 cm, 1 segment, sur les 12
> arêtes : deux boucles par arête d'un coup.

## Tutoriel 2 — Crease (GEO_Crease)
1. `Tab`, mode arête (`2`), sélectionnez les **4 arêtes du dessus**.
2. **`Shift+E`**, tapez `1`, `Entrée`. Overlay *Crease* (Viewport Overlays, Edit Mode) : les arêtes
   sont colorées.
3. `Tab` : dessus plat et net, dessous arrondi. Essayez 0,5 : un pli adouci.

## Tutoriel 3 — Optimiser (GEO_Pebble)
1. Properties → Modifiers → Subdivision : **Levels Viewport 1**, **Render 3**.
2. Statistics : le nombre de faces à l'écran est divisé par 16 ; le rendu `F12` reste lisse.

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_06_subdiv_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_06.py" --python-exit-code 1 -- --exercise subdiv --render
```
