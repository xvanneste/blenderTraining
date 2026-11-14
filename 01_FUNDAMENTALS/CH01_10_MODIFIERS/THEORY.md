# CH01.10 — Cours théorique : les modificateurs

## 1. Le principe non destructif
Un **modificateur** transforme la géométrie **à l'affichage et au rendu** sans toucher au
maillage d'origine. On empile plusieurs modificateurs : c'est la **pile** (*stack*), évaluée
**de haut en bas**. Tant qu'on n'applique pas, tout reste réglable et réversible.

**Analogie.** Le maillage est une photo ; les modificateurs sont des **calques de réglage**
dans un logiciel de retouche : on peut les changer, les réordonner, les masquer, et la photo
d'origine reste intacte.

Où : *Properties → Modifiers* (clé à molette bleue) → **Add Modifier** (catégories *Edit,
Generate, Deform, Normals, Physics…*). Chaque modificateur a :
- des icônes d'activation : *Edit Mode*, *Viewport* (écran), *Render* (appareil photo) ;
- un menu ˅ : *Apply* (`Ctrl+A` au survol), *Duplicate*, *Copy to Selected*, *Move to
  First/Last* ; une poignée `::::` pour réordonner.

## 2. Six modificateurs essentiels
| Modificateur | Catégorie | Effet | Réglages clés | Usage cinéma |
|---|---|---|---|---|
| **Array** | Generate | Répète l'objet | *Count* / *Fit Length* / *Fit Curve* ; *Relative Offset* (en tailles d'objet), *Constant Offset* (en mètres), *Object Offset* (un Empty pour tourner/échelonner) ; *Merge* | Planchers, clôtures, escaliers, rails |
| **Mirror** | Generate | Symétrie | Axes X/Y/Z, *Bisect*, *Clipping* (empêche de traverser le plan), *Merge* | Personnages, véhicules, architecture symétrique |
| **Solidify** | Generate | Donne une épaisseur | *Thickness*, *Offset*, *Even Thickness* | Murs, vêtements, contenants, feuilles |
| **Bevel** | Generate | Adoucit les arêtes | *Amount*, *Segments*, *Limit Method* (Angle par défaut), *Profile* | Accroches de lumière réalistes sur tout objet manufacturé |
| **Subdivision Surface** | Generate | Lisse en subdivisant | *Levels Viewport* / *Render* (CH00.03 : ×4 par niveau), *Optimal Display* | Formes organiques, objets lisses |
| **Boolean** | Generate | Union / différence / intersection avec un autre objet | *Operation*, *Object*, *Solver* | Trous, découpes (vu en CH02.07) |

## 3. L'ordre compte
La pile est un **pipeline** : chaque modificateur reçoit le résultat du précédent.
| Ordre | Résultat pour le seau |
|---|---|
| Solidify → Subdivision | épaisseur régulière, puis lissage de l'ensemble : **correct** |
| Subdivision → Solidify | lissage d'une surface sans épaisseur, puis épaisseur : bords durs, coût plus élevé |
| Mirror → Subdivision | la symétrie est lissée au centre : **correct** |
| Subdivision → Mirror | couture visible au plan de symétrie |
| Bevel → Subdivision | biseau puis lissage : les arêtes restent nettes mais douces |
| Array → Bevel | chaque copie biseautée ; Bevel → Array : idem mais coût moindre |
Règle pratique : **générer** (Mirror, Array) → **épaissir** (Solidify) → **arrondir les
arêtes** (Bevel) → **lisser** (Subdivision) → **déformer** (phase 6).

## 4. Appliquer : quand et pourquoi
*Apply* fige le résultat dans le maillage (le modificateur disparaît). À faire seulement :
- pour une **retouche manuelle** impossible autrement ;
- pour un **export** vers un logiciel qui ne connaît pas les modificateurs (souvent l'export
  le fait automatiquement) ;
- jamais « pour alléger » : les modificateurs **sont** légers tant que leurs niveaux le sont.
En production, un asset garde sa pile ; le **niveau de subdivision au rendu** est un réglage
de plan (plus élevé en gros plan).

## 5. Échelle et modificateurs
Un objet à l'échelle non appliquée fausse *Bevel*, *Solidify*, *Array (Constant Offset)*
(CH01.06) : appliquez l'échelle **avant** de régler ces modificateurs.
