# CH01.13 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Light Objects | https://docs.blender.org/manual/en/latest/render/lights/light_object.html |
| Manuel — World | https://docs.blender.org/manual/en/latest/render/lights/world.html |
| Manuel — Track To | https://docs.blender.org/manual/en/latest/animation/constraints/tracking/track_to.html |

Vérifications 5.3.0 (`properties_data_light.py`, API `bpy.types.Light`) : *Temperature*
(case + kelvins, la couleur devient *Tint*), *Exposure*, *Normalize*, *Radius* (Point/Spot),
*Angle* (Sun), *Shape* / *Size* (Area), *Custom Distance*, *Shadow*. Rendu de référence
contrôlé (luminance moyenne 0,31) et visuellement.
