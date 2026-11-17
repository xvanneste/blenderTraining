# CH07.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_08_walk_starter.blend` (mannequin sans animation, bras le long du corps). Sauvegardez sous `ch07_08_walk_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le contact (30 min)
Image 1 : pose de contact : cuisse gauche −19,6°, jambe gauche −19,4° ; cuisse droite +19,4°, jambe droite +19,6° (rotations autour de l'axe X monde, voir le tableau de THEORY.md §4) ; hanches (location) abaissées à 0,899 m ; bras gauche +20°, bras droit −20°. Insérez les clés de rotation de tous les bones et de position de hips (I).

## Tutoriel 2 — Les trois autres poses (45 min)
Images 4, 7 et 10 : mêmes opérations avec les angles du tableau.

## Tutoriel 3 — L'autre côté (30 min)
Images 13, 16, 19, 22 : les mêmes poses, gauche et droite échangées. Image 25 : copie de l'image 1.

## Tutoriel 4 — Interpolation (10 min)
Dope Sheet ou Graph Editor : sélectionnez toutes les clés, T > Linear (le pied d'appui avance à vitesse constante).

## Tutoriel 5 — Plage et boucle (10 min)
Gardez la plage 1–25 à 24 i/s pour le correcteur et comparez les poses aux images 1 et 25. Cherchez un à-coup juste avant la reprise de la boucle et surveillez la hauteur du pied d’appui entre les clés. Pour exporter un cycle de 24 images sans doubler la pose de raccord, rendez 1–24 dans une copie de la scène.

## Tutoriel 6 — Régler (30 min)
Vérifiez au correcteur : pas (0,6 m), pied d'appui au sol, levée du pied libre (≥ 6 cm), hanches, bras. Corrigez les poses fautives.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_08_walk_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_08.py" -- --exercise walk --debug
```

Remarque d'honnêteté : la solution est calculée par script (IK analytique à deux segments, une clé par image) ; les angles du tableau sont ceux de cette solution, mesurés par script ; une version à neuf clés (Bezier ou Linear) a été fabriquée par script et acceptée par le correcteur (42/42). Les gestes du tutoriel (saisie des angles, T > Linear) n'ont pas été rejoués dans l'interface 5.3 par une personne. Le croquis (squelette de profil, numpy) a été regardé : contact, descente, passage, montée.

## Variante de contrôle

Placez un repère au sol sous un pied en contact. Vérifiez son déplacement à plusieurs images et regardez le bassin. **Preuve** Un tableau de positions et deux cadres montrent la durée d’appui et distinguent le mouvement attendu du glissement.
