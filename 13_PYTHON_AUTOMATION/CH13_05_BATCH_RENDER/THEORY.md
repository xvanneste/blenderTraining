# Théorie — Rendu par lot

## Commande unitaire

Les options sont traitées dans l’ordre. Une option placée après -f ne configure pas le rendu déjà lancé.

## Lot et chemins

Une liste d’arguments subprocess traite les chemins qui contiennent des espaces.

## Panne et reprise

Un lot doit distinguer échec d’entrée, échec Blender et absence de produit attendu.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Blender charge les arguments de gauche à droite. Charger le fichier modifie les réglages de scène. Placer -o avant la scène risque donc de voir le chemin remplacé. L’option -f déclenche le rendu des images précisées. Vérifier une nouvelle sortie dans un dossier provisoire empêche qu’un ancien PNG soit pris pour le résultat d’un calcul qui a échoué.
