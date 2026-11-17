# CH12.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_05_titles_starter.blend`. Sauvegardez sous `ch12_05_titles_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le titre (10 min)
Strip TITLE : texte « LE LONG VOYAGE », taille 56, location (0,5 ; 0,5), images 1–36.

## Tutoriel 2 — Les sous-titres (15 min)
SUB1 : « Bonjour. » images 49–84 ; SUB2 : « Il fait nuit. » images 91–120 ; location (0,5 ; 0,1), taille 30.

## Tutoriel 3 — L'export (5 min)
Dans l’éditeur Sequencer, choisissez *View → Export Subtitles*. Ouvrez le SRT dans un éditeur de texte et comparez-le à `SUBTITLES.srt`. L’export de l’exercice inclut aussi le strip du titre. Pour une piste de sous-titres destinée à la livraison, retirez l’entrée du titre si elle est redondante, puis renumérotez les entrées et contrôlez leurs timecodes.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : titre, SRT, position.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_05_titles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_05.py" -- --exercise titles --debug
```

Remarque d'honnêteté : l'API des strips TEXT (`text`, `font_size`, `location`, `anchor_x`, `anchor_y`, `color`) et l'opérateur d'export `sequencer.export_subtitles` ont été vérifiés par exécution : il faut que la fenêtre soit un éditeur Sequencer, avec `scene` et `sequencer_scene` dans le contexte et des strips sélectionnés ; il exporte tous les strips de texte, y compris le titre, quelle que soit la sélection ; je n'ai trouvé AUCUN opérateur d'import SRT dans la liste des opérateurs du séquenceur 5.3 ; les libellés du menu (Add > Text, Export Subtitles) et le panneau de propriétés du texte n'ont pas été regardés dans l'interface ; la police est la police par défaut, avec retour à la ligne automatique sur les titres larges.

## Variante de contrôle

Faites relire le sous-titre à vitesse réelle. Comparez ses bornes, le moment de la parole et la lisibilité du texte sur un fond similaire à la séquence. **Preuve** Les sous-titres restent lisibles sans occuper le point focal et le SRT relu correspond au montage.
