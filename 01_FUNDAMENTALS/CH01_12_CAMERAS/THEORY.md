# CH01.12 — Cours théorique : la caméra

## 1. La caméra, c'est le regard du spectateur
En cinéma 3D, rien n'existe hors du cadre. La caméra décide **ce qu'on voit**, **à quelle
taille**, **sous quel angle** et **avec quelle netteté**. Une scène banale peut devenir
inquiétante ou héroïque selon la focale et la hauteur de caméra. Ce chapitre installe les
bases techniques ; la grammaire cinématographique est approfondie en CH09 et CH18.10.

## 2. Ajouter, activer, regarder
- `Shift+A` → *Camera* ; la caméra active de la scène : `Ctrl+Num 0` (ou *Scene → Camera*).
- `Num 0` : vue caméra. Le rectangle = cadre de l'image ; la zone grisée hors cadre est le
  *Passepartout* (*Object Data → Viewport Display*).
- Placer : naviguer puis `Ctrl+Alt+Num 0` (CH01.02) ; ou en vue caméra, *Lock Camera to View*
  (sidebar `N` → *View*), naviguer, **puis le décocher** ; ou `G`/`R` avec la caméra sélectionnée
  en vue caméra (`G` puis `MMB` glissé = travelling avant/arrière : `G Z Z` en local).
- Viser un objet en permanence : contrainte **Track To** ou **Damped Track** vers un Empty.

## 3. La focale et le capteur
Réglages : *Object Data (caméra) → Lens → Focal Length* et *Camera → Sensor Fit / Size*
(36 mm par défaut, plein format).
| Focale (plein format) | Nom | Effet | Usage |
|---|---|---|---|
| 14–24 mm | Grand-angle | Champ large, perspective exagérée, déforme les visages proches | Décors, action, plans subjectifs, malaise |
| 35 mm | Grand-angle modéré | Naturel, immersif | Plans d'ensemble « humains », steadicam |
| 50 mm | Normale | Proche de la perception humaine | Plans moyens |
| 65–85 mm | Courte téléfocale | Visages flatteurs, arrière-plan rapproché | **Portraits**, dialogues |
| 135 mm + | Téléobjectif | Compression, isolement du sujet | Gros plans, espionnage, foules compressées |
**Changer la focale ≠ rapprocher la caméra** : la focale change le cadrage **et** la
compression des distances ; rapprocher change la perspective.

Autres réglages : *Lens Unit* (mm ou champ de vision en degrés), *Type* (*Perspective*,
*Orthographic* (CH01.02), *Panoramic* (Cycles : fisheye, équirectangulaire), *Custom*),
*Shift X/Y* (décentrement sans déformer les verticales — architecture), *Clip Start/End*.

## 4. Composition : la règle des tiers
Divisez l'image en 3 × 3 : placer les éléments importants (les yeux, l'horizon) sur les
**lignes** ou leurs **intersections** rend l'image plus dynamique que le centrage.
*Object Data → Viewport Display → Composition Guides* : *Thirds*, *Center*, *Diagonal*,
*Golden Ratio/Triangles*, *Harmonious Triangles*. **Regard dirigé** : laisser de l'espace
devant le regard du personnage (*lead room*).
Hauteur de caméra : à hauteur d'œil (neutre) ; plongée (au-dessus, rend petit/vulnérable) ;
contre-plongée (en dessous, rend imposant).

## 5. Profondeur de champ (*Depth of Field*)
Le flou d'arrière-plan d'une vraie caméra, qui guide l'œil vers le sujet.
- *Object Data → Depth of Field* (case à cocher) → **Focus on Object** (un Empty sur les
  yeux : le point suit le sujet) ou **Focus Distance** (mètres).
- *Aperture → F-Stop* : petit nombre (1,4–2,8) = beaucoup de flou ; grand (8–16) = tout net.
- Le flou augmente avec la **focale** et quand le sujet est **proche** de la caméra.
- Visible en mode *Rendered* (EEVEE et Cycles) et au rendu final.

## 6. Résolution et format d'image
*Output → Format* : 1920 × 1080 (16:9), 2048 × 858 (≈ 2,39:1, « scope » cinéma), 1080 × 1920
(vertical). Le **format** fait partie de la composition : un 2,39:1 appelle des compositions
horizontales, des paysages, des duos face à face.

## 7. En production
Chaque plan a **sa** caméra (`CAM_sq010_sh0010`), héritée du storyboard (CH18.20) puis
affinée au layout. Focale, hauteur et mouvement sont des décisions de mise en scène
documentées ; changer de focale entre deux plans d'un même dialogue est une faute de
continuité si ce n'est pas voulu.
