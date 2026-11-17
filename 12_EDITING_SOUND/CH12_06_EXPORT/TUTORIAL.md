# CH12.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_06_export_starter.blend` (le dossier `ASSETS/ch12_06_audio/` doit rester accessible). Sauvegardez sous `ch12_06_export_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Output Properties : PNG, 50 %, 30 i/s, plage 1–24.

## Tutoriel 2 — Format (10 min)
Dans *Output Properties → Output*, choisissez **Video** comme type de média. Blender active la sortie FFmpeg. Dans *Encoding*, choisissez MPEG-4, H.264 et AAC. À 24 i/s, la plage inclusive de 1 à 48 correspond à 2 s de vidéo. Vérifiez l’image et le son dans le fichier produit.

## Tutoriel 3 — Cadre (10 min)
640 × 360 à 100 % ; Frame Rate 24 ; Frame End 48.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : il produit le fichier et lit ses boîtes.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_06_export_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_06.py" -- --exercise export --debug
```

Remarque d'honnêteté : l'export FFmpeg intégré à Blender (média Vidéo, conteneur MPEG-4, H.264, AAC) a été exécuté ici ; l'analyseur `mp4probe.py` est un petit lecteur de boîtes ISO écrit pour ce chapitre (aucun ffprobe sur la machine) : il a été validé sur les fichiers produits par ce Blender 5.3 (isom, avc1, mp4v, mp4a), pas sur d'autres sources ; la durée (2,006 s) est celle de `mvhd` ; les panneaux Output > Encoding n'ont pas été regardés dans l'interface ; DaVinci Resolve, Audacity, Reaper, FFmpeg en ligne de commande et OpenTimelineIO, cités dans le programme, n'ont été ni installés ni testés ; aucun contrôle de loudness (LUFS) ni de compatibilité de lecteurs.

## Variante de contrôle

Avant le rendu long, exportez un extrait couvrant une coupe et un événement sonore. Rouvrez-le et vérifiez durée, dimensions, piste audio et synchronisation. **Preuve** La copie de revue s’ouvre et la fiche indique les médias et réglages nécessaires pour reconstruire la livraison.
