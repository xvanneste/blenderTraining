# Projet de phase P12 — « Une séquence finalisée »

**Phase :** 12 — Montage, son et finition · **Durée estimée :** 25 à 40 h · **Évalue :** C12.01 → C12.06

## Brief
Vous recevez une séquence de six plans (des couleurs, à la place d'images de film) et des sons. Vous la **montez** (rythme qui accélère, échelles alternées, fondu enchaîné final), vous la **titrez** et la **sous-titrez**, vous **calez** le son sur l'image et vous le **mixez** (la musique s'efface sous la voix), puis vous la **livrez** en deux versions : une version web (640 × 360) et un master (1 280 × 720), en H.264 + AAC. Le contenu des plans est volontairement abstrait : c'est la méthode qui est évaluée.

## Livrables
1. `PROJECTS/p12_sequence/p12_scene_<prenom>_v0NN.blend` : la scène (strips des plans, Crossfade, TITLE, sous-titres, AMB, HIT, VOICE, MUSIC, marqueurs IMPACT et LINE).
2. `PROJECTS/p12_sequence/renders/p12_web.mp4` et `p12_master.mp4`.
3. `PORTFOLIO/p12/` : la fiche de livraison (conteneur, codecs, résolution, durée, poids des deux fichiers), la liste de synchronisation du son, 10 lignes sur les choix de rythme et de mixage.

## Contraintes techniques (vérifiées par `validate_p12.py`)
1. **Montage** : échelles de plan (suffixe du nom : wide, medium, close) jamais identiques à deux plans de suite ; durées des cinq premiers plans (par début) non croissantes ; SH6_wide (la résolution) dure au moins deux fois le cinquième plan ; Crossfade (type CROSS) du cinquième plan vers SH6, recouvrement de 8 à 16 images ; plage de la scène de l'image 1 à la dernière image du montage.
2. **Titres** : strip TITLE de texte non vide, centré (location 0,5 ; 0,5), taille ≥ 40, commençant à l'image 1 ; deux sous-titres en bas (y ≤ 0,2) : le SRT exporté (Sequencer > Export Subtitles) donne « Bonjour. » de 1,25 s à 2,25 s et « Il fait nuit. » de 3,50 s à 4,33 s à ± 2 images.
3. **Son** : HIT commence à IMPACT (image 55) ± 2 ; VOICE à LINE (image 85) ± 3 ; AMB couvre tout le montage ; aucun strip sonore muet.
4. **Mixage** (mixdown de chaque strip seul) : MUSIC (images 20–40) de 0,03 à 0,09 de RMS ; ducking : MUSIC pendant la réplique (85–104) / avant ≤ 0,5 ; VOICE ≥ 2 × MUSIC pendant la réplique ; mixage complet : RMS de 0,03 à 0,15, crête ≤ 0,9.
5. **Livraison** : `renders/p12_web.mp4` : H.264 (avc1) + AAC (mp4a), 640 × 360, poids ≤ 1,5 Mo ; `renders/p12_master.mp4` : H.264 + AAC, au moins 1 280 × 720 ; la durée de chaque fichier égale celle de la scène (± 0,15 s).

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p12_sequence\p12_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "12_EDITING_SOUND\PROJECT_P12\validate_p12.py" -- --debug
```
Le correcteur est testé par `python 12_EDITING_SOUND/PROJECT_P12/test_p12.py` : la référence est acceptée (90/90) ; dix variantes fausses sont refusées, chacune par le contrôle visé (faux raccord d'échelle, rythme qui ralentit, Crossfade absent, faute dans un sous-titre, coup en retard, voix muette, musique sans ducking, version web absente, master trop petit, version web sans audio).

## Référence
`REFERENCE/p12_scene_reference.blend` (+ `renders/p12_web.mp4`, `renders/p12_master.mp4`) produite par `build_p12_reference.py` en **assemblant** les chapitres : six plans de 30, 24, 18, 12, 12 et 28 images avec un Crossfade de 12 images (CH12.01, CH12.02), titre « LE LONG VOYAGE » et deux sous-titres (CH12.05), sons générés calés sur IMPACT (55) et LINE (85) (CH12.03), musique à 0,3 avec ducking à 0,1 (CH12.04), exports FFmpeg MPEG-4 / H.264 / AAC en 640 × 360 et 1 280 × 720 (CH12.06). Mesures : durée 4,67 s (112 images à 24 i/s) ; musique 0,041, ducking 0,28, voix 10,9 × la musique ; RMS 0,075, crête 0,45 ; fichiers de 0,13 Mo.
**Limites honnêtes** : les plans sont des aplats de couleur et les sons des signaux synthétiques : on ne juge ni le contenu ni la qualité sonore ; le contrôle des fichiers repose sur un analyseur MP4 minimal (`mp4probe.py`), pas sur ffprobe ; le loudness (LUFS), la compatibilité des lecteurs, les métadonnées et OpenTimelineIO ne sont pas évalués ; les menus Add > Text, Export Subtitles et Output > Encoding n'ont pas été regardés dans l'interface ; la musique s'arrête à 4,2 s (la séquence dure 4,67 s) : le correcteur ne mesure la musique que sur les images 20–40.
Ne copiez pas la référence : changez les durées, les textes et les sons, et justifiez votre rythme.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Rythme et lisibilité du montage | 20 | Faire décrire l'effet du rythme à un tiers |
| Qualité du titre et des sous-titres (lisibilité, durée à l'écran) | 15 | Lecture du master |
| Qualité du mixage (voix intelligible, ambiance, pas d'écrêtage) | 15 | Écoute au casque et sur haut-parleur |
| Livraison (deux fichiers conformes, fiche) | 10 | Fiche de livraison |
| Documentation (10 lignes, limites dites) | 10 | PORTFOLIO |
**Phase 12 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Montez en silence d'abord : le rythme doit fonctionner sans le son.
2. Calez les sons sur les marqueurs avant de mixer.
3. Mixez à faible volume : si la voix est claire ainsi, elle le sera partout.
4. Exportez la version web d'abord (rapide) pour vérifier le montage, le master à la fin.
5. Vérifiez les deux fichiers avec le correcteur avant de les remettre.
