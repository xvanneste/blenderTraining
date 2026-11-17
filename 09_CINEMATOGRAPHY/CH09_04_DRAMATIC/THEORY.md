# CH09.04 — Cours théorique : Dramatique et stylisé

## 1. Intention et mesure
Une ambiance se décrit par deux nombres : le ratio de contraste (flanc éclairé / flanc d'ombre) et la luminance moyenne du sujet.

## 2. Low-key
Peu de lumière, presque pas de fill : ratio élevé et image sombre. Solution LOWKEY : Key 70 W, Fill 0,5 W, Rim 250 W ; ratio 8,8 ; moyenne 0,057 ; la Rim apporte 57 % de la bande du haut.

## 3. High-key
Beaucoup de lumière enveloppante : fill proche de la key. Solution HIGHKEY : Key 250 W, Fill 150 W, Rim 100 W ; ratio 0,9 ; moyenne 0,60.

## 4. Couleur
Deux teintes opposées sur le cercle chromatique (complémentaires) séparent les plans : Key orange (1 ; 0,65 ; 0,35) = teinte 28°, Rim bleu-vert (0,35 ; 0,75 ; 1) = 203°.

## 5. Deux scènes
Scene Properties, menu des scènes en haut de la fenêtre. Objets partagés (liés dans les deux scènes) : Subject, CAM, EMP_Target ; lampes propres à chaque scène.

## 6. Mesure
Par scène : rendu avec toutes les lampes (zones flanc éclairé, flanc d'ombre, bande du haut) puis sans la Rim (contribution). Cycles CPU, 96 × 96, 48 échantillons.

## 7. Pièges
- Jouer sur le ratio sans toucher à la quantité de lumière.
- Une Rim de même teinte que la Key : aucune séparation.
- Modifier la scène active sans le savoir (vérifier le nom de la scène).

## 8. Limites
Sujet sphérique unique ; pas de fond ni de décor ; teintes limitées à orange / bleu-vert ; mesure par zones, pas de jugement esthétique.
