# Fiche de révision — CH04.01 UV

Seams (Edge > Mark Seam, Ctrl+E) sur les arêtes vives · Unwrap (Angle Based / Conformal / Minimum Stretch) · Average Islands Scale (même densité de texels) · Pack Islands (Rotate, Margin ≈ 0,02) → tout dans [0, 1].
Contrôle : damier UV Grid = carrés réguliers.
Seuils du correcteur : étirement moyen ≤ 1,15 (p95 ≤ 1,6) · densité (écart-type du log) ≤ 0,20 · chevauchement ≤ 2 % · occupation ≥ 50 % · 4–40 îlots · ≥ 6 seams.
Solution : 22 îlots, étirement 1,00, occupation 68 %. Correcteur : `--exercise uv [--debug]`.
