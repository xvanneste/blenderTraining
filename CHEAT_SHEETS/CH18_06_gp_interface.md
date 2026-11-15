# Fiche de révision — CH18.06 Grease Pencil : interface et objets

Objet GP → données → calques (+ groupes) → images clés → traits → points 3D.
**Add → Grease Pencil** : Blank · Stroke · Monkey · Scene/Collection/Object Line Art.
**Modes** (`Ctrl+Tab`) : Object · Edit · Sculpt · Draw · Weight Paint · Vertex Paint.
**File → New** : 2D Animation · Storyboarding.

| Réglage (en-tête Draw Mode) | Options |
|---|---|
| Stroke Placement | Origin · 3D Cursor · Surface · Stroke |
| Drawing Plane | View · Front (X-Z) · Side (Y-Z) · Top (X-Y) · Cursor |

Calques : `+`, dossier = groupe, cadenas, œil, Opacity ; `Y` menu calque actif ; `H` masquer le
calque actif, `Alt+H` tout réafficher ; `Num *` isoler.
**Rendu hybride : cocher View Layer → Passes → Data → Z** (sinon le GP passe devant la 3D).
Stroke Depth Order (Object Data → Settings) : ordre des traits entre eux (2D Layers / 3D Location).
Conventions : `GP_Nom`, collection DRAWINGS, un objet par élément indépendant.
