# CH10.02 — Cours théorique : Cycles en profondeur

## 1. Les rebonds
Chaque rebond diffus renvoie la lumière sur une autre surface mate. Max Bounces > Total plafonne l'ensemble ; Diffuse, Glossy, Transmission, Volume, Transparent plafonnent chaque famille.

## 2. La lumière indirecte
Pièce sans rebond : seul ce que la lampe voit directement est éclairé. Mesuré : plafond 0,013 (Diffuse 0) contre 0,33 (Diffuse 4).

## 3. Les échantillons
Chaque échantillon ajoute un rayon par pixel : moins de bruit, plus de temps. Mesuré : 4 échantillons → bruit 0,049 ; 64 → 0,0097.

## 4. L'échantillonnage adaptatif
Case dans l'en-tête de Sampling > Render (Noise Threshold). Les pixels qui convergent s'arrêtent ; Max Samples plafonne le total. Le seuil 0,5 laisse plus de bruit (0,0138 contre 0,0097).

## 5. Mesurer le bruit
Deux rendus avec deux graines : le signal est identique, la différence est du bruit pur ; l'écart-type de la différence divisé par √2 estime le bruit de chaque rendu.

## 6. L'exercice
Départ : Diffuse 0, adaptatif off, 4 échantillons. Solution : Diffuse 4, adaptatif on, seuil 0,02, 64 échantillons.

## 7. Pièges
- Régler le bruit avec un grand nombre d'échantillons au lieu d'un seuil.
- Oublier que les lampes orientées vers le bas n'éclairent pas le plafond sans rebonds.
- Confondre bruit et lucioles (pixels très clairs isolés, voir CH10.03).
- Mesurer le temps sur une machine occupée.

## 8. Limites
Light Tree (Sampling > Lights), caustiques (Light Paths > Caustics) et rebonds glossy ne sont pas mesurés ; une seule scène ; CPU.
