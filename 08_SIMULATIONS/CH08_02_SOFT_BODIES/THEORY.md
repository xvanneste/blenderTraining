# CH08.02 — Cours théorique : Soft Bodies

## 1. Principe
Un Soft Body simule un maillage comme un réseau de masses (sommets) et de ressorts (arêtes) soumis à la gravité. Les ressorts résistent à l'étirement (Pull), à la compression (Push) et à la flexion (Bending).

## 2. Le goal
Chaque sommet reçoit un poids de goal (de 0 à 1, par un groupe de sommets) : il est tiré vers sa position d'origine avec cette force. Poids 1 : accroché ; poids 0 : libre. Paramètres : Default (sommets hors du groupe), Min et Max (plage des poids), Stiffness/Spring et Damping/Friction.

## 3. L'exercice
GEO_Plate : grille de 12 × 12 carrés (2 × 2 m, 169 sommets, 312 arêtes) à z = 2 m ; groupe « pin » : poids 1 sur le bord x = −1 (13 sommets), poids 0 ailleurs. Goal coché, groupe pin, Default 1,0, Min 0, Max 1 ; Edges coché, Pull 0,9, Push 0,9, Bending 1,0 ; masse 1 kg.

## 4. Mesures
Solution : 39/39 ; bord accroché immobile (0 mm) ; bord libre à z = 0,19 m (la plaque pend) ; arêtes étirées de 1,01 fois au plus ; plus bas 0,16 m. Contre-exemples : sans goal (−39 m) ; sans groupe (tout reste à 2,0 m) ; Pull et Push à 0,02 (étirement 2,8) ; masse 30 kg (étirement 1,20, bord libre à 1,10 m) ; sans arêtes (213 fois).

## 5. Piège mesuré sur le goal
Avec Goal Default à 0, la plaque entière est tombée, même avec un groupe de poids 1 sur le bord (essai en arrière-plan) ; avec Default 1,0 et des poids explicites 0 sur les sommets libres, l'accrochage a fonctionné. La règle de l'exercice est donc : Default 1, poids explicites.

## 6. Pièges
- Oublier le groupe ou les poids 0 explicites.
- Arêtes trop molles ou masse trop forte : plaque étirée.
- Lire la simulation sans repartir de l'image 1.
- Trop de sommets : simulation lente.

## 7. Limites
Une plaque, un seul accrochage, pas de collision avec un autre objet ni d'auto-collision ; mesure à l'image 100 (la plaque se balance encore : pas de test de repos) ; Soft Body ne remplace pas Cloth pour les tissus.
