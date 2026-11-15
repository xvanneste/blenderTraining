# CH18.16 — Cours théorique : animation 2D, principes et image par image

## 1. Image par image (*frame by frame*)
En animation 2D traditionnelle, **chaque dessin est une image clé** : rien n'est interpolé. Dans
Grease Pencil, un calque contient une suite de dessins (*keyframes* GP) ; chacun reste affiché jusqu'au
suivant. Animer « en un » = un dessin par image (24/s) ; « en deux » = un dessin toutes les 2 images
(12/s, le standard de l'animation 2D, plus économique et souvent plus lisible) ; « en trois » pour les
mouvements lents ou un style saccadé assumé.

## 2. Poses clés, extrêmes, intervalles
Méthode **pose à pose** :
1. **Poses clés** (*keys*) : celles qui racontent le mouvement (départ, contacts, sommets).
2. **Extrêmes** : les points où le mouvement change de sens (le sommet d'un rebond).
3. **Breakdowns** : la pose intermédiaire qui décide du chemin (arc) entre deux clés.
4. **Intervalles** (*inbetweens*) : les dessins qui remplissent, selon une **charte d'espacement**.
Blender marque ces rôles par le **type de clé** dans la Dope Sheet (R) : *Keyframe*, *Extreme*,
*Breakdown*, *Jitter*, *Moving Hold* — uniquement un repère visuel (couleur/forme), utile pour s'y
retrouver et pour filtrer l'onion skinning (*Filter by Type*).
L'autre méthode, **straight ahead** (droit devant), dessine dans l'ordre : vivante pour le feu, l'eau,
la fumée (CH18.18), mais dérive en volume et en trajectoire.

## 3. Timing et espacement
- **Timing** = combien d'images dure une action (la chute de la balle : 12 images).
- **Espacement** (*spacing*) = la distance entre deux dessins successifs. Dessins **rapprochés** =
  mouvement lent (*slow in / slow out*, ralenti) ; **écartés** = rapide.
Balle : la gravité la ralentit en montant et l'accélère en tombant → dessins serrés au **sommet**,
espacés près du **sol**. Mesure dans l'exemple : vitesse verticale près des sommets ≈ 0,36 × celle
près du sol.

## 4. Écrasement et étirement (*squash & stretch*)
- **Écrasement** au contact : la balle s'aplatit (plus large, moins haute).
- **Étirement** juste avant et juste après le contact : la balle s'allonge dans le sens du mouvement
  (un artifice qui imite le flou de mouvement).
- **Volume constant** : ce que la balle perd en hauteur, elle le gagne en largeur.
- L'intensité diminue avec l'énergie : le dernier rebond s'écrase moins que le premier.

## 5. Amortissement et arcs
Chaque rebond monte à ~60 % de la hauteur précédente (balle en caoutchouc ; une balle de bowling
rebondit à peine, une balle de ping-pong beaucoup) et dure moins longtemps. La trajectoire est une suite
d'**arcs** paraboliques ; l'avancée horizontale est régulière.

## 6. L'onion skinning
Affiche les dessins voisins en transparence (avant/après) : indispensable pour régler arcs et
espacement. Réglages : Object Data Properties > *Onion Skinning* (Mode *Keyframes*/relatif, *Keyframes
Before/After*, *Opacity*, filtre par type) ; affichage : *Viewport Overlays > Onion Skin* ; par calque :
case d'onion skinning dans la liste des calques.
