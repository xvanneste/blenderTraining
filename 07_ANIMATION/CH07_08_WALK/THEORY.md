# CH07.08 — Cours théorique : Cycles de marche

## 1. Les quatre poses d'un pas
- **Contact** : le talon touche ; jambes écartées (0,6 m) ; hanches au plus bas (0,899 m).
- **Descente** : le corps s'abaisse sur la jambe d'appui, la jambe libre se replie.
- **Passage** : la jambe libre passe sous le corps ; hanches au plus haut (0,950 m).
- **Montée** : la jambe d'appui pousse, la libre avance.
Chaque pose existe de l'autre côté, 12 images plus tard. Le cycle fait 24 images (2 pas à 12 images) : à 24 i/s, un pas toutes les 0,5 s, soit 2 pas/seconde.

## 2. Marche sur place
Le personnage ne se déplace pas : le sol défile à la vitesse d'appui du pied. Le pied d'appui recule donc à vitesse constante (0,6 m en 12 images = 0,05 m/image).

## 3. Cinématique de la solution
Jambe = cuisse 0,43 m + jambe 0,47 m ; cheville à 0,05 m du sol. Pied : appui (y de −0,30 à +0,30, au sol) puis ballant (retour de +0,30 à −0,30 avec une levée en sinus de 0,12 m). Hanches : z = 0,05 + √(0,90² − y²) (jambe d'appui tendue) : 0,899 m aux contacts, 0,950 m aux passages. Le genou plie vers l'avant (−Y). Bras : balancement de ±20° opposé à la jambe du même côté.

## 4. Poses clés (angles par rapport à la verticale)

| Image | Pose | Cuisse G / D | Jambe G / D | Hanches (z) | Bras G / D |
|---|---|---|---|---|---|
| 1 | Contact | −19,6° / +19,4° | −19,4° / +19,6° | 0,899 m | +20° / −20° |
| 4 | Descente | −9,7° / −15,5° | −9,5° / +34,3° | 0,937 m | +14° / −14° |
| 7 | Passage | −0,1° / −31,4° | +0,1° / +28,5° | 0,950 m | 0° / 0° |
| 10 | Montée | +9,5° / −36,7° | +9,7° / +13,1° | 0,937 m | −14° / +14° |
(Angle de la direction du bone par rapport à la verticale descendante, dans le plan Y–Z : positif = vers l'arrière (+Y), négatif = vers l'avant (−Y). Images 13, 16, 19, 22 : les mêmes poses avec gauche et droite échangées ; image 25 = image 1.)


## 5. Boucle
L'image 25 est un double de l'image 1 : l'animation boucle en lisant les images 1 à 24 (ou 1 à 25 avec un doublon). À l'image 13 : demi-cycle (gauche et droite échangées).

## 6. Mesures
Solution : 42/42. Écart de boucle 0,0 mm ; pas 0,60 m ; 13 images au sol par pied ; levée 12 cm ; recul 0,050 m/image (écart à la droite 0 mm) ; amplitude des hanches 5,1 cm ; poignet gauche derrière le droit de 37,6 cm au contact gauche. Version à neuf clés (images 1, 4, 7, 10, 13, 16, 19, 22, 25), Bezier ou Linear : 42/42 (écart à la droite : 15 à 18 mm en Bezier, 0,6 mm en Linear).

## 7. Pièges
- Cycle qui ne boucle pas (saut à chaque pas).
- Pied d'appui qui glisse (interpolation ou clés trop éloignées).
- Pieds qui traînent (aucune levée).
- Hanches fixes (marche de robot).
- Bras du même côté que la jambe (marche de pantin).
- Pas trop court : le personnage patine.

## 8. Limites
Mannequin FK de capsules, marche sur place seulement, vue de profil non rendue (croquis de squelette numpy) ; pas de talon/pointe, pas de rotation du bassin ; la qualité du style n'est pas jugée.
