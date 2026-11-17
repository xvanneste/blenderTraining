# CH07.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_10_acting_starter.blend`. Sauvegardez sous `ch07_10_acting_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le plan (15 min)
Plage 1–72 à 24 i/s. Notez les beats : 1–19 idle ; 20–27 remarque ; 27–45 réflexion ; 44–58 préparation et action.

## Tutoriel 2 — La remarque (30 min)
Pose Mode : image 19 : clé de rotation de tous les bones (pose neutre). Image 27 : tête tournée de 55° autour de Z (R puis Z puis 55), clé de rotation de la tête.

## Tutoriel 3 — Le corps suit (30 min)
Image 24 : clé de rotation neutre pour le buste (chest) ; image 38 : buste tourné de 30° (en tenant compte de la rotation du parent). Hanches : image 28 neutre, image 44 à 15°.

## Tutoriel 4 — Le maintien (10 min)
Entre les images 27 et 45, ne touchez pas à la tête : la valeur est identique à l'image 45.

## Tutoriel 5 — L'anticipation (30 min)
Colonne (spine) : image 44 : 0° ; image 50 : −8° autour de X (recul) ; image 58 : +14° (avance) ; image 72 : +6°.

## Tutoriel 6 — Régler (15 min)
Ouvrez le Graph Editor : arrondissez les courbes (Auto Clamped) ; vérifiez au correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_10_acting_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_10.py" -- --exercise acting --debug
```

Remarque d'honnêteté : la solution est calculée par script (rotations monde, une clé par image) ; les gestes de l'interface (R puis Z puis valeur, rotation avec le parent) n'ont pas été rejoués dans l'interface 5.3 ; en production, les rotations se saisissent dans le repère local du bone. Les courbes de la scène (numpy) ont été regardées : montée rapide de la tête, montée plus lente du buste et des hanches, creux puis pic de la colonne.

## Variante de contrôle

Écoutez ou regardez le plan sans annoncer l’intention. Demandez quel geste marque la décision. Corrigez une pose ou un regard avant de retoucher le rythme général. **Preuve** Le point de bascule a une image et une raison, puis une seconde lecture permet de mesurer la différence.
