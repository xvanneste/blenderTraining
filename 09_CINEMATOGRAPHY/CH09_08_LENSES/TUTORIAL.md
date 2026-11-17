# CH09.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_08_lenses_starter.blend`. Sauvegardez sous `ch09_08_lenses_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Vue caméra (Numpad 0) : le cylindre vert (fond) est environ deux fois plus petit que le rouge.

## Tutoriel 2 — Reculer (5 min)
CAM > Object Properties > Transform > Location Y : −24. Tout devient minuscule.

## Tutoriel 3 — Allonger la focale (5 min)
CAM > Object Data Properties (caméra) > Lens > Focal Length : 144 mm. Le sujet retrouve 40 % de la hauteur ; le fond a grandi.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : hauteur du sujet, compression, focale.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_08_lenses_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_08.py" -- --exercise lenses --debug
```

Remarque d'honnêteté : le rendu de contrôle est du Workbench plat segmenté par couleur ; les valeurs (rapport 0,46 au départ, 0,78 à la solution ; sujet 39 % puis 40 %) sont mesurées sur cette scène 160 × 90 et la quantification de 90 lignes explique l'écart avec la théorie (0,5 et 0,8) ; les libellés Lens > Focal Length et Sensor viennent de l'API (`Camera.lens`, `sensor_width`, `sensor_fit`), pas d'une relecture dans l'interface 5.3. Rendus de départ et de solution regardés.

## Variante de contrôle

Faites deux portraits avec une taille du sujet comparable. Pour y parvenir, changez la position et la focale ensemble, puis indiquez les deux valeurs. **Preuve** La relation du sujet au fond change et vous justifiez l’effet par un changement de position de la caméra.
