# CH00.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — La VRAM | La scène doit tenir dans la mémoire de la carte graphique. |
| Q2 | **b** — Le CPU | Le CPU (sauf GPU Subdivision au viewport). |
| Q3 | — | Une limite de ressources fixée à l'avance : ex. 20 min de rendu par image, 10 Go de VRAM, 100 000 triangles par personnage, 2 Go de textures par décor. |
| Q4 | — | Non : cela dépend de la machine et de la scène ; il faut mesurer (benchmark). |
| Q5 | **c** — Vulkan | Vulkan depuis 5.3 (OpenGL reste disponible). |
| Q6 | — | Non : le backend concerne l'affichage (interface, viewport) ; Cycles utilise CUDA/OptiX/HIP/oneAPI ou le CPU. |
| Q7 | **c** — 64 000 | 1 000 × 4³ = 64 000. |
| Q8 | — | Les statistiques montrent la géométrie du viewport (Levels Viewport) ; le rendu utilise Levels Render, souvent plus élevé. |
| Q9 | — | Menu Overlays de la vue 3D > Statistics. |
| Q10 | **b** — Ctrl+L | Ctrl+L. (Ctrl+J joint les objets, Alt+D crée une duplication liée, Shift+D une copie.) |
| Q11 | — | Il plafonne globalement (subdivision, etc.) sans modifier les objets : réversible en un clic, idéal pour prévisualiser ou sécuriser un rendu. |
| Q12 | — | Les 200 changent : ils partagent les mêmes données. Pour en isoler un : Object Data > bouton du nombre d'utilisateurs (Make Single User). |
<!-- QUIZ_ANSWERS_END -->

## Exercices de leçon
- **L1 moyen :** fumée → CPU + RAM ; EEVEE → GPU + VRAM ; Geometry Nodes → CPU ; montage →
  RAM + disque (+ décodage vidéo) ; Cycles GPU → GPU + VRAM.
- **L1 difficile :** les déformations (armatures, modificateurs) sont calculées par le CPU,
  objet par objet ; le GPU attend des données. Solutions : proxies basse résolution, Simplify,
  désactiver les modificateurs au viewport, découper la scène.
- **L3 :** 80 × 4³ = 5 120 ; 20 000 × 4² × 50 = 16 000 000 → trop pour une foule : versions
  basse résolution (LOD) pour les personnages lointains, Subdivision rendu 1, instances.

## Exercice 1
Starter : 200 galets + sol + fond, ≈ 320 000 faces viewport (Subdivision 2), 16 384 002
estimées au rendu, 202 maillages distincts. Cause : Subdivision **rendu 5** (×1 024) et
données dupliquées.

## Exercice 2 (valeurs de référence)
| Étape | Faces estimées | Maillages |
|---|---|---|
| Starter | 16 384 002 | 202 |
| 1. Données partagées | 16 384 002 | 3 |
| 2. + Subdivision 1/2 | 256 002 | 3 |
| 3. + Simplify (Max 1/2) | 256 002 | 3 |
Le partage ne change pas ce qui est rendu (chaque galet reste subdivisé) mais Blender ne
stocke plus 200 copies du maillage d'origine : fichier et RAM plus légers.

## Exercice 3
Fichier de référence : `COMPLETED_EXAMPLES/ch00_03_heavy_scene_solution.blend`
(maillage partagé, Subdivision 1/2, Simplify 1/2 → 256 002 faces, 3 maillages).
Mesure de référence (RTX 3080, OptiX, 50 %, 32 éch.) : 8,1 s → 5,5 s.
