# CH11.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_01_compositor_starter.blend`. Sauvegardez sous `ch11_01_compositor_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (10 min)
Espace de travail Compositing : l'arbre Render Layers → Group Output. F12 : image sombre et granuleuse.

## Tutoriel 2 — Exposure (10 min)
Ajoutez un nœud Exposure (Add > Color) entre les deux ; prise Exposure : 1,5.

## Tutoriel 3 — Blur (10 min)
Ajoutez un nœud Blur (Add > Filter) ; prise Size : 3 et 3 pixels.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : luminance, bruit, lisibilité.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_01_compositor_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_01.py" -- --exercise compositor --debug
```

Remarque d'honnêteté : l'API 5.3 du compositeur a été vérifiée par exécution (`scene.compositing_node_group`, nœuds `CompositorNodeRLayers`, `CompositorNodeExposure`, `CompositorNodeBlur`, `NodeGroupOutput` avec une prise « Image » ; le nœud `CompositorNodeGamma` n'existe plus ; les réglages sont des prises) ; la case Compositing (Output Properties > Post Processing > Pipeline) a été relue dans `bl_ui/properties_output.py` ; je n'ai pas vérifié comment l'interface 5.3 crée l'arbre de compositing de la scène (le fichier de départ le fournit) ni les menus Add > Color et Add > Filter ; Viewer et Backdrop ne sont pas mesurés ; les valeurs (0,277 → 0,459 ; bruit 0,019 → 0,0063) sont mesurées sur cette scène à 128 × 72.

## Variante de contrôle

Séparez une sortie de diagnostic et l’image finale. Comparez Exposure sur l’intervalle bas et haut de votre rendu en gardant la même visualisation. **Preuve** Les deux sorties sont identifiables et le graphe relu correspond à l’image réellement exportée.
