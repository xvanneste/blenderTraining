# CH18.18 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_18_shot_starter.blend` ; lisez le texte `SCENARIO` (Text Editor).

## Tutoriel 1 — Les poses du personnage (USER_Char)
1. Mode Draw, calque `USER_Char`. Image 1 : buste, attente (visage neutre).
2. Poses clés (Shift+I à chaque image) : 24 clignement → 26 neutre ; 36 regard vers l'ampoule ;
   44 yeux plissés (anticipation) ; 49 sursaut **écrasé** ; 51 **étiré** ; 53 surprise (tenue jusqu'à
   79) ; 81–89 retour ; 91 soulagement tenu jusqu'à la fin.
3. Lecture : chaque tenue doit être lisible, le sursaut doit « claquer ».

## Tutoriel 2 — L'effet (USER_FX)
1. Calque `USER_FX`, image 48 : éclair (étoile de traits autour de l'ampoule), 49 et 50 : plus grand.
2. Images 52 à 70 en deux : fumée — quelques cercles qui grossissent, montent et se séparent.
3. Image 72 : **Insert Blank Keyframe** (Shift+I) sans dessiner : la fumée disparaît.
4. (Conseillé) Calque `PROP_Bulb`, image 48 : clé vide — l'ampoule a éclaté.

## Tutoriel 3 — Le tremblement de caméra
1. Sélectionnez `CAM_Sheet` (Object Mode). Image 47 : survol de *Location* > I (position de repos).
2. Images 48, 49, 50, 52, 54, 56 : déplacez légèrement la caméra (X et Z, ±0,05 à ±0,2 m, sens
   alternés, amplitude décroissante), I à chaque fois.
3. Image 58 : remettez exactement la position de repos (0, −10, 0), I.
4. Graph Editor : les courbes doivent osciller puis s'éteindre.

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_18_shot_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_18.py" -- --exercise shot --render
```
Référence : `COMPLETED_EXAMPLES/ch18_18_shot_contact.png` (images 10, 38, 44, 48, 50, 58, 66, 100).

## Variante de contrôle

Isolez l’acting puis l’effet. Retardez l’effet de deux images et contrôlez le regard du spectateur avec la version originale. **Preuve** Le personnage reste compréhensible et l’effet renforce le moment prévu plutôt que de le couvrir.
