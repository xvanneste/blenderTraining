# CH10.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_03_denoising_starter.blend`. Sauvegardez sous `ch10_03_denoising_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
F12 : le damier est piqué de grain.

## Tutoriel 2 — Activer (5 min)
Properties > Render > Sampling > Render > Denoise : cochez la case de l'en-tête ; Denoiser OpenImageDenoise ; Passes Albedo and Normal ; Prefilter Accurate.

## Tutoriel 3 — Comparer (10 min)
Rendez avec et sans la case ; comparez le damier.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : EQM, contraste.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_03_denoising_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_03.py" -- --exercise denoising --debug
```

Remarque d'honnêteté : le panneau Denoise (Denoiser, Passes, Prefilter, Quality) a été relu dans `addons_core/cycles/ui.py`, pas regardé dans l'interface 5.3 ; les valeurs sont mesurées sur cette scène à 160 × 90 avec OpenImageDenoise sur CPU et la graine 0 ; OptiX n'est pas testé (énumération dynamique vide en arrière-plan) ; j'ai mesuré que le préfiltre None n'apporte presque rien mais aussi que la passe RGB seule fait aussi bien qu'Albedo+Normal sur ce damier (0,055 contre 0,056) : le correcteur n'exige donc pas les passes, seulement un préfiltre actif ; le débruitage d'animations n'est pas traité.

## Variante de contrôle

Gardez le nombre d’échantillons fixe dans la première comparaison et activez le débruitage au rendu. Comparez une texture fine à une ombre bruitée. Le débruitage de la vue 3D est un réglage distinct. **Preuve** Deux recadrages montrent où le filtre aide et où il retire un détail utile.
