# CH18.09 — Cours théorique : dessiner dans l'espace 3D, organiser une scène

## 1. Le dessin a une adresse dans l'espace
Chaque point d'un trait a des coordonnées X, Y, Z. Deux réglages de l'en-tête du Draw Mode
décident où atterrit un nouveau trait (rappel CH18.06) :
- **Stroke Placement** — *sur quoi* on projette : **Origin** (origine de l'objet), **3D Cursor**
  (le curseur 3D), **Surface** (la surface des objets visibles, avec un petit décalage *Offset*),
  **Stroke** (les traits déjà dessinés).
- **Drawing Plane** — *quel plan* passe par ce point : **View** (face à la vue), **Front (X-Z)**,
  **Side (Y-Z)**, **Top (X-Y)**, **Cursor** (le plan orienté comme le curseur 3D).
| Je veux dessiner… | Stroke Placement | Drawing Plane |
|---|---|---|
| un décor vertical à 14 m (montagnes) | 3D Cursor (curseur à Y = 14) | Front (X-Z) |
| une route, un tapis, des ombres au sol | 3D Cursor (curseur à Z = 0) | Top (X-Y) |
| un mur de côté | 3D Cursor | Side (Y-Z) |
| sur la surface d'un objet 3D (tag, fissure) | Surface | — |
| une retouche sur un dessin existant | Stroke | — |

**Placer le curseur 3D** : `Shift+clic droit` dans le viewport, ou en saisie précise :
barre latérale `N` → onglet **View** → **3D Cursor** → *Location*.

## 2. Le Canvas : une grille pour se repérer
Menu **Viewport Overlays** (en Draw Mode) → section **Canvas** : case **Use Grid**, *Opacity*,
*Scale*, *Subdivisions*… La grille apparaît dans le **plan de dessin actif** : indispensable pour
vérifier qu'on dessine bien à plat sur le sol (Top) ou bien de face (Front). *Canvas X-Ray*
la rend visible à travers les objets. Dans la même fenêtre : **Fade Inactive Layers** et
**Fade Inactive Objects** atténuent ce qui n'est pas en cours d'édition.

## 3. Construire un décor en profondeur
Méthode de layout dessiné (utilisée aussi pour la prévisualisation de plans 3D) :
1. Caméra posée d'abord (focale, hauteur, direction) — c'est elle qui décide de la composition.
2. Un objet GP de décor (`GP_Set`) avec **un calque par plan** : GROUND, BG, MID, FG.
3. Pour chaque plan : placer le curseur 3D à la bonne distance, choisir le plan de dessin, dessiner
   **en vue caméra** (`Num 0`), puis **orbiter** pour contrôler la profondeur.
4. Dessiner plus **grand** ce qui est loin : un trait de 1 m à 25 m de la caméra paraît minuscule.
5. Les éléments proches se placent avec prudence : à 3 m de la caméra, ils couvrent l'écran.
Résultat : une parallaxe réelle quand la caméra bouge (travelling, panoramique), impossible avec un
dessin plat — c'est la base du *2.5D* et de l'animatique en profondeur (module D).

## 4. Les images de référence
**Add → Image → Reference** (ou **Background**) crée un *empty* qui affiche une image dans la
scène (concept, plan, photo, planche de storyboard). L'image ne se rend pas ; on la règle
(*Opacity*, *Depth*, *Side*) dans Properties → Object Data de l'empty. Conseils : une collection
`REFERENCES`, image **empaquetée** (*File → External Data → Pack Resources*) pour ne pas perdre le
lien, opacité 30–50 %.

## 5. Organiser une scène GP
- **Collections** : SET (3D), DRAWINGS (GP), REFERENCES, CAMERAS, LIGHTS.
- **Un objet GP par ensemble qui bouge ou se règle ensemble** ; calques par profondeur ou par
  fonction (LINE, COLOR…).
- **Lights** des calques : décoché pour des couleurs plates (style dessin) ; coché pour que le
  dessin réagisse aux lampes (intégration 3D). Dans ce chapitre, la solution les décoche.
- **Passe Z** activée pour un rendu correct devant/derrière la 3D (CH18.06).
- Plusieurs **scènes** dans un fichier (sélecteur de scène en haut) : une scène par plan ou par
  séquence, objets partagés par *Link* — approfondi en phase 15.

## 6. Optimiser
| Problème | Réglage |
|---|---|
| Viewport lent pendant la lecture | Properties → Render → **Simplify** → sous-panneau **Grease Pencil** : *Playback Only*, désactiver *Fill*, *Modifiers*, *Shader Effects*, *Layers Tinting*, *Antialiasing* |
| Traits trop lourds (milliers de points) | modificateur **Simplify** ou Edit Mode → *Simplify* |
| Trop d'objets/calques visibles | masquer, isoler (`Num *`), *Fade Inactive Layers* |
| Fichier lourd | une scène par plan, références empaquetées raisonnablement (images compressées) |
