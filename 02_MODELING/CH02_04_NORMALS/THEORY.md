# CH02.04 — Cours théorique : les normales

## 1. Qu'est-ce qu'une normale ?
Une **normale** est un vecteur perpendiculaire à une surface, qui indique de quel côté est
« l'extérieur ». Le moteur de rendu l'utilise pour calculer comment la lumière se reflète : une
normale fausse = un ombrage faux. Blender distingue :
- la **normale de face** (orientation de chaque polygone) ;
- les **normales de coin** (*corner normals*, une par coin de face) : ce sont **elles** que le rendu
  utilise. Elles sont égales à la normale de face (rendu **plat**) ou moyennées avec les faces
  voisines (rendu **lisse**).

## 2. Orientation : dehors ou dedans ?
L'ordre des sommets d'une face fixe le sens de sa normale. Extrusions, Bridge, imports ou
`Flip` malencontreux peuvent produire des faces **retournées**.
- **Voir** : Viewport Overlays → **Face Orientation** : bleu = face vue de l'extérieur, rouge = face
  vue de l'intérieur.
- **Réparer** : Edit Mode, `A`, **Mesh → Normals → Recalculate Outside** (`Shift+N`) ; *Recalculate
  Inside* (`Shift+Ctrl+N`) pour un intérieur de pièce vu de dedans ; **Flip** pour une sélection.
**Piège** : dans EEVEE et Cycles, les faces retournées s'affichent souvent **normalement** (faces
visibles des deux côtés). Le défaut casse pourtant : *Solidify* (épaisseur du mauvais côté),
*Weighted Normal*, le *Backface Culling*, les exports vers moteurs de jeu, les simulations, le calcul
du « dedans/dehors » des booléens. Vérifiez Face Orientation **avant** de livrer un asset.

## 3. Lisse ou plat
- **Shade Flat** : chaque face a sa normale ; facettes visibles.
- **Shade Smooth** : normales de coin moyennées ; surface continue… y compris là où on voulait une
  arête vive : couvercles « gonflés », reflets qui bavent.
- **Shade Auto Smooth** (menu *Object*, Blender ≥ 4.1) : ajoute un modificateur **Smooth by Angle**
  (Geometry Nodes) : les arêtes dont l'angle dépasse le seuil (*Angle*, 30° par défaut) restent
  vives, le reste est lissé. Remplace l'ancienne case « Auto Smooth » des données de maillage
  (supprimée en 4.1 : attention aux anciens tutoriels).
- **Marquer** une arête vive à la main : Edge → **Mark Sharp** (respectée par Smooth by Angle tant
  que son entrée *Ignore Sharpness* reste décochée — entrées du modificateur : *Angle*,
  *Ignore Sharpness*).

## 4. Weighted Normal : les grandes faces d'abord
Sur un objet **chanfreiné et lissé**, les normales de coin des grandes faces sont moyennées avec
les petites faces du chanfrein : dégradés et taches sur des surfaces censées être planes. Le
modificateur **Weighted Normal** (catégorie *Normals*) pondère les normales selon la surface des
faces (*Weighting Mode* : Face Area, Corner Angle…) :
- **Weight** : 50 = neutre ; plus haut = les grandes faces dominent davantage ;
- **Keep Sharp** : respecte les arêtes vives ; **Face Influence** : utilise la « force » de face
  (*Set Face Strength* dans Mesh → Normals).
Mesure faite pour ce chapitre (pavé chanfreiné) : écart des normales des grandes faces
(produit scalaire avec la normale de face) **0,876** sans modificateur, **0,994** avec Weight 50,
**1,000** avec Weight ≥ 75 → surfaces parfaitement planes, chanfreins lisses : le rendu
« hard surface » propre.

## 5. Normales personnalisées
Weighted Normal produit des **normales personnalisées** (*custom normals*). Elles se perdent si on
modifie fortement la géométrie après les avoir appliquées ; d'où l'intérêt de garder le modificateur
en fin de pile (non destructif, CH02.07). *Mesh → Normals → Set from Faces*, *Average*, *Point to
Target* permettent des retouches manuelles (feuillages, cartoon).

## 6. Au cinéma
Un *lookdev artist* refuse un asset aux normales cassées : le moindre reflet faux se voit sur un
plan rapproché de 4K. Les vérifications de normales font partie de la checklist de CH02.01.
