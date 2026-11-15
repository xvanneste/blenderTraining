# CH18.08 — Cours théorique : calques, masques, modificateurs, transformations

## 1. Non destructif : la règle d'or
Un travail **non destructif** se modifie à tout moment sans redessiner : on empile des réglages
(modificateurs, masques, modes de fusion, transformations de calque) **au-dessus** du dessin, sans
toucher aux traits. On n'**applique** (*Apply*) un modificateur que lorsqu'il faut figer le
résultat (export, retouche à la main) — et on garde une copie du fichier avant.

## 2. Calques avancés (Properties → Object Data → Layers)
Sous la liste des calques : **Blend Mode**, **Opacity**, **Lights**. Sous-panneaux :
**Masks**, **Transform**, **Adjustments**, **Relations**, **Display**.
| Réglage | Effet | Usage typique |
|---|---|---|
| **Blend Mode** : *Regular, Hard Light, Add, Subtract, Multiply, Divide* | mélange le calque avec ceux du dessous | **Multiply** pour les ombres, **Add** pour lumières et lueurs |
| **Opacity** | transparence du calque | esquisse à 30 %, ombres à 60 % |
| **Lights** | le calque réagit aux lampes de la scène | décocher pour des couleurs « plates » exactes |
| **Transform** : *Translation, Rotation, Scale* | déplace le calque entier sans modifier ses traits ni l'objet | recaler un décor, un nuage, une couche d'effet |
| **Adjustments** : *Tint Color/Factor*, *Stroke Thickness* | teinte et épaisseur pour tout le calque | assombrir un arrière-plan, épaissir un contour |
| **Relations** : *Parent*, *Pass Index*, *Use Masks in Render* | parenter le calque à un objet/os ; index pour filtrer | calque attaché à un os (rig 2D) |

## 3. Les masques de calque
Un masque limite l'affichage d'un calque à la forme dessinée sur **un autre calque**.
1. Calque à masquer actif (ex. FX_LIGHT) → sous-panneau **Masks** : cocher la case de l'en-tête
   (*Use Masks*).
2. Bouton **+** → choisir le calque masque (ex. MASK_WINDOW). Plusieurs masques possibles ; chaque
   masque a une icône d'**inversion** (montrer à l'extérieur au lieu de l'intérieur).
3. Rendre le calque masque **invisible mais actif** : **Opacity = 0**.
**Piège vérifié dans Blender 5.3.0** : si l'on **ferme l'œil** du calque masque (*hide*), le masque
**cesse d'agir** (mesuré pour ce chapitre : rayons visibles partout avec l'œil fermé, limités à la
fenêtre avec l'œil ouvert et l'opacité à 0). Le menu **+** propose aussi *Mask with Layer Above /
Below* (calque voisin).

## 4. Les modificateurs Grease Pencil
Properties → **Modifiers** → *Add Modifier* : catégories et modificateurs GP de Blender 5.3 :
| Catégorie | Modificateurs |
|---|---|
| **Edit** | Texture Mapping, Time Offset, Vertex Weight Proximity, Vertex Weight Angle |
| **Generate** | Array, Build, Dot Dash, Envelope, Length, **Line Art**, Mirror, Multiple Strokes, Outline, Simplify, Subdivide |
| **Deform** | Armature, Hook, Lattice, **Noise**, Offset, Shrinkwrap, Smooth, **Thickness** |
| **Color** | Hue/Saturation, Opacity, **Tint** |

Les plus utiles en production :
- **Thickness** : épaissir ou uniformiser le trait (*Thickness Factor*, *Uniform Thickness*).
- **Noise** : tremblement du trait (effet « boiling » de l'animation dessinée, avec *Step*).
- **Tint** : teinter (couleur + *Factor*) ; **Opacity**, **Hue/Saturation** : corrections.
- **Build** : le dessin **se trace** dans le temps (*Mode* : Sequential / Concurrent / Additive ;
  *Transition* : Grow / Shrink / Vanish ; *Length*, *Delay*) — génériques, schémas animés.
- **Smooth**, **Simplify** : nettoyer des traits trop tremblés ou trop denses.
- **Line Art** : génère des contours à partir de la géométrie 3D (scène, collection, objet) —
  cœur du rendu « dessin » d'une scène 3D (CH18.19).
Chaque modificateur a un panneau **Influence** : **Layer** (ou groupe de calques), **Material**,
**Vertex Group**, avec inversion. C'est ce qui permet de n'épaissir **que** le calque LINE.
L'ordre de la pile compte, comme pour les maillages (CH01.10).

## 5. Les effets visuels (Shader FX)
Properties → onglet **Effects** → *Add Effect* : **Blur, Colorize, Flip, Glow, Pixelate, Rim,
Shadow, Swirl, Wave Distortion**. Ils agissent sur l'image rendue de l'objet (ombre portée
« papier découpé », lueur de magie, flou de profondeur). Coût de rendu plus élevé : à utiliser
avec mesure.

## 6. Transformations : objet, calque ou traits ?
| Je veux… | Je modifie… |
|---|---|
| déplacer tout le dessin dans la scène | l'**objet** (Object Mode, `G`) |
| décaler un seul calque sans toucher aux traits | la **Transform** du calque |
| corriger la forme de certains traits | les **points** (Edit Mode) |
| animer un décalage ou un rebond | la Transform du calque ou l'objet (clés `I`) |
