# CH07.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_01_principles_starter.blend` : la balle saute. Sauvegardez sous `ch07_01_principles_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Regarder (10 min)
Lecture (Espace) : la balle monte et redescend sans se déformer. Vérifiez l'origine de la balle : elle est à sa base.

## Tutoriel 2 — Les clés de repos (10 min)
À l’image 1, réglez *Scale* sur (1, 1, 1) dans *N → Item*. Survolez ce champ et pressez `I` pour insérer la clé d’échelle. Répétez à l’image 40 et vérifiez les canaux d’échelle dans le Dope Sheet.

## Tutoriel 3 — L'anticipation (15 min)
Image 5 : Scale (1,18 ; 1,18 ; 0,72) + clé d'échelle. (1,18 = 1/√0,72.)

## Tutoriel 4 — L'étirement (20 min)
Image 8 : Scale (0,86 ; 0,86 ; 1,35) + clé. Image 13 : (0,89 ; 0,89 ; 1,25). Image 23 : (0,91 ; 0,91 ; 1,2). Image 18 (sommet) : (1, 1, 1).

## Tutoriel 5 — Le contact et le rebond (15 min)
Image 28 : (1,29 ; 1,29 ; 0,6) + clé. Image 32 : (0,95 ; 0,95 ; 1,1) + clé.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_01_principles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_01.py" -- --exercise principles --debug
```

Remarque d'honnêteté : la solution est générée par script avec `keyframe_insert` ; la touche I et le menu d'insertion cités n'ont pas été relus dans l'interface 5.3 (CH07.02 les détaille). Le croquis (silhouettes numpy) a été regardé : écrasée, étirée, neutre au sommet, écrasée au contact.

## Variante de contrôle

Sur un rebond, comparez la silhouette aux images de contact et en l’air. Changez la durée d’une anticipation en gardant l’arrivée. **Preuve** Le changement de rythme se voit sans modifier la position d’arrivée. Distinguez écrasement, étirement et timing.
