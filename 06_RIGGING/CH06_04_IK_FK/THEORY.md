# CH06.04 — Cours théorique : IK/FK

## 1. FK et IK
**FK** (Forward Kinematics) : on tourne chaque os, les enfants suivent. **IK** (Inverse Kinematics) : on place le bout de la chaîne (la main) et le solveur calcule les rotations de la chaîne (épaule, coude). IK : contacts (main sur une table, pied au sol) ; FK : mouvements en arc (balancer le bras).

## 2. La contrainte IK
`pose.bones['fore'].constraints.new('IK')` : `target` (objet armature), `subtarget` (nom du bone cible : ik_hand), `pole_target`/`pole_subtarget` (ik_pole), `pole_angle`, `chain_count` (2 : fore et upper), `use_tail`, `use_stretch`. Côté bone : `ik_stretch` (0 = jamais d'étirement).
- **Cible** : l'extrémité de la chaîne vise la tête du bone cible.
- **Pôle** : un second contrôleur qui oriente le plan de la chaîne ; le **Pole Angle** compense l'orientation des os (ici 90°, trouvé par calibrage : le coude monte quand le pôle monte, descend quand il descend).
- **Chain Length** : nombre d'os affectés.

## 3. Pièges de l'IK
- **Singularité** d'une chaîne droite : le solveur ne sait pas de quel côté plier ; on **pré-fléchit** (ici fore pointe de 10° vers le bas : le coude est « vers le haut »).
- **Étirement** : ik_stretch > 0 allonge les os hors de portée.
- **Pole Angle** à calibrer par essais.
- **Chaîne trop courte** (chain_count 1) : upper ne participe pas, le bout n'atteint pas la cible.

## 4. L'interrupteur
Propriété personnalisée `ik_fk` sur le bone `switch` (`pose.bones["switch"]["ik_fk"]`, 1 = IK, 0 = FK) ; **driver** sur l'influence de l'IK (`driver_add('pose.bones["fore"].constraints["IK"].influence')`), type Averaged Value, une variable Single Property pointant `pose.bones["switch"]["ik_fk"]`. L'animateur peut animer ik_fk pour passer de l'un à l'autre.

## 5. Mesures de la solution
Cible (0,45 ; 0 ; 0,25) : bout à 0,0 mm ; longueurs 0,300/0,300 m ; coude à +26 cm au-dessus de la droite épaule–bout pôle en haut, et au-dessous pôle en bas ; cible (0,9 ; 0 ; 0) : bras tendu à 0,600 m, longueurs conservées ; FK : fore suit upper à 0,0 mm, bout à 67 cm de la cible.

## 6. Limites
Un bras de deux os dans le plan XZ ; pas de main, d'épaule ni de torsion. Le calibrage du Pole Angle dépend de l'orientation des bones : il se refait pour chaque chaîne. Le réglage fin d'un vrai rig est fait par Rigify (CH06.05).
