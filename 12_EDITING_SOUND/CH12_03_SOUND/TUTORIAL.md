# CH12.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_03_sound_starter.blend` (le dossier `ASSETS/ch12_03_audio/` doit rester accessible). Sauvegardez sous `ch12_03_sound_starter_<prenom>_v001.blend` dans STARTER_FILES.

## Tutoriel 1 — Voir (5 min)
Espace Video Editing : trois strips sonores et deux marqueurs : IMPACT (49), LINE (61).

## Tutoriel 2 — Caler (15 min)
Déplacez HIT pour que son début soit sur IMPACT ; VOICE sur LINE.

## Tutoriel 3 — L'ambiance (10 min)
Déplacez AMB pour commencer à l'image 1 ; vérifiez qu'elle couvre 1–96.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : positions, mixage, crête.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_03_sound_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_03.py" -- --exercise sound --debug
```

Remarque d'honnêteté : les sons sont générés par ce script (ambiance de bruit filtré, coup sinusoïdal à décroissance, tons modulés) : ils ne ressemblent pas à de vrais sons ; l'opérateur `sound.mixdown` (WAV, PCM) fonctionne en arrière-plan sur cette machine ; l'API `strips.new_sound(name, filepath, channel, frame_start)` a été vérifiée par exécution ; les chemins des sons sont relatifs (`//../ASSETS/ch12_03_audio/…`) : ne déplacez pas le dossier ; le menu Add > Sound, la boîte de propriétés Sound d'un strip et le menu de mixage n'ont pas été regardés dans l'interface ; la réplique est un signal synthétique, à remplacer par votre propre voix ; les seuils sont calibrés sur ces sons.

## Variante de contrôle

Calez un bruit d’impact sur une image repère, puis décalez-le de deux images dans une copie. Écoutez puis regardez les différentes versions à vitesse nominale. **Preuve** Le marqueur et le départ sonore justifient le montage retenu.
