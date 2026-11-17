# Théorie — Pipelines de rendu

## Préparer le lot

Un worker traite une plage dans un environnement identifié. Les images de coupe doivent rester distinctes des plages locales avec poignées.

## Distinguer retour et résultat

Un processus peut finir sans fournir toutes les images. La présence seule ne valide ni dimensions ni provenance.

## Reprendre et publier

L’isolation des versions protège les images approuvées et permet un retour arrière.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Un lot est associé à un plan, une version, une plage locale, un profil de rendu et des produits attendus. Un plan monté peut couvrir moins d’images que la plage de calcul si des poignées servent à un raccord. Compter les fichiers seulement n’identifie ni les trous dans la numérotation, ni une définition erronée, ni un mélange de versions.
