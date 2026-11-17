# Atelier guidé — Pipeline Developer

En Python 3, partez des deux scripts fournis. Écrivez un simulateur de worker qui crée les deux images attendues lors du cas nominal ou s’arrête après la première lors du cas fautif. Branchez le rendu Blender après avoir validé la logique de publication.

## 1. Contrat des entrées

Lisez la feuille de plans et validez schéma, identifiants et plages. Définissez un code de retour non nul pour les erreurs de structure.

**Pourquoi** Une erreur avant lancement évite de gaspiller des ressources et laisse la version approuvée intacte.

**Contrôle** Le contrat reçoit un cas valide et refuse chevauchement et doublon.

## 2. Publier en deux étapes

Faites le rendu dans un dossier provisoire. Vérifiez les sorties avant publication dans une version neuve. Conservez un manifeste de pièces.

**Pourquoi** Une publication offre un point de reprise. Une panne peut laisser un calcul partiel dans le dossier de travail.

**Contrôle** Le scénario d’échec conserve le rendu approuvé et le scénario nominal crée une version complète.

## 3. Tester et documenter

Ajoutez trois mutations aux entrées : fichier absent, image invalide, dépendance inconnue. Exécutez et consignez les résultats.

**Pourquoi** Un test de pipeline doit vérifier les refus et le comportement de reprise. Les hypothèses sont explicites et versionnées.

**Contrôle** Une commande refait les tests nominal et négatifs, avec code de sortie et rapport cible.

## Référence exécutable

[Script de publication](../ASSETS_ATELIERS/publier_lot.py) · [Tests de référence](../ASSETS_ATELIERS/test_publication.py). Lancez le fichier de test avec Python 3 pour observer quatre refus et une reprise réussie. Le script utilise une réservation locale sur un seul dossier de destination. Sur un stockage distribué, définissez une réservation adaptée à l’infrastructure et un protocole de reprise pour les réservations abandonnées.

## Vérification sur une variante

Simulez un worker qui s’arrête après une image, puis une tentative concurrente. Le dernier lot approuvé doit rester accessible. Lancez un worker complet et comparez son manifeste aux deux produits attendus.
