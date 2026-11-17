# CH09.06 — Cours théorique : Exposition et contraste

## 1. Valeurs de scène et image affichée
Le rendu calcule des valeurs linéaires (le soleil peut valoir des centaines). Pour l'affichage, la gestion des couleurs applique une vue puis l'exposition et un look.

## 2. Vue
Standard coupe à 1 : tout ce qui dépasse devient blanc uni. AgX, Filmic et Khronos PBR Neutral compriment progressivement les hautes lumières. Mesures (96 × 96) : Standard : 4,5 % brûlés ; AgX : 0 % ; AgX +0,5 : 0 % et moyenne 0,42 ; Khronos PBR Neutral : 0 %, écart 0,87.

## 3. Exposition
Exposure se compte en diaphragmes : +1 double la lumière. Moyenne visée : 0,3 à 0,55.

## 4. Look
Après la vue, un Look règle le contraste : AgX - Punchy assombrit (moyenne 0,279), AgX - High Contrast brûle 2,7 % de pixels. Les noms exacts s'obtiennent dans l'interface ; ils dépendent de la vue.

## 5. Lire une image
Trois nombres : pixels brûlés (≤ 1 %), luminance moyenne (0,3–0,55), contraste (p95 − p5 ≥ 0,55).

## 6. L'exercice
Scène : sol gris, sphères Bright (émission 6), Mid, Dark, soleil 3 W/m². Properties > Render > Color Management : View Transform, Look, Exposure.

## 7. Pièges
- Régler l'exposition avec la vue Standard : les hautes lumières restent brûlées.
- Ne comparer que la moyenne (un look sombre a une belle étendue mais une moyenne basse).
- Corriger l'exposition de la scène au lieu de la vue.

## 8. Limites
Une seule scène ; seuils calibrés dessus ; vues et looks listés par l'interface (non énumérables en -b) ; pas de rendu EEVEE testé.
