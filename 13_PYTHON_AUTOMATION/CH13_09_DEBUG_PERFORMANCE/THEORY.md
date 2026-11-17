# Théorie — Débogage et performance

## Reproduire

Le type d’exception précise le mécanisme. La pile montre comment l’exécution y est arrivée.

## Corriger

Une règle d’absence explicite évite un résultat incomplet difficile à voir.

## Mesurer

La création du dictionnaire fait partie de la mesure. Les temps servent à comparer ce jeu de données.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Une recherche linéaire répétée parcourt des lignes jusqu’au résultat. Un index paie d’abord le coût de construction, puis évite de parcourir toutes les lignes à chaque appel. Avant d’attribuer un gain à l’index, vérifiez égalité des résultats, ordre et traitement des demandes absentes. Un changement de comportement peut être une régression même avec un temps plus bas.
