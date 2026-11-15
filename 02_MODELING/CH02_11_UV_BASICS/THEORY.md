# CH02.11 — Cours théorique : UV fondamentaux

## 1. Qu'est-ce qu'une UV ?
Une texture est une image **plate** (coordonnées **U** horizontale, **V** verticale, de 0 à 1). Pour
la poser sur un objet 3D, chaque coin de face reçoit une coordonnée UV : c'est le **dépliage**
(*unwrap*), comme on découpe et aplatit un patron de couture. Sans UV, une texture image ne sait pas
où se placer (rendu `ch02_11_uv_starter_view.png` : couleur uniforme).

## 2. Coutures et îles
- Une **couture** (*seam*, Edge → **Mark Seam**, rouge) dit où « couper » la surface.
- Chaque morceau déplié est une **île**. Moins d'îles = moins de raccords visibles ; trop peu de
  coutures = **étirement** (la surface ne peut pas s'aplatir sans se déformer).
- Placer les coutures là où elles se voient le moins : dessous, arrière, angles vifs, plis.
Exemple classique : un cylindre = **1 arête verticale + 2 cercles** (les couvercles) → 3 îles :
un rectangle et deux disques.

## 3. Les méthodes (menu `U` en Edit Mode, Blender 5.3)
| Méthode | Principe | Usage |
|---|---|---|
| **Unwrap** | déplie selon les coutures (*Angle Based*, *Conformal*, *Minimum Stretch*) | tout objet avec coutures choisies |
| **Smart UV Project** | coupe automatiquement selon un angle (*Angle Limit*) | objets anguleux, props simples, rapide |
| *Cube / Cylinder / Sphere Projection* | projection géométrique | formes correspondantes, rapide |
| *Follow Active Quads* | suit une grille de quads | rubans, routes, rails |
| *Lightmap Pack* | une île par face | lightmaps, cas particuliers |
Ensuite, dans l'**UV Editor** : *UV → Pack Islands* (rangement, *Margin*), *Average Islands Scale*
(même densité pour toutes les îles), *Seams from Islands*.

## 4. Contrôler avec un damier
Une image générée **UV Grid** ou **Color Grid** (*Image → New*, *Generated Type*) affichée en
Material Preview :
- carrés **déformés** = étirement ;
- carrés de **tailles différentes** = densité de texels incohérente ;
- **cassure** du motif = couture (normal) ;
- motif identique sur deux zones = îles **superposées** (sauf choix volontaire).

## 5. Densité de texels
La **densité de texels** = nombre de pixels de texture par mètre de surface. Dans un même plan,
deux objets côte à côte doivent avoir une densité comparable, sinon l'un paraît flou. Dans la
solution du chapitre, chaque objet est rangé seul dans son carré UV : la boîte, plus petite, reçoit des
carrés plus petits que la caisse. Pour les uniformiser : *Average Islands Scale* sur plusieurs objets
édités ensemble, puis *Pack Islands* (phase 4 : texel density précise, UDIM).

## 6. Mesures du correcteur
Le correcteur vérifie : UV dans 0–1, occupation (30–100 %), chevauchement (rasterisation 128 × 128,
≤ 2 %), étirement (dispersion du rapport surface UV / surface 3D, ≤ 0,25), coutures du cylindre.
Contre-épreuve faite : une *Cube Projection* sans coutures sur la boîte est refusée (UV hors
du carré, îles superposées, aucune couture).
