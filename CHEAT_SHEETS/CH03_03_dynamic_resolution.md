# Fiche de révision — CH03.03 Résolution dynamique

Voxel Remesh : Object Data > Remesh > Voxel Size + Voxel Remesh (Sculpt : R taille, Ctrl+R remesh).
Masses qui SE CHEVAUCHENT (ponts : cou, abdomen, épaules) ; Alt+A avant de joindre ; Ctrl+A échelle.
Voxel ≈ H/150 pour un blocage (0,012 m). Preserve Attributes garde masque/couleurs.
DynTopo : case Dyntopo (Sculpt) ; Detail Size ; triangles ; détruit UV → remesh + retopo ensuite.
Multires : Subdivide ×n ; Levels Viewport < Sculpt = Render ; Unsubdivide, Delete Higher, Apply Base ;
ne pas appliquer (base légère = rig/UV).
Choix : fusionner/uniformiser → VOXEL · densité locale → DYNTOPO · détail sur base propre → MULTIRES.
