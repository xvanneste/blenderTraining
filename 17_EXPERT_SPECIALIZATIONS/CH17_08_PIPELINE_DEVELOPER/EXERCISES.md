# Exercices — Pipeline Developer

## Exercice guidé

Assembler un mini-pipeline versionné qui refuse les entrées invalides et peut reprendre un lot. Suivez le [tutoriel](TUTORIAL.md). Joignez le fichier de travail et consignez les trois preuves avec le nom et la version du fichier.

- **Contrat des entrées**. Le contrat reçoit un cas valide et refuse chevauchement et doublon.

- **Publier en deux étapes**. Le scénario d’échec conserve le rendu approuvé et le scénario nominal crée une version complète.

- **Tester et documenter**. Une commande refait les tests nominal et négatifs, avec code de sortie et rapport cible.

## Exercice autonome — Variante

Simulez deux workers qui voudraient publier le même lot. Faites réserver un nom de version ou un identifiant par worker avant le calcul. La concurrence doit éviter l’écrasement et identifier l’auteur d’un résultat.

**Validation** Deux tentatives ne remplacent jamais silencieusement le même dossier approuvé.
