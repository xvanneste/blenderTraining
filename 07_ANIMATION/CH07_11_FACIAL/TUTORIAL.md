# CH07.11 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_11_lipsync_starter.blend` (visage et texte PHONEMES dans l'éditeur de texte). Sauvegardez sous `ch07_11_lipsync_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lire la piste (10 min)
Éditeur de texte : PHONEMES : 1 M, 7 A, 13 O, 19 E, 25 M, 31 A, 37 E, 43 M. Plage 1–48 à 24 i/s.

## Tutoriel 2 — Les visèmes (30 min)
Pose Mode : à chaque phonème f, posez la bouche aux images f − 1 et f : jaw (rotation X) : M 0°, A −12°, O −7°, E −4° ; ctl_smile (X) : E 0,04 m, sinon 0. Insérez les clés (I) des trois canaux à chaque image.

## Tutoriel 3 — L'interpolation (10 min)
Dope Sheet : toutes les clés : T > Bezier (jamais Constant).

## Tutoriel 4 — Le clignement (15 min)
ctl_blink (X) : image 19 : 0 ; image 21 : 0,05 ; image 23 : 0.

## Tutoriel 5 — Vérifier (15 min)
Lancez le correcteur : visèmes, continuité, clignement ; regardez la mâchoire et le sourire dans le Graph Editor.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_11_lipsync_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_11.py" -- --exercise lipsync --debug
```

Remarque d'honnêteté : la solution est générée par script (`keyframe_insert` des contrôles) à partir du rig de CH06.09 ; la piste de phonèmes est un texte synthétique (pas de fichier audio) et le correcteur contrôle les poses, pas la perception de la synchronisation. Les gestes de l'interface (I, T > Bezier) n'ont pas été rejoués dans l'interface 5.3. Les courbes (numpy) ont été regardées : trois creux de mâchoire, deux bosses de sourire, un clignement.

## Variante de contrôle

Posez un repère sur une fermeture de bouche et comparez la lecture à demi-vitesse et à cadence normale. Ajustez un visème sur une copie. **Preuve** L’instant de fermeture reste cohérent avec le son et l’expression reste lisible entre les événements.
