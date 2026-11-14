# CH01.05 — Cours théorique : Object Mode et Edit Mode

## 1. Les modes
Le menu en haut à gauche de la vue 3D choisit le **mode d'interaction** avec l'objet actif :
| Mode | On manipule… | Phase |
|---|---|---|
| **Object Mode** | des objets entiers (déplacer une chaise) | 1 |
| **Edit Mode** | les composants de la géométrie (sommets, arêtes, faces) | 1–2 |
| Sculpt Mode | la surface comme de l'argile | 3 |
| Vertex / Weight / Texture Paint | couleurs, poids, textures peintes | 4, 6 |
| Pose Mode (armatures) | les os d'un squelette | 6–7 |
| Draw / Edit / Sculpt (Grease Pencil) | des traits 2D | 18 |
`Tab` bascule Object ↔ Edit ; `Ctrl+Tab` ouvre le menu circulaire des modes.

**Analogie.** Object Mode, c'est déplacer une statue dans un musée ; Edit Mode, c'est
prendre le ciseau et modifier la statue elle-même.

## 2. Les composants d'un maillage
- **Sommet** (*vertex*) : un point.
- **Arête** (*edge*) : un segment entre deux sommets.
- **Face** : une surface fermée par 3 arêtes ou plus (triangle, quadrilatère, n-gone).
Un cube = 8 sommets, 12 arêtes, 6 faces.

Modes de sélection : `1` sommets · `2` arêtes · `3` faces (ou les 3 icônes de l'en-tête ;
`Shift`+clic sur une icône combine les modes).

## 3. Sélectionner en Edit Mode
| Geste | Effet |
|---|---|
| `LMB`, `Shift+LMB` | Un élément, ajouter/retirer |
| `A`, `Alt+A`, `Ctrl+I` | Tout, rien, inverser |
| `B`, `C`, `Ctrl+RMB` | Rectangle, cercle, lasso |
| `Alt+LMB` sur une arête | **Boucle** (*edge loop*) |
| `Ctrl+Alt+LMB` sur une arête | **Anneau** (*edge ring*) |
| `L` sous la souris / `Ctrl+L` | Toute la partie connectée (*linked*) |
| `Ctrl+Num +` / `Ctrl+Num −` | Agrandir / réduire la sélection |
| **X-Ray** `Alt+Z` | Voir et sélectionner **à travers** l'objet (sinon, `B` ne prend que le visible) |

## 4. Transformer des composants
Les mêmes `G`, `R`, `S`, axes et saisies numériques qu'en Object Mode, mais appliqués aux
composants. Le point de pivot (CH01.07) détermine le centre des rotations/échelles.
- **Extrude** `E` : tire une nouvelle géométrie depuis la sélection (le geste de base de la
  modélisation, CH02).
- **Scale 0 sur un axe** (`S X 0`) : aligne parfaitement la sélection sur un plan — ici,
  écrase la face extrudée en une arête de faîtage.
- **Merge** `M` : fusionner des sommets (*At Center*, *At Cursor*, *Collapse*, *By Distance*).
- **Supprimer** `X` : menu *Vertices / Edges / Faces / Dissolve…* (différence capitale :
  supprimer des faces laisse un trou ; dissoudre retire sans trou — CH02.03).

## 5. L'édition proportionnelle
`O` active/désactive l'**édition proportionnelle** : les éléments voisins suivent le
déplacement, avec une influence qui décroît avec la distance. Pendant la transformation, la
**molette** règle le rayon d'influence (cercle affiché). Le menu à côté de l'icône choisit
la courbe d'atténuation (*Smooth*, *Sphere*, *Root*, *Sharp*, *Linear*, *Constant*,
*Random*) et l'option *Connected Only*. Idéal pour terrains, tissus, formes organiques.

## 6. Deux règles d'hygiène
1. **Ressortez d'Edit Mode** (`Tab`) avant d'enregistrer, de rendre, de lancer un script :
   les modifications sont « validées » dans le maillage à la sortie du mode.
2. En Edit Mode, `Ctrl+Z` annule les étapes d'édition ; sortir puis annuler peut annuler
   plus qu'on ne voudrait — annulez **avant** de sortir.

## 7. En production
Les modélisateurs vivent en Edit Mode (phase 2), mais les **animateurs ne doivent jamais**
modifier la géométrie d'un personnage riggé : un sommet ajouté ou supprimé casse les poids,
les shape keys et les UV. On distingue donc strictement les étapes (modélisation figée →
rigging → animation).
