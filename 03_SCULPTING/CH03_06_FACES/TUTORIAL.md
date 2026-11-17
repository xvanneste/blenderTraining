# CH03.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_06_face_starter.blend` : le buste réaliste de CH03.05 **sans** détails de visage, avec
orbites creusées et globes `EYE_L` / `EYE_R`. Un objet caché `REF_Base` (collection `REFERENCE`) est la copie de départ
utilisée par le correcteur : **ne le supprimez pas**. Sauvegardez sous `ch03_06_face_<prenom>_v001.blend`.

## Tutoriel 1 — Paupières (≈ 40 min)
En *Sculpt Mode*, activez la symétrie X. Autour de chaque globe, posez un **bourrelet** de 1,5 à 2,5 mm.
La paupière haute descend sur le haut de l’iris, la basse est plus fine. Choisissez *Clay Strips* parmi les brosses
de sculpture et procédez par traits courts. Lissez légèrement avec `Shift` pendant le trait. Creusez un **pli**
(*Draw Sharp* ou *Crease Sharp*) à 1 cm au-dessus du bourrelet. Vérifiez de face et de 3/4.

## Tutoriel 2 — Nez : ailes et narines (≈ 40 min)
Vue du dessous (tournez la vue sous le nez) : sous le bout du nez, deux creux de 4 à 5 mm de profondeur, de part et d'autre
de la cloison. *Draw Sharp* ou *Crease Sharp* pour creuser, *Pinch/Magnify* pour affirmer le bord de l’aile, *Smooth*
ensuite. Gardez le volume **fermé** : un creux, pas un trou.

## Tutoriel 3 — Bouche (≈ 50 min)
Une ligne entre les lèvres, creusée sur ≈ 4 mm, large comme l'écart des pupilles (≈ 6 à 8 cm ici), avec deux petits
creux aux commissures. La lèvre haute est un peu plus en retrait que la basse. *Crease Sharp* pour la ligne, *Inflate/
Deflate* pour les volumes des lèvres, *Smooth* pour les raccords. Vérifiez en profil que les lèvres gardent du relief
après le lissage.

## Tutoriel 4 — Oreilles (≈ 40 min)
Un sillon qui suit le bord (hélix) et un creux central (conque), de 3 à 4 mm. Elles vont de la ligne des sourcils à la
base du nez. *Grab* (G) pour leur donner du relief, *Draw Sharp* pour le sillon.

## Tutoriel 5 — Le sourire (≈ 60 min)
Enregistrez une copie `…_smile_v001.blend`. *Grab* (G) à faible rayon sur chaque commissure : montez-la d'≈ 6 mm en un glissé court (un glissé de 20 mm étire la surface et laisse des balafres), puis lissez ;
creusez davantage les plis naso-géniens ; remontez un peu les joues. Un seul côté ne suffit pas : Mirror X.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_06_face_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_06.py" -- --exercise face --render
```
Pour le sourire : `-- --exercise smile`. Ajoutez `--debug` pour voir les grandeurs brutes. Références :
`ch03_06_face_reference.png` (neutre) et `ch03_06_smile_reference.png` (sourire), chacune en face, 3/4, profil.

Remarque d'honnêteté : les gestes ci-dessus (rayons, nombre de passes, vues oblique et de droite) sont ceux qui ont **réellement produit** les solutions dans Blender 5.2 via MCP ; en 5.3 le sculpt interactif n'a pas été exécuté. Le correcteur a été éprouvé (SOLUTIONS.md).

## Variante de contrôle

Sur votre tête neutre, comparez les deux orbites avant d’ajouter des plis. Utilisez le globe comme repère volumique. Regardez la ligne de paupière s’appuyer sur le globe et comparez le relief du nez en profil. **Preuve** Les zones corrigées se lisent en argile avant d’ajouter les matériaux.
