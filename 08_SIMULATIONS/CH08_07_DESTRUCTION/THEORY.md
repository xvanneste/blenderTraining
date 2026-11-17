# CH08.07 — Cours théorique : Destruction

## 1. Pièces et liaisons
Un décor qui se brise est un ensemble de pièces rigides (ici 24 briques) maintenues par des contraintes. Physics > Rigid Body > Connect (menu Object > Rigid Body > Connect) crée des objets « Constraint » entre les objets sélectionnés : Type (Fixed…), Location (Center), Connection Pattern (Selected to Active ou Chain by Distance). Il n'y a PAS de réglage de distance : pour un mur il faut connecter les voisines une paire à la fois (38 paires).

## 2. Contrainte cassable
Panneau Settings de la contrainte (onglet Physics de l objet Constraint) : Breaking coché, Threshold (seuil). Au-dessus du seuil la liaison est détruite.

## 3. L'exercice
Sol Ground (12 × 12 m, Passive) ; briques Brick_i_k 0,5 × 0,3 × 0,5 m ; boulet Wreck_Ball 40 kg, Animated de 1 à 60 (de y = −5 à y = 2) puis lâché ; monde 30 sous-étapes, 30 itérations, images 1–120. Solution : 38 Fixed, Breaking, seuil 1.

## 4. Mesure
La rupture ne laisse pas de trace dans l'API (la propriété enabled reste vraie) : le correcteur compare la distance entre briques voisines à l'image 120 et au repos (écart > 10 cm = liaison cassée). Solution : 12 à 13 liaisons sur 38 (seuils 0,5 à 2) ; seuil 5 ou plus : 0.

## 5. Stabilité
Mesuré : avec le boulet à ≈ 5 m/s (30 images) et 10 sous-étapes, tout le mur est expulsé et traverse le sol (z jusqu'à −68 m) ; boulet à ≈ 2,5 m/s (60 images) et 30 sous-étapes : comportement raisonnable. La cause exacte n'a pas été isolée.

## 6. Pièges
- Connect sans distance : une seule passe SELECTED_TO_ACTIVE par paire.
- Un boulet animé qui traverse les briques trop vite.
- Seuil trop haut ou case Breaking oubliée.
- Sol sans physique.

## 7. Limites
Pas de fracture automatique (Cell Fracture absente de la 5.3 de base) ; les pièces sont des briques régulières ; la rupture est mesurée indirectement ; ni débris ni poussière (voir CH08.04, CH08.06) ; le boulet est un cube.
