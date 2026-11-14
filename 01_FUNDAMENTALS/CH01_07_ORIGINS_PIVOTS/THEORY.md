# CH01.07 — Cours théorique : origines, pivots et curseur 3D

## 1. L'origine d'un objet
Le petit **point orange** d'un objet sélectionné est son **origine** : le point qui
représente l'objet. La *Location* de l'objet est la position de son origine ; les rotations
et mises à l'échelle de l'objet se font **autour** de son origine (par défaut).

**Analogie.** L'origine est le **clou** qui fixe une affiche au mur : si le clou est au
milieu, l'affiche pivote autour du milieu ; s'il est dans un coin, elle pivote autour du coin.

Où doit être l'origine ?
| Objet | Origine idéale | Pourquoi |
|---|---|---|
| Porte | Charnière | Elle s'ouvre en tournant autour |
| Personnage, meuble | Au sol, entre les pieds | On le pose à z = 0, il se met à l'échelle depuis le sol |
| Roue, hélice | Axe de rotation | Animation de rotation |
| Lampe suspendue | Point d'accroche | Balancement |

## 2. Déplacer l'origine (sans bouger la géométrie)
*Object → Set Origin* :
| Commande | Effet |
|---|---|
| **Origin to 3D Cursor** | l'origine va au curseur 3D (la plus précise : on place d'abord le curseur) |
| **Origin to Geometry** | l'origine va au centre de la géométrie |
| **Geometry to Origin** | la géométrie se déplace pour être centrée sur l'origine |
| **Origin to Center of Mass (Surface / Volume)** | centre de masse (utile en physique) |
Autre méthode : en-tête de la vue 3D → *Options* → *Transform → Affect Only → Origins* :
on déplace alors l'origine avec `G` (avec snapping) ; **pensez à décocher ensuite**.

## 3. Le curseur 3D
Le cercle rouge et blanc est le **curseur 3D** : un point de référence dans l'espace.
- Les nouveaux objets apparaissent **au curseur**.
- Il peut servir de **point de pivot** et de destination de *Set Origin*.
- Le placer : `Shift+RMB` (clic droit avec Shift) à l'endroit visé (sur une surface avec
  *Surface Project*), ou menu `Shift+S` :
  *Cursor to Selected* (au centre de la sélection — en Edit Mode, au milieu des sommets
  sélectionnés), *Cursor to World Origin*, *Cursor to Grid*, *Cursor to Active*.
- Inversement : *Selection to Cursor* (amener la sélection au curseur).
- Valeurs exactes : sidebar `N` → onglet *View* → *3D Cursor*.

## 4. Le point de pivot (*Transform Pivot Point*)
Menu `.` (point) ou en-tête : autour de quoi se font les rotations/échelles d'une sélection.
| Pivot | Rotation de plusieurs objets autour de… |
|---|---|
| **Median Point** (défaut) | la moyenne de leurs origines |
| **Bounding Box Center** | le centre de la boîte englobante de la sélection |
| **3D Cursor** | le curseur 3D |
| **Individual Origins** | chacun autour de **sa propre** origine |
| **Active Element** | l'objet actif |
Exemple : faire tourner 3 boulons autour du centre d'une roue → curseur au centre de la roue,
pivot *3D Cursor*. Faire tourner chaque boulon sur lui-même → *Individual Origins*.

## 5. Pourquoi c'est vital en animation
On anime **l'objet** (sa transformation) : une porte dont l'origine est au centre ne peut
**pas** s'ouvrir correctement par une simple rotation. En production, chaque asset est livré
avec ses origines au bon endroit — c'est un point de contrôle de la publication des assets
(CH02.13). Corriger une origine après l'animation casse toutes les clés posées.
