# CH02.05 — Cours théorique : hard surface

## 1. Qu'appelle-t-on hard surface ?
Les objets **manufacturés** : appareils, véhicules, armes, mobilier industriel, robots, décors
SF. Leur lecture repose sur des **surfaces planes ou régulières** séparées par des **arêtes
contrôlées** : vives, chanfreinées ou arrondies. La qualité d'un modèle hard surface se juge… sur ses
arêtes et sur ses reflets.

## 2. Aucune arête n'est infiniment vive
Dans la réalité, une arête usinée ou moulée a toujours un **rayon** (souvent 0,5 à 3 mm). Au rendu,
ce minuscule arrondi **accroche la lumière** et dessine la forme ; une arête mathématiquement vive
reste noire ou disparaît. D'où trois familles d'arêtes :
| Type | Rendu | Outil |
|---|---|---|
| Vive mais « cassée » | fin liseré lumineux | Bevel modificateur *Angle*, 1–3 mm, 2 segments |
| Chanfrein | facette visible | Bevel 1 segment |
| Arrondi | courbe douce | Bevel 3–6 segments, ou Subdivision + boucles de maintien (CH02.06) |

## 3. Le workflow non destructif par modificateurs Bevel
Plutôt que de biseauter la géométrie (CH02.02), on empile des **modificateurs Bevel** :
- **Limit Method** : *None* (toutes les arêtes), **Angle** (arêtes au-delà d'un angle), **Weight**
  (arêtes munies d'un **Bevel Weight**), *Vertex Group*.
- **Width**, **Segments**, **Profile** (forme de l'arrondi), *Width Type*, *Clamp Overlap*,
  *Outer Miter* (jonctions).
- **Shading → Harden Normals** : redresse les normales des grandes faces (même effet que Weighted
  Normal, CH02.04) ; nécessite **Shade Smooth**.
Recette classique en 2 modificateurs :
1. **Bevel « Weight »** large (ici 2 cm, 4 segments) sur les arêtes choisies — les coins d'un boîtier.
   Le poids se pose en Edit Mode : *Edge → Edge Bevel Weight* (valeur 0 à 1).
2. **Bevel « Angle »** fin (2–3 mm, 2 segments, Harden Normals) sur toutes les autres arêtes vives.

## 4. Arêtes de maintien et contrôle
Quand on utilise la **subdivision** (CH02.06) au lieu du bevel, on contrôle la netteté par des
**boucles de maintien** (*holding / support edges*) près des arêtes : plus elles sont proches, plus
l'arête reste vive. Le bevel modificateur et la subdivision sont deux écoles ; le cinéma utilise
souvent la subdivision pour les personnages et objets déformables, le bevel pour les décors rigides.

## 5. Détails mécaniques : penser fabrication
- **Panneaux et creux** : Inset + Extrude vers l'intérieur (écran, trappe, grille).
- **Boutons, vis, connecteurs** : objets **séparés** ou joints (`Ctrl+J`) ; pas besoin de les
  fusionner topologiquement à la coque (*floaters*, s'ils ne bougent pas).
- **Booléens** pour percer et découper proprement : CH02.07.
- **Échelle réelle et échelle d'objet à 1** (`Ctrl+A` → *Scale*) : sinon les largeurs de bevel sont
  déformées selon les axes.

## 6. Lire un objet hard surface
Grandes formes → formes moyennes (panneaux, creux) → petits détails (boutons, vis, fentes). Un
modèle crédible respecte cette **hiérarchie** : beaucoup de surfaces calmes, quelques zones de détail
denses. Trop de détails partout = bruit visuel.
