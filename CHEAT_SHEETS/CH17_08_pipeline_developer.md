# CH17.08 — Pipeline Developer

- **Contrat des entrées**. Le contrat reçoit un cas valide et refuse chevauchement et doublon.

- **Publier en deux étapes**. Le scénario d’échec conserve le rendu approuvé et le scénario nominal crée une version complète.

- **Tester et documenter**. Une commande refait les tests nominal et négatifs, avec code de sortie et rapport cible.

**Erreur fréquente** Le processus sort sans erreur mais manque un fichier nécessaire. Inspectez le manifeste et les fichiers avant d’autoriser la publication.
