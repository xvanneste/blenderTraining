# CH18.11 — Cours théorique : continuité et dialogue

## 1. La continuité : le spectateur ne doit jamais se perdre
Le montage assemble des plans tournés séparément. Pour que le spectateur croie à un espace et un
temps continus, on respecte des **raccords** : à chaque coupe, il doit savoir où il est, qui regarde
qui, et dans quelle direction on va.

## 2. Le découpage classique d'un dialogue
1. **Plan d'installation** (*master*, plan d'ensemble ou plan moyen) : montre A, B et le lieu.
2. **Champ / contrechamp** : B vu par-dessus l'épaule de A (**amorce**), puis A par-dessus l'épaule de B.
3. **Plans serrés** (PRP, GP) quand l'émotion monte ; **insert** sur l'objet qui compte.
4. Retour au **master** pour respirer ou relancer l'action.
Le mini-dialogue du chapitre : SH010 master → SH020 amorce sur B → SH030 amorce sur A → SH040 B
serré → SH050 A serré → SH060 insert sur la tasse.

## 3. Les raccords à respecter
| Raccord | Règle |
|---|---|
| **Axe (180°)** | toutes les caméras du même côté de la ligne A–B (CH18.10) |
| **Regard** | A, à gauche, regarde vers la droite de l'écran ; B, à droite, vers la gauche — dans **tous** les plans |
| **Position à l'écran** | A reste dans la moitié gauche, B dans la moitié droite (le correcteur le mesure) |
| **Direction** | un personnage qui sort du cadre par la **droite** entre dans le plan suivant par la **gauche** |
| **Mouvement** | on coupe pendant un geste (raccord mouvement) : le geste continue dans le plan suivant |
| **Accessoires, lumière** | la tasse ne change pas de main, la lumière ne saute pas d'un plan à l'autre |
Un **faux raccord** est une rupture de ces règles (involontaire) ; un *jump cut* est une coupe entre
deux plans trop semblables.

## 4. Entrées et sorties de champ
Pour faire traverser un lieu à un personnage en plusieurs plans : il sort par un côté, entre par le
côté opposé, et garde le **même sens de déplacement** à l'écran (gauche → droite par exemple). Un
changement de sens signifie un demi-tour… ou un faux raccord.

## 5. Dans Blender : marqueurs et caméras
Un découpage se construit directement dans la scène :
- une caméra par plan (`CAM_SH010`…) ;
- dans la Timeline, un **marqueur** par début de plan (`M`, renommer `F2`) ;
- **Marker → Bind Camera to Markers** (`Ctrl+B`) : à cette image, la caméra active change. La lecture
  de la scène devient un **montage** des plans : c'est la base de l'animatique (CH18.14) et du layout
  (phase 15).
