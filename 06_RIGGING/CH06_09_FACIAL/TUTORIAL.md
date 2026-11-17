# CH06.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_09_facial_starter.blend` : tête, armature (head, jaw, ctl_smile, ctl_blink) et poids de peau sont faits. Sauvegardez sous `ch06_09_facial_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Essayer la mâchoire (10 min)
Pose Mode, bone jaw : Rotation X de −15° : le menton descend. Inspectez les poids (Weight Paint) : dégradé de head vers jaw.

## Tutoriel 2 — Les shape keys (30 min)
GEO_Face > Object Data > Shape Keys : Basis, puis smile et blink. En Edit Mode du key smile, montez les sommets proches des deux coins de la bouche de 12 mm (Proportional Editing pour la décroissance) ; pour blink, descendez ceux des paupières. Créez les groupes smile_zone et blink_zone (poids 1 au centre, décroissants) et assignez-les dans le champ Vertex Group de chaque key.

## Tutoriel 3 — Les glissières (20 min)
Bone ctl_smile > Bone Constraints > Limit Location : Min X 0, Max X 0,05, Min/Max Y et Z à 0, Owner Space Local Space. Idem pour ctl_blink.

## Tutoriel 4 — Les drivers (20 min)
Clic droit sur la Value du key smile > Add Driver ; Scripted Expression `x / 0.05` ; variable x : Transform Channel, objet RIG_Face, bone ctl_smile, X Location, Local Space. Répétez le branchement pour `blink` avec `ctl_blink`. Testez chaque commande seule avant de les combiner. À mi-course en X local, la valeur de la forme doit être proche de 0,5.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_09_facial_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_09.py" -- --exercise facial --debug
```

Remarque d'honnêteté : les shape keys de la solution sont écrits par script avec des poids normalisés ; en les modelant à la main, ajustez l'amplitude jusqu'à ce que le correcteur affiche 10–14 mm. Les noms de panneaux et raccourcis cités n'ont pas été relus dans l'interface 5.3. Le croquis (fil de fer) a été regardé : menton qui descend, coins relevés, paupières abaissées.

## Variante de contrôle

Isolez l’ouverture de la mâchoire et une forme des lèvres, puis combinez les deux sur une copie. Regardez le profil et le raccord des commissures. **Preuve** Deux contrôles seuls et leur combinaison permettent de localiser une collision ou une double déformation.
