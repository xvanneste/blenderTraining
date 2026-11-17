# Exercices — Opérateurs et interface

## Exercice guidé

Créer une commande Blender visible dans la barre latérale et annulable. Suivez le [tutoriel](TUTORIAL.md). Joignez le fichier de travail et consignez les trois preuves avec le nom et la version du fichier.

- **Définir la commande**. Dans la vue 3D, N affiche la catégorie BCMA.

- **Tester le panneau**. Un repère apparaît au curseur et dans la collection active.

- **Annuler et changer de mode**. Le repère disparaît avec l’annulation et l’action est indisponible en mode Édition.

## Exercice autonome — Variante

Ajoutez une FloatProperty pour régler la taille de visualisation de l’Empty. Testez 0,1 m puis 0,5 m. Une propriété d’opérateur paramètre un résultat sans toucher à sa position.

**Validation** Le repère garde les coordonnées du curseur et change de taille à l’écran.
