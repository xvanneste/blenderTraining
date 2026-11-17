# CH10.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_01_eevee_starter.blend`. Sauvegardez sous `ch10_01_eevee_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
F12 : la boule n'a pas d'ombre, la sphère chromée est plate.

## Tutoriel 2 — Les ombres (5 min)
Properties > Render > Sampling > Shadows : cochez la case de l'en-tête.

## Tutoriel 3 — Le ray tracing (5 min)
Properties > Render > Raytracing : cochez la case de l'en-tête ; Sampling > Render > Samples : 64.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_01_eevee_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_01.py" -- --exercise eevee --debug
```

Remarque d'honnêteté : les panneaux Raytracing, Fast GI Approximation, Sampling > Shadows et Sampling > Render > Samples ont été relus dans `bl_ui/properties_render.py` mais pas regardés dans l'interface 5.3 ; les valeurs (ombres 0,96 → 0,70 ; sphère chromée 0,008 → 0,081 ; 1 échantillon avec ray tracing 0,022) sont mesurées sur cette scène en EEVEE sur la machine de développement (le résultat d'EEVEE dépend du GPU) ; l'effet de Fast GI n'a pas pu être mesuré (activé ou non, aucune zone testée ne change) et n'est pas évalué ; le rendu est un contrôle, pas un rendu artistique.

## Variante de contrôle

Isolez une seule amélioration d’ombre dans EEVEE. Comparez deux rendus au même cadre et notez votre version du moteur. **Preuve** Le défaut est visible sur un bord ou un contact précis, et le profil indique quand le coût supplémentaire devient utile.
