# CH06.08 — Cours théorique : shape keys et drivers

## 1. Shape keys
Un shape key est une copie des positions des sommets. Basis est la forme de repos ; les autres keys sont relatifs à Basis. La Value (curseur, ici 0 à 1) dose le mélange. Les shape keys sont appliqués AVANT l'armature : leur déplacement est ensuite plié par le skinning.

## 2. Limiter par un groupe de sommets
Dans le panneau Shape Keys, le champ Vertex Group multiplie l'effet du key par le poids du sommet. Ici le groupe « elbow » vaut 1 − ((x − 0,30)/0,12)² (nul au-delà de 12 cm du coude).

## 3. Le problème du coude
Le bras-tube de CH06.03 plié à 90° : l'anneau du coude (x = 0,30) a un rayon moyen de 4,08 cm (5,00 cm au repos), 2,5 cm côté intérieur. Le key elbow_fix gonfle radialement le coude de 22 % (coefficient calibré par le script : anneau à 4,97 cm à 90°). Le gonflage est un déplacement en espace de repos, plié ensuite par l'armature.

## 4. Le driver
Valeur du key = a / 1,5708 où a est la rotation Z locale de fore (radians) : 0 au repos, 0,5 à 45°, 1 à 90°. Variable Transform Channel (objet RIG_Arm, bone fore, Z Rotation, Local Space) ; fore en Rotation Mode XYZ Euler. Le curseur est limité à 0–1.

## 5. Mesures
Repos : valeur 0, maillage identique (écart 0). 45° : 0,50. 90° : 1,00 ; anneau du coude 4,97 cm (sans key : 4,08). Loin du coude : écart 0,0 mm ; au coude : 11 mm de déplacement.
Contre-exemples : sans groupe, 11 mm d'écart partout ; key trop faible (+5 %) : 4,28 cm ; mauvais bone : valeur 0.

## 6. Pièges
- Oublier Basis : le premier key créé devient la base.
- Modifier le key en Edit Mode sans l'activer (« Pin Shape » / index actif).
- Driver en degrés au lieu de radians.
- Valeur non bornée : un key à 1,5 déforme.
- Shape key et modificateurs : ordre (shape keys d'abord, armature ensuite).

## 7. Limites
Le key est un gonflage radial simple ; les correctifs professionnels sont sculptés pour chaque pose (plusieurs keys combinés par plusieurs drivers). La mesure porte sur l'anneau du coude et la localité, pas sur l'esthétique.
