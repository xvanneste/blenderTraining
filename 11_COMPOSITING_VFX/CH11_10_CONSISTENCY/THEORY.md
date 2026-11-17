# CH11.10 — Cours théorique : Cohérence visuelle

## 1. Les trois critères
Exposition (luminance), dominante de couleur, grain : les premiers défauts qui trahissent une incrustation.

## 2. Exposition
Rapport de la luminance du dessus du cube à celle du sol de la plaque. Départ 1,86. Un diaphragme en moins ne suffit pas : −1 → 1,37 ; −2 → 1,01.

## 3. Dominante
(rouge − bleu) du dessus − (rouge − bleu) du sol : départ −0,20 ; Gain (1,3 ; 1,0 ; 0,6) : +0,007.

## 4. Où corriger
Entre Render Layers et Alpha Over : le rendu seul.

## 5. Grain
La plaque a un grain de 0,011. Cycles sans débruitage à 2 échantillons donne 0,012 sur le cube ; 128 échantillons : 0,0016 (trop propre).

## 6. L'exercice
Exposure −2, Color Balance Gain chaud, 2 échantillons.

## 7. Pièges
- Corriger l'image entière.
- Un seul critère juste.
- Débruiter le cube (il devient trop propre).
- Comparer des valeurs linéaires et affichées.

## 8. Limites
Trois critères ; un cube gris ; valeurs affichées ; pas de nœud de grain dédié trouvé en 5.3.
