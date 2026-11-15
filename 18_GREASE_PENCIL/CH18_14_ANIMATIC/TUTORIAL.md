# CH18.14 — Tutoriels pas à pas

## Tutoriel 1 — Lire la liste de plans et calculer les images
1. Ouvrez `STARTER_FILES/ch18_14_animatic_starter.blend`.
2. Un éditeur **Text Editor** : choisissez le texte `SHOTLIST` (code;valeur;mouvement;durée en s).
3. Sur papier ou tableur, calculez pour chaque plan : images = durée × 24 (arrondi), image de début
   (1, puis cumul). Vérifiez : 12 plans, total **456** images.
4. Output Properties (icône imprimante) > *Format* : *Frame Rate* 24 ; *Frame Range* : *End* = 456.

## Tutoriel 2 — Une image clé par plan
1. Sélectionnez `GP_Animatic`, mode **Draw**, calque `USER_Panels` actif (panneau *Layers* dans
   Object Data Properties).
2. Placez la tête de lecture à l'image 1 et dessinez le plan 1 (Pencil, cadre gris = bord de l'image).
3. Allez à l'image de début du plan 2 (Ctrl+clic sur la timeline ou saisie du numéro) :
   *Draw > Animation > Insert Blank Keyframe (Active Layer)* (Shift+I) puis dessinez le plan 2.
   Variante : *Duplicate Active Keyframe (Active Layer)* pour partir du dessin précédent et le modifier.
4. Répétez jusqu'au plan 12. Dans la Dope Sheet (mode *Grease Pencil*), vous voyez une clé par plan.

## Tutoriel 3 — Les marqueurs
1. Dans la Timeline, à l'image de début de chaque plan : **M** (*Add Marker*).
2. **F2** sur le marqueur (*Rename Marker*) : `SQ020_SH0010`, `SQ020_SH0020`…
3. Navigation : *Marker > Jump to Next Marker* / *Jump to Previous Marker*.

## Tutoriel 4 — Le mouvement de caméra du dernier plan
1. Sélectionnez `CAM_Sheet`, Object Data Properties (caméra) : *Orthographic Scale*.
2. Image 361 (début du dernier plan) : valeur 10 (plus serré), survol du champ + **I**.
3. Image 456 : valeur 12, **I**. Lecture (Espace) : zoom arrière = « travelling arrière » de la planche.

## Tutoriel 5 — L'incrustation et la sortie
1. Output Properties > *Metadata* : décochez les champs inutiles (Date, Time, Render Time, File…),
   cochez *Marker* et *Frame* ; sous-panneau *Burn Into Image* : coché.
2. Contrôle rapide : *View > Render Playblast* dans la vue 3D (aperçu de l'animation).
3. Correcteur :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_14_animatic_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_14.py" --python-exit-code 1 -- --exercise animatic --render
```

## Tutoriel 6 — L'animatique 3D à caméras multiples
1. Ouvrez `STARTER_FILES/ch18_14_layout_starter.blend` (A rouge à gauche, B bleu à droite) ; lisez
   `SHOTLIST` (code;valeur;sujet;durée).
2. Pour chaque plan : *Add > Camera*, renommez `CAM_SH0010`… ; cadrez depuis la vue caméra
   (Num 0 après Ctrl+Num 0) en ajustant position et *Focal Length* pour obtenir la valeur demandée
   sur le sujet (repères de CH18.10). Restez côté **y < 0** (règle des 180°).
3. Marqueurs aux images de début (M, F2). Pour chacun : sélectionnez la caméra (vue 3D), puis le
   marqueur (Timeline), *Marker > Bind Camera to Markers* (Ctrl+B).
4. *End* = durée totale (324). Lecture : les caméras s'enchaînent.
5. Correcteur : `-- --exercise layout --render`. Référence : `COMPLETED_EXAMPLES/ch18_14_layout_contact.png`.
