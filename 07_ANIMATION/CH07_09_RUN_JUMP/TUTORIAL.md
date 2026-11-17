# CH07.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_09_jump_starter.blend`. Sauvegardez sous `ch07_09_jump_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les hanches (30 min)
Pose Mode, bone `hips` : clés de déplacement VERTICAL (G puis Z dans la vue 3D : axe Z du monde ; le bone étant vertical, son axe Y local est l'axe vertical) : image 1 : 0 ; 4 : 0 ; 8 : −0,30 (flexion à 0,65 m) ; 10 : 0 ; 17 : +0,417 (sommet) ; 24 : 0 ; 28 : −0,27 ; 36 : 0 ; 40 : 0 (déplacements relatifs à la position de repos : hanches à 0,95 m).

## Tutoriel 2 — Les poignées (15 min)
Dans le Graph Editor, tracez une première arche de vol avec le sommet en *Auto Clamped* et des transitions franches au décollage et à la réception. Pour comparer à une trajectoire sous gravité constante, posez des clés supplémentaires sur le déplacement local vertical de `hips`. Aux images 12, 14 et 16, les déplacements depuis le repos sont respectivement 0,2044 m, 0,3406 m et 0,4088 m. Reportez les mêmes valeurs aux images 22, 20 et 18. Elles suivent `Δz = 0,5 × (9,81 / 24²) × (f − 10) × (24 − f)`.

## Tutoriel 3 — Les jambes (45 min)
Contrôlez les chevilles de profil. Elles sont à 0,05 m jusqu’à l’image 10 comprise, puis de nouveau à partir de 24. En vol, repliez les jambes progressivement jusqu’à l’image 12, puis dépliez-les entre 22 et 24. Pour isoler le travail de courbe, ouvrez une copie du corrigé avec les jambes réglées et comparez les hauteurs à celles de votre fichier.

## Tutoriel 4 — Les bras (15 min)
Balancement arrière à l'image 8, levée à l'image 10 à 17, retombée à 28.

## Tutoriel 5 — Régler (30 min)
Vérifiez au correcteur : flexion, vol de 10 à 18 images, hauteur de 0,30 à 0,55 m, gravité, réception, pieds plantés. Ajustez les clés.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_09_jump_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_09.py" -- --exercise jump --debug
```

Remarque d'honnêteté : la solution est calculée par script (hanches par morceaux lissés et parabole, IK analytique des jambes, une clé par image) ; le tutoriel décrit une version à clés espacées que le correcteur n'a pas validée telle quelle (la solution en 40 clés par bone l'est). Les gestes de l'interface (poignées Vector, saisie des rotations) n'ont pas été rejoués dans l'interface 5.3. La courbe de hauteur (numpy) a été regardée : creux, impulsion, arche, creux d'amortissement.

## Variante de contrôle

Isolez décollage, apex et réception. Comparez la trajectoire du bassin à la pose des pieds. Déplacez un événement d’un petit nombre d’images sans changer la hauteur maximale. **Preuve** Le moment d’impulsion et la réception restent lisibles dans le même cadre.
