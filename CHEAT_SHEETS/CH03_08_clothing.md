# Fiche de révision — CH03.08 Vêtements

Workflow : collider simplifié (Collision, Wire, ÉVALUÉ) + sol (Collision) → tissu à maille régulière trouée au col → Physics > Cloth →
simuler (1→120) → APPLIQUER (Ctrl+A) → contrôler.
Réglages de la solution : Quality Steps 12 · Vertex Mass 0,3 · Air Viscosity 2 · Tension/Compression 15 · Shear 5 · Bending 0,4 ·
Damping 5/5/5/0,5 · Collisions Quality 5 · Distance 0,005 · Self Collisions décochées.
Mesures : 0 % de pénétration · arête ≈ repos (16 mm) · épaules couvertes ≥ 80 % · rugosité ≥ 3 mm · z ≥ 0.
Pièges : collider masqué = non évalué ; auto-collision = vibration ; tissu trop grand = nappe.
Correcteur : `--exercise poncho [--debug]`.
