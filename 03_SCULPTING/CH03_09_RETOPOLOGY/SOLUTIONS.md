# CH03.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Le sculpt est trop dense et désordonné : il faut un maillage léger, de quads, qui se déforme bien | Le sculpt a ≈ 75 000 faces ; la retopo en a 404 ici. |
| Q2 | — | Les quads forment des boucles et des anneaux qui suivent les muscles, se subdivisent proprement (Subdivision Surface) et se déforment de façon prévisible ; les triangles cassent ces boucles. |
| Q3 | — | Des anneaux concentriques autour des yeux et de la bouche (là où les muscles circulaires plissent la peau), des boucles pour les plis naso-géniens et le front. |
| Q4 | **b** — Un sommet de valence ≠ 4 (3, 5…) qui tord les boucles et les déformations | Mesuré dans la solution : 96 % des sommets intérieurs sont de valence 4. |
| Q5 | — | Un maillage léger se rigge, se simule et se déforme vite ; trop dense, ce n'est plus une retopo (ici 300–2 500 faces ; la solution en a 404). |
| Q6 | **b** — Shrinkwrap (Wrap Method : Project / Nearest Surface Point) | Libellés vérifiés en 5.3 : Wrap Method, Project, axes X/Y/Z, Negative/Positive, Offset. |
| Q7 | — | Poly Build (Edit Mode), avec l'accrochage (Snap) sur les faces du sculpt ; l'overlay Retopology aide à voir le maillage devant le sculpt. |
| Q8 | — | Les faces de l'anneau créé ; les faces d'origine deviennent le centre. En supprimant l'anneau au lieu du centre, on laisse des îlots flottants au milieu des yeux (bug rencontré dans ce chapitre). |
| Q9 | — | Un sommet qui ne touche aucune surface reste sur le plan de départ alors que ses voisins collent au crâne : le quad qui les relie est énorme. On retire ces faces avant le Shrinkwrap. |
| Q10 | **a** — Mesh > Faces > Tris to Quads | L'opérateur mesh.tris_convert_to_quads existe en 5.3 ; il ne remplace pas une vraie retopo. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_09_retopo_solution.blend` (+ `_reference.png` : face, 3/4, profil ; le fil de fer y est une copie ajoutée **après** la sauvegarde pour le
rendu ; la solution ne contient que `RETOPO_Face`).

**Honnêteté sur la fabrication.** La solution est **générée par script** (`build_ch03_09_files.py`) : grille 2D de ≈ 7,5 mm, *Inset Region* ×2 autour de chaque œil et de la
bouche, suppression des faces centrales, retrait des faces qui ne touchent pas une surface tournée vers l'avant, Shrinkwrap (Project, Y, Positive, Offset 2 mm), Apply.
C'est un masque facial régulier, pas une retopo de production (pas de boucles du nez ni de la joue, pas d'oreilles, de cou ni de crâne).

Mesures du correcteur sur la solution : 404 faces, 100 % de quads ; distance au sculpt moyenne 1,5 mm (95ᵉ centile 1,9 mm) ; 3 ouvertures sur 3 (yeux, bouche) ; faces
autour des yeux et de la bouche à 70 % de la taille des autres ; valence 4 pour 96 % des sommets intérieurs (324/336) ; couverture 100 % ; normales 98 %. Score 22/22.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_uniform` | grille sans anneaux ni ouvertures | ouvertures (0/3) et densité (116 %) |
| `…_triangulated` | tout en triangles | quads (0 %) et valence |
| `…_floating` | pas de Shrinkwrap (plan à y = −0,2) | adhérence (117 mm) et couverture (0 %) |
| `…_too_dense` | subdivisé ×2 (6 496 faces) | budget de faces |
| `…_misplaced` | anneaux décalés de 3 cm | ouvertures (0/3) et densité (105 %) |
Aussi refusé : le starter (pas de `RETOPO_Face`).

**Ce que le développement a appris** (consigné aussi dans CLAUDE.md) :
1. une première version projetait TOUS les sommets : ceux hors de la silhouette restaient sur le plan de départ et des quads s'étiraient en dalles sur le côté
   de la tête (vu sur le rendu) ; on retire désormais les faces dont un sommet ne touche pas une surface tournée vers l'avant ;
2. le filtre d'inclinaison supprimait aussi les parois des orbites : on protège yeux, bouche et cœur du visage ;
3. `bmesh.ops.inset_region` renvoie les faces de l'**anneau** ; j'ai d'abord supprimé l'anneau au lieu du centre : le correcteur a révélé 14 « trous »
   superposés, des îlots dans les yeux et 87 % de normales correctes ; on supprime la région d'origine (devenue le centre) ;
4. avec une grille de 1 cm la solution n'avait que 201 faces : maille de ≈ 7,5 mm → 404 faces ;
5. le budget minimal et la densité ont été assouplis (300 faces, ≤ 80 %) parce que « uniform » et « misplaced » étaient refusés pour le mauvais motif (nombre de faces).

## Limites
- Le correcteur compte des trous aux positions des yeux et de la bouche : une retopo qui garde l'œil fermé (sans ouverture) sera refusée, même si ses anneaux sont corrects.
- Il suppose le visage vers −Y et les yeux/bouche aux positions du fichier de départ.
- Il mesure la topologie, pas la qualité des boucles ni de la déformation (à valider en rig, phase 6).
