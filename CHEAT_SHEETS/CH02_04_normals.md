# Fiche de révision — CH02.04 Normales

Normale de face (orientation) · normales de coin (utilisées au rendu).
**Voir** : Viewport Overlays → Face Orientation (bleu dehors, rouge dedans).
**Réparer** : Edit, `A`, `Shift+N` Recalculate Outside · `Shift+Ctrl+N` Inside · Flip · menu `Alt+N`.
Défaut d'orientation souvent invisible au rendu mais casse Solidify, exports, culling, booléens.

Object → Shade Flat / Shade Smooth / **Shade Auto Smooth** (modificateur Smooth by Angle, 30°).
Auto Smooth de l'ancien panneau Object Data : supprimé depuis 4.1. Arête vive : Edge → Mark Sharp.
**Weighted Normal** (Add Modifier → Normals) : Face Area, Weight 50 neutre → 75–100 grandes faces
planes, Keep Sharp, Face Influence (Set Face Strength). Toujours en fin de pile, objet en Smooth.
