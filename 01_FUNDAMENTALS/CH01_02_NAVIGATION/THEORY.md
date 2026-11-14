# CH01.02 — Cours théorique : naviguer dans l'espace 3D

## 1. Le repère 3D de Blender
- **X** (rouge) : gauche → droite. **Y** (vert) : avant → arrière (la « profondeur »).
  **Z** (bleu) : bas → haut. Blender est « Z-up » : le sol est le plan X-Y.
- L'**origine du monde** (0, 0, 0) est au croisement des lignes rouge et verte de la grille.
- La vue de **face** (*Front*, `Num 1`) regarde **vers +Y** (on se tient du côté −Y).

**Analogie.** Vous êtes un drone-caméra : la navigation déplace **le drone** (votre point
de vue), jamais la scène. Orbiter ne fait pas tourner les objets.

## 2. Les trois gestes fondamentaux
| Geste | Souris | Clavier / alternative |
|---|---|---|
| **Orbiter** | `MMB` glissé | `Num 2 4 6 8` (par crans de 15°), gizmo de navigation |
| **Panoramique** | `Shift+MMB` | `Ctrl+Num 2 4 6 8`, icône main du gizmo |
| **Zoom** | Molette, `Ctrl+MMB` | `Num +` / `Num −`, icône loupe ; `Shift+B` zoom sur un rectangle |

Point de pivot de l'orbite : centre de la vue, ou la sélection si *Orbit Around Selection*
(CH00.02), ou ce qui est sous la souris avec *Auto Depth*.

## 3. Vues prédéfinies et projections
| Touche | Vue |
|---|---|
| `Num 1` / `Ctrl+Num 1` | Face / arrière |
| `Num 3` / `Ctrl+Num 3` | Droite / gauche |
| `Num 7` / `Ctrl+Num 7` | Dessus / dessous |
| `Num 9` | Vue opposée à la vue actuelle |
| `Num 5` | Perspective ↔ orthographique |
| `Num 0` | Vue caméra (caméra active) |
| `` ` `` (accent grave) | Menu circulaire des vues |

- **Perspective** : les objets lointains paraissent plus petits (comme l'œil, comme une
  caméra). Pour juger d'une composition.
- **Orthographique** : pas de déformation de distance, les parallèles restent parallèles.
  Pour modéliser avec précision, aligner, mesurer. Le nom de la vue en haut à gauche
  indique l'état (*Front Orthographic*, *User Perspective*).

## 4. Cadrer
| Commande | Raccourci | Usage |
|---|---|---|
| Frame Selected | `Num .` | Amener la vue sur la sélection — **la commande la plus utilisée** |
| Frame All | `Home` | Voir toute la scène |
| Vue locale | `Num /` (ou `/`) | N'afficher que la sélection ; même touche pour sortir |
| Clipping Region | `Alt+B` (tracer un rectangle) | Découper la vue pour voir à l'intérieur ; `Alt+B` à nouveau pour annuler |
| Center View to Cursor | `Alt+Home` | Centrer sur le curseur 3D |

## 5. Navigation à la première personne : Walk / Fly
`Shift+`` (accent grave) : **Walk** (par défaut) — `W A S D` pour avancer/reculer/strafe,
souris pour regarder, `E/Q` monter/descendre, molette = vitesse, `Shift` = courir, `Tab` =
gravité, `LMB` valider, `RMB`/`Échap` annuler. Utile dans les décors et pour placer des
caméras « à hauteur d'homme ». (*View → Navigation → Fly / Walk Navigation*.)

## 6. Caméras et vue
- `Num 0` : regarder **à travers** la caméra active.
- `Ctrl+Num 0` : faire de l'objet sélectionné la caméra active.
- `Ctrl+Alt+Num 0` : **placer la caméra active là où vous regardez** (*Align Active Camera
  to View*). Méthode reine pour cadrer : naviguer, puis aligner.
- *Lock Camera to View* (sidebar `N` → *View*) : en vue caméra, naviguer **déplace la
  caméra** (à désactiver ensuite, sinon on dérègle ses plans !).
- Caméra **orthographique** (*Object Data → Lens → Type*) : *Orthographic Scale* règle la
  largeur visible (en mètres). Utilisée pour les vues techniques, les rendus de plans
  d'architecture, les styles 2D.

## 7. Navigation en production
Les layout artists naviguent dans des décors immenses : ils utilisent la vue locale,
les collections masquées, Walk pour les points de vue humains, et surtout la recherche
d'objets (Outliner + `Num .`). Un animateur passe sans cesse de la vue caméra (ce que verra
le spectateur) à des vues de travail (pour poser les membres).
