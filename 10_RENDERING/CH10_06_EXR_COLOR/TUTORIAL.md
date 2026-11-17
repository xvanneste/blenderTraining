# CH10.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_06_exr_starter.blend`. Sauvegardez sous `ch10_06_exr_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Mesurer le départ (5 min)
Lancez le correcteur : 16 bits et DWAA déforment 1000,7 en 1001,5.

## Tutoriel 2 — Le type de média (10 min)
Dans *Output Properties → Output*, choisissez **Multi-Layer EXR** comme type de média. Réglez la profondeur et la compression après ce choix, car le changement de type réinitialise ces réglages.

## Tutoriel 3 — Profondeur et codec (10 min)
Color Depth : 32 (Float) ; codec : ZIP. Si vous changez le type de média après, revérifiez-les.

## Tutoriel 4 — La passe Z et la mesure (10 min)
View Layer Properties > Passes > Data > Z ; lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_06_exr_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_06.py" -- --exercise exr --debug
```

Remarque d'honnêteté : les valeurs (32 bits ZIP/PIZ 1000,700 ; PXR24 1000,703 ; 16 bits 1000,5 ; DWAA 1001,5) sont mesurées en écrivant et relisant des EXR avec Blender 5.3 ; le type de média s'écrit `image_settings.media_type` (`MULTI_LAYER_IMAGE`) : le libellé exact dans le panneau Output n'a pas été regardé dans l'interface 5.3 ; changer de type de média remet la profondeur et le codec par défaut (constaté) ; l'espace colorimétrique de l'EXR n'est pas évalué (aucune différence détectée en relisant les pixels) ; les codecs B44/B44A n'existent pas dans la liste 5.3 ; les canaux de profondeur ne sont pas relus en valeur.

## Variante de contrôle

Enregistrez un EXR de travail et un PNG de revue puis rouvrez les deux. Comparez une zone de hautes lumières sous des réglages identifiés. **Preuve** Vous distinguez le signal exploité en compositing de la présentation choisie pour la revue.
