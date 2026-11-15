# CH18.07 — Cours théorique : brushes, traits, remplissages, matériaux

## 1. Pinceau, outil, matériau : qui fait quoi ?
En Draw Mode, trois choses déterminent l'aspect d'un trait :
| Élément | Détermine | Où |
|---|---|---|
| **Outil** (*Draw, Fill, Erase, Tint*, primitives Line/Box/Circle…) | ce que fait le clic | barre d'outils à gauche (`T`) |
| **Pinceau** (*brush*) | comment le trait est tracé : épaisseur, force, pression, lissage, type Stroke/Fill/Both | en-tête de l'outil, **étagère d'assets** en bas du viewport |
| **Matériau GP** | de quoi le trait est fait : couleur du trait, couleur du remplissage, style | `U` (menu du matériau actif), Properties → Material |

## 2. Les pinceaux livrés (Essentials, Blender 5.3)
Depuis Blender 4.3, les pinceaux sont des **assets** choisis dans l'étagère en bas du viewport
(ou le sélecteur de l'en-tête). Pinceaux de dessin livrés (vérifié dans
`essentials_brushes-gp_draw.blend`) : **Pencil**, **Pencil Soft**, **Pen**, **Ink Pen**,
**Ink Pen Rough**, **Marker Bold**, **Marker Chisel**, **Airbrush**, **Tint**, **Fill**,
**Eraser Hard**, **Eraser Soft**, **Eraser Stroke**.
| Pinceau | Caractère | Usage |
|---|---|---|
| Pencil / Pencil Soft | fin, légèrement irrégulier | esquisse, construction |
| Ink Pen / Pen | net, épaisseur variable avec la pression | encrage |
| Marker Bold / Chisel | large, régulier | masses, storyboard rapide |
| Airbrush | doux, diffus | ombres, lumières |

Réglages essentiels : **Size** (taille, `F` ou `[` `]`), **Strength** (opacité), icône de
**pression** à côté de chacun (tablette graphique), **Stroke Mode** (trois icônes dans l'en-tête) : *Stroke* (trait seul),
*Fill* (remplissage seul), *Both* (les deux), **Caps Type** (*Round* / *Flat*).

## 3. Les remplissages dans Blender 5.3 (important)
Dans Blender 5.3, **le remplissage est une propriété de chaque trait**, plus une case du matériau :
- dessiner avec un pinceau en **Stroke Mode : Fill** ou **Both** produit un trait rempli ;
- l'outil **Fill** (pinceau « Fill ») crée un trait rempli qui épouse une **zone fermée** cliquée ;
- en Edit Mode, **Set Stroke Type** change des traits existants en Stroke / Fill / Both.
Le matériau fournit les **couleurs** (panneaux *Stroke* et *Fill* → *Base Color*) et les styles.
Attention aux tutoriels antérieurs : les cases à cocher « Stroke » et « Fill » du matériau
n'apparaissent plus dans l'interface 5.3.

### L'outil Fill
- Clic gauche dans une zone fermée : remplit ; `Ctrl+clic` : remplissage **inversé** ;
  `Alt+glisser` : dessine des **lignes guides** de fermeture (supprimées ensuite si *Auto-Remove
  Fill Guides* est actif).
- **Layer Mode** : quels calques servent de frontières (*Visible*, *Active*, *Layer Above*,
  *Layer Below*…). On encre sur un calque et on remplit sur un calque **en dessous** : les aplats
  ne recouvrent jamais l'encrage.
- **Boundary** (*All*, *Strokes*, *Edit Lines*), **Precision**, **Dilate/Contract** (déborde un peu
  sous le trait pour éviter les liserés blancs).
- **Gap Closure** : *Closure Mode* (*Extend* / *Radius*) et *Closure Size* ferment
  automatiquement les petites ouvertures d'un dessin.

## 4. Les matériaux GP
Properties → Material (bouton **+** pour un nouveau matériau, nommé `MAT_GP_...`) :
- **Stroke** : *Line Type* (*Line*, *Dots*, *Squares*), *Style* (*Solid*, *Texture*),
  *Base Color*, *Holdout* (le trait « perce » les calques en dessous).
- **Fill** : *Style* (*Solid*, *Gradient*, *Texture*), *Base Color*.
Bonnes pratiques : **une couleur = un matériau nommé** (palette de personnage) ; on change la
couleur d'un personnage dans tout le film en modifiant un seul matériau. `U` change le matériau
actif ; *Vertex Paint* permet de nuancer sans multiplier les matériaux.

## 5. Gommer proprement
Outil **Erase** ou `Ctrl+clic gauche` en Draw Mode. Modes (*Eraser Mode*) : **Dissolve**
(gomme douce, diminue l'opacité), **Point** (coupe les traits), **Stroke** (supprime le trait
entier touché). Pour un dessin propre : *Stroke* sur les traits ratés, puis on redessine.

## 6. Méthode professionnelle d'encrage
1. Calque **SKETCH** : crayon (Pencil), recherche libre, puis opacité 30 % et verrou.
2. Calque **LINE** : encre (Ink Pen), traits continus et **fermés** là où l'on veut remplir.
3. Calque **COLOR** **sous** LINE : outil Fill, *Layer Mode : Layer Above* ou *Visible*.
4. Ombres : calque **SHADE** au-dessus de COLOR, aplats plus foncés ou *Tint*.
Ce découpage est celui des studios 2D ; il prépare les calques et modificateurs de CH18.08.
