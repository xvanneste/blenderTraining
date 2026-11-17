# Captures d’atelier dans Blender 5.3

Les images ci-dessous proviennent de l’interface de Blender ouverte sur les fichiers du cours. Les références de face et de profil sont des gabarits synthétiques.

| Capture | À observer |
|---|---|
| [Cube en mode Objet](assets/captures/01-modes-objet.png) et [mode Édition](assets/captures/01-modes-selections.png) | Bandeau, boutons sommet/arête/face et sélection des sommets supérieurs. |
| [Caisse ouverte](assets/captures/02-inset-extrude.png) | Rebord, épaisseur et cavité en mode Édition. |
| [Mirror sur la lame](assets/captures/03-miroir-couture.png) | Axe X, Merge, Clipping et couture entre les moitiés. |
| [Gabarit de face](assets/captures/04-images-ortho.png) et [de profil](assets/captures/04-images-profil.png) | Sol, alignement, affichage orthographique, opacité et profondeur. |
| [Boucles du bras](assets/captures/05-extrusion-bras.png) | Épaule continue et zone de flexion mise en évidence. |
| [Maillage du visage](assets/captures/06-visage-cage.png) | Circulation des arêtes autour de l’orbite et de la bouche. |
| [Coude fléchi et poids](assets/captures/07-coude-poids.png) | Groupe avantbras.L et transition vers le bras. |
| [GLB réimporté](assets/captures/08-reimport-export.png) | Personnage et armature dans le fichier de contrôle. |

Pour régénérer les captures, lancez une instance dédiée de Blender 5.3 avec `--factory-startup --python capturer_ateliers.py` depuis ce dossier. Le script ouvre les scènes, réalise les captures, puis ferme cette instance. Pour extraire un seul écran, ajoutez `--` suivi du nom sans extension.
