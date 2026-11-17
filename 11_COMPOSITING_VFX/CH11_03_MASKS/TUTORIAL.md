# CH11.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_03_masks_starter.blend`. Sauvegardez sous `ch11_03_masks_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Compositing : Render Layers a une prise Object Index ; trois sphères en couleur.

## Tutoriel 2 — Désaturer (10 min)
Ajoutez un nœud Hue/Saturation : Saturation 0.

## Tutoriel 3 — Masquer (15 min)
Ajoutez ID Mask (Index 2, entrée ← Object Index) puis Mix (Factor = masque, A = désaturé, B = image) → Group Output.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : saturations de A, B, C et du fond.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_03_masks_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_03.py" -- --exercise masks --debug
```

Remarque d'honnêteté : les nœuds `CompositorNodeIDMask`, `CompositorNodeCryptomatteV2` et `ShaderNodeMix`, la prise « Object Index » de Render Layers (Cycles seulement) et les prises du nœud Cryptomatte ont été vérifiés par exécution ; la variante Cryptomatte (source Render, matte_id Sphere_B) a été construite depuis la solution et validée (41/41) mais n'est pas livrée comme fichier ; les menus de création de nœuds et le sélecteur de Cryptomatte (clic sur le Pick) n'ont pas été regardés dans l'interface ; les mesures portent sur trois sphères à bords nets.

## Variante de contrôle

Contrôlez le masque seul en niveaux de gris avant de modifier la couleur d’un objet. Testez une transition douce sur un contour étroit. **Preuve** La modification affecte l’objet visé, et la comparaison montre si le contour laisse passer une partie du fond.
