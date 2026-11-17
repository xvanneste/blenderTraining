# CH09.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_05_volumetrics_starter.blend`. Sauvegardez sous `ch09_05_volumetrics_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Trouver le brouillard (5 min)
Sélectionnez Fog ; Material Properties : le Principled Volume est relié à Volume.

## Tutoriel 2 — La densité (10 min)
Density : 0,08. Rendu (F12) : un cône de lumière apparaît.

## Tutoriel 3 — Comparer (10 min)
Essayez 0,004 puis 1,5 : trop mince, trop dense.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : luminance du faisceau et contraste.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_05_volumetrics_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_05.py" -- --exercise volumetrics --debug
```

Remarque d'honnêteté : les rendus du correcteur sont faits avec Cycles CPU (64 échantillons) : le volume est bruité, la mesure moyenne le bruit ; les bords valent presque 0 dans la solution, le rapport de contraste est donc très grand et peu informatif (la fenêtre de luminance du centre est le vrai contrôle) ; EEVEE n'a pas été testé ; les libellés (Principled Volume, Density, Anisotropy) viennent de l'API ; les trois rendus de contrôle (numpy, éclaircis ×4) ont été regardés.

## Variante de contrôle

Faites une version de brouillard très faible et une autre deux fois plus dense, avec même volume et éclairage. Comparez la silhouette, le fond et le temps de rendu. **Preuve** Le seuil de visibilité du premier plan fixe votre choix plutôt que le seul nombre du curseur.
