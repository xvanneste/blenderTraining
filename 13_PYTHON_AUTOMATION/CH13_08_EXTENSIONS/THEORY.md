# Théorie — Extensions Blender

## Préparer le paquet

L’identifiant stabilise l’installation. La version et la version minimale sont deux propriétés distinctes.

## Valider puis construire

La validation détecte les problèmes de manifeste avant l’installation.

## Installer localement

Le scénario d’installation doit couvrir l’enregistrement et le retrait des classes.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

L’identifiant du manifeste désigne l’extension installable, la version précise une publication et la version minimale précise l’environnement visé. Le ZIP contient les fichiers nécessaires au paquet. La présence du code à la racine ne prouve pas que les classes se libèrent correctement à la désactivation. Vérifiez le cycle dans un profil distinct.
