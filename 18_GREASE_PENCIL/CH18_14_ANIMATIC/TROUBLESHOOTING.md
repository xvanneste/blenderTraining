# CH18.14 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le dessin du plan 1 reste affiché partout | Pas de nouvelle image clé : on a dessiné sur la même | *Insert Blank Keyframe* (Shift+I) au début de chaque plan |
| Le correcteur ne trouve pas la clé d'un plan | Clé sur un autre calque, ou décalée d'une image | Calque `USER_Panels` actif ; vérifiez dans la Dope Sheet (mode Grease Pencil) |
| « Marqueurs : trouvé [153] » | Erreur d'arrondi ou de cumul | Recalculez le tableau (exercice 1) ; déplacez le marqueur (G) |
| La fin de scène est refusée | *End* ≠ total | *End* = dernière image du dernier plan |
| La caméra ne bouge pas à la lecture | Clés posées sur un autre champ ou à la même valeur | Survol du champ *Orthographic Scale* + I, deux valeurs différentes |
| L'incrustation n'apparaît pas | *Burn Into Image* décoché | Output Properties > Metadata > Burn Into Image |
| La caméra active ne change pas (3D) | Marqueurs non liés | Caméra sélectionnée, marqueur sélectionné, Ctrl+B dans la Timeline |
| « PM au lieu de PRP » | Cadre trop large | Rapprochez la caméra ou augmentez la focale (CH18.10) |
| Règle des 180° refusée | Caméra passée de l'autre côté de A–B | Gardez y < 0 |
