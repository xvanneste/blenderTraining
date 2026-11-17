# CH03.09 — Cours théorique : la retopologie

## 1. Pourquoi
Le sculpt (CH03.06) a ≈ 75 000 faces, sans ordre. Pour animer, simuler, texturer, il faut une **topologie** : peu de faces, tout en
**quads**, des **boucles** qui suivent la forme et les muscles, quelques **pôles** bien placés.

## 2. Boucles faciales
Les muscles circulaires de l'œil et de la bouche plissent la peau en anneaux : la topologie doit offrir des **anneaux concentriques**
autour des yeux et de la bouche, plus **serrés** que sur le front ou la joue. Aussi des boucles le long des plis naso-géniens et du front.
Dans ce chapitre : trois anneaux (deux yeux + bouche), des **ouvertures** au centre (yeux, bouche).

## 3. Les mesures d'une bonne retopo
| Mesure | Solution | Pourquoi |
|---|---|---|
| Quads | 100 % (404 faces) | boucles, subdivision |
| Budget | 300–2 500 faces | léger |
| Adhérence au sculpt | moyenne 1,5 mm, 95ᵉ centile 1,9 mm | épouse la forme (le décalage voulu est de 2 mm) |
| Ouvertures | 3/3, aux bons endroits (±1,5 cm) | yeux, bouche |
| Densité autour des yeux/bouche | faces à 70 % des autres | des anneaux serrés |
| Valence 4 | 96 % des sommets intérieurs | peu de pôles |
| Couverture du devant du visage | 100 % | tout est retopologisé |
| Normales | 98 % vers l'extérieur | pas de faces retournées |

## 4. Les outils (libellés 5.3 vérifiés)
- **Poly Build** (barre d'outils, Edit Mode) : construire face par face en s'accrochant au sculpt.
- **Snap** : *Snap Base*, *Snap Target*, *Snap Target for Individual Elements* (Face Project, Nearest) — voir CH01.
- **Shrinkwrap** (modificateur) : *Wrap Method* = **Project**, axes *X/Y/Z*, *Negative/Positive*, *Face Cull*, *Offset*. Ici : axe Y, Positive,
  cible `SCULPT_Bust`, Offset 0,002 m, puis Apply.
- **Overlay Retopology** (View Overlays) : voir le maillage devant le sculpt.
- **Inset Faces**, **Loop Cut and Slide**, **Tris to Quads** pour construire et nettoyer.

## 5. Principe de la solution (et pourquoi elle est « scriptée »)
Les outils interactifs (Poly Build, Snap) n'existent pas en arrière-plan. La solution applique le même principe, mais par script :
(1) une grille 2D de ≈ 7,5 mm devant le visage ; (2) *Inset Region* deux fois autour de chaque œil et de la bouche : deux anneaux concentriques ;
(3) suppression des faces centrales : les ouvertures ; (4) on retire les faces dont un sommet ne touche pas une surface tournée vers l'avant ;
(5) Shrinkwrap (Project) puis Apply. C'est un **masque facial** : le front, le nez, les joues, la bouche, le menton — pas le crâne ni le cou ni les oreilles.

## 6. Limites
La grille est très régulière : elle n'a ni les boucles du nez, ni celles de la joue, ni les pôles bien placés d'une vraie retopo de production.
Elle suffit à enseigner et à mesurer les principes ; une retopo de personnage complet demande beaucoup plus de travail à la main.
