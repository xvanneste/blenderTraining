# CH08.03 — Cours théorique : Cloth

## 1. Cloth
Un modificateur Cloth transforme un maillage en tissu : ressorts d'arêtes (tension, compression), rigidité en flexion (Bending), amortissement (Air Damping), masse. Quality fixe le nombre de pas de calcul par image.

## 2. Collisions
Le tissu a ses propres réglages de collision (Collisions : Quality, Distance, auto-collision). Les obstacles sont des objets avec un modificateur Collision.

## 3. La scène
CLOTH_Sheet 2,4 × 2,4 m, grille 40 × 40, à z = 1,2 m ; COL_Ball (rayon 0,5 m, centre à l'origine) ; COL_Floor (plan 6 × 6 m à z = −0,5 m, tangent à la sphère).

## 4. Réglages de la solution
Quality 12 ; Bending Stiffness 0,4 ; Air Damping 5 ; Collisions : Quality 5, Distance 5 mm, Self Collisions décochées.

## 5. Mesures
Solution : 40/40 ; sommet central à z = 0,525 m ; distance minimale au centre de la sphère 0,520 m ; point le plus bas −0,475 m ; repos 10 mm (images 110 à 120). Contre-exemples : sans collision de la sphère (z central −0,475 m) ; sans collision du sol (−0,841 m) ; Quality 1 et Distance 50 mm (repos 42 mm) ; gravité à 0 (le drap reste à 1,2 m).

## 6. Pièges
- Oublier Collision sur un obstacle.
- Distance trop grande (le drap flotte au-dessus) ou trop petite (il traverse).
- Quality trop basse.
- Auto-collision inutile.
- Lire une image sans simuler depuis la première.

## 7. Limites
Un drap, deux obstacles fixes ; pas de pin (accrochage), de couture, de vent ni de vêtement sur personnage (CH03.08 et CH08.09) ; temps de calcul d'environ 10 s en arrière-plan pour 120 images.
