# CH03.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_04_bust_starter.blend` : studio, caméras de face, 3/4 et profil, planche
`GP_Design` (trois silhouettes de référence).

## Tutoriel 1 — Choisir l'idée
Regardez les trois silhouettes (grosse tête, costaud, long). Écrivez en une phrase le caractère de
votre personnage et la forme dominante (cercle, carré, triangle).

## Tutoriel 2 — Le blocage en ellipsoïdes
1. *Add > Mesh > UV Sphere*, puis Sidebar > *Dimensions* : poitrine 0,42 × 0,22 × 0,2 m (z ≈ 0,08).
2. Cou (0,11 × 0,11 × 0,14, z ≈ 0,19), tête (0,25 × 0,27 × 0,3, z ≈ 0,34), crâne, nez, arcades,
   menton, oreilles, mèche : chaque masse **chevauche** sa voisine.
3. Alt+A, sélectionnez toutes les masses, Ctrl+J, F2 → `SCULPT_Bust`, Ctrl+A > *Rotation & Scale*.
4. Object Data > *Remesh* : Voxel Size 0,005 → **Voxel Remesh**.

## Tutoriel 3 — Creuser les orbites (Boolean)
1. Deux sphères de 3 cm de rayon à l'emplacement des yeux, enfoncées dans le visage.
2. `SCULPT_Bust` : *Add Modifier > Generate > Boolean* : *Difference*, *Object* : la première
   sphère ; *Apply* (Ctrl+A sur le modificateur). Idem pour la seconde. Supprimez les sphères.
3. Voxel Remesh de nouveau : arêtes adoucies, volume régulier.
   *Variante métaballes* : bloquez avec *Add > Metaball*, deux éléments *Negative* pour les orbites,
   puis *Object > Convert > Mesh*.

## Tutoriel 4 — Le socle
Edit Mode, A, *Mesh > Bisect* : tracez une ligne horizontale au ras du bas en vue de face ; panneau
de l'opérateur : *Clear Inner* et *Fill* cochés. Object Mode : placez le socle à z = 0.

## Tutoriel 5 — Sculpter les plans
Sculpt Mode, Mirror X : Clay Strips (C) pour les pommettes et les arcades, Scrape/Fill pour des
plans nets, Pinch (P) pour affirmer l'arête du nez. Vérifiez la silhouette de face et de profil.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_04_bust_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_04.py" --python-exit-code 1 -- --exercise bust --render
```
Référence : `COMPLETED_EXAMPLES/ch03_04_bust_reference.png` (face, 3/4, profil).
