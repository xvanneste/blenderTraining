# CH06.07 — Cours théorique : rig mécanique

## 1. Les trois outils
- **Drivers** : une propriété (ici la rotation d'une roue) est calculée à partir d'une autre (le déplacement de root). Type Scripted Expression, variable Transform Channel.
- **Damped Track** : l'axe du bone vise une cible (bone ou objet) ; c'est ainsi que se monte un vérin.
- **Limit Rotation** : borne la rotation d'un bone (par axe, en radians dans l'API, en degrés dans l'interface).

## 2. Le camion de l'exercice
Un maillage unique (GEO_Truck) dont les groupes de sommets portent les noms des bones (poids 1 : pièces rigides). Armature RIG_Truck : root, body, quatre roues (axe du bone dirigé vers +X, rayon 0,30 m), bed (charnière arrière à y = −1,0, axe X), bed_pt (attache du vérin sur la benne), anchor (attache sur le châssis), cyl (corps du vérin, 0,6 m) et rod (tige, 0,6 m, enfant de bed_pt). Avant du camion : +Y.

## 3. Les roues
Roulement sans glissement : angle = −d / 0,30 (le signe vient de l'orientation). Driver sur `pose.bones["wheel_FL"].rotation_euler[1]` (le Rotation Mode du bone doit être XYZ Euler) ; expression `-d / 0.3` ; variable d : Transform Channel, objet RIG_Truck, bone root, Location Y, Local Space. Les quatre roues doivent être enfants de root pour avancer avec lui. Mesures : root +0,5 m → −1,667 rad ; +0,2 m → −0,667 rad ; le repère de la roue reste dans son plan (0,0 mm).

## 4. Le vérin
cyl (parent body) : Damped Track vers bed_pt. rod (parent bed_pt) : Damped Track vers anchor. À 30° : écart de direction 0,0°, tête de tige exactement sur bed_pt, recouvrement des deux tubes 0,47 m. La longueur des bones ne change jamais : c'est le recouvrement qui varie (un vrai vérin télescope).

## 5. La benne
Limit Rotation sur bed : X de 0 à 45°, Y et Z à 0, Owner Space Local. À 30° le bout avant de la benne est à z = 1,235 m ; demandée à 80°, elle s'arrête à 1,477 m (45°).

## 6. Pièges
- Rotation Mode du bone resté en Quaternion : le driver sur rotation_euler ne s'applique pas (le correcteur le voit à la rotation nulle).
- Mauvais axe : tourner autour de X ou Z fait vriller la roue (écart de plan 13 à 34 mm mesuré).
- Rayon faux : la roue glisse.
- Roues non enfants de root : elles ne suivent pas (0,024 m au lieu de 0,5 m).
- Damped Track absent : le vérin reste en place (écart 27° et 57° à 30°).
- Limit Rotation absent : course illimitée.

## 7. Limites
Le camion est un volume simple ; pas de direction (roues avant qui braquent), pas de suspension, pas de chenilles : à ajouter en exercice 3. Les drivers « simples » (expression sans fonction Python) fonctionnent même si l'exécution automatique de scripts est désactivée.
