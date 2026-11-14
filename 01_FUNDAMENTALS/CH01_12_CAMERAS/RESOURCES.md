# CH01.12 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Cameras | https://docs.blender.org/manual/en/latest/render/cameras.html |
| Manuel — Camera View | https://docs.blender.org/manual/en/latest/editors/3dview/navigate/camera_view.html |
| Manuel — Depth of Field (Cycles) | https://docs.blender.org/manual/en/latest/render/cycles/object_settings/cameras.html |
| Manuel — Track To constraint | https://docs.blender.org/manual/en/latest/animation/constraints/tracking/track_to.html |

Vérifications 5.3.0 (`properties_data_camera.py`, API) : panneaux *Lens* (Type, Focal Length,
Lens Unit, Shift X/Y, Clip Start/End), *Camera* (Sensor Fit, Size), *Depth of Field* (Focus on
Object, Focus Distance), *Aperture* (F-Stop, Blades, Rotation, Ratio) ; types de caméra :
Perspective, Orthographic, Panoramic, Custom. Cadrage de la solution calculé et contrôlé par
projection (`world_to_camera_view`) puis vérifié visuellement sur le rendu de référence.
