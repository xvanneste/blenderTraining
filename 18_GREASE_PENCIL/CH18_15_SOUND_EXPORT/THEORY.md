# CH18.15 — Cours théorique : son, rythme, transitions, export, révision

## 1. Le son fait la moitié de l'animatique
Une animatique muette se juge mal : le son **donne le tempo**, raccorde les plans et rend l'action
lisible. Trois couches, posées dans cet ordre :
1. **Dialogues temporaires** (*scratch*) : voix enregistrées vite (souvent par l'équipe) ; elles fixent
   la durée des plans parlés. Ici, une « réplique temporaire » synthétique (`temp_dialogue_oh.wav`)
   tient la place — remplacez-la par votre propre voix (micro, téléphone) : c'est l'usage réel.
2. **Bruitages clés** (*sfx*) : uniquement ceux qui portent l'action (chute, rattrapage).
3. **Musique temporaire** : une nappe qui donne l'émotion ; elle entre et sort en **fondu**.

## 2. La synchronisation
Un son est **synchrone** quand il démarre à l'image de l'événement. À 24 i/s, un décalage de 2 images
(83 ms) se remarque sur un impact ; ±1 image est la tolérance pratique. Les **marqueurs** des plans
servent de repères : on cale le son sur le marqueur, puis on ajuste à l'oreille et à l'image (le son
d'un impact peut précéder la coupe d'une ou deux images : *J-cut* / *L-cut* en montage).

## 3. Le rythme au montage
Dans l'animatique, on teste les durées : on rallonge une réaction, on raccourcit une chute illisible.
Le son révèle souvent qu'un plan est trop court (la réplique ne tient pas) ou trop long (silence vide).
Toute modification est notée (code, image, remarque) et reportée dans la liste de plans.

## 4. Les transitions
- **Coupe franche** : la règle (95 % des raccords).
- **Fondu enchaîné** (*Crossfade*) : passage du temps, changement de lieu, douceur — à justifier.
  Dans le Video Sequencer, il demande que les deux plans **se chevauchent** (sur deux canaux) ; la durée
  du fondu = durée du chevauchement.
- **Fondu au noir** (*Fade Out*) : fin de séquence ou de film ; **ouverture au noir** (*Fade In*) au début.
- **Volet** (*Wipe*) : effet de style, rare.

## 5. L'export
Format de travail courant : conteneur **MPEG-4**, vidéo **H.264**, son **AAC** — lisible partout,
léger. Dans Blender 5.3 : Output Properties > *Output* > *Media Type* : *Video* (File Format *FFmpeg
Video*) ; *Encoding* : *Container* MPEG-4, *Video Codec* H.264 ; *Audio* : *Audio Codec* AAC. Sans codec
audio, la vidéo est **muette** même si le montage contient du son. Nom versionné :
`projet_SQ020_animatic_v001.mp4` ; on n'écrase jamais une version déjà envoyée.

## 6. La révision
Le réalisateur (ou vous, le lendemain) regarde l'animatique et note : **code du plan · image ·
remarque**. Une note sans image précise est inutilisable. Chaque série de notes produit une nouvelle
version (v002…). C'est la boucle de travail de toute la production (phase 15, projets CH18.22).
