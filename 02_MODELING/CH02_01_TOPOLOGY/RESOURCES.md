# CH02.01 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Mesh Structure (sommets, arêtes, faces, boucles) | https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html |
| Manuel — Select All by Trait | https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html |
| Manuel — Merge / Clean Up | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html |
| Manuel — Grid Fill | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/grid_fill.html |
| Manuel — Mesh Analysis | https://docs.blender.org/manual/en/latest/modeling/meshes/mesh_analysis.html |

Vérifications faites dans Blender 5.3.0 : menus *Select All by Trait* (Non Manifold, Loose Geometry,
Interior Faces, Faces by Sides et ses types), raccourcis `Alt+J`, `M`, `Alt+F`, `J`, nom
*Merge by Distance*, types de Mesh Analysis. Le seuil de 80 % de quads est calculé : une UV Sphere
24 × 12 garde 48 triangles aux pôles (maximum 83 % de quads).

Ressources produites (licence BCMA) : scène de départ, solution (générée avec les mêmes opérateurs
que la consigne pour Grid Fill), rendu de référence regardé.
