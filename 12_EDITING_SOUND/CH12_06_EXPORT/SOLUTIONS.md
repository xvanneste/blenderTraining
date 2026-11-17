# CH12.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un fichier qui range des pistes vidéo et audio (MP4, MKV…) | Ici MPEG-4 (.mp4), marque `isom`. |
| Q2 | **a** — Une piste vidéo H.264 | MPEG-4 Part 2 donne `mp4v` : refusé. |
| Q3 | **a** — Une piste audio AAC | Sans audio : aucune piste « soun ». |
| Q4 | — | Le master doit contenir le son : no_audio donne un fichier de 11,7 Ko sans piste audio. |
| Q5 | — | Output Properties > Output > Encoding > Audio Codec (propriété `ffmpeg.audio_codec`) : relu par l'API ; panneau non regardé. |
| Q6 | **a** — 48 images ÷ 30 i/s = 1,6 s | À 24 i/s : 2,0 s. |
| Q7 | **a** — Il parcourt les boîtes MP4 (ftyp, mvhd, trak/stsd) avec un analyseur | SCRIPTS/mp4probe.py : conteneur, codecs, largeur × hauteur, durée. |
| Q8 | — | DaVinci Resolve, Audacity/Reaper, FFmpeg en ligne de commande, OpenTimelineIO : aucun n'est installé ni testé ici ; seul l'export FFmpeg intégré à Blender est mesuré. |
| Q9 | — | Le loudness (LUFS), les métadonnées, la compatibilité réelle des lecteurs, le débit : le poids (≤ 400 Ko) n'en est qu'un indice. |
| Q10 | — | Il gère les fichiers produits par Blender 5.3 (boîtes simples) ; pas les MP4 fragmentés ni toutes les variantes ; la lecture de la durée suit le conteneur, pas le contenu. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_06_export_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_06_files.py`, `mp4probe.py`) : tonalité de 2 s, strips PICTURE/TONE, variantes de sortie ; mesures par rendu réel et lecture des boîtes MP4. Score 53/53 ; starter 3/17. Fiche regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_mpeg4_codec` | codec vidéo MPEG-4 (mp4v) | codec vidéo |
| `…_no_audio` | codec audio NONE | codec audio |
| `…_half_res` | résolution à 50 % : 320 × 180 | résolution |
| `…_fps30` | 30 i/s : durée 1,6 s | cadence ; durée |
| `…_short_range` | plage 1–24 : 1 s | durée |
Aussi refusé : le starter.

## Limites
- Analyseur MP4 minimal.
- Outils externes non testés.
- Pas de loudness.
