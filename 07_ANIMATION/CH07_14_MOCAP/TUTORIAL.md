# CH07.14 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_14_mocap_starter.blend` (BVH déjà importé ; `ch07_14_mocap_noisy.bvh` est dans le même dossier : File > Import > Motion Capture (.bvh) pour refaire l'import). Sauvegardez sous `ch07_14_mocap_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Diagnostiquer (15 min)
Graph Editor : sélectionnez RIG_Mocap (Pose Mode, tous les bones) : courbe Spine, Z Euler Rotation : bruit visible et trois pics (images 21, 48, 72).

## Tutoriel 2 — Les glitches (15 min)
Supprimez les trois pics (sélectionner les clés aberrantes, X) sur chaque courbe concernée (Spine, Head, Arm_L : rotation Z ; Hips : position Y à l'image 48).

## Tutoriel 3 — Lisser (15 min)
Toutes les courbes sélectionnées : Key > Smooth > Smooth (Gaussian) (réglez le facteur jusqu'à ce que le bruit disparaisse sans écraser le mouvement).

## Tutoriel 4 — Décimer (15 min)
Key > Density > Decimate (Allowed Change) (tolérance de l'ordre de 3 % de l'amplitude), puis Key > Density > Clean Keyframes : au plus 38 clés par courbe.

## Tutoriel 5 — Interpolation (5 min)
T > Bezier sur toutes les clés restantes. N'éditez jamais l'action « MOCAP_RAW ».

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_14_mocap_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_14.py" -- --exercise mocap --debug
```

Remarque d'honnêteté : le BVH est un fichier synthétique généré par script (un squelette de quatre joints, pas une vraie capture) ; la solution est calculée par script (médiane, gaussien, Ramer-Douglas-Peucker) et non par les opérateurs du Graph Editor, qui nécessitent une zone d'interface ; les libellés Key > Smooth > Smooth (Gaussian), Key > Density > Decimate (Allowed Change) et Clean Keyframes sont lus dans les sources de l'interface 5.3 (`space_graph.py`), mais les réglages à choisir (facteur de lissage, tolérance) sont à ajuster à l'œil et au correcteur ; le résultat d'un nettoyage manuel n'a pas été fabriqué. Le contre-exemple « raw_modified » échoue aussi sur les mesures, la référence étant altérée. La courbe de la solution (numpy) a été regardée : points gris dispersés, courbe orange lisse, clés blanches espacées.

## Variante de contrôle

Avant de transférer les clés, identifiez cadence, échelle et orientation de repos. Travaillez sur une courte section avec un appui. Repérez un saut et comparez les courbes avant et après nettoyage. **Preuve** Le rapport d’import décrit la source et la correction, puis distingue la réouverture Blender de la compatibilité d’une application tierce.
