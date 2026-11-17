# CH04.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Des directions de normales encodées en RVB (relief simulé) | Chaque pixel code un vecteur normal (x, y, z) dans [−1, 1] converti en [0, 1] ; un plat vaut (0,5 ; 0,5 ; 1). |
| Q2 | **b** — Pour garder l'apparence du détail avec peu de polygones | Le détail est stocké dans l'image : la basse définition est légère à rendre. |
| Q3 | **b** — Non-Color | C'est une donnée : en sRGB, Blender appliquerait une courbe qui fausse les vecteurs. |
| Q4 | — | Le bake écrit dans l'image selon les UV du basse définition : des îlots qui se chevauchent ou sortent de [0,1]² donnent un bake faux. |
| Q5 | — | Bump : hauteur → normale perturbée à la volée ; normal map : normales stockées dans une image ; displacement : déplace réellement la géométrie (CH04.08). |
| Q6 | **a** — Image Texture ACTIF et sélectionné dans le matériau du basse définition | Le bake écrit dans l'image du nœud Image Texture actif du matériau de l'objet actif. |
| Q7 | **a** — Selected to Active | Sélectionner le haute définition puis le basse définition (actif) avec Selected to Active. |
| Q8 | — | Blender interprète la couleur comme un vecteur dans l'espace objet sans conversion tangente : l'éclairage est faux ; le correcteur exige Image → Normal Map → Normal. |
| Q9 | — | À étendre les pixels des îlots d'une bande de quelques pixels pour éviter des coutures sombres au filtrage et au mip-mapping. |
| Q10 | — | Quelques pixels au bord des îlots ou en zone localement plate ne s'écartent pas de 0,02 du plat ; le seuil de 85 % tolère cela. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_07_baking_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_07_files.py`) avec le **vrai opérateur** `bpy.ops.object.bake(type='NORMAL')` de Blender 5.3 en arrière-plan (Cycles, CPU, 1 échantillon, Selected to Active, Extrusion 0,25 m, Margin 16 px, espace Tangent). Image `T_Rock_N` 512 × 512 Non-Color empaquetée.
Mesures du correcteur : couverture du relief 99,4 %, longueur moyenne des normales 1,00, z moyen 0,87 ; HIGH 20 480 faces, LOW 320 ; score 19/19. Starter : 14/19.
Rendu regardé : un rocher à 320 faces dont le relief fin vient de la normal map, silhouette légèrement facettée (inévitable avec 320 faces), deux vues cohérentes. La première version, trop claire, a été assombrie.

**Ce que le développement a appris** :
1. `bmesh.ops.create_icosphere(subdivisions=n)` donne 20·4^(n−1) faces : les valeurs 5 et 2 ne donnaient que 5 120 et 80 faces (le correcteur l'a signalé) ; il faut 6 et 3 pour 20 480 et 320 ;
2. changer `colorspace_settings.name` APRÈS avoir écrit les pixels d'une image générée réinitialise son tampon (image noire, non empaquetée) : régler l'espace colorimétrique d'abord ;
3. `mathutils.noise.fractal(position, H, lacunarity, octaves)` n'a pas d'argument de type de bruit dans 5.3.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_unbaked` | image restée plate (rien de baké) | Bake présent : 0 % (seul test en échec) |
| `…_srgb` | image en sRGB | Espace colorimétrique (seul) |
| `…_no_normalmap` | image reliée directement à Normal | Image → Normal Map → Normal (seul) |
| `…_partial` | moitié de l'image non bakée | Bake présent : 50 % (seul) |
| `…_direct_color` | Normal Map branchée sur Base Color | Image → Normal Map → Normal (seul) |
Aussi refusé : le starter (bake 0 %, HIGH visible).

## Limites
- Le correcteur ne compare pas la normal map au relief du haute définition (fidélité) ; il vérifie présence, validité et branchement.
- Les contre-exemples « partial » et « srgb » sont produits en modifiant l'image bakée ou son espace, pas à la main.
