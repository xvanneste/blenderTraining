# CH06.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_02_constraints_starter.blend` : `RIG_Gaze` (bones head, eye.L, eye.R) et la cible `EMP_Target` (sphère en (0 ; −2 ; 1,74)), sans contraintes. Sauvegardez sous `ch06_02_constraints_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les yeux (20 min)
Sélectionnez l'armature, passez en **Pose Mode**, sélectionnez eye.L ; onglet **Bone Constraints** > Add Bone Constraint > **Damped Track** : Target EMP_Target, Track Axis **Y**. Même chose pour eye.R. Déplacez la cible : les yeux la suivent, même quand la tête est tournée.

## Tutoriel 2 — La tête (25 min)
Sur `head` : Damped Track → EMP_Target, Track Axis Y, **Influence 0,5**. Déplacez la cible : la tête tourne de moitié, les yeux terminent le mouvement.

## Tutoriel 3 — La limite (20 min)
Sur `head`, SOUS le Damped Track : **Limit Rotation**, cochez Limit Z, Min −35°, Max 35°, Owner Space **Local**. Éloignez la cible de côté : la tête plafonne ; les yeux continuent de viser.

## Tutoriel 4 — L'ordre (10 min)
Comparez à cible identique avec la limite au-dessus du suivi puis en dessous. Lorsque la limite vient en premier, le suivi peut réorienter ensuite la tête. Gardez la limite en dernier pour rendre le plafond de rotation visible.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_02_constraints_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_02.py" -- --exercise constraints --debug
```
Le correcteur déplace la cible lui-même.

Remarque d'honnêteté : la solution est générée par script ; le comportement est mesuré (trois positions de la cible) et résumé par un croquis vue de dessus. Un défaut de construction a été trouvé grâce au correcteur : le studio avait déjà un objet nommé EMP_Target et ma cible s'appelait EMP_Target.001, de sorte que les contraintes ne visaient pas l'objet attendu. Les noms des onglets et boutons (Bone Constraints, Add Bone Constraint) n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Faites déplacer la cible du regard en trois emplacements sans retoucher les autres contrôleurs. Comparez l’effet d’une contrainte active et de son influence nulle. **Preuve** Le résultat permet d’isoler l’orientation réglée par le rig de l’orientation de repos.
