# Dépannage — Validation d’une scène

**Symptôme** Un chemin commençant par // semble absent alors que l’image existe.

**Cause à vérifier** Le chemin Blender est relatif au fichier ou à sa bibliothèque.

**Correction** Utilisez bpy.path.abspath avec la bibliothèque de l’image avant de vérifier le chemin.

Refaites le contrôle final. Le rapport repasse à zéro et une vue de contrôle compare la silhouette.
