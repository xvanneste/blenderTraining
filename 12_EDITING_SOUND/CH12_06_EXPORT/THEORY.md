# CH12.06 — Cours théorique : Export et livraison

## 1. Conteneur et codecs
Conteneur : MP4 (MPEG-4). Codec vidéo : H.264 (`avc1`). Codec audio : AAC (`mp4a`).

## 2. Les réglages Blender 5.3
Média Vidéo (`image_settings.media_type = 'VIDEO'`), File Format FFmpeg Video ; `render.ffmpeg` : `format` ('MPEG4'), `codec` ('H264'), `audio_codec` ('AAC'), `constant_rate_factor`, `audio_bitrate`.

## 3. Résolution, cadence, plage
640 × 360 à 100 %, 24 i/s, images 1–48 : 2 s.

## 4. Le nom du fichier
Blender ajoute la plage au nom : `web_0001-0048.mp4`.

## 5. Vérifier
Parcours des boîtes : `ftyp` (marque), `mvhd` (durée), `trak` > `hdlr` (type de piste), `stsd` (codec, dimensions).

## 6. L'exercice
Réglages de sortie ; le correcteur rend et analyse.

## 7. Pièges
- Rendre en PNG sans le savoir.
- Audio oublié.
- Résolution à 50 % héritée.
- Plage de la scène trop courte.

## 8. Outils complémentaires
DaVinci Resolve (étalonnage et finition), Audacity/Reaper (son), FFmpeg (conversions), OpenTimelineIO (échange de montages) : cités par le programme, non testés ici.
