# CH11.09 — Cours théorique : Intégration 3D/réel

## 1. Lire la lumière de la plaque
Les ombres réelles donnent la direction, la longueur donne la hauteur du soleil, leur netteté donne la dureté de la lumière.

## 2. Le shadow catcher
Un plan 3D (le sol) marqué Shadow Catcher : il n'affiche que les ombres des objets 3D, le reste est transparent. Propriété `Object.is_shadow_catcher` (Cycles).

## 3. Le film transparent
Render Properties > Film > Transparent (`render.film_transparent`) : fond et sol deviennent transparents.

## 4. Le soleil
Rotation X 50°, Z −50° : l'ombre du cube tombe à droite, comme celle du poteau de la plaque.

## 5. Composer
Alpha Over : Background = plaque, Foreground = Render Layers Image.

## 6. L'exercice
Départ : sol opaque, fond opaque, soleil à droite. Solution : catcher, film transparent, soleil à gauche, Alpha Over.

## 7. Pièges
- Soleil du mauvais côté.
- Sol non catcher ou film opaque.
- Oublier la plaque dans le compositeur.
- Cube flottant (sans contact avec le sol).

## 8. Limites
Plaque synthétique ; pas de HDRI capturé ni de grain ; caméra calée à la main.
