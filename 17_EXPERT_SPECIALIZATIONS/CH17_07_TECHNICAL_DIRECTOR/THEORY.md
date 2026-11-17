# Théorie — Technical Director

## Reproduire

Une panne reproductible sépare symptôme, cause probable et preuve. Conservez une bonne scène pour le diagnostic.

## Localiser

Un contrôle peut bouger tout en ne pilotant plus le bone de déformation. Le diagnostic suit le chemin des dépendances.

## Corriger et livrer

Le rig livré doit préserver les plans existants. Le test de régression vérifie les comportements connus.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Un rig de production est un réseau de dépendances. Un contrôleur peut bouger dans la vue quand la contrainte vers le bone de déformation est rompue. Le diagnostic compare le contrôle, la chaîne évaluée et le mesh sous la même pose. Une correction doit être rejouée dans les scènes utilisatrices.
