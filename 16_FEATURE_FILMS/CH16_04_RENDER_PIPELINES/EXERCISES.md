# Exercices — Pipelines de rendu

## Exercice guidé

Découper un rendu en lots vérifiables, rejouer un lot en échec et conserver les bons produits. Suivez le [tutoriel](TUTORIAL.md). Joignez le fichier de travail et consignez les trois preuves avec le nom et la version du fichier.

- **Préparer le lot**. Chaque lot indique plage, version et chemin complet de sortie.

- **Distinguer retour et résultat**. L’inventaire détecte l’image manquante par son numéro.

- **Reprendre et publier**. La nouvelle version contient toutes ses images attendues et l’ancienne reste consultable.

## Exercice autonome — Variante

Répartissez un lot de 96 images en blocs de 32 et simulez la panne du second bloc. Calculez ce qui doit être rejoué. Une granularité plus fine réduit la reprise et augmente les opérations de suivi.

**Validation** 32 images sont à refaire et aucune intersection entre lots n’est créée.
