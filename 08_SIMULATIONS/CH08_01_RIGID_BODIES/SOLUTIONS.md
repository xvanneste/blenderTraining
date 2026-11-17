# CH08.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — L'actif obéit à la physique, le passif est un obstacle fixe | Sol Passive, briques et boule Active. |
| Q2 | **a** — La résistance au glissement au contact | Friction 0,05 : les briques glissent sans fin (710 mm de déplacement entre les images 140 et 150). |
| Q3 | **a** — Box | La boîte épouse la brique et coûte peu. |
| Q4 | — | Elle épaissit la forme de collision ; sur de petits objets elle les fait se chevaucher : on la met à 0 pour des briques de 0,3 m. |
| Q5 | — | Une valeur réaliste et cohérente entre corps ; la boule de 20 kg est assez lourde pour les disperser (une boule de 0,3 kg n'en déplace aucune). |
| Q6 | **a** — Le corps suit son animation au lieu de la physique | Cochée à l'image 1 puis décochée à l'image 21 : la boule suit sa trajectoire puis est lâchée. |
| Q7 | **a** — La physique dépend de l'état de l'image précédente | Sauter directement à l'image 150 ne simule rien (mesuré en arrière-plan). |
| Q8 | — | Sans sol rigide, le mur tombe à travers : z minimal de −174 m après 150 images. |
| Q9 | — | Le cache du monde s'arrête à l'image 60 : la simulation se fige (9 briques déplacées au lieu de 21). |
| Q10 | — | Mesurer le déplacement des briques avant l'arrivée de la boule : 8 mm au plus à l'image 12 dans la solution. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_01_rigid_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_01_files.py`) : maillages par bmesh, `rigidbody.object_add`, clés de location et de kinematic. Score 47/47 ; starter 2/23. Vue de dessus regardée. Les maillages sont créés par bmesh (et non par primitive + transform_apply : ce dernier a fait exploser le mur).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_ground` | sol sans corps rigide : le mur tombe à travers | sol ; stabilité ; sous le sol ; repos |
| `…_passive_bricks` | briques passives (immobiles) | briques ; effondrement |
| `…_light_ball` | boule de 0,3 kg | boule ; effondrement |
| `…_no_release` | boule jamais lâchée (Animated reste coché) | boule ; effondrement ; avance |
| `…_low_friction` | friction des briques à 0,05 : elles glissent sans fin | briques ; repos |
| `…_no_world_frames` | cache du monde arrêté à l'image 60 | monde ; effondrement |
Aussi refusé : le starter.

## Limites
- Collisions en boîtes, pas de contraintes ni de destruction.
- Résultat sensible aux paramètres : seuils qualitatifs.
- Les contre-exemples « light_ball » et « no_release » échouent aussi sur l'effondrement (conséquence).
