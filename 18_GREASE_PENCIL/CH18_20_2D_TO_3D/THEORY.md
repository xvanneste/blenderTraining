# CH18.20 — Cours théorique : workflow 2D → 3D

## 1. Pourquoi storyboarder dans le décor 3D
Dessiner le board **à travers la caméra d'un décor 3D** (même grossier) donne d'emblée : la bonne
perspective, la bonne focale, la bonne échelle des personnages. Chaque case du board EST une caméra
du futur film : rien n'est à « traduire » au layout, les cadrages sont **réutilisés** tels quels.

## 2. Le board dans la caméra
Méthode simple, sans extension :
1. une caméra par plan, liée à son marqueur (*Bind Camera to Markers*, CH18.14) ;
2. un objet GP « BOARD_SHxxxx » **enfant de la caméra** (*Object Properties > Relations > Parent*),
   placé juste devant elle (ici 0,5 m), face à l'objectif : on y dessine en vue caméra, *Drawing Plane*
   *View* ; le dessin suit la caméra si on l'ajuste ;
3. seul le board du plan courant doit être visible (masquer les autres, H) ; les boards sont des guides :
   ils sont **exclus du rendu final** (*Disable in Renders*).
L'extension tierce *Story Pencil* automatise une partie de ce travail ; elle n'est ni installée ni
nécessaire ici.

## 3. Du board au blocking
Le **blocking** place les personnages et accessoires 3D dans leurs **poses clés**, plan par plan, sans
animation fine. À partir du board :
- pour chaque marqueur, vue caméra, on superpose le mannequin 3D à la silhouette dessinée (pieds sur
  les pieds, tête sur la tête) ;
- on pose une clé (K > *Location & Rotation*) à l'image du marqueur ;
- les clés sont en interpolation **Constant** (T dans le Graph Editor ou la Dope Sheet) : le personnage
  change de place **à la coupe**, sans glisser d'un plan à l'autre.
Le correcteur compare les deux silhouettes dans l'image (recouvrement des boîtes, IoU ≥ 0,5, pieds
alignés) : mesures de l'exemple 0,70 / 0,76 / 0,80.

## 4. Ce que le blocking révèle
Un dessin peut tricher (personnage trop grand pour le décor, deux plans incompatibles) : le blocking 3D
met ces erreurs en évidence. On corrige alors le board ou le décor — c'est le dialogue 2D ↔ 3D qui
fait la qualité du layout (phase 9 et phase 15).

## 5. Styles hybrides
Trois familles :
- **3D sous un rendu dessiné** (Line Art, shaders toon, phase 10) ;
- **2D dans un décor 3D** (CH18.19) : personnages GP, décors en volume ;
- **3D avec effets ou annotations 2D** (fumée, impacts, lignes de vitesse en GP par-dessus).
Dans tous les cas : un style de trait commun, une cohérence de lumière, une seule « direction artistique ».
