# CH07.09 — Cours théorique : Course, saut, interactions

## 1. La course
Comme la marche, un cycle (deux pas) ; mais chaque pas comporte une phase aérienne (les deux pieds hors du sol), un pas plus court en durée (moins d'images), une inclinaison du corps vers l'avant, des bras plus fléchis et plus amples, des foulées qui se posent sur l'avant du pied. Cycle typique : 16 à 18 images (non testé ici).

## 2. Interactions
Pousser : corps incliné, pieds écartés et bas, mouvement lent et appuyé. Tirer : poids vers l'arrière, bras tendus. L'objet bouge après le contact de la main (overlap). Prendre un objet : approche, anticipation, contact, retrait (non testé ici).

## 3. Le saut en quatre phases
1. **Anticipation** : flexion (hanches de 0,95 à 0,65 m, images 4 à 8).
2. **Impulsion** : extension rapide (0,65 à 0,95 m en 2 images) ; décollage à l'image 10.
3. **Vol** : parabole (g = 0,01703 m/image²) ; 14 images de décollage à contact (images 10 à 24), sommet à l'image 17 : 1,367 m, soit 0,417 m au-dessus du décollage.
4. **Réception** : amortissement (0,68 m à l'image 28) puis retour debout (0,95 m à l'image 36).

## 4. Hanches et jambes
Les hanches (bone hips, position Z) pilotent le saut ; les chevilles sont au sol hors du vol (z = 0,05 m) ; en vol z_cheville = z_hanches − e avec e de 0,90 m à 0,78 m aux images 10–12 et de 0,78 m à 0,90 m aux images 22–24 (jambes légèrement fléchies). Les jambes (cuisse 0,43 m, jambe 0,47 m) sont calculées par IK analytique.

## 5. Gravité
Pendant le vol : h = g·T²/8 (T en images, g = 9,81/24² m/image²). Mesure sur la solution : accélération médiane −0,0170 m/image² ; vol de 13 images au-dessus de 0,07 m ; hauteur 0,417 m.

## 6. Mesures
Solution : 43/43 ; flexion 0,65 m ; vol images 11 à 23 (13 images) ; hauteur 0,417 m ; réception 0,68 m ; pieds plantés (z max 0,050 m, glissement 0) ; retour 0,950 m. Contre-exemples : sans flexion (0,95 m) ; sans amortissement (0,95 m) ; vol de 21 images (accélération 0,0069) ; sommet à 0,12 m (0,0049) ; glissement de 73 mm ; fin à 0,722 m.

## 7. Pièges
- Pas d'anticipation : le saut part de nulle part.
- Parabole ratée (gravité de Lune ou de plomb).
- Réception sans amortissement.
- Pieds qui glissent avant et après le saut.
- Oublier le retour debout.

## 8. Limites
Un saut sur place, un mannequin FK ; course et interactions présentées mais non testées ; pas de déplacement horizontal ; les bras suivent des courbes simples non jugées.
