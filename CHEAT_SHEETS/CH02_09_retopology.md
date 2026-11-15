# Fiche de révision — CH02.09 Retopologie

But : cage légère en quads sur une forme dense. Densité selon l'usage ; boucles où ça plie.
**Rapide** : cube Subdivide (5) → To Sphere → mise à l'échelle qui **enveloppe** → Shrinkwrap
(Nearest Surface Point, Offset 5 mm). Cage trop petite = zones non couvertes.
**Manuelle** : aimant `Shift+Tab`, Snap Target for Individual Elements **Face Project**, Target
Selection : décocher **Include Active** ; **Poly Build** (clic extruder, `Ctrl+clic` face,
`Shift+clic` supprimer) ; overlay **Retopology** ; Mirror (Clip).
Contrôle : Statistics, X-ray, quads (Faces by Sides), Shrinkwrap Project final.
