# CH18.15 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_15_edit_starter.blend`, espace de travail **Video Editing** (onglet en haut ;
sinon ajoutez-le par le « + » des onglets > Video Editing > Video Editing). Les 12 plans sont sur le
canal 2, les marqueurs portent leurs codes.

## Tutoriel 1 — La musique et ses fondus
1. Image 1 (Shift+←). *Add > Sound…* : `ASSETS/ch18_15_audio/music_bed.wav` (canal libre, ex. 5).
2. Strip sélectionné : *Add > Fade > Fade In and Out*. Blender anime *Volume* au début et à la fin.
3. Sidebar (N) > *Strip* > *Sound* : *Volume* ; baissez la nappe si elle couvre les bruitages.

## Tutoriel 2 — Caler les bruitages et la réplique
1. Sautez au marqueur SQ020_SH0050 (*Marker > Jump to Next Marker*).
2. *Add > Sound…* `sfx_whoosh.wav` : le son se pose à la tête de lecture (image 152).
3. Même méthode : `sfx_catch.wav` sur SQ020_SH0080 (205), `temp_dialogue_oh.wav` sur SQ020_SH0040 (133).
4. Pour déplacer finement : G puis saisie au clavier du décalage en images, ou *Sidebar > Strip > Time*.
5. Écoutez (Espace) : la forme d'onde s'affiche dans le strip ; ajustez à l'oreille sans dépasser ±2 images.

## Tutoriel 3 — Le fondu enchaîné
1. Sélectionnez SQ020_SH0120, montez-le sur le canal 3 (G, Y pour rester sur l'axe vertical ou glisser).
2. Allongez son début de 12 images vers la gauche (poignée gauche du strip) : il commence à 349 et
   finit toujours à 456 ; il chevauche SH0110 de 12 images.
3. Sélectionnez SH0110 **puis** SH0120 (Shift+clic) : *Add > Transition > Crossfade*.

## Tutoriel 4 — Le fondu au noir
SQ020_SH0120 seul sélectionné : *Add > Fade > Fade Out* (anime l'opacité de la fin du strip).

## Tutoriel 5 — L'export
1. Output Properties > *Output* : chemin `//export/SQ020_animatic_v001_` ; *Media Type* : *Video*.
2. *Encoding* : *Container* MPEG-4, *Video Codec* H.264 ; *Audio* : *Audio Codec* AAC.
3. *Metadata* : décochez tout sauf *Strip Name* et *Frame* ; *Burn Into Image* coché.
4. *Render > Render Animation* (Ctrl+F12). Ouvrez la vidéo dans votre lecteur : image, son, incrustation.

## Tutoriel 6 — Les notes de révision
Regardez la vidéo une fois sans vous arrêter, puis une seconde fois en notant dans le texte
`REVIEW_NOTES` (Text Editor) : `SQ020_SH0050 · 0155 · chute illisible : essayer 16 images`.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_15_edit_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_15.py" --python-exit-code 1 -- --exercise edit --render
```
`--render` exporte réellement une vidéo de contrôle (dossier temporaire) et vérifie qu'elle contient
456 images et une piste son audible.
