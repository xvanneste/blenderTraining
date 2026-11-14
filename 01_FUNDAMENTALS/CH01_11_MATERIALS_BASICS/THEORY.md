# CH01.11 — Cours théorique : matériaux simples

## 1. Qu'est-ce qu'un matériau ?
Un **matériau** décrit comment une surface réagit à la lumière : couleur, brillance, aspect
métallique, transparence, émission de lumière. La forme dit **ce qu'est** un objet ; le
matériau dit **de quoi il est fait**. Une même sphère peut être une bille d'acier, une balle
en caoutchouc ou une perle.

Dans Blender 5.3, chaque matériau est un petit graphe de **nœuds** (*Shader Editor*, phase 4).
Par défaut : un nœud **Principled BSDF** relié à **Material Output**. L'onglet *Material* de
Properties affiche les réglages de ce nœud sous forme de panneaux : on peut tout faire sans
ouvrir l'éditeur de nœuds au début.

## 2. Le Principled BSDF : les réglages à connaître dès maintenant
| Réglage | Rôle | Valeurs typiques |
|---|---|---|
| **Base Color** | Couleur de la surface | Pas de noir pur ni de blanc pur (0,03–0,9) |
| **Metallic** | 0 = non métal (bois, plastique, peau), 1 = métal | **0 ou 1**, rarement entre les deux |
| **Roughness** | 0 = miroir/verni, 1 = mat | Plastique brillant 0,2 · bois 0,6 · tissu 0,9 |
| **IOR** | Indice de réfraction | 1,45–1,5 (défaut convient) |
| **Alpha** | Opacité | 1 = opaque |
| **Transmission** (*Weight*) | Verre, liquides | 1 pour le verre (+ Roughness 0) |
| **Emission** (*Color*, *Strength*) | La surface émet de la lumière | Strength 5–20 pour un néon, une lampe |
| Coat, Sheen, Subsurface | Vernis, velours, peau | Phase 4 |
Règle mentale : **un métal tire sa couleur de ses reflets** (cuivre, or : Base Color colorée,
Metallic 1) ; un non-métal a une couleur diffuse et des reflets blancs.

## 3. Emplacements (slots) et affectation par face
Un objet peut avoir **plusieurs matériaux** : la liste d'**emplacements** (*Material Slots*)
en haut de l'onglet *Material*.
- `+` / `−` : ajouter / retirer un emplacement ; **New** : créer un matériau ; le menu
  déroulant (sphère) : choisir un matériau existant.
- En **Edit Mode**, sélectionnez des faces, choisissez l'emplacement, cliquez **Assign**.
  *Select* / *Deselect* sélectionnent les faces d'un emplacement.
- Le **premier emplacement** est celui de toutes les faces par défaut.
- `Ctrl+L` → *Link Materials* : copier les matériaux de l'objet actif vers la sélection.

## 4. Voir les matériaux : les modes d'affichage
`Z` (menu circulaire) ou boutons en haut à droite de la vue 3D :
| Mode | Affiche | Usage |
|---|---|---|
| **Wireframe** | arêtes | voir à travers |
| **Solid** | volumes, couleur d'objet/matériau simplifiée | modélisation |
| **Material Preview** | matériaux réels sous un éclairage HDRI de test | réglage des matériaux |
| **Rendered** | le rendu réel avec vos lumières | réglage final |

## 5. Les matériaux sont des données partagées
Un matériau est un datablock (CH01.04) : s'il est utilisé par 10 objets, le modifier les
modifie tous. Pour une variante : bouton de copie dans la ligne de datablock (crée
`MAT_Roof.001` → renommez-le). C'est voulu : une bibliothèque de matériaux cohérente
(phase 4) se met à jour partout.

## 6. En production
Les matériaux sont créés par le département *surfacing/lookdev* et publiés en bibliothèque.
Les artistes ne les modifient pas dans les plans ; ils choisissent parmi les matériaux
validés. Convention BCMA : `MAT_<Matière>_<Variante>` (`MAT_Wood_Oak`, `MAT_Metal_Rusty`).
