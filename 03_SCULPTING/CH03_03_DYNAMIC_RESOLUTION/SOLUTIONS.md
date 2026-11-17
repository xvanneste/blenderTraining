# CH03.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Ses masses ne se chevauchent pas (pas de cou, de taille, bras écartés de la cage) : seules les masses qui se recouvrent fusionnent. |
| Q2 | **b** — Ctrl+R | R règle la taille de voxel à l'écran. |
| Q3 | **b** — Les détails fins (doigts) disparaissent | Le volume est reconstruit à la résolution du voxel. |
| Q4 | — | Tout désélectionner (Alt+A) pour ne pas joindre le sol ou d'autres objets, puis sélectionner seulement les masses. |
| Q5 | — | Il ajoute ou retire des triangles sous la brosse pendant le sculpt : densité locale à la demande. |
| Q6 | **c** — Multiresolution | Les autres reconstruisent la topologie. |
| Q7 | — | Pour garder un affichage fluide tout en sculptant au niveau de détail maximal. |
| Q8 | — | Non : la base légère sert au rig ; le détail est cuit en textures (normal/displacement). |
| Q9 | **b** — DynTopo | Densité ajoutée localement. |
| Q10 | — | Masses + Voxel Remesh, exploration (DynTopo/Remesh), retopologie, Multires sur la base propre, cuisson des détails. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
`COMPLETED_EXAMPLES/ch03_03_remesh_solution.blend` (+ `_reference.png`) : cou (cylindre r = 6,8 cm),
abdomen, deux épaules ajoutés ; masses jointes, échelle appliquée, Voxel Remesh 0,012 m.
Mesures : 1 composante, 0 arête non manifold, 100 % de quads, arête moyenne 1,02 cm, 18 278 faces,
1,75 m. Contre-épreuve : les mêmes masses SANS ponts → 3 composantes, refusé avec la piste « ajoutez
cou, abdomen, épaules ».
Note : lors d'un essai, le sol du studio, resté sélectionné, a été joint aux masses (objet de 20 m,
5,5 millions de faces) — d'où la consigne « Alt+A avant de sélectionner les masses ».

## Exercice 2
`COMPLETED_EXAMPLES/ch03_03_multires_solution.blend` : Multires 5 niveaux (Catmull-Clark), Levels
Viewport 3, Sculpt 5, Render 5 ; base de 384 faces intacte. **Sculptée à la brosse au niveau 5** dans Blender 5.2 via MCP (*Inflate/Deflate* pour nez, pommettes, orbites et bouche, *Draw* pour les arcades, *Smooth*) :
2 043 sommets déplacés, jusqu'à 9,7 mm, la base de 384 faces reste intacte (le détail vit dans le Multires). Le correcteur mesure le relief local au niveau max :
0,029 mm (solution) contre 0,002 mm pour `COUNTER_EXAMPLES/ch03_03_multires_nosculpt.blend` (Multires bien réglé mais jamais sculpté : refusé).

## Exercice 3 — réponses de DECISIONS
1 VOXEL (fusion de boules) · 2 DYNTOPO (densité locale) · 3 MULTIRES (base légère conservée) ·
4 VOXEL (densité uniforme) · 5 MULTIRES (seul à conserver la topologie, donc les UV).
Tailles de voxel (mesures indicatives à refaire chez vous) : 0,03 m → mains et doigts « fondus » ;
0,012 m → bon blocage ; 0,005 m → plusieurs centaines de milliers de faces, réservé au détail.
