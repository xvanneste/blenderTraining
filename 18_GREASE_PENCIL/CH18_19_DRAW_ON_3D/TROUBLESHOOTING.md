# CH18.19 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Au rendu, le personnage passe devant la caisse | Passe Z désactivée | View Layer Properties > Passes > Data > Z |
| Line Art invisible | Radius trop petit (mètres) ou pas de caméra active | Radius ≈ 0,02 ; caméra active définie |
| Line Art vide | Mauvaise source ou calque cible | Source Type / collection ; Target Layer existant |
| Traits du personnage dispersés en profondeur | Stroke Placement : Surface au lieu de 3D Cursor | 3D Cursor + Drawing Plane Front |
| Personnage qui flotte | Curseur 3D au-dessus du sol | Curseur à z = 0 (Sidebar > View) |
| Affiche qui scintille | Traits exactement dans la surface | Offset de surface (0,005) |
| Le dessin sur surface « bave » sur d'autres objets | Projection sur tout ce qui est visible | Project Onto Selected + sélectionner la surface |
| Viewport lent | Line Art recalculé en permanence | Bake Line Art une fois le cadrage figé |
