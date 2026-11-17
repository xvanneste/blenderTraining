# Théorie — Opérateurs et interface

## Définir la commande

poll borne le contexte d’usage. execute réalise la modification et RENVOIE un statut.

## Tester le panneau

L’opérateur utilise le curseur de la scène et lie le résultat à la collection active.

## Annuler et changer de mode

Le drapeau UNDO rend l’action annulable. poll évite la création dans un contexte non prévu.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Un opérateur prend en charge une action. Son poll indique dans quel contexte elle est disponible. Un panneau construit l’interface qui la déclenche. Dans ce cas, cliquer lit le curseur et la collection du contexte, crée un Empty et rend une action annulable. Le corps de draw peut être appelé plusieurs fois. Les mutations vont dans execute.
