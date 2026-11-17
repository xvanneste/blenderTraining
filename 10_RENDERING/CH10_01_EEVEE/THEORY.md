# CH10.01 — Cours théorique : EEVEE en profondeur

## 1. EEVEE
Moteur de rendu temps réel : rasterisation + approximations. Rapide, mais certaines lumières (réflexions hors écran, caustiques) sont approchées.

## 2. Les ombres
Render Properties > Sampling > Shadows (case d'en-tête). Sans elle, aucune ombre portée : rapport ombre / lumière 0,96 ; avec : 0,70.

## 3. Le ray tracing
Render Properties > Raytracing (case d'en-tête). Il rend les réflexions et la lumière indirecte approchée dans l'espace écran. Mesuré sur la sphère chromée : écart-type de la luminance 0,008 sans, 0,081 avec.

## 4. Fast GI Approximation
Sous-panneau de Raytracing (case d'en-tête, relu dans bl_ui). Non mesuré ici : l'activer ne changeait aucune zone testée.

## 5. Les échantillons
Sampling > Render > Samples. Peu d'échantillons : bruit et reflets instables (8 échantillons : sphère correcte mais hors plage du correcteur ; 1 échantillon avec ray tracing : 0,022). Beaucoup : temps perdu pour peu de gain (512 : mêmes valeurs qu'à 64).

## 6. L'exercice
Départ : Shadows off, Raytracing off, 1 échantillon. Solution : Shadows, Raytracing, 64 échantillons.

## 7. Pièges
- Régler EEVEE puis rendre avec Cycles (le correcteur vérifie le moteur).
- Croire que le ray tracing d'EEVEE égale Cycles.
- Monter les échantillons sans mesurer le gain.
- Oublier d'activer les ombres sur chaque lampe (non testé ici).

## 8. Limites
Une scène ; trois zones d'image fixes ; Fast GI non mesuré ; pas de mesure de temps (non déterministe).
