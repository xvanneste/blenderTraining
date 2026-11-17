# CH11.05 — Cours théorique : Glare et effets

## 1. Glare
Nœud Glare : Type (Bloom, Ghosts, Streaks, Fog Glow, Simple Star), Quality, Threshold, Strength, Size. Mesuré (anneau 20–30 pixels) : sans 0,0003 ; Fog Glow 0,0066 ; Bloom 0,88 ; Ghosts 1,0.

## 2. Le seuil
Un halo ne vient que de valeurs supérieures à Threshold : un rendu HDR (lampe à 30) est nécessaire.

## 3. Doser
Fog Glow par défaut est subtil ; Bloom et Ghosts demandent de baisser Strength et Size.

## 4. Où placer le Glare
Avant la distorsion et l'étalonnage : sur des valeurs linéaires.

## 5. Lens Distortion
Prise Distortion (Radial) : mesuré 0,1 → +2 pixels, 0,3 → +7, 0,6 → la barre sort de l'image.

## 6. L'exercice
Render Layers → Glare (Fog Glow) → Lens Distortion (0,3) → Group Output.

## 7. Pièges
- Halo trop fort.
- Distorsion excessive (les bords sortent).
- Appliquer le Glare à une image écrêtée (valeurs ≤ 1).
- Mesurer le halo trop près de la lampe (la distorsion la grossit).

## 8. Limites
Pas de grain (pas de nœud dédié trouvé) ; pas de dispersion chromatique mesurée ; scène minimale.
