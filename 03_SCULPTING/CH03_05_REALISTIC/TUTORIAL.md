# CH03.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_05_bust_starter.blend` : studio, caméras de face (`CAM_Front`), 3/4 et profil, et
le guide `GP_Guide` (ovale de tête et six repères : couronne, racine des cheveux, sourcils, base du nez,
menton, ligne des yeux en rouge). Le visage regarde vers **−Y**.

## Tutoriel 1 — Lire le guide
Num 1 (face). Relevez sur le guide : la tête fait 23 cm de la couronne (z = 0,50) au menton (z = 0,27) ; la
ligne rouge des yeux (z = 0,385) est à la **moitié**. Notez les quatre autres repères : ils découpent le visage
en tiers. Posez votre idée de visage (âge, caractère) en une phrase.

## Tutoriel 2 — Le blocage (ellipsoïdes qui se chevauchent)
*Add > Mesh > UV Sphere*, puis Sidebar (N) > Item > *Dimensions* et *Location* (valeur = diamètre) :
| Masse | Location (x, y, z) | Dimensions (x, y, z) |
|---|---|---|
| Crâne | 0 ; 0,025 ; 0,395 | 0,156 ; 0,20 ; 0,20 |
| Face | 0 ; −0,012 ; 0,335 | 0,132 ; 0,124 ; 0,17 |
| Mâchoire | 0 ; −0,014 ; 0,297 | 0,112 ; 0,116 ; 0,084 |
| Menton | 0 ; −0,05 ; 0,288 | 0,044 ; 0,06 ; 0,048 |
| Arcade | 0 ; −0,052 ; 0,402 | 0,12 ; 0,044 ; 0,032 |
| Pommette (×2, x = ±0,05) | ±0,05 ; −0,03 ; 0,368 | 0,03 ; 0,056 ; 0,026 |
| Arête du nez | 0 ; −0,07 ; 0,374 | 0,02 ; 0,034 ; 0,06 |
| Bout du nez | 0 ; −0,081 ; 0,341 | 0,028 ; 0,034 ; 0,028 |
| Ailes du nez (×2) | ±0,016 ; −0,072 ; 0,335 | 0,02 ; 0,024 ; 0,02 |
| Lèvre haute / basse | 0 ; −0,067 ; 0,318 / 0 ; −0,066 ; 0,299 | 0,048 ; 0,022 ; 0,014 / 0,04 ; 0,022 ; 0,016 |
| Cou | 0 ; 0,015 ; 0,19 | 0,114 ; 0,12 ; 0,20 |
| Sterno-cléido (×2) | ±0,032 ; −0,012 ; 0,2 | 0,038 ; 0,056 ; 0,14 |
| Poitrine | 0 ; 0 ; 0,06 | 0,38 ; 0,2 ; 0,24 |
| Pentes de trapèze (×2) | ±0,1 ; 0,012 ; 0,13 | 0,17 ; 0,14 ; 0,07 |
Chaque masse **chevauche** sa voisine. Les oreilles viennent plus tard (tutoriel 4). *Ctrl+J* (Join) →
renommez `SCULPT_Bust`, *Ctrl+A > Rotation & Scale*. Si l'origine n'est pas en (0, 0, 0) : *Object > Set Origin
> Origin to 3D Cursor* (curseur au centre du monde, Shift+C).

## Tutoriel 3 — Remesh et fondre les blocs
1. Object Data > *Remesh* > *Voxel Size* 0,0025 m (2,5 mm), bouton **Voxel Remesh** (en Sculpt Mode : Ctrl+R).
   Le buste fait alors ≈ 70 000 faces.
2. En mode Sculpture, activez la symétrie X. Lissez en maintenant `Shift`, **uniquement sur les raccords** (arcade/nez,
   pommette/joue, menton/mâchoire). Le but : chaque bloc disparaît dans le suivant. Comparez à la solution :
   elle fond les blocs par un lissage qui conserve le volume ; vous le faites à la brosse.
3. Avant de détailler, comparez la même joue de face et de trois-quarts sous une lumière latérale.
   Si une crête marque encore le bord de l'ellipsoïde, lissez cette crête par touches courtes. Arrêtez
   dès que le reflet traverse le raccord sans rupture et que la pommette reste visible. Enregistrez une copie de ce palier.

## Tutoriel 4 — Orbites, yeux, oreilles
1. Deux sphères de 3,1 cm de diamètre à (±0,032 ; −0,056 ; 0,385). `SCULPT_Bust` > *Add Modifier > Generate >
   Boolean* : *Difference*, *Object* = la sphère, solveur **Manifold** (si *Exact* donne un objet vide, voir
   TROUBLESHOOTING), puis *Apply*. Idem pour l'autre. Supprimez les sphères, nouveau Voxel Remesh.
2. Deux sphères de 2,5 cm de diamètre nommées **`EYE_L`** et **`EYE_R`** à (±0,032 ; −0,05 ; 0,385), posées dans
   les orbites. Le correcteur retrouve les yeux par ces **noms**.
3. Oreilles : deux ellipsoïdes (0,02 × 0,038 × 0,058 m) à (±0,075 ; 0,016 ; 0,372), à joindre **après** le travail
   de lissage (sinon vous les effacez), puis Voxel Remesh.

## Tutoriel 5 — Le socle
Edit Mode, A, *Mesh > Bisect* : ligne horizontale au ras du bas en vue de face ; dans le panneau de l'opérateur
*Clear Inner* et *Fill* cochés. Coupez **là où la poitrine est déjà large** (z ≈ 0,005 avec la poitrine du tutoriel 2 : ≈ 34 cm de large) ; une coupe trop près du bas de l'ellipsoïde laisse un socle étroit (le correcteur exige ≥ 200 cm²). Object Mode : le bas du buste à z = 0.

## Tutoriel 6 — Plans, transitions, détails
1. **Plans** : *Clay Strips* (C) pour l'arcade, les pommettes, le plan du nez ; *Scrape/Fill* (Shift+T) pour
   reposer un plan ; Ctrl maintenu inverse le sens d'une brosse. Contrôlez de **face, de profil, de trois-quarts**
   (caméras `CAM_Front`, `CAM_Side`, `CAM_34`).
2. **Secondaires** : plis naso-géniens, sillon entre les lèvres, poches sous les yeux avec *Draw Sharp* ou
   *Crease Sharp* (shelf de brosses), adoucis au *Crease Polish* (Shift+C) ou à *Smooth* ; profondeur ≈ 1–2 mm.
3. **Tertiaires** : subdivisez d'abord (Multires > *Subdivide*, puis *Sculpt Level* supérieur, ou Voxel Size
   plus petit ; **copie de sécurité avant**). Rides fines du front (≈ 1 mm), grain de peau : brosse fine, force
   faible, passes courtes.

## Tutoriel 7 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_05_bust_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_05.py" -- --exercise bust --render
```
Ajoutez `--debug` pour voir les grandeurs brutes (creux, grain, repères). Référence :
`COMPLETED_EXAMPLES/ch03_05_bust_reference.png` (face, 3/4, profil).

## Variante de contrôle

Enlevez temporairement la couleur, les cheveux ou les éléments accessoires qui distraient. Comparez la projection du front, de la bouche et du menton de profil. Faites une seule correction d’abord, puis jugez à distance. **Preuve** Trois vues au même cadre expliquent le rôle de la correction.
