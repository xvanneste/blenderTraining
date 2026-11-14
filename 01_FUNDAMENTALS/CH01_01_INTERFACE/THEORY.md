# CH01.01 — Cours théorique : l'interface de Blender

## 1. La logique d'ensemble
Blender ne ressemble pas à un logiciel à menus classiques : c'est un **atelier
reconfigurable**. Une seule fenêtre est découpée en **zones** (*areas*) ; chaque zone
affiche un **éditeur** (*editor*) ; chaque éditeur a ses **régions** (en-tête, barre
d'outils, sidebar…). Un jeu de zones prêt à l'emploi est un **workspace** (onglets en haut).

```
┌──────────────────────── Topbar : menus File Edit Render Window Help │ onglets de workspaces ──┐
│ ┌─────────────────────────────────────────────┐ ┌────────────────────────┐ │
│ │ En-tête (header) de la vue 3D               │ │ Outliner               │ │
│ │┌──┐                                    ┌───┐│ │ (arborescence scène)   │ │
│ ││T │      3D VIEWPORT                   │ N ││ ├────────────────────────┤ │
│ ││oo│      (zone principale)             │ s ││ │ Properties             │ │
│ ││ls│                                    │ i ││ │ (propriétés de l'objet │ │
│ │└──┘                                    │ de││ │  actif, de la scène…)  │ │
│ └─────────────────────────────────────────────┘ │                        │ │
│ ┌─────────────────────────────────────────────┐ │                        │ │
│ │ Timeline (lecture, images clés)             │ │                        │ │
│ └─────────────────────────────────────────────┘ └────────────────────────┘ │
└──────────── Status bar : raccourcis contextuels · statistiques · version ──────────────┘
```

**Analogie.** Le workspace est une **pièce** de l'atelier (la pièce « modélisation », la
pièce « éclairage »…), les zones sont les **établis** de cette pièce, et l'éditeur est
**l'outil posé sur l'établi**. On peut changer l'outil d'un établi à tout moment.

## 2. Les éditeurs essentiels (première rencontre)
| Éditeur | Rôle | Phase où il devient central |
|---|---|---|
| **3D Viewport** | Voir et manipuler la scène 3D | toutes |
| **Outliner** | Arborescence de tout ce que contient la scène / le fichier | 1 |
| **Properties** | Réglages de l'objet actif, de ses données, de la scène, du rendu | 1 |
| **Timeline / Dope Sheet / Graph Editor** | Temps, images clés, courbes | 7 |
| **Shader Editor** | Matériaux par nœuds | 4 |
| **Geometry Node Editor** | Géométrie procédurale | 5 |
| **Image Editor / UV Editor** | Images, rendus, dépliage UV | 4, 10 |
| **Compositor** | Retouche des rendus par nœuds | 11 |
| **Video Sequencer** | Montage | 12, 18 |
| **Text Editor / Python Console / Info** | Scripts, consignes, journal des actions | 13 |
| **File Browser / Asset Browser** | Fichiers, bibliothèques d'assets | 2, 16 |
| **Spreadsheet** | Données de géométrie (attributs) | 5 |

## 3. Les régions d'un éditeur
- **Header** (en-tête) : menus de l'éditeur et réglages rapides. `RMB` sur l'en-tête →
  le déplacer en haut/en bas, le masquer.
- **Toolbar** (`T`) : outils actifs (sélection, déplacement, rotation…).
- **Sidebar** (`N`) : onglets *Item* (transformations numériques), *Tool*, *View*, et
  ceux des add-ons.
- **Tool Settings** : options de l'outil actif (sous l'en-tête de la vue 3D).
- **Adjust Last Operation** : panneau en bas à gauche après une action (ex. ajout d'un
  cube) pour modifier ses paramètres **après coup** — réouvrable avec `F9`.

## 4. Manipuler les zones
| Action | Comment |
|---|---|
| Redimensionner | Glisser la frontière entre deux zones |
| Diviser | Glisser depuis un **coin** d'une zone vers l'intérieur ; ou `RMB` sur une frontière → *Vertical Split / Horizontal Split* |
| Fusionner | Glisser depuis un coin vers la zone voisine (une flèche indique la zone absorbée) ; ou `RMB` sur la frontière → *Join Areas* |
| Changer d'éditeur | Bouton *Editor Type* (icône à gauche de l'en-tête) |
| Maximiser une zone | `Ctrl+Space` (même raccourci pour revenir) |
| Plein écran sans interface | `Ctrl+Alt+Space` |
| Changer de workspace | Clic sur l'onglet ; `Ctrl+PageUp / PageDown` |
| Nouveau workspace | `+` à droite des onglets, ou `RMB` sur un onglet → *Duplicate* |

## 5. Trouver ce qu'on cherche
- **`F3` — Menu Search** : tapez le nom d'une commande (« subdivide », « add cube ») :
  Blender la trouve dans les menus et affiche le chemin de menu et le raccourci.
- **Infobulles** : survolez un bouton ; avec les *Python Tooltips* (Preferences →
  Interface), le nom Python s'affiche aussi (utile en phase 13).
- **Clic droit (`RMB`)** : menu contextuel de l'élément survolé (dans la vue 3D : menu
  de l'objet ; sur un champ : *Copy to Selected*, *Reset to Default*, *Add to Quick
  Favorites*…).
- **`Q` — Quick Favorites** : votre menu personnel ; `RMB` sur une commande → *Add to
  Quick Favorites*.
- **Status bar** : affiche les raccourcis de la souris valables **maintenant**.

## 6. Le principe « survol » (*hover*)
Les raccourcis s'appliquent à **l'éditeur sous la souris**. `A` (tout sélectionner) dans
l'Outliner sélectionne dans l'Outliner ; dans la vue 3D, dans la vue 3D. Beaucoup de
débutants croient qu'un raccourci « ne marche pas » : la souris était au-dessus d'un autre
éditeur.

## 7. Les modes (aperçu)
Le menu en haut à gauche de la vue 3D (*Object Mode*, *Edit Mode*, *Sculpt Mode*…) change
ce que fait la vue : on manipule des objets entiers, ou leurs sommets, ou on les sculpte…
`Tab` bascule Object/Edit. Détails en CH01.05.

## 8. L'interface en production
Chaque département a son workspace : *Layout* pour la mise en place, *Modeling*,
*Shading*, *Animation*… Les studios distribuent leur `startup.blend` avec des workspaces
adaptés (CH00.02). Vous construirez les vôtres au fil de l'académie.
