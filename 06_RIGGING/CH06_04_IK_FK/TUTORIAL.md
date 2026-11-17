# CH06.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_04_ikfk_starter.blend` : `RIG_ArmIK` avec les bones upper, fore (pré-fléchi de 10°), ik_hand, ik_pole et switch (propriété ik_fk = 1), sans IK ni driver. Sauvegardez sous `ch06_04_ikfk_starter_<prenom>_v001.blend`.

## Tutoriel 1 — L'IK (20 min)
Pose Mode, sélectionnez fore ; Bone Constraints > **Inverse Kinematics** : Target RIG_ArmIK, Bone ik_hand ; Chain Length **2**. Déplacez ik_hand : le bras suit.

## Tutoriel 2 — Le pôle (25 min)
Pole Target RIG_ArmIK, Bone ik_pole ; essayez Pole Angle 0°, 90°, −90°, 180° : gardez celui où le coude monte avec le pôle (90° ici) et descend quand le pôle descend.

## Tutoriel 3 — Pas d'étirement (10 min)
Bone Properties de upper et fore > Inverse Kinematics : Stretch 0. Éloignez ik_hand : le bras se tend sans s'allonger.

## Tutoriel 4 — Le driver (30 min)
Clic droit sur l'Influence de la contrainte > Add Driver ; type Averaged Value ; variable Single Property : Prop = RIG_ArmIK, Path `pose.bones["switch"]["ik_fk"]`. Mettez ik_fk à 0 : le bras est en FK (tournez upper : fore suit). À 1, déplacez la cible IK et vérifiez que la main l’atteint. Les deux poses doivent être alignées avant de changer de mode si vous voulez éviter un saut pendant une animation.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_04_ikfk_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_04.py" -- --exercise ikfk --debug
```
Référence : `ch06_04_ikfk_reference.png` (quatre poses, vue de côté).

Remarque d'honnêteté : la solution est générée par script ; le Pole Angle (90°) a été trouvé par balayage automatique. Mon premier bras était parfaitement droit : le solveur le laissait droit (singularité) ; j'ai pré-fléchi le bras de 10° et c'est devenu un point de cours. Mon premier test du côté du coude regardait la coordonnée z du coude, ce qui est faux quand la cible est surélevée : il mesure maintenant la distance signée à la droite épaule–bout. Les noms de panneaux et l'ouverture du menu de driver n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Placez la cible de main à trois endroits et regardez le déplacement du coude lorsque seul le pôle change. Au raccord FK–IK, gardez une capture de chaque mode et comparez la position de la main. **Preuve** La pose utile est stable grâce au pôle et la différence de mode reste identifiable.
