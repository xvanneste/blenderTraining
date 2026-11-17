# Théorie — Pipeline Developer

## Contrat des entrées

Une erreur avant lancement évite de gaspiller des ressources et laisse la version approuvée intacte.

## Publier en deux étapes

Une publication offre un point de reprise. Une panne peut laisser un calcul partiel dans le dossier de travail.

## Tester et documenter

Un test de pipeline doit vérifier les refus et le comportement de reprise. Les hypothèses sont explicites et versionnées.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

La publication d’un lot se fait après validation de tous les produits attendus. Une réservation locale évite à deux processus coopératifs de cibler simultanément la même version. Le dossier provisoire isole les sorties partielles. Le manifeste permet ensuite de relier fichiers, empreintes et version. Sur réseau, la réservation et sa reprise doivent correspondre au stockage utilisé.
