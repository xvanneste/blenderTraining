# CH09.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_09_dof_starter.blend`. Sauvegardez sous `ch09_09_dof_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Rendu F12 : les deux barres sont nettes.

## Tutoriel 2 — Activer (5 min)
CAM > Object Data Properties (caméra) > Depth of Field : cochez.

## Tutoriel 3 — Régler (5 min)
Focus Distance : 5 m. F-Stop : 1,0.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : pic proche et pic lointain.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_09_dof_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_09.py" -- --exercise dof --debug
```

Remarque d'honnêteté : la mesure est faite avec Cycles (32 échantillons, sans débruitage) car le Workbench n'a produit aucun flou dans l'essai ; les pics (solution 1,00 et 0,31 ; départ 1,00 et 1,00) sont mesurés sur cette scène 320 × 180 ; une barre de 20 cm de large avait un pic flou de 0,91 : c'est pourquoi les barres sont fines. Les libellés Depth of Field, Focus Distance, F-Stop viennent de l'API (`Camera.dof`), pas d'une relecture dans l'interface 5.3. Rendus de départ et de solution regardés.

## Variante de contrôle

Mettez au point sur le premier sujet puis sur l’arrière-plan, avec ouverture et cadre stables. Rouvrez les deux fichiers et repérez l’objet ou la distance de focus. **Preuve** La zone nette attendue se lit sans ambiguïté et le contrôle retrouve le réglage responsable.
