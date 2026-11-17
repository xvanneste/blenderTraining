# CH08.08 — Cours théorique : Cheveux et fourrure

## 1. Parents et enfants
Un système Hair possède des parents (Number, ici 300) simulés et des enfants (Display Amount 10 par parent : 3 000) déduits. Hair Length en mètres ; Segments (hair_step) 6.

## 2. Racines
Les racines sont tirées sur la surface ; le groupe de sommets « scalp » (z > 0,3) pondère la densité (Vertex Groups > Density). Mesuré : racines à z ≥ 0,23 m.

## 3. Mèches
Children : Interpolated ; Clumping rassemble les enfants autour du parent. Mesure : distance extrémité enfant–parent le plus proche (étape 4 de `co_hair`) : 73 mm (Clumping 0), 39 mm (0,5), 0 (1).

## 4. L'exercice
Head : UV sphère de 1 m ; système « Hair » : 300 × 0,5 m, 6 segments, densité « scalp », enfants Interpolated 10, Clumping 0,5, Hair Dynamics.

## 5. Dynamique
Le moteur de tissu simule le cheveu (qualité 5, masse 0,3, rigidité de flexion 0,5 par défaut). Les cheveux dressés retombent : pointes à 0,96 m puis 0,28 m (images 1 et 30). Sans dynamique, ils restent figés.

## 6. Lire les données
Parents : `particles[i].hair_keys` (7 clés). Enfants : `co_hair(object, particle_no=nb_parents + j, step=k)` ; les étapes valides vont de 0 à 4 (5 et plus renvoient (0, 0, 0)).

## 7. Pièges
- `use_hair_dynamics` est une propriété du système (ParticleSystem), pas des réglages (ParticleSettings).
- Lire la simulation image par image.
- Beaucoup de parents ralentit la dynamique.

## 8. Limites
Pas de collisions avec la tête (la chevelure traverse la sphère : non testé) ; pas de rendu des cheveux ; nouvel objet Curves et nœuds de cheveux non testés ; pas de vent (CH08.09).
