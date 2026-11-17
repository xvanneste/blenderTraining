# CH03.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « REF_Base manquant » | Objet caché supprimé | Append > Object depuis le starter (collection REFERENCE) ; ne pas le supprimer |
| Paupières refusées (0 %) | Bourrelet trop faible (< 0,8 mm) ou hors anneau | Clay Strips plus appuyé ; relief ≈ 2 mm autour du globe, à 1,2–2 cm du centre |
| Narines refusées | Creux trop superficiels ou mal placés | 4–5 mm sous le bout du nez, de part et d'autre de la cloison |
| Narine percée | Trop de Draw Sharp inversé / Boolean | Un creux qui se referme ; Voxel Remesh pour refermer le volume |
| Bouche refusée | Ligne trop peu profonde ou pas au centre | ≥ 3 mm de profondeur, qui part du milieu des lèvres |
| Largeur de bouche hors 60–130 % | Bouche trop étroite ou trop large | Environ l'écart des pupilles |
| Oreilles refusées | Pas de creux ≥ 1,2 mm | Sillon d'hélix 3 mm, conque 3–4 mm |
| Sourire refusé (< 4 mm) | Commissures peu relevées | Grab court (≈ 6 mm), rayon large, puis Smooth ; Mirror X |
| Sourire qui ressemble à une grimace | Seule la bouche bouge | Remontez les joues, plissez un peu l'œil |
| Correcteur « vert » sans que ça se voie | Détails trop petits pour le rendu | Éclairage latéral (CH09.*), rendu de contrôle |
| Mesures étranges après Voxel Remesh | Densité modifiée | Pas de souci : la référence est une surface, pas des indices de sommets |
| Brosse « Crease » introuvable | Elle n'existe pas seule en 5.3 | Crease Sharp / Crease Polish (Shift+C) |
