# CH08.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_01_rigid_starter.blend`. Sauvegardez sous `ch08_01_rigid_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le sol (10 min)
GEO_Ground : propriétés Physics > Rigid Body ; Type Passive ; Shape Box.

## Tutoriel 2 — Les briques (20 min)
Sélectionnez les 30 briques ; Rigid Body : Active, Mass 1 kg, Friction 0,6, Shape Box, Margin : coché à 0. (Pour copier sur toutes les briques : Object > Rigid Body > Copy from Active.)

## Tutoriel 3 — La boule (20 min)
BALL_Impact : Active, Mass 20 kg, Shape Box. Dynamics : Animated coché à l'image 1 (clé sur la case : I en survolant la case) ; image 21 : décochée, clé.

## Tutoriel 4 — Le monde (10 min)
Dans *Scene → Rigid Body World*, réglez la plage de cache de 1 à 150 et *Substeps* à 10. Changez ensuite seulement la vitesse ou les sous-pas sur une copie pour comparer le contact. Vérifiez à l’image 21 que la case *Animated* est décochée et porte une clé.

## Tutoriel 5 — Lire la simulation (15 min)
Lecture depuis l'image 1 (Espace) : la boule arrive, lâchée à l'image 21, heurte le mur ; lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_01_rigid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_01.py" -- --exercise rigid --debug
```

Remarque d'honnêteté : la solution est générée par script (opérateur `rigidbody.object_add`, propriétés `rigid_body.*`, clés sur `kinematic`) et simulée par le correcteur image après image en arrière-plan ; les noms de panneaux (Physics > Rigid Body, Dynamics > Animated, Scene > Rigid Body World) et « Copy from Active » n'ont pas été relus dans l'interface 5.3. Résultat d'impact : déterministe mais sensible aux paramètres : mes essais ont montré qu'une colonne de cubes de 1 m glisse au lieu de s'effondrer, d'où le mur de briques. La vue de dessus (numpy) a été regardée : mur en ligne, briques dispersées autour de la boule.

## Variante de contrôle

Réglez d’abord le sol passif et observez une seule brique. Sur une copie, changez la marge de collision et relevez la distance entre l’objet et le sol. **Preuve** Le premier impact est visible et le contrôle sépare pénétration et marge.
