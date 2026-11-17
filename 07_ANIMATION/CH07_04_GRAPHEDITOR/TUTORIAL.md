# CH07.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_04_graph_starter.blend`. Sauvegardez sous `ch07_04_graph_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les courbes (10 min)
Éditeur Graph Editor : repérez Y Euler Rotation (clés à 1, 13, 25) et Z Location (plate).

## Tutoriel 2 — Bezier et poignées (15 min)
Sélectionnez les clés de rotation, T > Bezier, puis V > Auto Clamped : la courbe s'arrondit aux extrémités.

## Tutoriel 3 — Cycles (10 min)
Courbe de rotation sélectionnée, barre latérale (N), onglet des modificateurs : ajoutez Cycles. Lisez l'animation sur 72 images : elle se répète.

## Tutoriel 4 — Noise (15 min)
Courbe Z Location : ajoutez Noise ; Strength 0,06 ; Scale 6.

## Tutoriel 5 — La plage (5 min)
Timeline : End = 48.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_04_graph_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_04.py" -- --exercise graph --debug
```

Remarque d'honnêteté : les fichiers sont générés par script (`keyframe_points`, `handle_left_type`, `fcurve.modifiers.new`) ; T et V sont les touches de la keymap par défaut (vérifiées) ; l'emplacement exact de l'onglet des modificateurs dans la barre latérale du Graph Editor n'a pas été relu dans l'interface 5.3. Le croquis du Graph Editor (numpy) a été regardé : trois arches égales (cycles) et un frémissement discret.

## Variante de contrôle

Repérez un dépassement de position entre deux clés. Comparez une variante linéaire et une variante Bézier en gardant les mêmes points. **Preuve** La courbe et la lecture indiquent où la vitesse ou le dépassement change. Réglez les poignées en fonction de l’effet attendu.
