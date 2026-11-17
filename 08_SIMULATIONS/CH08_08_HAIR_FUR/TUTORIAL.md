# CH08.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_08_hair_starter.blend`. Sauvegardez sous `ch08_08_hair_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le système (10 min)
Le starter étudie le système historique de particules Hair. Sélectionnez *Head*, ajoutez un système dans *Particles* et choisissez le type *Hair*. Réglez *Number* à 300, *Hair Length* à 0,5 et *Segments* à 6. Gardez ce système pour reproduire le cache et les mesures du chapitre. Les cheveux sur objets *Curves* suivent un autre workflow.

## Tutoriel 2 — La calotte (5 min)
Vertex Groups > Density : « scalp ».

## Tutoriel 3 — Enfants et mèches (15 min)
Children : Interpolated ; Display Amount 10 ; Clumping 0,5.

## Tutoriel 4 — Dynamique (10 min)
Hair Dynamics coché ; lecture depuis l'image 1 jusqu'à 30 ; lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_08_hair_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_08.py" -- --exercise hair --debug
```

Remarque d'honnêteté : la solution est générée par script (`ParticleSettings.type = 'HAIR'`, `vertex_group_density`, `child_type`, `clump_factor`, `ParticleSystem.use_hair_dynamics`) ; le correcteur lit les données évaluées (aucun rendu des cheveux) ; les libellés des panneaux n'ont pas été relus dans l'interface 5.3 ; l'objet Curves et les nœuds de cheveux n'ont pas été testés ; la collision avec la tête n'est pas gérée. Vue de face (numpy) regardée : cheveux dressés à l'image 1, retombés à l'image 30.

## Variante de contrôle

Distinguez les cheveux historiques de l’exercice et les objets Hair Curves organisés autrement. Sur le système utilisé dans la scène, comparez une silhouette de près et de loin, puis testez une zone peignée. **Preuve** Le rapport nomme le système et donne le cadrage auquel l’augmentation de densité devient inutile.
