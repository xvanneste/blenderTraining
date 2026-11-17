# CH02.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_04_normals_starter.blend`. Passez le viewport en **Material Preview**
(`Z` → Material Preview) : la boîte de conserve a des reflets « gonflés », le pavé bleu des taches.
Comparez la [vue avant correction](COMPLETED_EXAMPLES/ch02_04_normals_starter_view.png)
et le [rendu de référence](COMPLETED_EXAMPLES/ch02_04_normals_reference.png).

## Tutoriel 1 — Voir l'orientation (GEO_Flipped)
1. Viewport Overlays → cochez **Face Orientation**. Des carrés **rouges** apparaissent sur le cube.
2. Lancez `F12` : le rendu paraît correct ! Le défaut est invisible ici… mais pas pour Solidify,
   les exports ou le Backface Culling (essayez : Viewport Shading → *Backface Culling*).
3. Sélectionnez le cube, `Tab`, `A`, **`Shift+N`** (*Mesh → Normals → Recalculate Outside*).
   Les faces retournées cessent d’apparaître en rouge depuis l’extérieur. La couleur
   des faces avant dépend du thème d’affichage.

## Tutoriel 2 — Lisser avec des arêtes vives (GEO_Can)
1. Object Mode, sélectionnez la boîte. **Object → Shade Auto Smooth**.
2. Panneau de l'opération : *Angle* **30°**. Les couvercles redeviennent plats, le flanc reste lisse.
3. Properties → Modifiers : un modificateur **Smooth by Angle** est apparu ; son réglage *Angle*
   reste modifiable à tout moment.

## Tutoriel 3 — Weighted Normal (GEO_Block)
1. Sélectionnez le pavé (il est en Shade Smooth : taches sur les grandes faces).
2. Properties → Modifiers → *Add Modifier → Normals → Weighted Normal*.
3. Cochez **Keep Sharp** et réglez **Weight** sur 100. Comparez les reflets, car le
   modificateur pondère les normales d’ombrage sans déplacer les sommets. Activez
   **Face Influence** pour le réglage de l’exercice. Il utilise les valeurs de *Face
   Strength* lorsque le maillage en porte.
4. Essayez Weight 50 puis 100 en orbitant : la différence se voit dans les reflets.

## Tutoriel 4 — Vérifier
Enregistrez `ch02_04_normals_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_04_normals_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_04.py" -- --exercise normals --render
```

## Variante de contrôle

Inspectez séparément Face Orientation et les reflets. Sur GEO_Flipped, vérifiez l’orientation depuis l’extérieur après Shift+N. Sur GEO_Block, gardez la caméra et la lumière fixes pour comparer avec et sans Weighted Normal. **Preuve** Les faces ne changent pas de position. Vous expliquez la différence entre corriger une orientation et contrôler la normale utilisée pour l’ombrage.

[Manuel Blender 5.3 des normales](https://docs.blender.org/manual/en/5.3/modeling/meshes/editing/mesh/normals.html)
