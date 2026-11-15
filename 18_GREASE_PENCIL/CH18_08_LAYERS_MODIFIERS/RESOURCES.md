# CH18.08 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Grease Pencil Layers (masques, transformations) | https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html |
| Manuel — Modificateurs Grease Pencil | https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/index.html |
| Manuel — Line Art | https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html |
| Manuel — Visual Effects (Shader FX) | https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/index.html |

Vérifications faites dans Blender 5.3.0 : liste et catégories des modificateurs GP (menus
Edit/Generate/Deform/Color de `properties_data_modifier.py`), filtre de calque `tree_node_filter`
(libellé *Layer*), modes de fusion, effets disponibles (onglet *Effects*), libellés *Translation /
Rotation / Scale* du sous-panneau Transform. Comportement des masques mesuré par rendu (masque
caché = inactif ; opacité 0 = actif).

Ressources produites (licence BCMA) : scène de départ, solution, 2 rendus de référence regardés.
