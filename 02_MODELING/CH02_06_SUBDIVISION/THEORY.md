# CH02.06 — Cours théorique : Subdivision Surface

## 1. Cage et surface limite
Le modificateur **Subdivision Surface** (algorithme *Catmull-Clark*) découpe chaque face en quatre
et lisse le résultat, à chaque niveau. On modélise une **cage** légère (le maillage de contrôle) ;
la surface lisse finale tend vers une **surface limite**. Avantages : peu de sommets à manipuler,
surfaces parfaitement lisses au rendu, déformation propre en animation — c'est la base des
personnages et de nombreux objets de cinéma.

Réglages (modificateur, catégorie *Generate*) : **Levels Viewport**, **Render**, *Optimal Display*,
*Subdivision Type* (*Catmull-Clark* / *Simple*), *Quality*, *Use Limit Surface*, *UV Smooth*,
*Boundary Smooth*, **Use Creases**, *Use Custom Normals*. Raccourci : `Ctrl+0` … `Ctrl+5`
(ajoute/règle la subdivision de l'objet sélectionné, Object Mode).

## 2. Le problème : tout s'arrondit
Un cube de 8 sommets subdivisé devient une **boule molle**. Mesure faite pour ce chapitre :
volume / volume de la boîte englobante = **0,52** (1 = cube parfait). La subdivision tire chaque
sommet vers la moyenne de ses voisins : plus les arêtes de la cage sont **éloignées**, plus l'arrondi
est grand.

## 3. Première solution : les boucles de maintien
On ajoute des **boucles de maintien** (*support / holding loops*) près des arêtes à garder nettes.
Règle : **distance boucle–arête = rayon de l'arrondi**. À 5 cm des bords d'un cube de 80 cm, le
remplissage mesuré remonte à **0,99** : un cube aux coins légèrement adoucis.
Façons de les créer : *Loop Cut* `Ctrl+R` (puis glisser ou `S` axe), *Bevel* 1 segment à très
petite largeur sur les arêtes (crée deux boucles d'un coup), *Inset*. Avantage : contrôle parfait,
topologie explicite, fonctionne partout (export, autres logiciels). Inconvénient : plus de géométrie
dans la cage.

## 4. Deuxième solution : le crease
Le **crease** (pli) est une valeur de 0 à 1 par arête (ou par sommet) qui dit à la subdivision de
**moins lisser** cette arête : `Shift+E` puis valeur (Edit Mode). Avec crease = 1 sur les 4 arêtes du
dessus d'un cube, le dessus devient plat (0,42 m² plats mesurés sur 0,64 m², coins arrondis en plan
car les arêtes verticales ne sont pas pliées) et le dessous reste arrondi. Rapide, sans géométrie
en plus ; mais moins portable (export) et un crease 1 donne une arête parfaitement vive, rarement
réaliste. Overlay *Crease* (Edit Mode) pour visualiser.

## 5. Bonnes pratiques de cage
- **Quads** partout : triangles et n-gons créent des bosses et pincements visibles après subdivision.
- **Pôles** sur les zones plates (CH02.01).
- **Densité régulière** ; les boucles de maintien servent à **décider** où la surface est tendue.
- Pas de faces internes ni de sommets en double (la subdivision les révèle brutalement).
- Modifier la **cage**, jamais le résultat : on n'applique pas le modificateur.

## 6. Performances
Chaque niveau multiplie le nombre de faces par **4** (2 niveaux = ×16, 3 = ×64). Réglage
professionnel : **Levels Viewport 0 ou 1**, **Render 2 ou 3**. Le Simplify de la scène (*Render →
Simplify → Max Subdivision*) plafonne tous les objets d'un coup dans un plan lourd.
