# CH02.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_09_retopo_starter.blend`. `GEO_Sculpt` (20 480 triangles) est non
sélectionnable (Outliner : flèche de sélection désactivée) pour éviter de la modifier.

## Tutoriel 1 — Retopologie rapide par Shrinkwrap
1. Curseur 3D au centre du rocher : `Shift+S` → *Cursor to World Origin*, puis `N` → View → 3D
   Cursor Z = 0.62. `Shift+A` → *Cube*. `F2` → `GEO_Retopo`.
2. `Tab`, `A`, clic droit → **Subdivide**, panneau : *Number of Cuts* **5**.
3. `Shift+Alt+S` (*To Sphere*) → `1` `Entrée` : une sphère de quads. `Tab`.
4. `N` → *Item* → *Dimensions* ≈ **2 × 1,56 × 1,32 m** : la cage doit **envelopper** le rocher.
   `Ctrl+A` → *Scale*.
5. *Add Modifier → Deform → Shrinkwrap* : *Target* `GEO_Sculpt`, *Wrap Method* **Nearest Surface
   Point**, *Offset* **0.005**. La cage se colle au rocher : 216 quads au lieu de 20 480 triangles.
6. Masquez la sculpture au rendu (icône caméra de l'Outliner).

## Tutoriel 2 — Contrôler le résultat
1. `GEO_Retopo`, `Tab`, Viewport Overlays → **Retopology** : la cage s'affiche par-dessus.
2. `Alt+Z` (X-ray) : vérifiez qu'aucune zone du rocher ne dépasse de la cage.
3. Statistics : comparez le nombre de faces des deux objets.

## Tutoriel 3 — Retopologie manuelle (découverte)
1. Nouveau plan `GEO_Patch`, `Tab`, supprimez tout sauf une arête.
2. Activez l'aimant (`Shift+Tab`) ; menu Snapping : *Snap Target for Individual Elements* →
   **Face Project** ; *Target Selection* : décochez **Include Active**.
3. Activez **Poly Build** dans la barre d’outils. Glissez une arête pour l’extruder en
   quad. `Ctrl` et un clic créent un sommet et, lorsque le bord s’y prête, un triangle.
   `Shift` et un clic dissolvent un sommet ou suppriment une face. Tracez une bande
   de quads le long d’une crête et inspectez sa profondeur de côté.

[Manuel Blender 5.3 de Poly Build](https://docs.blender.org/manual/en/5.3/modeling/meshes/tools/poly_build.html)

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_09_retopo_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_09.py" -- --exercise retopo --render
```
Le correcteur mesure l'écart cage → sculpture et la couverture sculpture → cage (arbres BVH).

## Variante de contrôle

Choisissez une zone convexe et une zone où des surfaces se rapprochent. Comparez la projection dans deux vues éloignées de l’axe d’une seule caméra. Si la retopologie saute sur l’autre paroi, isolez la zone et revoyez la direction de projection ou l’épaisseur. **Preuve** Une tranche ou une vue latérale montre la bonne surface cible et des boucles lisibles.
