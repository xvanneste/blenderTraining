# CH06.02 — Cours théorique : contraintes

## 1. Principe
Une **contrainte** modifie la transformation de son propriétaire (objet ou bone) après la sienne. Une pile de contraintes s'évalue **de haut en bas** ; chacune a une **influence** (0–1). Contraintes de bone : en Pose Mode, `object.pose.bones[nom].constraints.new('TYPE')`.

## 2. Les contraintes du chapitre (types de l'API)
- **Damped Track** (`DAMPED_TRACK`) : oriente l'axe choisi (`track_axis`, ici `TRACK_Y` : la direction du bone) vers `target`. Rotation minimale : pas de torsion.
- **Track To** (`TRACK_TO`) : vise aussi, avec un axe « haut » (`up_axis`) imposé ; plus rigide.
- **Limit Rotation** (`LIMIT_ROTATION`) : borne les angles (`use_limit_z`, `min_z`, `max_z`) dans un espace (`owner_space = 'LOCAL'`).
Autres contraintes courantes (CH06.04+) : Copy Rotation/Location/Transforms, Child Of, IK, Stretch To, Limit Location/Scale…

## 3. Le rig de regard
Bone `head` orienté vers l'avant (−Y) ; `eye.L`, `eye.R` enfants de head ; cible `EMP_Target`.
- eye.L, eye.R : Damped Track → EMP_Target, Track Axis Y, Influence 1.
- head : (1) Damped Track → EMP_Target, Track Axis Y, **Influence 0,5** ; (2) Limit Rotation, Limit Z ± 35°, Local.
Les yeux, enfants de la tête, sont évalués avec la tête déjà tournée : leur Damped Track corrige le reste.

## 4. Mesures de la solution (cible déplacée)
| Cible | Angle cible | Rotation tête | Erreur des yeux |
|---|---|---|---|
| T1 (0 ; −2 ; 1,74) | 0° | 0° | 0° |
| T2 (1,5 ; −1,5 ; 1,74) | 45° | 22,5° | 0° |
| T3 (3 ; −0,2 ; 1,74) | 86,2° | 35,0° (plafonnée) | 0° |
Contre-exemple « ordre inversé » (limite avant le suivi) : T3 → 43,1°. « Sans limite » : 43,1°. « Tête à 100 % » : 35° dès T2 (limite atteinte à 45°).

## 5. Pièges
- Mauvais Track Axis : les yeux visent de côté (90° d'erreur devant).
- Pas de Target : contrainte invalide, aucun effet.
- Limite avant le suivi : sans effet.
- Contrainte sur le bone en Edit Mode : les contraintes de bone se posent en Pose Mode.
- Deux objets du même nom (le studio avait déjà un EMP_Target : la cible du rig devenait EMP_Target.001) : vérifier le nom de la cible.

## 6. Limites
Le correcteur teste ce rig (trois cibles, six contraintes) ; il n'évalue ni la souplesse, ni les transitions, ni le roulis. Le rig est un point de départ pour les yeux et la tête du rig facial (CH06.09).
