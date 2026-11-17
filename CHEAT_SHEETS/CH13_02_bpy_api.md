# Fiche de révision — CH13.02 L’API bpy

- `bpy.data.objects.get(nom)` trouve un objet par nom dans le fichier.
- `bpy.context.view_layer.objects.active` désigne l’objet actif dans le calque.
- `objet.data = objet.data.copy()` sépare les données de géométrie avant une modification.
- `bpy.ops.…poll()` vérifie le contexte de l’opérateur.
- Après un ajout, capturez immédiatement le nouvel objet, puis restaurez la sélection si nécessaire.

Révision J+7 : reprenez un starter et recolorez l’autre caisse sans modifier sa jumelle.
