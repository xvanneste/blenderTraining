# CH02.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_04_normals_starter.blend`. Passez le viewport en **Material Preview**
(`Z` → Material Preview) : la boîte de conserve a des reflets « gonflés », le pavé bleu des taches.
Comparez avec `COMPLETED_EXAMPLES/ch02_04_normals_starter_view.png` puis `_reference.png`.

## Tutoriel 1 — Voir l'orientation (GEO_Flipped)
1. Viewport Overlays → cochez **Face Orientation**. Des carrés **rouges** apparaissent sur le cube.
2. Lancez `F12` : le rendu paraît correct ! Le défaut est invisible ici… mais pas pour Solidify,
   les exports ou le Backface Culling (essayez : Viewport Shading → *Backface Culling*).
3. Sélectionnez le cube, `Tab`, `A`, **`Shift+N`** (*Mesh → Normals → Recalculate Outside*).
   Tout devient bleu.

## Tutoriel 2 — Lisser avec des arêtes vives (GEO_Can)
1. Object Mode, sélectionnez la boîte. **Object → Shade Auto Smooth**.
2. Panneau de l'opération : *Angle* **30°**. Les couvercles redeviennent plats, le flanc reste lisse.
3. Properties → Modifiers : un modificateur **Smooth by Angle** est apparu ; son réglage *Angle*
   reste modifiable à tout moment.

## Tutoriel 3 — Weighted Normal (GEO_Block)
1. Sélectionnez le pavé (il est en Shade Smooth : taches sur les grandes faces).
2. Properties → Modifiers → *Add Modifier → Normals → Weighted Normal*.
3. Cochez **Keep Sharp** et **Face Influence**, réglez **Weight** sur 100. Les grandes faces
   deviennent parfaitement planes, les chanfreins accrochent la lumière.
4. Essayez Weight 50 puis 100 en orbitant : la différence se voit dans les reflets.

## Tutoriel 4 — Vérifier
Enregistrez `ch02_04_normals_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_04_normals_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_04.py" --python-exit-code 1 -- --exercise normals --render
```
