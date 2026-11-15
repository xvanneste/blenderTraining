# CH18.06 — Cours théorique : Grease Pencil, interface et objets

## 1. Ce qu'est un objet Grease Pencil
Dans Blender, le dessin n'est pas une image plate : chaque trait (*stroke*) est une suite de
**points en 3D** (position, rayon, opacité). Un objet Grease Pencil (type `GREASEPENCIL`, nouvelle
architecture « GP v3 » depuis Blender 4.3) se comporte comme tout objet : il a une origine, se
déplace, s'anime, se range dans des collections, et ses traits existent **dans l'espace de la
scène**. On peut donc dessiner un personnage **devant** une maison 3D et un ciel **derrière**.

Organisation des données :
```
Objet GP_Character (transformations, modificateurs)
└─ Données Grease Pencil (Object Data)
   ├─ Matériaux GP (trait / remplissage)
   └─ Calques (Layers) — éventuellement rangés dans des groupes (Layer Groups)
      └─ Images clés (frames) → un dessin (drawing) → des traits → des points
```

## 2. Créer un objet
**Add → Grease Pencil** (en Object Mode, `Shift+A`) propose (libellés Blender 5.3) :
| Entrée | Contenu |
|---|---|
| **Blank** | Objet vide (un calque, un matériau) : point de départ habituel |
| **Stroke** | Un trait d'exemple, calques « Lines » et « Color », 6 matériaux |
| **Monkey** | Suzanne dessinée |
| **Scene Line Art / Collection Line Art / Object Line Art** | Contours générés automatiquement depuis la 3D (CH18.08, CH18.19) |

## 3. Les modes
Le sélecteur de mode (en haut à gauche du 3D Viewport, ou `Ctrl+Tab` pour le menu circulaire)
propose pour un objet GP : **Object Mode**, **Edit Mode** (modifier points et traits),
**Sculpt Mode** (déformer les traits au pinceau), **Draw Mode** (dessiner), **Weight Paint**
(poids pour les os) et **Vertex Paint** (couleur peinte sur les points).
| Mode | Sert à | Exemple |
|---|---|---|
| Draw | dessiner, gommer, remplir | encrer un personnage |
| Edit | sélectionner/transformer des points | corriger une main trop grande |
| Sculpt | lisser, pousser, tordre | adoucir un trait tremblé |
| Weight Paint | attribuer des poids aux os | rig 2D (CH18.18) |
| Vertex Paint | colorer sans changer de matériau | ombres colorées |

## 4. Les espaces de travail
**File → New** propose des modèles d'application (*templates*). Vérifié en 5.3 :
- **2D Animation** : workspaces « 2D Animation » et « 2D Full Canvas », un objet *Stroke* et une
  caméra, 1920×1080 à 24 i/s ; idéal pour l'animation 2D (module E).
- **Storyboarding** : workspaces « Storyboarding » et « Video Editing », trois caméras et trois
  objets GP ; utilisé au module D (animatique).
Dans un fichier 3D ordinaire, on dessine simplement dans le 3D Viewport ; c'est l'usage du layout
et du dessin hybride (modules F).

## 5. Où atterrit le trait ? Placement et plan de dessin
En Draw Mode, l'en-tête du viewport propose :
- **Stroke Placement** : **Origin** (sur un plan passant par l'origine de l'objet — défaut),
  **3D Cursor** (plan passant par le curseur 3D), **Surface** (projeté sur la surface des objets
  visibles), **Stroke** (sur les traits existants).
- **Drawing Plane** : **View** (face à la vue — défaut), **Front (X-Z)**, **Side (Y-Z)**,
  **Top (X-Y)**, **Cursor**.
Conséquence pratique : pour dessiner à 10 m dans le décor, on déplace l'**origine** de l'objet (ou
le curseur 3D) à cet endroit **avant** de dessiner. Le chapitre CH18.09 approfondit.

### Profondeur au rendu : le piège de la passe Z
Dans le viewport, un dessin placé derrière une maison est caché par elle. **Au rendu final (F12),
ce n'est pas le cas par défaut** : sans la passe **Z**, le Grease Pencil est dessiné **par-dessus**
les maillages, en EEVEE, Workbench et Cycles. Constaté et mesuré pour ce chapitre dans Blender
5.2 et 5.3.0 ; un comportement analogue est signalé dans le rapport Blender T92052.
**Correctif** : *Properties → View Layer → Passes → Data → **Z*** (cochez). Le rendu respecte
alors la profondeur. À faire dans **toute scène hybride 2D/3D**.

Ne pas confondre avec **Stroke Depth Order** (*Object Data → Settings*) : *2D Layers* (ordre des
calques et des traits, comme en dessin traditionnel — défaut) ou *3D Location* (position réelle
des points). Ce réglage ordonne les **traits entre eux** ; il ne règle pas l'occlusion par les
maillages au rendu (vérifié : même résultat dans les deux modes).

## 6. Calques et groupes de calques
Panneau **Properties → Object Data → Layers** : bouton **+** (nouveau calque), icône **dossier**
(nouveau groupe de calques), cadenas (verrouiller), œil (masquer), opacité. Un calque est
l'équivalent d'une feuille de papier calque : *SKETCH* (recherche, verrouillée et pâle), *LINE*
(encrage), *COLOR* (aplats). Les groupes rangent les calques d'un même personnage ou décor.

## 7. Bonnes pratiques de production
- Un objet GP **par élément** qui bouge indépendamment (personnage, décor, effets).
- Préfixe `GP_` dans les noms (DOCUMENTATION/CONVENTIONS.md), collection dédiée (DRAWINGS).
- Calque de recherche verrouillé, jamais supprimé avant validation.
- Les objets GP apparaissent au rendu **EEVEE**, **Workbench** et aussi **Cycles** (vérifié en
  5.3 : un même dessin donne la même image dans les deux moteurs). Ce ne sont pas des surfaces
  path-tracées : pour des effets avancés en hybride, on les isole dans un View Layer et on
  compose (phase 11).
