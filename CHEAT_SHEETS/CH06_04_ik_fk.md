# Fiche de révision — CH06.04 IK/FK

IK : Target + Pole Target + Chain Length 2 ; Pole Angle calibré ; ik_stretch 0 ; pré-flexion (une chaîne droite est une singularité). Interrupteur : propriété ik_fk sur un bone, driver sur l'influence de l'IK (pose.bones["switch"]["ik_fk"]).
Tester : cible atteinte, longueurs conservées, coude vers le pôle, hors de portée = bras tendu, FK à 0. Correcteur : `--exercise ikfk [--debug]`.
