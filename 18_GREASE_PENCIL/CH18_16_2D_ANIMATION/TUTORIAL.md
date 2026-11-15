# CH18.16 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_16_bounce_starter.blend` (Num 0 : vue caméra). Disposition conseillée :
vue 3D + **Dope Sheet** en mode *Grease Pencil* en bas.

## Tutoriel 1 — Préparer l'animation
1. `GP_Practice` sélectionné, mode **Draw**, calque `USER_Ball` actif.
2. *Viewport Overlays* (menu des superpositions) > cochez *Onion Skin*. Object Data Properties >
   *Onion Skinning* : 2 clés avant / 2 après (déjà réglé).
3. Matériau `MAT_GP_Ball` (trait + remplissage) ; pinceau en mode *Stroke Mode : Both* pour tracer
   contour et aplat en un geste (CH18.07).

## Tutoriel 2 — Les poses clés (exercice « keys »)
1. Image 1 : dessinez la balle **au sommet** sur le cercle guide (gauche).
2. Image 13 : Shift+I (*Insert Blank Keyframe*), dessinez la balle **écrasée** posée sur la ligne de sol.
3. Sommet du 2ᵉ rebond vers l'image 22 (≈ 60 % de la hauteur), contact suivant vers 32, sommet 39,
   contact 46, sommet 52, contact 57 (avancez régulièrement vers la droite, jusqu'à la zone d'arrivée).
4. Dope Sheet : sélectionnez les contacts, R > *Keyframe* ; les sommets, R > *Extreme*.
5. Lecture (Espace) : un « diaporama » de poses. Vérifiez : `-- --exercise keys`.

## Tutoriel 3 — Les intervalles (exercice « bounce »)
1. Fichier : enregistrez sous `…_bounce_v002.blend`.
2. Entre deux clés, ajoutez un dessin toutes les 2 images (Shift+I aux images 3, 5, 7…).
3. Espacement : près des sommets, dessins très proches ; près du sol, écartés (l'onion skin montre les
   voisins : vérifiez que les écarts grandissent en descendant).
4. Image juste avant et juste après chaque contact : balle **étirée** verticalement ; au sommet : ronde.
5. Dope Sheet : intervalles sélectionnés, R > *Breakdown*.
6. Après le dernier contact : gardez la balle au sol jusqu'à 64 (maintien).

## Tutoriel 4 — Contrôler
- *View > Render Playblast* (vue 3D) pour une lecture en temps réel fidèle.
- Correcteur :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_16_bounce_<prenom>_v002.blend" `
  --python "SCRIPTS\validate_ch18_16.py" --python-exit-code 1 -- --exercise bounce --render
```
- Référence : `COMPLETED_EXAMPLES/ch18_16_bounce_reference.png` (toutes les images superposées).
