# Fiche de révision — CH02.07 Booléens et non destructif

Boolean (Generate) : Difference / Union / Intersect · Operand Type Object / **Collection** ·
Solver Float (rapide) / **Exact** (robuste) / Manifold (rapide, maillages fermés).
Cutter qui **dépasse** (jamais coplanaire). Collection CUTTERS, noms `CUT_*`, Display As **Wire**,
Show In **Renders** décoché, cutters parentés à la pièce.
Pile (haut → bas) : Mirror/Array → **Boolean** → **Bevel** (Harden Normals) → Weighted Normal.
Pas de subdivision après booléen. Appliquer seulement à la fin, sur une copie
(Object → Apply → Visual Geometry to Mesh). Trous traversants : V − E + F = 2 − 2g.
