# CH08.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_07_destruction_starter.blend`. Sauvegardez sous `ch08_07_destruction_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Une liaison (10 min)
Cliquez Brick_0_0 puis, en maintenant Maj, Brick_1_0 (la dernière cliquée devient active). Object > Rigid Body > Connect ; panneau de l'opération : Type Fixed, Location Center, Connection Pattern Selected to Active.

## Tutoriel 2 — Les 38 paires (30 min)
Répétez pour chaque paire de voisines (6 colonnes × 4 rangées : 20 horizontales + 18 verticales). Les objets Constraint apparaissent dans une collection.

## Tutoriel 3 — Rendre cassable (15 min)
Pour chaque Constraint : Physics > Settings : Breaking coché, Threshold 1. Commencez par vérifier une paire avant de configurer les autres contraintes. Lors d’une comparaison de seuils, gardez la masse et la vitesse du projectile constantes.

## Tutoriel 4 — Jouer (10 min)
Lecture depuis l'image 1 (à jouer dans l'ordre) ; lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_07_destruction_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_07.py" -- --exercise destruction --debug
```

Remarque d'honnêteté : la solution est générée par script, en appelant l'opérateur réel `bpy.ops.rigidbody.connect` pour chaque paire ; Cell Fracture n'est pas livrée avec la 5.3 (non testée) ; la rupture n'est pas lisible dans l'API (mesure par les positions) ; l'astuce Alt+clic du tutoriel 3 n'a pas été vérifiée ; la cause de l'explosion à grande vitesse n'est pas isolée ; vue de dessus (numpy) regardée : mur fracturé avec trou à gauche, bloc poussé à droite.

## Variante de contrôle

Sur deux fragments, testez une liaison avant de réutiliser le réglage sur toutes les paires. Notez l’instant de rupture et l’ordre des événements. **Preuve** Une variante tient jusqu’au contact, et le rapport situe la liaison qui cède trop tôt.
