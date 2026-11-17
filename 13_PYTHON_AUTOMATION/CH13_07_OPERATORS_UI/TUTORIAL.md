# Atelier guidé — Opérateurs et interface

Depuis Scripting ouvrez le fichier Python et lancez **Run Script**. Dans la vue 3D, utilisez **Shift+clic droit** avec la configuration par défaut pour déplacer le curseur. Appuyez sur **N**, puis choisissez **BCMA**.

## 1. Définir la commande

Ouvrez le script dans Text Editor et repérez bl_idname, poll et execute. Lancez le script une seule fois dans une session neuve.

**Pourquoi** poll borne le contexte d’usage. execute réalise la modification et RENVOIE un statut.

**Contrôle** Dans la vue 3D, N affiche la catégorie BCMA.

## 2. Tester le panneau

Placez le curseur 3D hors origine puis cliquez Ajouter un repère. Comparez les coordonnées du nouvel Empty à celles du curseur.

**Pourquoi** L’opérateur utilise le curseur de la scène et lie le résultat à la collection active.

**Contrôle** Un repère apparaît au curseur et dans la collection active.

## 3. Annuler et changer de mode

Annulez le repère avec Ctrl+Z, sélectionnez un maillage, passez en mode Édition et vérifiez la disponibilité de la commande.

**Pourquoi** Le drapeau UNDO rend l’action annulable. poll évite la création dans un contexte non prévu.

**Contrôle** Le repère disparaît avec l’annulation et l’action est indisponible en mode Édition.

## Vérification sur une variante

Préparez deux collections et des positions de curseur distinctes. Appelez l’opérateur dans chacune. Vérifiez les coordonnées des repères, l’action Undo dans l’interface et l’indisponibilité en mode Édition.
