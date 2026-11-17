# CH06.10 — Cours théorique : contrôleurs et ergonomie

## 1. Trois familles de bones
- **Contrôleurs** (root, ctl_spine, ctl_arm.L/.R) : ce que touche l'animateur ; jamais de déformation.
- **Déformation** (DEF-spine, DEF-arm.L/.R) : portent les poids du maillage ; suivent les contrôleurs par Copy Transforms (World → World).
- **Mécanisme** (MCH-pivot) : intermédiaires que personne ne touche ; ici parent de ctl_spine.
Ce découpage est celui des rigs de production (Rigify : ORG-, MCH-, DEF-, contrôleurs).

## 2. Collections de bones
Armature properties > Bone Collections : Controls, Deform, Mechanism ; chaque bone est assigné à une collection ; l'œil masque la collection. Dans l'exercice, Deform et Mechanism sont masquées. API : `arm.collections.new`, `collection.assign(bone)`, `collection.is_visible`.

## 3. Formes personnalisées
Un contrôleur peut s'afficher avec la forme d'un objet (maillage en fil de fer) : Bone properties > Viewport Display > Custom Shape. Les objets WGT_circle (anneau de 24 segments, plan XZ du bone) et WGT_box (cube fil de fer) sont rangés dans une collection WIDGETS masquée. Par défaut la forme est mise à l'échelle par la longueur du bone. Un anneau autour de l'axe d'un bone invite à le tourner.

## 4. Couleurs
Bone properties > Bone Color : palettes DEFAULT, THEME01 à THEME20 (et CUSTOM). Convention de l'exercice : root THEME09, centre (ctl_spine) THEME03, gauche (.L) THEME04, droite (.R) THEME01. Seul l'écart entre côtés compte pour le correcteur, pas la teinte choisie.

## 5. Verrous
ctl_arm.L/.R : Location et Scale verrouillés (rotation seule) ; ctl_spine : Scale verrouillé. Les verrous agissent sur l'interface (ils ne bloquent pas une affectation par script) ; c'est une protection ergonomique, pas une contrainte.

## 6. Mesures
Tourner ctl_arm.L de 30° : DEF-arm.L tourne de 30,0°, DEF-arm.R de 0,00°. Tourner ctl_spine de 20° : les deux bras de 20,0°. Contre-exemple « broken_link » : 0,0° dans tous les cas, alors que toute la structure est correcte.

## 7. Pièges
- Contrôleurs avec use_deform actif.
- Collections masquées mais bones oubliés dans « Default ».
- Formes laissées visibles dans la scène.
- Rig ordonné mais lien cassé : toujours tester le mouvement.

## 8. Limites
Rig minimal de 8 bones ; pas de sélecteur d'interface (panneau Python) ni de collections de bones multiples par membre ; les couleurs personnalisées (CUSTOM) ne sont pas testées.
