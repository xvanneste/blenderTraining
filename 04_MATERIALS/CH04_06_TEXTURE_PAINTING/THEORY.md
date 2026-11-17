# CH04.06 — Cours théorique : Texture Painting

## 1. Principe
En mode **Texture Paint** (mode d'objet de la vue 3D, `TEXTURE_PAINT` dans l'API), le pinceau est projeté sur la surface visible et modifie l'**image** active du matériau, aux coordonnées UV du point touché. Tout passe donc par les UV : des îlots propres, sans chevauchement, à densité uniforme (CH04.01–02).

## 2. L'image
- Une image créée dans Blender n'existe qu'en mémoire : **Image > Pack** (menu de l'éditeur d'images, libellé confirmé dans `space_image.py`) l'embarque dans le .blend ; sinon, il faut l'enregistrer (Save As).
- L'image est ici en espace colorimétrique sRGB ; les valeurs stockées sont celles de l'affichage. La couleur d'un pinceau, elle, est **linéaire** dans l'API (0,8 en linéaire → ≈ 0,91 en sRGB) : un script doit convertir.

## 3. Pinceaux (essentials, Blender 5.2/5.3)
Le fichier d'assets `essentials_brushes-mesh_texture.blend` contient notamment *Paint Hard*, *Paint Soft*, *Airbrush*, *Fill*, *Erase Hard*, *Erase Soft*, *Blur*, *Smear*, *Clone*, *Mix*, *Lighten*, *Darken*, *Draw Pen*, *Draw Marker*… Nous utilisons **Paint Hard** (bords nets).

## 4. Méthode
1. Vue orthographique de face ; zoom sur la zone ; taille du pinceau en pixels d'écran.
2. Un trait par côté (0°, 90°, 180°, 270°) en restant à ≤ 53° de la normale : les traits se recouvrent aux jonctions.
3. Couleurs : bande rouge (0,80 ; 0,08 ; 0,06), pastilles bleues (0,10 ; 0,20 ; 0,80), fond crème (0,80 ; 0,74 ; 0,58).
4. Image > Pack, enregistrer.

## 5. Mesures du correcteur
Fond = couleur dominante ; pixel peint = écart > 0,08 par canal. Couverture des îlots UV : solution 14,6 % (exigé 3–50 %) ; couleurs : rouge ≈ 81 % des pixels peints, bleu ≈ 18 % ; peinture hors des îlots : 0 %. Image empaquetée.

## 6. Pièges
- Image non empaquetée : peinture perdue.
- UV qui se chevauchent : la peinture apparaît à deux endroits.
- Peindre en vue rasante : traits étirés.
- Peinture hors des îlots (plan de l'image) : perdue.

## 7. Limites
Le correcteur mesure la peinture, pas son esthétique ; il prend la couleur dominante pour le fond (un repeint total du fond n'est pas détectable en soi, voir contre-exemple « flood »).
