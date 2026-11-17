# CH09.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_07_composition_starter.blend`. Sauvegardez sous `ch09_07_composition_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Vue caméra (Numpad 0) : le sujet est au centre. Properties > Object Data (caméra) > Viewport Display > Composition Guides : cochez Thirds (panneau et option vérifiés dans les sources 5.3) pour voir la grille.

## Tutoriel 2 — Shift X (5 min)
CAM > Object Data Properties (caméra) > Lens > Shift X : 0,167. Le sujet passe au tiers gauche.

## Tutoriel 3 — Shift Y (5 min)
Shift Y : −0,1. L'horizon monte au tiers haut.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : position du sujet, horizon, marges, taille.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_07_composition_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_07.py" -- --exercise composition --debug
```

Remarque d'honnêteté : le rendu de contrôle est du Workbench plat (couleurs d'objet) segmenté par couleur : il suppose un sujet rouge, un ciel bleu et un sol gris (les couleurs de la scène) ; les calibrages (Shift X +0,167 → 33 %, Shift Y −0,1 → 33 %) sont mesurés sur cette scène ; les libellés Viewport Display > Composition Guides > Thirds ont été relus dans le fichier `bl_ui/properties_data_camera.py` (l'affichage n'a pas été regardé dans l'interface) ; les libellés Lens > Shift X / Y viennent de l'API. Grille des tiers (numpy) regardée sur le rendu de départ et la solution.

## Variante de contrôle

Comparez un recadrage par décalage du film à un changement de direction de la caméra. Tracez des repères verticaux du décor. **Preuve** Le résultat choisi place le point d’intérêt à la bonne hauteur tout en gardant la perspective voulue.
