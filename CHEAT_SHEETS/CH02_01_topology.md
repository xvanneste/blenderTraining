# Fiche de révision — CH02.01 Topologie

Forme = position des sommets · Topologie = liaisons. Quads = standard ; tris = plans, à limiter ;
n-gons = OK si plat et statique.
Boucle `Alt+clic` · anneau `Ctrl+Alt+clic`. Pôle = 3 ou ≥ 5 arêtes ; à placer sur zone plate.
Densité homogène, cage légère + subdivision.

| Défaut | Trouver | Réparer |
|---|---|---|
| N-gons | Select All by Trait → Faces by Sides (4, Greater Than) | Knife, Grid Fill, `J` |
| Triangles | Faces by Sides (3, Equal To) | `Alt+J` Triangles to Quads |
| Doublons | Statistics | `M` → By Distance |
| Trous | Non Manifold | `Alt+F`, `F`, Grid Fill |
| Isolés / internes | Loose Geometry / Interior Faces | supprimer |
Overlays : Statistics · Mesh Analysis (Overhang, Thickness, Intersect, Distortion, Sharp).
