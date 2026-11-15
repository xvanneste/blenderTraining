# CH18.15 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| *Add > Transition* grisé | Pas exactement 2 strips image/vidéo sélectionnés | Sélectionnez les deux plans (pas de son) |
| Le fondu enchaîné ne dure rien | Les plans ne se chevauchent pas | Mettez-les sur deux canaux et faites-les se recouvrir |
| La durée totale a changé | Strip déplacé au lieu d'être allongé | Allongez la poignée de début ; la fin reste à 456 |
| Vidéo muette | *Audio Codec* : No Audio | Encoding > Audio > AAC |
| Le son n'est pas entendu dans Blender | Strip son coupé (mute) ou volume 0 | Sidebar > Strip ; décochez la sourdine (H/Alt+H) |
| Son décalé à l'export | Son posé à l'œil sans repère | Calez sur le marqueur, vérifiez le début du strip (Sidebar > Time) |
| Le papier blanc paraît gris | *View Transform* AgX | Render/Color Management > View Transform : Standard |
| Fichier `…v0010001-0456.mp4` | Blender ajoute la plage d'images au nom | Renommez la version, ou terminez le chemin par `_` |
| Le fondu au noir n'agit pas | Fade appliqué à un autre strip | Sélectionnez le dernier plan seul, *Add > Fade > Fade Out* |
