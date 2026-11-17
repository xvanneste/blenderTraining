# CH13.06 — Validation d’une scène

- **Point zéro**. Le terminal affiche zéro anomalie pour la référence.

- **Défauts contrôlés**. Le rapport contient NOM, ECHELLE et IMAGE_ABSENTE avec les noms concernés.

- **Réparation**. Le rapport repasse à zéro et une vue de contrôle compare la silhouette.

**Erreur fréquente** Un chemin commençant par // semble absent alors que l’image existe. Utilisez bpy.path.abspath avec la bibliothèque de l’image avant de vérifier le chemin.
