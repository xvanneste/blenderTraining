# CH08.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_04_particles_starter.blend`. Sauvegardez sous `ch08_04_particles_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le système (10 min)
EMITTER : propriétés Particles > « + » (Particle System) ; type Emitter.

## Tutoriel 2 — Émission (15 min)
Number 200 ; Frame Start 1, End 30 ; Lifetime 60 ; Emit From Faces ; Velocity > Normal 3.

## Tutoriel 3 — Physique et rendu (10 min)
Physics : Newtonian ; Field Weights > Gravity 1 ; Render > Render As : None.

## Tutoriel 4 — Le sol (10 min)
COL_Floor : Physics > Collision ; Damping 0,5. Lisez depuis l’image 1. Examinez une image pendant l’émission, puis une après l’image 30. Observez que les particules émises avant la fin persistent jusqu’à leur propre fin de vie. Ce test utilise les particules historiques du starter.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_04_particles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_04.py" -- --exercise particles --debug
```

Remarque d'honnêteté : la solution est générée par script (modificateur `PARTICLE_SYSTEM`, `ParticleSettings`, `COLLISION`) et simulée par le correcteur en arrière-plan ; les noms de panneaux (Particles, Emission, Velocity, Field Weights, Render As) n'ont pas été relus dans l'interface 5.3. Le nuage (numpy) a été regardé : une colonne de particules qui retombent ; la hauteur de la fontaine est modeste (1,46 m).

## Variante de contrôle

Le chapitre utilise les particules historiques pour faire varier émission, durée de vie et distribution. Comparez le nombre d’éléments sur deux images avec une graine fixe. Pour un nouveau système de distribution statique, comparez l’atelier Geometry Nodes de CH05.04. **Preuve** Le rapport nomme le système utilisé et indique si le nombre dépend du temps.
