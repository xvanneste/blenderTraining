# CH03.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — 3 et 2 | Les quatre doigts ont trois phalanges ; le pouce en a deux (plus un métacarpien mobile). |
| Q2 | — | Majeur > annulaire ≈ index > auriculaire (solution : index 95 % et annulaire 96 % du majeur). |
| Q3 | — | Il part du poignet (son métacarpien est dans la paume) et atteint à peu près la première articulation de l'index ; ici ≈ 61 % de la longueur du majeur. |
| Q4 | **b** — Ils s'effilent : phalanges proximales plus épaisses | Mesuré dans la solution : majeur 19,4 mm à la base, 16,9 mm près du bout (×1,15). |
| Q5 | — | Pour sculpter, retopologiser et peindre chaque doigt sans fusion ; on les rapproche ensuite par le rig. Une moufle est impossible à riguer. |
| Q6 | **b** — Le creux sous le milieu du pied qui ne touche pas le sol | Mesuré dans la solution : le milieu du pied est à 1,2 cm du sol. |
| Q7 | — | Le gros orteil, puis le 2ᵉ, 3ᵉ, 4ᵉ et le petit orteil en décroissant (à 2 mm près pour le correcteur) ; les vrais pieds varient, mais le gros orteil est le plus épais. |
| Q8 | — | Plus étroit : 59 % de la largeur de l'avant-pied dans la solution (le correcteur accepte 50–85 %). |
| Q9 | **a** — Mesh > Bisect avec Fill (ou Fill/Grid Fill) | Mesh > Bisect (Clear Inner / Clear Outer + Fill), comme le socle du buste en CH03.04. |
| Q10 | — | Parce que les doigts séparés produisent un pic chacun, avec un creux entre eux ; une moufle ou des doigts fusionnés n'en produisent presque pas (moufle de test : 2 pics). |
<!-- QUIZ_ANSWERS_END -->

## Exercices 2 et 3
`COMPLETED_EXAMPLES/ch03_07_hand_solution.blend` et `ch03_07_foot_solution.blend`, avec `_reference.png` (dessus, 3/4, profil).

**Honnêteté sur la fabrication.** Les deux solutions sont **générées par script** (`build_ch03_07_files.py`) à partir
d'ellipsoïdes qui se chevauchent, Join → Voxel Remesh 2,5 mm → lissage de Taubin → coupe plane (poignet, cheville, semelle).
Ce sont des **mannequins simplifiés** : la main évoque une main de mannequin de dessin (doigts légèrement « en chapelet »),
le pied est un volume stylisé (cheville tronquée, orteils en boules allongées). Ni l'un ni l'autre n'est un modèle anatomique.

Mesures du correcteur — main : un volume fermé, 21,9 cm × 18,2 cm × 4,0 cm, cinq pics (proéminences 0,06 / 0,07 / 0,13 / 0,08 /
0,04 m), majeur le plus long, index 95 % et annulaire 96 % du majeur, auriculaire 2 cm plus court, pouce à 61 % du majeur, majeur
effilé ×1,15. Pied : un volume fermé, 27,7 cm de long, 14,0 cm de haut avec la jambe, semelle 112 cm², voûte 1,2 cm, avant-pied
11,1 cm, talon à 59 %, cinq orteils décroissants.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| main `…_fused_fingers` | moufle | cinq doigts (2 pics) |
| main `…_four_fingers` | pas d'auriculaire | cinq doigts (4 pics) |
| main `…_equal_fingers` | quatre doigts de 7,5 cm | auriculaire le plus court |
| main `…_no_thumb` | pas de pouce | cinq doigts (4 pics) et largeur |
| main `…_tiny` | moitié d'échelle | longueur, largeur |
| pied `…_fused_toes` | bloc entre les orteils | cinq orteils (2 pics) |
| pied `…_four_toes` | pas de petit orteil | cinq orteils (4 pics) |
| pied `…_flat_foot` | pas de voûte | voûte (0,0 cm) |
| pied `…_short_big_toe` | gros orteil plus court que le 2ᵉ | gros orteil à l'extrémité, ordre décroissant |
| pied `…_tiny` | moitié d'échelle | longueur, hauteur, semelle… |
Aussi refusés : les deux starters, le pied à l'exercice `hand` et la main à l'exercice `foot`.

**Ce que le correcteur a révélé pendant la construction** (consigné aussi dans CLAUDE.md) :
1. une première semelle (ellipsoïdes descendus pour être coupés à z = 0) a **disloqué le pied en deux morceaux** et ne donnait
   que 39 cm² ; solution : deux patins plats centrés sur z = 0 (112 cm²) ;
2. le 5ᵉ orteil flottait hors de la balle (positions calculées avant le changement des rayons) : les positions sont désormais
   **calculées à partir des rayons** avec un écart fixe, et l'avant-pied est élargi ;
3. des orteils trop rapprochés fusionnent au remesh (4 pics au lieu de 5) : écart de 5 mm ;
4. l'intervalle de largeur de la main (9–17 cm) était faux : une main ouverte, pouce écarté, fait 18 cm.
Les guides Grease Pencil des starters ont aussi été refaits après un rendu : le premier était décentré (main) ou tourné de 90° (pied).

## Limites
- Le correcteur compte des pics : une main très « fermée » (doigts collés) échouera même si elle est correcte ; pour une autre
  pose, adaptez la pose de contrôle (CH03.10).
- Il suppose la convention d'axes (+Y, à plat / sur z = 0) et ≈ 2–3 mm d'arête.

## Essai de finition à la brosse (Blender 5.2 via MCP) — non retenu
Sur la main, j'ai essayé en vrai : *Smooth* le long de chaque doigt (3 passes, 1 236 sommets, **1,1 mm** au plus) puis *Inflate/Deflate* sur les jointures, *Crease Sharp* pour les tendons du dos
de la main et un pad à la base du pouce (703 sommets, **2,6 mm** au plus). Le correcteur reste vert (23/23) mais le rendu est quasiment inchangé : les « chapelets » viennent du pincement entre
ellipsoïdes à l'échelle du centimètre, que des brosses douces à ce rayon n'effacent pas. La solution livrée reste donc le **mannequin scripté** ; une vraie main demanderait une base
sculptée (Dyntopo/Multires, CH03.03) et beaucoup plus de temps de brosse. Le pied n'a pas été retravaillé.

