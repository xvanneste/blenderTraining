# CH18.06 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Grease Pencil (introduction, structure) | https://docs.blender.org/manual/en/latest/grease_pencil/index.html |
| Manuel — Modes Grease Pencil | https://docs.blender.org/manual/en/latest/grease_pencil/modes/index.html |
| Manuel — Draw Mode, Stroke Placement | https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/stroke_placement.html |
| Manuel — Layers | https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html |
| Manuel — View Layer passes | https://docs.blender.org/manual/en/latest/render/layers/passes.html |
| Rapport Blender T92052 (GP au-dessus de la géométrie au rendu) | https://developer.blender.org/T92052 |

Ressources produites (licence BCMA) : scène de départ, solution générée par script, correcteur
(position des traits mesurée par rapport à la caméra), rendu de référence regardé.

Note de vérification : le comportement « passe Z » a été mesuré pour ce chapitre (différence
d'images avec / sans dessin sur la zone de la maison : 256 pixels modifiés sans passe Z, 0 avec)
dans Blender 5.3.0 ; même résultat dans 5.2.0 sur une scène minimale.
