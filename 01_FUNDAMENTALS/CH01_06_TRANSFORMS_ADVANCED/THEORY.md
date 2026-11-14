# CH01.06 — Cours théorique : transformations avancées

## 1. Échelle ≠ dimensions
- **Scale** : un multiplicateur appliqué à l'objet (1 = taille d'origine des données).
- **Dimensions** : la taille réelle résultante, en mètres (sidebar `N` → *Item*).
Un cube de 1 m avec *Scale* (2, 1, 0,5) mesure 2 × 1 × 0,5 m. On peut obtenir la même
caisse avec un maillage de 2 × 1 × 0,5 m et une échelle de 1 : **même image, comportement
différent**.

## 2. Appliquer les transformations (`Ctrl+A`)
*Apply → Location / Rotation / Scale / All Transforms / Rotation & Scale…* : Blender
« cuit » la transformation dans les **données** (les sommets sont recalculés) puis remet la
transformation à zéro (échelle 1, rotation 0). Les dimensions ne changent pas.

**Pourquoi appliquer l'échelle ?** Beaucoup d'outils travaillent dans l'espace de l'objet
et sont faussés par une échelle non uniforme :
| Outil | Avec une échelle (2, 1, 0,5) non appliquée |
|---|---|
| Biseau (modificateur Bevel, outil `Ctrl+B`) | biseaux de largeurs différentes selon l'axe |
| Épaisseur (Solidify), textures procédurales | étirées |
| Simulations (tissu, rigid body, fluides) | masse, collisions et forces fausses |
| Rigging, parentage, export vers d'autres logiciels | déformations et échelles erronées |
Règle de production : **échelle appliquée (1, 1, 1) avant rigging, simulation, export.**
⚠️ Pour des objets **liés** (`Alt+D`), appliquer l'échelle exige de rendre les données
uniques d'abord (Blender le signale).

## 3. Les orientations de transformation
Menu *Transform Orientation* (en-tête, ou menu circulaire `,`) : dans quel repère sont
définis X, Y, Z pour `G`, `R`, `S` et les gizmos.
| Orientation | Axes |
|---|---|
| **Global** | ceux du monde |
| **Local** | ceux de l'objet (suivent sa rotation) |
| **Normal** | perpendiculaire à la sélection (en Edit Mode : à la face) |
| **Gimbal** | axes de rotation d'Euler (animation, CH07) |
| **View** | ceux de l'écran |
| **Cursor** | ceux du curseur 3D |
| **Parent** | ceux du parent |
Rappel : `G X` = axe de l'orientation courante ; `G X X` = deuxième orientation (locale si la
première est globale).

## 4. Le snapping (aimantation)
`Shift+Tab` active/désactive ; l'icône aimant de l'en-tête et son menu (`Ctrl+Shift+Tab`)
règlent :
- **Snap Target** (ce sur quoi on s'aimante) : *Increment*, *Grid*, *Origin*, *Vertex*,
  *Edge*, *Face*, *Volume*, *Edge Center*, *Edge Perpendicular*, *Face Center*.
- **Snap Target for Individual Elements** : *Face Project*, *Face Nearest* (chaque élément
  déplacé est projeté individuellement sur la surface).
- **Snap Base** (le point de l'objet qui s'aimante) : *Closest*, *Center*, *Median*, *Active*.
> ⚠️ Versions : avant Blender 4.x ces réglages s'appelaient *Snap To* et *Snap With* ; de
> nombreux tutoriels en ligne utilisent encore ces anciens noms.
- Options : *Align Rotation to Target* (orienter l'objet selon la face visée),
  *Affect* (Move, Rotate, Scale), *Exclude Non-Selectable*…
Maintenir `Ctrl` **pendant** une transformation active temporairement le snapping (sans
le laisser activé).

**Recette « poser un objet sur une surface »** : Snap Target = *Face*, Snap Base = *Closest*, puis `G Z` + `Ctrl` en survolant la surface — ou plus simplement, si
l'on connaît la hauteur, une saisie numérique.

## 5. Le curseur 3D (aperçu, détaillé en CH01.07)
`Shift+S` ouvre le menu circulaire *Snap* : *Cursor to Selected*, *Selection to Cursor*,
*Cursor to World Origin*… très utile pour placer précisément.

## 6. En production
Un **contrôle de pré-publication** vérifie toujours : échelles à 1, rotations raisonnables,
objets posés (pas de flottement ni d'interpénétration), orientation correcte (« l'avant »
d'un personnage regarde −Y). Le script `bcma_naming_check.py` sera étendu en phase 13 pour
détecter les échelles non appliquées.
