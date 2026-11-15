# Fiche de révision — CH02.06 Subdivision Surface

Cage légère → surface limite lisse (Catmull-Clark). `Ctrl+0…5` (Object Mode). ×4 faces par niveau.
Modificateur : Levels Viewport (0–1) · Render (2–3) · Optimal Display · Simple/Catmull-Clark ·
Quality · Use Limit Surface · UV Smooth · Boundary Smooth · **Use Creases**.
**Boucles de maintien** : distance boucle–arête = rayon (Loop Cut + `S`/Edge Slide `G G`, ou Bevel
1 segment). **Crease** : `Shift+E` 0–1 ; overlay Crease. Cage en quads, pôles sur zones plates.
Scène lourde : Render → Simplify → Max Subdivision. Ne pas appliquer : modifier la cage.
Mesures CH02.06 : cube subdivisé 0,52 de remplissage → 0,99 avec boucles à 5 cm.
