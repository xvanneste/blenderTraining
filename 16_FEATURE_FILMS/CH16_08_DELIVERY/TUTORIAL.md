# Atelier guidé — Livraison et archivage

Depuis la racine du cours, lancez `python 16_FEATURE_FILMS/ASSETS_ATELIERS/controle_pipeline.py livraison`. Extrayez la démonstration dans un dossier neuf et ouvrez `LIRE.md`. Le master utilise Matroska FFV1 avec un WAV séparé et la copie de revue utilise H.264/AAC. Pour votre propre livrable, adaptez ces réglages au cahier des charges.

## 1. Fabriquer les éléments

Exportez le master selon le cahier des charges choisi, le mix WAV et une copie de revue. Fournissez le SRT en UTF-8 pour les inscriptions utiles et le signal sonore.

**Pourquoi** Le master conserve la qualité de travail. Les dérivés répondent à un usage. Les sous-titres suivent le montage et la langue convenus.

**Contrôle** Les durées, la cadence, le plan de couleur et les canaux audio sont documentés.

## 2. Placer dans l’archive

Réunissez le projet et ses sources, les exports, les droits et les consignes de réouverture. Écrivez des chemins relatifs et une empreinte SHA-256 par élément.

**Pourquoi** Un hash permet de détecter une modification. La réouverture confirme que les dépendances sont localisées.

**Contrôle** Le manifeste connaît chaque pièce et un dossier différent permet de tout rouvrir.

## 3. Recevoir et contrôler

Extrayez la démonstration dans un dossier neuf. Faites jouer les 15 secondes et vérifiez les entrées de sous-titres. Comparez aux plages et rejouez les vérifications.

**Pourquoi** Une livraison passe du point de vue du destinataire. Il faut vérifier image, son, sous-titres et possibilité de reprendre le projet.

**Contrôle** Le rapport de réception liste format observé, pièce de preuve et verdict par fichier.

## Vérification sur une variante

Vérifiez le WAV, le master et le projet extraits dans un autre dossier. Ajoutez `--archive chemin/vers/copie.zip` à la commande pour contrôler votre copie. Faites deux essais indépendants. Dans le premier, modifiez un fichier et gardez les anciennes empreintes pour vérifier le diagnostic. Dans le second, placez la fin d’un sous-titre au-delà de la vidéo et mettez à jour l’empreinte de ce SRT. Le contrôle doit alors signaler la borne de temps.
