# CH11.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_04_depth_fx_starter.blend`. Sauvegardez sous `ch11_04_depth_fx_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Image 10 : trois barres nettes.

## Tutoriel 2 — Defocus (15 min)
Activez les passes Z et Vector sur le calque qui contient les barres. Réglez la distance de mise au point de la caméra à 5 m. Reliez *Render Layers → Image* à *Defocus → Image*, et *Depth* à *Z*. Activez *Use Z-Buffer* et réglez le F-stop du nœud à 1. Contrôlez la barre centrale avant de poursuivre.

## Tutoriel 3 — Vector Blur (10 min)
Reliez l’image de *Defocus* à *Vector Blur → Image*. Connectez *Vector* de *Render Layers* à *Speed* et *Depth* à *Depth*. Réglez *Shutter* à 1 et reliez le résultat à la sortie du Compositor. Comparez sur la même image avec *Shutter* à zéro pour isoler le flou de mouvement.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : pics de Near et Far, largeur de Mover.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_04_depth_fx_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_04.py" -- --exercise depth_fx --debug
```

Remarque d'honnêteté : les nœuds `CompositorNodeDefocus` (Image, Z ; propriétés scene, use_zbuffer, f_stop, blur_max) et `CompositorNodeVecBlur` (Image, Speed, Depth, Samples, Shutter) et les prises « Depth » et « Vector » de Render Layers ont été vérifiés par exécution en 5.3 ; la distance de mise au point du Defocus vient de `Camera.dof.focus_distance` (constaté : elle agit même avec use_dof désactivé) ; les valeurs (Far 0,92 → 0,30 ; Mover 12 → 27 px) sont mesurées sur ces barres à 320 × 180 ; les menus de création de nœuds et le libellé « Focus Distance » n'ont pas été regardés dans l'interface ; la mise au point à 30 m a laissé Near nette dans l'essai (le défocus en post n'est pas symétrique devant le plan net) : non mesuré en détail.

## Variante de contrôle

Testez un objet proche et un objet éloigné à partir de la même profondeur. Regardez un bord où ils se superposent. **Preuve** La profondeur sélectionne les bons plans et les limites aux occlusions sont visibles dans un cadre de contrôle.
