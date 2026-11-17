# CH12.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_04_mix_starter.blend` (le dossier `ASSETS/ch12_04_audio/` doit rester accessible). Sauvegardez sous `ch12_04_mix_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Niveaux (10 min)
MUSIC : volume 0,3 ; HIT : volume 0,8.

## Tutoriel 2 — Ducking (15 min)
Placez des clés sur le Volume de MUSIC : image 58 : 0,3 ; 61 : 0,1 ; 72 : 0,1 ; 76 : 0,3.

## Tutoriel 3 — Pan (5 min)
HIT : Pan −1.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : musique, ducking, voix, pan, niveau global.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_04_mix_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_04.py" -- --exercise mix --debug
```

Remarque d'honnêteté : les propriétés `Strip.volume` (animable : l'animation est prise en compte par le mixdown), `Strip.pan` (−1 : canal droit nul, mesuré), `mute` et l'opérateur `sound.mixdown` ont été vérifiés par exécution ; le correcteur mixe les strips un par un en les rendant muets temporairement (restaurés ensuite) ; la musique est un signal synthétique de trois sinusoïdes ; le RMS n'est pas une mesure de loudness (LUFS) ; le panneau Sound des propriétés du strip (Volume, Pan) n'a pas été regardé dans l'interface ; la mesure du ducking suppose que la musique de référence (images 20–40) soit comparable à celle de la réplique.

## Variante de contrôle

Écoutez d’abord la voix seule, puis avec la musique. Ajustez un passage de ducking et comparez intelligibilité, niveaux et crête. **Preuve** La musique revient après la phrase sans masquer le dernier mot et le mix ne sature pas.
