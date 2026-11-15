# CH02.02 — Cours théorique : outils polygonaux I

Six outils suffisent à modéliser la majorité des objets de décor : **Loop Cut**, **Extrude**,
**Inset**, **Bevel**, **Bridge** et **Fill**. Tous agissent en Edit Mode et laissent, après l'action,
un **panneau de l'opération** (en bas à gauche, *Adjust Last Operation*, `F9`) pour régler
précisément le résultat.

## 1. Loop Cut and Slide — `Ctrl+R`
Ajoute une **boucle d'arêtes** à travers un anneau de quads. Survolez une arête : un trait jaune
montre où passera la coupe ; **molette** = nombre de coupes ; clic gauche pour valider, puis glisser
(ou clic droit pour la laisser au milieu). Usages : ajouter de la résolution là où il faut une forme,
préparer une extrusion, poser des **boucles de maintien** (CH02.06).
Astuce du chapitre : après 2 coupes, les deux boucles restent sélectionnées ; `S X 2.25` les écarte
symétriquement autour du centre (positionnement précis).

## 2. Extrude — `E`
Crée de la nouvelle géométrie à partir de la sélection et la déplace. Sur des faces : `E` suit la
normale ; `E Z -0.2` contraint et chiffre le déplacement. Le menu `Alt+E` propose *Extrude Faces*,
*Extrude Faces Along Normals*, *Extrude Individual Faces* (chaque face pour elle-même), *Extrude
Manifold*, *Extrude Edges*, *Extrude Vertices*. Plusieurs faces voisines s'extrudent **en bloc** ;
des faces non voisines (les 4 coins d'une assise) s'extrudent chacune de leur côté.
**Extruder en plusieurs tronçons** crée des boucles intermédiaires : elles servent ensuite à
brancher d'autres éléments (traverses) ou à plier.

## 3. Inset — `I`
Crée une face plus petite **à l'intérieur** des faces sélectionnées, entourée d'un rebord de quads.
Options : *Thickness* (largeur du rebord), *Depth* (hauteur), *Individual* (une inset par face),
*Offset Even*. Combinaison classique : `I` puis `E` vers l'intérieur → un creux, un bouton, une
fenêtre, un écran.

## 4. Bevel — `Ctrl+B` (arêtes) / `Ctrl+Shift+B` (sommets)
Arrondit ou chanfreine. *Width* (largeur), *Segments* (molette pendant l'action ; 1 = chanfrein,
2–3 = arrondi léger), *Profile*. Dans la réalité, **aucune arête n'est parfaitement vive** :
un bevel de quelques millimètres accroche la lumière et rend un objet crédible au rendu.

## 5. Bridge Edge Loops — menu *Edge*
Relie **deux boucles** d'arêtes (ou deux faces sélectionnées : leurs faces sont supprimées et un tube
les relie — entrée *Bridge Faces* du menu contextuel). Options : *Number of Cuts*, *Twist* (décale
l'appariement des sommets si le pont est vrillé), *Interpolation*, *Smoothness*, *Merge*.
Conditions : même nombre de sommets de chaque côté, boucles bien face à face.

## 6. Fill et Make Edge/Face
- `F` (*Make Edge/Face*) : une arête entre 2 sommets, une face à partir de 3 ou plus.
- `Alt+F` (*Fill*) : remplit un contour de triangles ; *Grid Fill* (menu Face) en quads (CH02.01).

## 7. Méthode : du gros au fin
1. **Blocking** : volumes principaux à la bonne échelle (assise 40 × 40 cm, hauteur 48 cm).
2. **Découpe** : Loop Cut là où viendront les extrusions.
3. **Construction** : Extrude, Bridge.
4. **Finition** : Bevel, Inset, petits détails.
Travaillez toujours en **dimensions réelles** (barre latérale `N` → *Item* → *Dimensions*) : la
lumière, la physique et l'animation en dépendent.
